"""
翻译官 — 轻量化 Pipeline 执行引擎

灵感来自 BabyAGI functionz：用装饰器注册函数、声明依赖、自动按序执行、记录日志。

用法：
    from pipeline import Pipeline, register

    pipe = Pipeline()

    @register(pipe, dependencies=["step_a"])
    def step_b(ctx):
        ...

    pipe.run("step_b", ctx={"project_dir": "/path/to/project"})
"""

import json, os, sys, inspect, time, logging
from datetime import datetime
from functools import wraps

from utils import setup_logger, load_json, save_json, fatal

log = setup_logger("pipeline")


class Pipeline:
    """轻量级 Pipeline：注册函数 → 解析依赖 → 按序执行 → 记录日志"""

    def __init__(self):
        self._registry = {}       # {name: {"fn": callable, "dependencies": [...], "metadata": {...}}}
        self._executed = set()    # 当前 run 中已执行的函数名（防重复）
        self._log = []            # [{name, status, start, end, duration, error}]

    def register(self, fn=None, *, dependencies=None, metadata=None):
        """装饰器：注册一个函数到 pipeline"""
        dependencies = dependencies or []
        metadata = metadata or {}

        def decorator(func):
            name = func.__name__
            self._registry[name] = {
                "fn": func,
                "dependencies": dependencies,
                "metadata": metadata,
            }
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self.run(name, *args, **kwargs)
            return wrapper

        if fn is not None:
            return decorator(fn)
        return decorator

    def run(self, func_name, *args, ctx=None, _depth=0):
        """执行指定函数及其所有未执行的依赖"""
        if func_name not in self._registry:
            raise ValueError(f"Pipeline 中未注册函数: '{func_name}'")

        entry = self._registry[func_name]
        if ctx is None:
            ctx = {}

        # 递归执行依赖（使用同一个 ctx，结果会自动传播）
        for dep in entry["dependencies"]:
            if dep not in self._executed:
                self.run(dep, ctx=ctx, _depth=_depth + 1)

        # 防重复执行
        if func_name in self._executed:
            return ctx

        # 执行
        start = time.time()
        start_dt = datetime.now().isoformat()
        log.info(f"{'  ' * _depth}▶ {func_name}")

        try:
            result = entry["fn"](ctx)
            elapsed = time.time() - start
            log.info(f"{'  ' * _depth}✓ {func_name} ({elapsed:.1f}s)")
            self._log.append({
                "name": func_name,
                "status": "ok",
                "start": start_dt,
                "duration": round(elapsed, 2),
            })
            self._executed.add(func_name)

            # 如果函数返回了 dict，合并到 ctx
            if isinstance(result, dict):
                ctx.update(result)

        except Exception as e:
            elapsed = time.time() - start
            log.error(f"{'  ' * _depth}✗ {func_name}: {e}")
            self._log.append({
                "name": func_name,
                "status": "error",
                "start": start_dt,
                "duration": round(elapsed, 2),
                "error": str(e),
            })
            raise

        return ctx

    def save_log(self, path):
        save_json(path, self._log)

    def print_log(self):
        for entry in self._log:
            icon = "✓" if entry["status"] == "ok" else "✗"
            dur = entry.get("duration", 0)
            err = f" — {entry['error']}" if entry.get("error") else ""
            print(f"  {icon} {entry['name']} ({dur:.1f}s){err}")


# ── 辅助装饰器工厂 ──

def register(pipe, dependencies=None, metadata=None):
    """快捷装饰器，等价于 pipe.register(dependencies=..., metadata=...)"""
    def decorator(func):
        return pipe.register(func, dependencies=dependencies, metadata=metadata)
    return decorator
