// ============================================================
//  Lotofácil Pro - Harness de testes E2E (usuário real simulado)
// ============================================================
const path = require('path');
const fs = require('fs');
const path0 = require('path');
// playwright-core pode estar em node_modules local ou global
let chromium;
for (const alvo of ['playwright-core', 'playwright', path0.join(process.cwd(), 'node_modules', 'playwright-core')]) {
  try { chromium = require(alvo).chromium; break; } catch (e) { /* tenta o próximo */ }
}
if (!chromium) throw new Error('Instale playwright-core: npm i -D playwright-core');

const RAIZ = path0.resolve(__dirname, '..', '..');
const APP_FILE = process.env.APP_FILE || path0.join(RAIZ, 'APP_COMPLETO_100_FUNCIONAL.html');
const APP_URL = 'file://' + APP_FILE;
const SHOT_DIR = path0.join(__dirname, 'screenshots');
fs.mkdirSync(SHOT_DIR, { recursive: true });

// ---------- Resultado / assertivas ----------
const results = [];
let current = null;

function startTest(name, area) {
  current = { name, area, status: 'PASS', notes: [], error: null, evidence: [] };
  results.push(current);
  process.stdout.write(`\n[${area}] ${name}\n`);
  return current;
}
function ok(cond, msg) {
  if (cond) {
    process.stdout.write(`   ✅ ${msg}\n`);
    current.evidence.push('✅ ' + msg);
  } else {
    current.status = 'FAIL';
    process.stdout.write(`   ❌ ${msg}\n`);
    current.notes.push('❌ ' + msg);
    current.evidence.push('❌ ' + msg);
  }
  return !!cond;
}
function note(msg) {
  current.notes.push('ℹ️ ' + msg);
  process.stdout.write(`   • ${msg}\n`);
}
function fail(msg) {
  current.status = 'FAIL';
  current.notes.push('❌ ' + msg);
  process.stdout.write(`   ❌ ${msg}\n`);
}
async function screenshot(page, label) {
  try {
    const f = path.join(SHOT_DIR, `${label.replace(/[^a-z0-9_-]/gi, '_')}.png`);
    await page.screenshot({ path: f });
    return f;
  } catch (e) { return null; }
}

// ---------- Boot do app ----------
const LAUNCH_ARGS = ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
  '--enable-unsafe-swiftshader', '--force-device-scale-factor=1'];

async function launch() {
  // CHROMIUM_PATH permite usar um binário próprio (ex.: Chromium do @sparticuz/chromium em CI)
  const executablePath = process.env.CHROMIUM_PATH || undefined;
  return chromium.launch({ executablePath, headless: true, args: LAUNCH_ARGS });
}

async function newApp(browser, opts = {}) {
  const viewport = opts.viewport || { width: 414, height: 900 };
  const ctx = await browser.newContext({ viewport, acceptDownloads: true, permissions: [] });
  const page = await ctx.newPage();
  const errors = [];
  const dialogs = [];
  const dialogsCfg = { auto: 'accept', promptValue: null };
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => {
    const t = m.text();
    if (m.type() !== 'error') return;
    // erros de rede (fontes externas/offline) não são bugs de código
    if (/Failed to load resource|net::ERR_|ERR_FAILED|ERR_CONNECTION/.test(t)) return;
    errors.push('console: ' + t);
  });
  page.on('dialog', async d => {
    dialogs.push({ type: d.type(), message: d.message(), defaultValue: d.defaultValue() });
    try {
      if (dialogsCfg.auto === 'dismiss') await d.dismiss();
      else if (d.type() === 'prompt') await d.accept(dialogsCfg.promptValue != null ? dialogsCfg.promptValue : d.defaultValue());
      else await d.accept();
    } catch (e) { /* already handled */ }
  });
  if (opts.storage) {
    const s = opts.storage;
    await ctx.addInitScript(st => { for (const [k, v] of Object.entries(st)) localStorage.setItem(k, v); }, s);
  }
  // bloqueia requests externos (fontes) para testes estáveis offline
  await page.route('**/*', route => {
    const u = route.request().url();
    if (u.startsWith('file://')) return route.continue();
    return route.abort();
  });
  await page.goto(APP_URL, { waitUntil: 'load' });
  try {
    await page.waitForFunction(() => typeof window.showScreen === 'function' && typeof window.rodarIA === 'function', null, { timeout: 30000 });
  } catch (e) {
    throw new Error('App não inicializou (funções JS ausentes) em ' + APP_FILE + ': ' + errors.slice(0, 3).join(' | '));
  }
  await page.waitForTimeout(opts.settle != null ? opts.settle : 350);
  return { ctx, page, errors, dialogs, dialogsCfg };
}

// ---------- helpers de UI ----------
const activeScreen = p => p.evaluate(() => document.querySelector('.screen.active')?.id || null);
const navDisplay = p => p.evaluate(() => getComputedStyle(document.getElementById('bottomNav')).display);
const ls = (p, key) => p.evaluate(k => localStorage.getItem(k), key);
const lsAll = p => p.evaluate(() => Object.fromEntries(Object.entries(localStorage)));
const toastText = p => p.evaluate(() => {
  const t = document.getElementById('toast');
  return { text: t.textContent, shown: t.classList.contains('show') };
});
async function clickSel(p, sel, opts = {}) {
  const el = await p.waitForSelector(sel, { state: opts.state || 'visible', timeout: opts.timeout || 5000 });
  await el.click({ timeout: 5000 });
  if (opts.wait !== 0) await p.waitForTimeout(opts.wait != null ? opts.wait : 250);
}
async function clickText(p, sel, text, opts = {}) {
  const loc = p.locator(sel, { hasText: text }).first();
  await loc.click({ timeout: 5000 });
  if (opts.wait !== 0) await p.waitForTimeout(opts.wait != null ? opts.wait : 250);
}
const visible = async (p, sel) => p.evaluate(s => {
  const e = document.querySelector(s);
  if (!e) return false;
  const st = getComputedStyle(e);
  return st.display !== 'none' && st.visibility !== 'hidden' && e.offsetWidth > 0;
}, sel);
async function startApp(page) { // passa onboarding -> dashboard
  await page.evaluate(() => { localStorage.setItem('onboardDone', '1'); });
  await page.reload({ waitUntil: 'load' });
  await page.waitForTimeout(500);
}
async function stateSnapshot(page) {
  return page.evaluate(() => {
    const t = document.getElementById('toast');
    return JSON.stringify({
      screen: document.querySelector('.screen.active')?.id,
      toast: t ? t.textContent + '|' + t.classList.contains('show') : '',
      logs: document.getElementById('logArea')?.textContent.slice(-120) || '',
      rank: (document.getElementById('rankingList')?.innerHTML || '').length,
      fixas: document.getElementById('fixasChips')?.textContent || '',
      bloq: document.getElementById('bloqChips')?.textContent || '',
      ls: (() => {
        const ent = Object.entries(localStorage);
        const bruto = ent.map(([k, v]) => k + '=' + String(v)).join(';');
        let h = 0; for (let i = 0; i < bruto.length; i++) { h = (h * 31 + bruto.charCodeAt(i)) | 0; }
        return ent.length + '|' + bruto.length + '|' + h;
      })(),
      toggles: [...document.querySelectorAll('.screen.active .toggle')].map(t => t.classList.contains('on') ? 1 : 0).join(''),
      favs: (() => { try { return JSON.parse(localStorage.getItem('favoritos') || '[]').length; } catch (e) { return -1; } })(),
      ia: document.getElementById('iaModeLabel')?.textContent || '',
      det: document.getElementById('detId')?.textContent || '',
      banks: document.getElementById('bancaVal')?.textContent || '',
      top: document.getElementById('topScoreVal')?.textContent || '',
      gen: document.getElementById('genVal')?.textContent || '',
      heat: (document.getElementById('heatmapDash')?.innerHTML || '').length,
      sensor: (document.getElementById('gridSensor')?.innerHTML || '').length,
      chk: [...document.querySelectorAll('.screen.active .seg-btn.active,.screen.active .filtro-chip:not(.inactive),.screen.active .est-row .arrow,.screen.active .toggle.on,.screen.active .modo-card.active,.screen.active .tab.active')].map(e => e.textContent.trim()).join('|')
    });
  });
}

// seleciona a matriz recém-gerada (maior id/timestamp) em vez da posição 1 do ranking
async function matrizNova(page) {
  return page.evaluate(() => {
    const lista = JSON.parse(localStorage.getItem('rankingMatrizes') || '[]');
    return lista.slice().sort((a, b) => (b.id || 0) - (a.id || 0))[0] || null;
  });
}

function report(file) {
  fs.writeFileSync(file, JSON.stringify(results, null, 2));
  const pass = results.filter(r => r.status === 'PASS').length;
  console.log(`\n\n================ RESUMO ================`);
  results.forEach(r => console.log(`${r.status === 'PASS' ? '✅' : '❌'} [${r.area}] ${r.name}${r.status === 'FAIL' ? '  << FALHOU' : ''}`));
  console.log(`\nTOTAL: ${results.length} cenários | PASSOU: ${pass} | FALHOU: ${results.length - pass}`);
}

module.exports = {
  APP_URL, SHOT_DIR, results, startTest, ok, note, fail, screenshot, matrizNova,
  launch, newApp, activeScreen, navDisplay, ls, lsAll, toastText, clickSel, clickText, visible,
  startApp, stateSnapshot, report
};
