import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fileUrl = 'file://' + path.join(__dirname, 'index.html');

const ids = ['xhs-01','xhs-02','xhs-03','xhs-04','xhs-05'];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 2 });
await page.goto(fileUrl, { waitUntil: 'networkidle' });
await page.waitForTimeout(1500); // let WebGL ink-flow settle

for (const id of ids) {
  const el = await page.$(`#${id}`);
  if (!el) { console.error('MISSING', id); continue; }
  await el.screenshot({ path: path.join(__dirname, 'output', `${id}.png`), omitBackground: false });
  console.log('SHOT', id);
}
await browser.close();
console.log('ALL_DONE');
