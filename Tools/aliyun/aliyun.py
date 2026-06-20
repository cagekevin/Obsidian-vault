#!/usr/bin/env python3
"""
阿里云盘 CLI — 登录 / 查看 / 上传 / 下载 / 同步

默认操作【资源盘】（你 App 里"我的文件" / "资源库"），
不再让人猜盘、找盘。

命令:
  login                 扫码登录
  whoami                查看账号和所有盘容量
  ls [/路径]            列出目录（默认根目录 /）
  upload <本地路径> [/远程目录]   上传文件或文件夹（默认 /）
  download <远程路径> [本地目录]  下载文件或文件夹（并发+aria2）
  share <分享链接> [提取码]       从分享链接下载文件到 Temp/
  sync <本地文件夹> [/远程目录]   按 .gitignore 同步到云盘

注册: brew install aria2 && pip install aligo
触发: 兔子 aliyun、阿里云盘
"""
import os, shutil, subprocess, sys, fnmatch, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from aligo import Aligo, BaseFile

ali = Aligo(level=30)

# ─── 启动时自动切到资源盘 ───
try:
    u = ali.v2_user_get()
    RESOURCE_DRIVE = u.resource_drive_id
    if RESOURCE_DRIVE:
        ali.default_drive_id = RESOURCE_DRIVE
except Exception:
    RESOURCE_DRIVE = None


def _drive_name(did):
    """根据 drive_id 返回友好名称"""
    if did == RESOURCE_DRIVE:
        return '资源盘'
    return '备份盘' if did else '未知'


def _fmt(sz):
    if sz > 1e9: return f'{sz/1e9:.1f} GB'
    if sz > 1e6: return f'{sz/1e6:.1f} MB'
    if sz > 1e3: return f'{sz/1e3:.1f} KB'
    return f'{sz} B'


def _load_ignore(folder):
    """加载 .gitignore 规则"""
    for name in ('.gitignore', '.gitnore'):
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            rules = []
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    rules.append((line[1:], False) if line.startswith('!') else (line, True))
            return rules
    return []


def _match(path, rules):
    included = True
    for pat, ex in rules:
        if fnmatch.fnmatch(str(path), pat) or fnmatch.fnmatch(path.name, pat):
            included = not ex
    return included


# ─── 命令 ───

def login():
    Aligo(name='_re_login', re_login=True)
    print('✅ 登录成功')


def whoami():
    user = ali.get_user()
    drives = ali.list_my_drives()
    print(f'👤 {user.nick_name or user.user_name}  {user.phone}')
    for d in drives:
        name = _drive_name(d.drive_id)
        sz = _fmt(d.used_size or 0) + ' / ' + _fmt(d.total_size or 0) if d.total_size and d.total_size > 0 else _fmt(d.used_size or 0)
        star = ' ★' if d.drive_id == ali.default_drive_id else ''
        print(f'  {name:8s} {sz}{star}')
    print(f'当前操作盘: {_drive_name(ali.default_drive_id)}')


def ls(remote_path='/'):
    """列出目录"""
    folder = ali.get_folder_by_path(remote_path) if remote_path != '/' else None
    parent_id = folder.file_id if folder else 'root'
    files = ali.get_file_list(parent_id)
    if not files:
        print('（空）')
        return
    for f in files:
        if not f:
            continue
        icon = '📁' if f.type == 'folder' else '📄'
        sz = _fmt(f.size) if f.type == 'file' else ''
        print(f'  {icon}  {f.name:30s} {sz}')


def upload(local, remote_dir='/'):
    """上传文件或文件夹"""
    folder = ali.get_folder_by_path(remote_dir)
    if not folder:
        print(f'❌ 远程目录不存在: {remote_dir}')
        return
    local = os.path.abspath(local)
    if os.path.isdir(local):
        print(f'📤 上传文件夹: {local} → {remote_dir}')
        ali.upload_folder(local, parent_file_id=folder.file_id)
    elif os.path.isfile(local):
        print(f'📤 上传文件: {os.path.basename(local)} → {remote_dir}')
        ali.upload_file(local, parent_file_id=folder.file_id)
    else:
        print(f'❌ 路径不存在: {local}')
        return
    print('✅ 上传完成')


def download(remote_path, local_dir=None):
    """下载文件或文件夹（并发 + aria2 加速）"""
    local_dir = local_dir or os.getcwd()

    folder = ali.get_folder_by_path(remote_path)
    file = ali.get_file_by_path(remote_path) if not folder else None

    if folder:
        print(f'📥 下载文件夹: {remote_path}')
        dest = os.path.join(local_dir, os.path.basename(remote_path.rstrip('/')))
        os.makedirs(dest, exist_ok=True)

        files_to_dl = []
        def collect(path: str, f: BaseFile):
            local_path = os.path.join(local_dir, path.lstrip('/'))
            if f.type == 'folder':
                os.makedirs(local_path, exist_ok=True)
            else:
                files_to_dl.append((f, os.path.dirname(local_path)))
        ali.walk_files(collect, parent_file_id=folder.file_id)

        if not files_to_dl:
            print('（空文件夹）')
            return

        use_aria2 = shutil.which('aria2c')
        if use_aria2:
            print(f'📦 {len(files_to_dl)} 个文件, aria2 多线程加速')
        else:
            print(f'📦 {len(files_to_dl)} 个文件, 原生下载')

        done = 0
        with ThreadPoolExecutor(max_workers=5) as pool:
            fut = {}
            for f_obj, dl_dir in files_to_dl:
                if use_aria2:
                    url = ali.get_download_url(file_id=f_obj.file_id).url
                    cmd = ['aria2c', '-x', '5', '-s', '5', '--console-log-level=error',
                           '-d', dl_dir, '-o', f_obj.name, url]
                    fut[pool.submit(subprocess.run, cmd, capture_output=True, timeout=300)] = f_obj.name
                else:
                    fut[pool.submit(ali.download_file, file=f_obj, local_folder=dl_dir)] = f_obj.name
            for f in as_completed(fut):
                print(f'  ✅ {fut[f]}')
                done += 1
        print(f'✅ 下载完成: {done} 个文件 → {dest}')

    elif file:
        print(f'📥 下载文件: {file.name}')
        ali.download_file(file=file, local_folder=local_dir)
        print(f'✅ 下载完成 → {local_dir}')
    else:
        print(f'❌ 远程路径不存在: {remote_path}')


def sync(local_folder, remote_dir=None):
    """按 .gitignore 规则同步本地文件夹到云盘"""
    local_folder = os.path.abspath(local_folder)
    if not os.path.isdir(local_folder):
        print(f'❌ 文件夹不存在: {local_folder}')
        return

    if remote_dir is None:
        remote_dir = '/' + os.path.basename(local_folder)

    remote = ali.get_folder_by_path(remote_dir)
    if not remote:
        remote = ali.create_folder(os.path.basename(remote_dir), 'root')
        for part in remote_dir.strip('/').split('/')[1:]:
            remote = ali.create_folder(part, remote.file_id)
    print(f'📁 同步到: {remote_dir}')

    rules = _load_ignore(local_folder)
    rules.append(('.gitignore', True))
    rules.append(('.gitnore', True))

    matched = []
    for root, dirs, files in os.walk(local_folder):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            fp = Path(root) / f
            if fp.exists() and _match(fp, rules):
                matched.append(fp)

    if not matched:
        print('没有匹配的文件')
        return

    print(f'📦 {len(matched)} 个文件')
    for fp in matched:
        rel = str(fp.relative_to(local_folder))
        parts = rel.split('/')
        parent_id = remote.file_id
        for p in parts[:-1]:
            subs = ali.get_file_list(parent_id)
            found = None
            for s in subs:
                if s and s.type == 'folder' and s.name == p:
                    found = s; break
            if found:
                parent_id = found.file_id
            else:
                parent_id = ali.create_folder(p, parent_id).file_id
        try:
            ali.upload_file(str(fp), parent_file_id=parent_id)
            print(f'  📤 {rel}')
        except Exception as e:
            print(f'  ❌ {rel} → {e}')
    print('✅ 同步完成')


# ─── 分享链接下载 ───

def share(share_url, share_pwd=''):
    """
    从阿里云盘分享链接下载文件到 Temp/
    用法: python3 aliyun.py share <分享链接> [提取码]
    """
    # 1) 提取 share_id
    info = ali.share_link_extract_code(share_url)
    share_id = info.share_id
    share_pwd = share_pwd or info.share_pwd or ''

    print(f'📎 分享链接: {share_id}')
    print(f'🔑 提取码:   {share_pwd or "无"}')

    # 2) 获取 share_token
    share_token = ali.get_share_token(share_id, share_pwd=share_pwd)

    # 3) 列分享里的文件
    flist = ali.get_share_file_list(share_token)
    if not flist:
        print('❌ 分享链接里没有文件')
        return

    target_name = flist[0].name
    print(f'📄 文件: {target_name} ({_fmt(flist[0].size)})')

    # 4) 转存到当前默认盘
    print('⏳ 转存到云盘...')
    ali.share_file_save_all_to_drive(share_token)
    print('⏳ 等待服务器处理...')
    time.sleep(2)

    # 5) 在默认盘根目录找转存过来的文件
    found = None
    items = ali.get_file_list('root')
    base = target_name.rsplit('.', 1)[0]
    for f in items:
        if not f: continue
        if f.name == target_name or (base and base in f.name):
            found = f
            break

    # 6) 没找到再等一会
    if not found:
        print('⏳ 再等一下...')
        time.sleep(5)
        items = ali.get_file_list('root')
        for f in items:
            if not f: continue
            if f.name == target_name or (base and base in f.name):
                found = f
                break

    if not found:
        print(f'❌ 转存后未找到文件（可能重命名，请用 ls / 查看）')
        return

    # 7) 下载到 Temp/
    script_dir = Path(__file__).resolve().parent
    temp_dir = script_dir.parent / 'Temp'
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f'📥 下载到 Temp/...')
    ali.download_file(file=found, local_folder=str(temp_dir))
    print(f'✅ 完成 → Temp/{found.name} ({_fmt(found.size)})')


# ─── 入口 ───

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == 'login':
            login()
        elif cmd == 'whoami':
            whoami()
        elif cmd == 'ls':
            ls(sys.argv[2] if len(sys.argv) > 2 else '/')
        elif cmd == 'upload':
            if len(sys.argv) < 3:
                print('用法: python3 aliyun.py upload <本地路径> [/远程目录]'); sys.exit(1)
            upload(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '/')
        elif cmd == 'download':
            if len(sys.argv) < 3:
                print('用法: python3 aliyun.py download <远程路径> [本地目录]'); sys.exit(1)
            download(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
        elif cmd == 'sync':
            if len(sys.argv) < 3:
                print('用法: python3 aliyun.py sync <本地文件夹> [/远程目录]'); sys.exit(1)
            sync(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
        elif cmd == 'share':
            if len(sys.argv) < 3:
                print('用法: python3 aliyun.py share <分享链接> [提取码]'); sys.exit(1)
            share(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '')
        else:
            print(f'未知命令: {cmd}')
    except KeyboardInterrupt:
        print('\n已取消')
