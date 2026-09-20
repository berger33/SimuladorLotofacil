// ============================================================
//  Lotofácil Pro — Suíte E2E completa (funcional + regressivo)
//  Uso: LD_LIBRARY_PATH=/tmp/libs/lib node e2e.js [area]
// ============================================================
const L = require('./lib');

const ONLY = process.argv[2] || null;
const run = (area) => !ONLY || ONLY === area;

// ------------------------------------------------------------ utilidades de teste
async function bootOnboard(browser, opts = {}) {
  const app = await L.newApp(browser, opts);
  return app;
}
async function bootDashboard(browser, opts = {}) {
  const app = await L.newApp(browser, opts);
  await L.startApp(app.page);
  return app;
}
async function goto(page, name) {
  await page.evaluate(n => window.showScreen(n), name);
  await page.waitForTimeout(180);
}
// navegação como um usuário faria (abas inferiores, botões de voltar)
async function irPara(page, name) {
  const navOn = await L.navDisplay(page) === 'flex';
  const tab = await page.$(`#bottomNav .tab[data-screen="${name}"]`);
  if (navOn && tab) { await tab.click(); await page.waitForTimeout(200); return; }
  await page.evaluate(n => window.showScreen(n), name);
  await page.waitForTimeout(200);
}
const NUM = n => String(n).padStart(2, '0');

function validarJogo(jogo, fixas, bloqueadas) {
  const errs = [];
  if (!Array.isArray(jogo) || jogo.length !== 15) errs.push('não tem 15 dezenas');
  if (new Set(jogo).size !== jogo.length) errs.push('dezenas repetidas');
  if (jogo.some(n => n < 1 || n > 25 || !Number.isInteger(n))) errs.push('fora de 1..25');
  if (jogo.join(',') !== [...jogo].sort((a, b) => a - b).join(',')) errs.push('não ordenado');
  (fixas || []).forEach(f => { if (!jogo.includes(f)) errs.push(`fixa ${f} ausente`); });
  (bloqueadas || []).forEach(b => { if (jogo.includes(b)) errs.push(`bloqueada ${b} presente`); });
  return errs;
}

// ------------------------------------------------------------ suíte
(async () => {
  const browser = await L.launch();
  const T = L.startTest;

  // ============================================================ BOOT
  if (run('BOOT')) {
    T('Boot: app abre sem erro de JS e mostra onboarding na 1ª vez', 'BOOT');
    {
      const { page, errors, ctx } = await bootOnboard(browser);
      const scr = await L.activeScreen(page);
      L.ok(scr === 'screen-onboarding', `tela inicial = ${scr} (esperado screen-onboarding na 1ª execução)`);
      L.ok(await L.visible(page, '#screen-onboarding'), 'conteúdo do onboarding visível');
      L.ok(await L.navDisplay(page) === 'none', 'barra de navegação oculta no onboarding');
      L.ok(errors.length === 0, 'nenhum erro de JS no console: ' + (errors.slice(0, 3).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Boot: todas as funções da API pública existem (sem script quebrado)', 'BOOT');
    {
      const { page, ctx } = await bootOnboard(browser);
      const fns = ['carregarSorteios', 'calcularEstatisticasReais', 'renderUltimoConcurso', 'analisarAtrasos',
        'gerarPrevisaoMarkov', 'calcularFrequencia', 'gerarJogoAleatorio', 'gerarJogoBaseadoEmAntigos', 'filtrarJogo',
        'gerarSistema', 'avaliarSistema', 'setModoGeracao', 'showPremiumLock', 'iniciarMotorReal', 'gerarBase20',
        'gerarRankingInicial', 'getHeatColor', 'renderHeatmaps', 'renderSensor', 'rodarIA', 'renderAnomalias',
        'renderRanking', 'abrirDetalhes', 'toggleFixa', 'renderFixasBloqueadas', 'toggleBloq', 'editarFixas',
        'editarBloqueadas', 'setMutacao', 'setSeveridade', 'toggleMem', 'setEstrategia', 'fixarTop5', 'log',
        'showToast', 'copiarAposta', 'compartilharWhats', 'stressTest', 'testeCaos', 'verTodasApostas', 'favoritar',
        'setRankingTab', 'atualizarRanking', 'editarBanca', 'deletarDados', 'comprarPlano', 'restaurarCompras',
        'drawChart', 'showScreen', 'nextOnboard', 'pularOnboard', 'toggleMenu'];
      const missing = await page.evaluate(list => list.filter(f => typeof window[f] !== 'function'), fns);
      L.ok(missing.length === 0, `todas as ${fns.length} funções existem` + (missing.length ? ' — AUSENTES: ' + missing.join(', ') : ''));
      await ctx.close();
    }
  }

  // ============================================================ ONBOARDING
  if (run('ONB')) {
    T('Onboarding: 1/3 → 2/3 → 3/3 → Começar leva ao Dashboard', 'ONB');
    {
      const { page, errors, ctx } = await bootOnboard(browser);
      for (const passo of ['1/3', '2/3', '3/3']) {
        const txt = await page.textContent('#onboardPage');
        L.ok(txt.trim() === passo, `página do onboarding = ${txt.trim()} (esperado ${passo})`);
        if (passo !== '3/3') { await L.clickSel(page, '#btnOnboard', { wait: 200 }); }
      }
      L.ok((await page.textContent('#btnOnboard')).includes('Começar'), 'botão final muda para "Começar"');
      L.ok((await page.textContent('#onboardTitle')).includes('Jogos'), 'título da 3ª página correto: ' + (await page.textContent('#onboardTitle')).trim());
      await L.clickSel(page, '#btnOnboard', { wait: 400 });
      L.ok(await L.activeScreen(page) === 'screen-dashboard', 'foi para o Dashboard após Começar');
      L.ok(await L.ls(page, 'onboardDone') === '1', 'onboardDone salvo no localStorage');
      L.ok(await L.navDisplay(page) === 'flex', 'barra de navegação aparece no Dashboard');
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(500);
      L.ok(await L.activeScreen(page) === 'screen-dashboard', 'após recarregar, onboarding NÃO reaparece');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Onboarding: botão Pular vai ao Dashboard e não reaparece', 'ONB');
    {
      const { page, ctx } = await bootOnboard(browser);
      await L.clickText(page, '.btn-skip', 'Pular', { wait: 350 });
      L.ok(await L.activeScreen(page) === 'screen-dashboard', 'foi para o Dashboard com Pular');
      L.ok(await L.ls(page, 'onboardDone') === '1', 'onboardDone salvo');
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(500);
      L.ok(await L.activeScreen(page) === 'screen-dashboard', 'não reaparece após Pular');
      await ctx.close();
    }
  }

  // ============================================================ NAVEGAÇÃO
  if (run('NAV')) {
    T('Navegação: 5 abas inferiores trocam de tela corretamente', 'NAV');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      const abas = [['dashboard', '🏠'], ['heatmap', '📊'], ['gerador', '🔄'], ['ranking', '📋'], ['config', '⚙️']];
      for (const [scr] of abas) {
        await L.clickSel(page, `#bottomNav .tab[data-screen="${scr}"]`, { wait: 250 });
        const at = await L.activeScreen(page);
        L.ok(at === 'screen-' + scr, `aba ${scr} → tela ativa ${at}`);
        const tabActive = await page.evaluate(s => document.querySelector(`#bottomNav .tab[data-screen="${s}"]`)?.classList.contains('active'), scr);
        L.ok(tabActive, `aba ${scr} marcada como ativa (roxo)`);
      }
      L.ok(await L.navDisplay(page) === 'none', 'barra some nas Configurações (como no design)');
      await L.clickSel(page, '#screen-config .menu', { wait: 250 });
      L.ok(await L.activeScreen(page) === 'screen-dashboard', 'botão ← das Configurações volta ao Dashboard');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Navegação: ida e volta por todas as telas repetidas vezes (regressão)', 'NAV');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      const rota = ['heatmap', 'dashboard', 'gerador', 'dashboard', 'ranking', 'dashboard', 'config', 'dashboard', 'heatmap', 'gerador', 'ranking', 'config'];
      let falhas = 0;
      for (const alvo of rota) {
        await irPara(page, alvo).catch(() => falhas++);
        const at = await L.activeScreen(page);
        if (at !== 'screen-' + alvo) { falhas++; L.note(`rota ${alvo}: tela ativa ${at}`); }
      }
      L.ok(falhas === 0, `12 navegações seguidas sem falha (falhas=${falhas})`);
      // também via cards do dashboard
      const handlersAntes = await page.evaluate(() => document.querySelectorAll('[onclick]').length);
      L.ok(handlersAntes > 60, `elementos clicáveis presentes: ${handlersAntes}`);
      L.ok(errors.length === 0, 'sem erros de JS na navegação: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Navegação: tela Inteligência (IA) é acessível e tem volta', 'NAV');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      const entradas = await page.evaluate(() => {
        const els = [...document.querySelectorAll('[onclick]')].filter(e => /inteligencia/.test(e.getAttribute('onclick') || ''));
        return { bottom: !!document.querySelector('#bottomNav .tab[data-screen="inteligencia"]'), outros: els.length };
      });
      L.ok(entradas.bottom || entradas.outros > 0, `existe ao menos 1 forma de abrir a tela de IA (nav=${entradas.bottom}, botões=${entradas.outros})`);
      await goto(page, 'inteligencia');
      L.ok(await L.activeScreen(page) === 'screen-inteligencia', 'tela Inteligência abre');
      L.ok((await page.textContent('#totalSorteiosIA')).trim() === '3675', 'hero mostra 3675 sorteios');
      const temVolta = await page.evaluate(() => {
        const s = document.getElementById('screen-inteligencia');
        return [...s.querySelectorAll('[onclick]')].some(e => /showScreen\('(dashboard|heatmap|gerador|ranking|config)'\)|history\.back/.test(e.getAttribute('onclick') || ''));
      });
      L.ok(temVolta, 'existe botão de voltar na tela de Inteligência');
      if (temVolta) {
        await page.evaluate(() => {
          const s = document.getElementById('screen-inteligencia');
          const b = [...s.querySelectorAll('[onclick]')].find(e => /showScreen\(/.test(e.getAttribute('onclick') || ''));
          b.click();
        });
        await page.waitForTimeout(250);
        L.ok((await L.activeScreen(page)) !== 'screen-inteligencia', 'consegue sair da tela de Inteligência');
      }
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  // ============================================================ DASHBOARD
  if (run('DASH')) {
    T('Dashboard: top score, geração atual e 4 estatísticas coerentes', 'DASH');
    {
      const { page, ctx } = await bootDashboard(browser);
      const fmt = v => v.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, (m, o, str) => str.indexOf('.') === -1 ? '.' : m);
      const dados = await page.evaluate(() => ({
        rank: JSON.parse(localStorage.getItem('rankingMatrizes') || '[]'),
        top: parseFloat(localStorage.getItem('topScore') || '0')
      }));
      const melhorMatriz = dados.rank.reduce((a, m) => Math.max(a, m.score), 1234.56);
      const top = (await page.textContent('#topScoreVal')).trim();
      L.ok(Math.abs(dados.top - melhorMatriz) < 0.01, `top score inicial coerente com a melhor matriz real (R$ ${dados.top.toFixed(2)} = R$ ${melhorMatriz.toFixed(2)})`);
      L.ok(/^R\$ [\d.]+,\d{2}$/.test(top), `top score exibido em R$: "${top}"`);
      L.ok((await page.textContent('#genVal')).trim() === '42', 'geração atual = 42');
      const media = (await page.textContent('#statMedia')).trim();
      const max = (await page.textContent('#statMax')).trim();
      const limpa = t => parseFloat(t.replace(/\./g, '').replace(',', '.'));
      L.ok(Math.abs(limpa(media) - dados.top * 0.5) < 0.01, `MÉDIA = ${media} (= top*0,5)`);
      L.ok(Math.abs(limpa(max) - dados.top) < 0.01, `MÁXIMO = ${max} (= top score)`);
      const maxGen = (await page.textContent('#statMaxGen')).trim();
      L.ok(/Gera[çc][ãa]o 42/.test(maxGen), `rótulo do máximo coerente com a geração exibida: "${maxGen}"`);
      await ctx.close();
    }

    T('Dashboard: gráfico de convergência desenhado em canvas com 2 séries', 'DASH');
    {
      const { page, ctx } = await bootDashboard(browser);
      await page.waitForTimeout(400);
      const info = await page.evaluate(() => {
        const c = document.getElementById('chartConv');
        if (!c) return { err: 'canvas ausente' };
        const ctx2 = c.getContext('2d');
        const d = ctx2.getImageData(0, 0, c.width, c.height).data;
        const cores = new Set();
        let pintados = 0;
        for (let i = 0; i < d.length; i += 4) {
          const [r, g, b, a] = [d[i], d[i + 1], d[i + 2], d[i + 3]];
          if (a > 20) { pintados++; cores.add(`${r},${g},${b}`); }
        }
        return { w: c.width, h: c.height, pintados, cores: cores.size };
      });
      L.ok(!info.err, 'canvas existe');
      L.ok(info.w > 100 && info.h > 30, `canvas com tamanho real 2x retine: ${info.w}x${info.h}`);
      L.ok(info.pintados > 200, `pixels desenhados: ${info.pintados}`);
      L.ok(info.cores >= 2, `cores distintas no gráfico (2 linhas esperadas): ${info.cores}`);
      await ctx.close();
    }

    T('Dashboard: último concurso 3675 com as 15 dezenas reais', 'DASH');
    {
      const { page, ctx } = await bootDashboard(browser);
      const num = (await page.textContent('#ultimoConcursoNum')).trim();
      L.ok(num === 'Concurso 3675', `rótulo: "${num}"`);
      const bolas = await page.evaluate(() => [...document.querySelectorAll('#ultimoBolas .bola')].map(b => b.textContent.trim()));
      L.ok(bolas.length === 15, `15 bolas renderizadas (${bolas.length})`);
      const esperado = [2, 3, 5, 6, 9, 10, 11, 13, 14, 16, 18, 20, 23, 24, 25].map(NUM);
      L.ok(JSON.stringify(bolas) === JSON.stringify(esperado), `dezenas reais corretas: [${bolas.join(' ')}]`);
      await ctx.close();
    }

    T('Dashboard: anomalias reais (atraso vs média) e heatmap 5x5 com cores reais', 'DASH');
    {
      const { page, ctx } = await bootDashboard(browser);
      const anom = await page.evaluate(() => [...document.querySelectorAll('#anomaliasList .anom-row')].map(r => r.textContent.replace(/\s+/g, ' ').trim()));
      L.ok(anom.length >= 1, `linhas de anomalia renderizadas: ${anom.length}`);
      L.ok(anom.every(t => /Atual \d+ vs M[ée]dia/.test(t)), 'cada linha mostra "Atual X vs Média Y" (dados reais)');
      L.ok(anom.some(t => /ALTA|M[ÉE]DIA|BAIXA/.test(t)), 'badge de severidade presente (ALTA/MÉDIA/BAIXA)');
      const heat = await page.evaluate(() => {
        const cells = [...document.querySelectorAll('#heatmapDash .cell')];
        return { n: cells.length, cores: [...new Set(cells.map(c => c.style.background || c.style.backgroundColor))], nums: cells.slice(0, 5).map(c => c.textContent) };
      });
      L.ok(heat.n === 25, `grid 5x5 = 25 células (${heat.n})`);
      L.ok(heat.cores.length > 3, `cores de frequência distintas: ${heat.cores.length}`);
      L.ok(heat.nums.join(',') === '01,02,03,04,05', 'células numeradas 01..25');
      await ctx.close();
    }

    T('Dashboard: estatísticas reais 3675 (mais/menos frequente, média de ímpares)', 'DASH');
    {
      const { page, ctx } = await bootDashboard(browser);
      L.ok((await page.textContent('#totalSorteios')).trim() === '3675', 'total de sorteios = 3675');
      const mais = (await page.textContent('#dezenaMaisFreq')).trim();
      const menos = (await page.textContent('#dezenaMenosFreq')).trim();
      const impares = parseFloat((await page.textContent('#mediaImpares')).trim().replace(',', '.'));
      L.ok(/^\d{2} \(\d+x\)$/.test(mais), `dezena mais frequente: ${mais}`);
      L.ok(/^\d{2} \(\d+x\)$/.test(menos), `dezena menos frequente: ${menos}`);
      L.ok(impares > 7 && impares < 8.2, `média de ímpares ≈ 7,5 → ${impares}`);
      // clique no heatmap fixa dezena
      await page.click('#heatmapDash .cell:nth-child(3)');
      await page.waitForTimeout(250);
      L.ok((await L.toastText(page)).shown, 'clique no heatmap dá feedback (toast)');
      await ctx.close();
    }
  }

  // ============================================================ GERADOR
  if (run('GER')) {
    T('Gerador: modo dual (Antigos grátis ATIVO / Aleatório Premium bloqueado)', 'GER');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      const ativo = await page.evaluate(() => document.querySelector('.modo-card.active')?.id);
      L.ok(ativo === 'modoAntigos', `modo inicial ativo = ${ativo} (Antigos, grátis)`);
      L.ok(/Premium/i.test(await page.textContent('#modoAleatorio')), 'card Aleatório exibe selo Premium');
      L.ok(/Antigos/i.test(await page.textContent('#modoDesc')), 'descrição do modo = ' + (await page.textContent('#modoDesc')).trim().slice(0, 60));
      await L.clickSel(page, '#modoAleatorio', { wait: 300 });
      L.ok(await L.visible(page, '.premium-lock'), 'bloqueio 🔒 aparece ao tentar Aleatório sem Premium');
      L.ok(await L.ls(page, 'modoGeracao') === 'antigos', 'modo NÃO muda para aleatório sem Premium');
      L.ok(await L.activeScreen(page) === 'screen-gerador', 'permanece no gerador com o cadeado');
      // botão desbloquear
      await L.clickText(page, '.premium-lock .btn-unlock', 'Desbloquear', { wait: 400 });
      L.ok(await L.activeScreen(page) === 'screen-premium', 'botão "Desbloquear Premium" abre a tela Premium');
      // voltar e usar modo grátis
      await L.clickSel(page, '#screen-premium .menu', { wait: 300 });
      await goto(page, 'gerador');
      await L.clickSel(page, '#modoAleatorio', { wait: 250 });
      await L.clickText(page, '.premium-lock .btn-outline', 'Usar Modo Grátis', { wait: 350 });
      L.ok(!(await L.visible(page, '.premium-lock')), 'cadeado removido ao escolher modo grátis');
      L.ok(await page.evaluate(() => document.querySelector('.modo-card.active')?.id) === 'modoAntigos', 'modo Antigos continua ativo');
      await ctx.close();
    }

    T('Gerador: quantidade de jogos (10 Free / 15 / 20 / 33 Pro) com paywall', 'GER');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      const opts = await page.evaluate(() => [...document.querySelectorAll('#segJogos .seg-btn')].map(b => ({ v: b.dataset.v, txt: b.textContent.trim() })));
      L.ok(opts.length === 4, `4 opções de quantidade: ${opts.map(o => o.v).join('/')}`);
      L.ok(opts.some(o => o.v === '10' && /Free/i.test(o.txt)), 'opção 10 marcada como Free');
      await L.clickSel(page, '#segJogos .seg-btn[data-v="10"]', { wait: 200 });
      L.ok(await page.evaluate(() => document.querySelector('#segJogos .seg-btn.active')?.dataset.v) === '10', 'seleciona 10 jogos no Free');
      for (const v of ['15', '20', '33']) {
        await goto(page, 'gerador');
        await L.clickSel(page, `#segJogos .seg-btn[data-v="${v}"]`, { wait: 350 });
        L.ok(await L.activeScreen(page) === 'screen-premium', `opção ${v} sem Premium redireciona para Premium (paywall)`);
      }
      await ctx.close();
    }

    T('Gerador: engenharia genética — fixas, bloqueadas, limites e validações', 'GER');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      let fixas = await page.evaluate(() => [...document.querySelectorAll('#fixasChips .chip')].map(c => c.textContent.trim()));
      L.ok(fixas.length === 3 && fixas[0] === '01 ✕', `fixas iniciais: [${fixas.join(', ')}]`);
      let bloq = await page.evaluate(() => [...document.querySelectorAll('#bloqChips .chip')].map(c => c.textContent.trim()));
      L.ok(bloq.length === 1 && bloq[0] === '25 ✕', `bloqueadas iniciais: [${bloq.join(', ')}]`);
      // remover fixa
      await L.clickSel(page, '#fixasChips .chip:nth-child(1)', { wait: 250 });
      fixas = await page.evaluate(() => [...document.querySelectorAll('#fixasChips .chip')].map(c => c.textContent.trim()));
      L.ok(!fixas.some(f => f.startsWith('01')), `fixa 01 removida pela lixeira ✕ → agora [${fixas.join(', ')}]`);
      L.ok(JSON.parse(await L.ls(page, 'fixas')).join(',') === '5,10', 'localStorage de fixas atualizado');
      // adicionar fixa clicando no heatmap
      await goto(page, 'dashboard');
      await page.evaluate(() => { document.querySelectorAll('#heatmapDash .cell')[19].click(); });
      await page.waitForTimeout(250);
      const fixas2 = JSON.parse(await L.ls(page, 'fixas'));
      L.ok(fixas2.includes(20), `clique no heatmap adiciona fixa 20 → [${fixas2.join(', ')}]`);
      // máximo 6 fixas
      await page.evaluate(() => { [1, 2, 3, 4, 5, 6, 7, 8].forEach(n => window.toggleFixa(n)); });
      await page.waitForTimeout(200);
      const fixas3 = JSON.parse(await L.ls(page, 'fixas'));
      L.ok(fixas3.length <= 6, `limite de 6 fixas respeitado (${fixas3.length})`);
      // bloqueada não pode ser fixa e vice-versa (estado preparado por localStorage + reload)
      await page.evaluate(() => { localStorage.setItem('fixas', '[]'); localStorage.setItem('bloqueadas', '[7]'); localStorage.setItem('onboardDone', '1'); });
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(600); await goto(page, 'gerador');
      await page.evaluate(() => window.toggleFixa(7));
      await page.waitForTimeout(250);
      L.ok(!JSON.parse(await L.ls(page, 'fixas')).includes(7), 'não permite fixar dezena que está bloqueada');
      await page.evaluate(() => { localStorage.setItem('fixas', '[8]'); localStorage.setItem('bloqueadas', '[]'); });
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(600); await goto(page, 'gerador');
      await page.evaluate(() => window.toggleBloq(8));
      await page.waitForTimeout(250);
      L.ok(!JSON.parse(await L.ls(page, 'bloqueadas')).includes(8), 'não permite bloquear dezena que está fixa');
      // bloqueadas máx 5
      await page.evaluate(() => { localStorage.setItem('fixas', '[]'); localStorage.setItem('bloqueadas', '[]'); });
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(600); await goto(page, 'gerador');
      await page.evaluate(() => [1, 2, 3, 4, 5, 6, 7].forEach(n => window.toggleBloq(n)));
      await page.waitForTimeout(250);
      L.ok(JSON.parse(await L.ls(page, 'bloqueadas')).length <= 5, `limite de 5 bloqueadas respeitado (${JSON.parse(await L.ls(page, 'bloqueadas')).length})`);
      await ctx.close();
    }

    T('Gerador: edição de fixas/bloqueadas por texto com validação', 'GER');
    {
      const { page, ctx, dialogsCfg } = await bootDashboard(browser);
      await goto(page, 'gerador');
      dialogsCfg.promptValue = '1,3,5';
      await page.evaluate(() => window.editarFixas());
      await page.waitForTimeout(300);
      L.ok(JSON.parse(await L.ls(page, 'fixas')).join(',') === '1,3,5', 'editar fixas via campo de texto salva [1,3,5]');
      dialogsCfg.promptValue = '2, 30, abc, 4';
      await page.evaluate(() => window.editarFixas());
      await page.waitForTimeout(300);
      const fx = JSON.parse(await L.ls(page, 'fixas'));
      L.ok(fx.every(n => n >= 1 && n <= 25), `valores inválidos (30/abc) filtrados → [${fx.join(', ')}]`);
      dialogsCfg.promptValue = '1,2,3,4,5,6,7,8,9';
      await page.evaluate(() => window.editarFixas());
      await page.waitForTimeout(300);
      const fx2 = JSON.parse(await L.ls(page, 'fixas'));
      L.ok(fx2.length <= 6, `máximo de 6 fixas aplicado também na edição por texto (${fx2.length})`);
      dialogsCfg.promptValue = '7,8,9,10,11,12,13';
      await page.evaluate(() => window.editarBloqueadas());
      await page.waitForTimeout(300);
      const bl = JSON.parse(await L.ls(page, 'bloqueadas'));
      L.ok(bl.length <= 5, `máximo de 5 bloqueadas aplicado na edição por texto (${bl.length})`);
      dialogsCfg.promptValue = '';
      await page.evaluate(() => window.editarBloqueadas());
      await page.waitForTimeout(300);
      L.ok(JSON.parse(await L.ls(page, 'bloqueadas')).length === 0, 'permite limpar todas as bloqueadas');
      await ctx.close();
    }

    T('Gerador: filtros inteligentes (chips) com contador e persistência', 'GER');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      const chips = await page.evaluate(() => [...document.querySelectorAll('.filtro-chip')].map(c => ({ f: c.dataset.f, on: !c.classList.contains('inactive'), txt: c.textContent.trim() })));
      L.ok(chips.length === 6, `6 filtros disponíveis: ${chips.map(c => c.txt).join(' / ')}`);
      const badge0 = await page.textContent('#filtrosAtivosBadge');
      L.ok(badge0.trim() === '4 ativos', `badge inicial = "${badge0.trim()}" (4 ativos por padrão)`);
      await L.clickSel(page, '.filtro-chip[data-f="soma"]', { wait: 200 });
      L.ok((await page.textContent('#filtrosAtivosBadge')).trim() === '5 ativos', 'ativar filtro atualiza contador para 5');
      await L.clickSel(page, '.filtro-chip[data-f="soma"]', { wait: 200 });
      L.ok((await page.textContent('#filtrosAtivosBadge')).trim() === '4 ativos', 'desativar filtro volta contador para 4');
      const salvo = JSON.parse(await L.ls(page, 'filtrosAtivos'));
      L.ok(Array.isArray(salvo) && salvo.length === 4, `filtros persistidos: [${salvo.join(', ')}]`);
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(500); await goto(page, 'gerador');
      L.ok((await page.textContent('#filtrosAtivosBadge')).trim() === '4 ativos', 'contador correto após recarregar (persistência)');
      await ctx.close();
    }

    T('Gerador: sliders (mutação/severidade), toggles e estratégias', 'GER');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      const slider = page.locator('.slider').first();
      await page.evaluate(() => document.querySelector('.slider').scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(250);
      const box = await slider.boundingBox();
      const alvo = await page.evaluate(([x, y]) => { const e = document.elementFromPoint(x, y); return e ? (e.className || e.tagName).toString() : 'null'; }, [box.x + box.width * 0.5, box.y + box.height / 2]);
      L.ok(/slider/.test(alvo), `slider de mutação clicável (elemento no ponto central: ${alvo})`);
      await slider.click({ position: { x: box.width * 0.5, y: box.height / 2 } });
      await page.waitForTimeout(200);
      const mut = await page.textContent('#mutacaoVal');
      L.ok(Math.abs(parseInt(mut) - 13) <= 2, `clique no meio do slider de mutação → ${mut} (esperado ~13%)`);
      L.ok(/^\d+%$/.test((await page.textContent('#severidadeVal')).trim()), 'slider de severidade exibe percentual');
      L.ok((await L.ls(page, 'mutacao')) !== null, `mutação salva no localStorage (${await L.ls(page, 'mutacao')})`);
      const sevSlider = page.locator('.slider').nth(1);
      await page.evaluate(() => document.querySelectorAll('.slider')[1].scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(200);
      const sbox = await sevSlider.boundingBox();
      await sevSlider.click({ position: { x: sbox.width * 0.8, y: sbox.height / 2 } });
      await page.waitForTimeout(200);
      const sev = parseInt(await page.textContent('#severidadeVal'));
      L.ok(Math.abs(sev - 80) <= 3, `clique no slider de severidade → ${sev}% (esperado ~80%)`);
      // toggles
      const on0 = await page.evaluate(() => document.getElementById('toggleMemoria').classList.contains('on'));
      await L.clickSel(page, '#toggleMemoria', { wait: 200 });
      const on1 = await page.evaluate(() => document.getElementById('toggleMemoria').classList.contains('on'));
      L.ok(on0 !== on1, `toggle Memória de Erro alterna (${on0} → ${on1})`);
      await L.clickSel(page, '#toggleHamming', { wait: 200 });
      L.ok(true, 'toggle Distância de Hamming clicável sem erro');
      // estratégias
      for (const est of ['conservador', 'agressivo', 'robo', 'preguicoso']) {
        await L.clickSel(page, `.est-row[onclick="setEstrategia('${est}')"]`, { wait: 180 });
        const marca = await page.evaluate(e => {
          const map = { conservador: 'estCons', agressivo: 'estAgr', robo: 'estRobo', preguicoso: 'estPreg' };
          return document.getElementById(map[e]).textContent.trim();
        }, est);
        L.ok(marca === '✓', `estratégia ${est} marcada com ✓ (persistida: ${await L.ls(page, 'estrategia')})`);
      }
      await ctx.close();
    }

    T('Motor: geração real no modo grátis (Antigos) com 10 jogos', 'MOT');
    mot1: {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      await L.clickSel(page, '#segJogos .seg-btn[data-v="10"]', { wait: 150 });
      const antes = { gen: await page.textContent('#genVal'), rank: await page.evaluate(() => document.getElementById('rankingList').children.length) };
      const logs0 = await page.evaluate(() => document.querySelectorAll('#logArea .log-line').length);
      await L.clickSel(page, '#btnMotor', { wait: 120 });
      const durante = await page.evaluate(() => ({ dis: document.getElementById('btnMotor').disabled, txt: document.getElementById('btnMotor').textContent.trim() }));
      L.ok(durante.dis && /GERANDO/.test(durante.txt), `feedback imediato no botão: "${durante.txt}"`);
      await page.waitForTimeout(1800);
      const btn = await page.evaluate(() => ({ dis: document.getElementById('btnMotor').disabled, txt: document.getElementById('btnMotor').textContent.trim() }));
      L.ok(!btn.dis && /INICIAR MOTOR/.test(btn.txt), 'botão volta ao normal após gerar');
      const toast = await L.toastText(page);
      L.ok(toast.shown && /10 jogos gerados/i.test(toast.text), `toast de sucesso: "${toast.text}"`);
      const logsN = await page.evaluate(() => document.querySelectorAll('#logArea .log-line').length);
      L.ok(logsN >= logs0 + 4, `logs detalhados da geração (${logsN - logs0} linhas novas)`);
      const store = await page.evaluate(() => ({
        rank: JSON.parse(localStorage.getItem('rankingMatrizes') || '[]'),
        gen: parseInt(localStorage.getItem('geracaoAtual')),
        top: parseFloat(localStorage.getItem('topScore'))
      }));
      const melhor = store.rank.slice().sort((a, b) => b.score - a.score)[0];
      L.ok(store.rank.length >= 9, `ranking ganhou a nova matriz (total ${store.rank.length})`);
      const nova = await L.matrizNova(page);
      L.ok(nova && nova.jogos && nova.jogos.length === 10, `matriz nova contém 10 jogos (${nova && nova.jogos ? nova.jogos.length : 0})`);
      if (!nova || !nova.jogos) { await ctx.close(); break mot1; }
      L.ok(store.gen === 43, `geração avançou 42 → ${store.gen}`);
      const fx = JSON.parse(await L.ls(page, 'fixas')), bl = JSON.parse(await L.ls(page, 'bloqueadas'));
      const errosJogos = [];
      nova.jogos.forEach((j, i) => { const e = validarJogo(j, fx, bl); if (e.length) errosJogos.push(`jogo${i + 1}: ${e.join('; ')}`); });
      L.ok(errosJogos.length === 0, 'todos os jogos válidos (15 dezenas, fixas presentes, bloqueadas ausentes)' + (errosJogos.length ? ' → ' + errosJogos.slice(0, 2).join(' / ') : ''));
      L.ok(new Set(nova.jogos.map(j => j.join(','))).size === nova.jogos.length, 'nenhum jogo duplicado dentro da geração');
      L.ok(nova.score > 0, `score real calculado (R$ ${nova.score.toFixed(2)})`);
      L.ok(store.top >= nova.score && (!melhor || Math.abs(store.top - melhor.score) < 0.01), `top score = melhor matriz (R$ ${store.top.toFixed(2)} vs gerada R$ ${nova.score.toFixed(2)})`);
      L.ok((await page.textContent('#genVal')).trim() === '43', 'KPI geração atual atualizado na tela');
      const maxTxt = (await page.textContent('#statMax')).trim().replace(/\./g, '').replace(',', '.');
      L.ok(Math.abs(parseFloat(maxTxt) - store.top) < 0.01, `KPI MÁXIMO sincronizado com o top score (${await page.textContent('#statMax')} vs R$ ${store.top.toFixed(2)})`);
      L.ok(errors.length === 0, 'sem erros de JS durante a geração: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Motor: 3 gerações seguidas (regressão) + ranking ordenado por score', 'MOT');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      await L.clickSel(page, '#segJogos .seg-btn[data-v="10"]', { wait: 150 });
      const gens = [];
      for (let i = 0; i < 3; i++) {
        await L.clickSel(page, '#btnMotor', { wait: 1500 });
        gens.push(parseInt(await L.ls(page, 'geracaoAtual')));
      }
      L.ok(gens.join(',') === '43,44,45', `gerações incrementais: ${gens.join(' → ')}`);
      const rank = await page.evaluate(() => JSON.parse(localStorage.getItem('rankingMatrizes')));
      L.ok(rank.length === 11, `ranking com 11 matrizes (8 iniciais + 3 novas) → ${rank.length}`);
      const ordenado = rank.every((m, i) => i === 0 || rank[i - 1].score >= m.score);
      L.ok(ordenado, 'ranking ordenado por score decrescente');
      const cards = await page.evaluate(() => [...document.querySelectorAll('#rankingList .rank-card')].length);
      L.ok(cards === rank.length, `cards renderizados = ${cards}`);
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Motor: modo Aleatório 33 jogos após Premium (sem paywall)', 'MOT');
    mot4: {
      const { page, errors, ctx } = await bootDashboard(browser, { storage: { isPremium: 'true' } });
      await goto(page, 'gerador');
      await L.clickSel(page, '#modoAleatorio', { wait: 300 });
      L.ok(!(await L.visible(page, '.premium-lock')), 'sem cadeado para usuário Premium');
      L.ok(await page.evaluate(() => document.querySelector('.modo-card.active')?.id) === 'modoAleatorio', 'card Aleatório fica ativo');
      L.ok(await L.ls(page, 'modoGeracao') === 'aleatorio', 'modo aleatório persistido');
      L.ok(/Aleat[óo]rio/.test(await page.textContent('#modoDesc')), 'descrição muda para modo aleatório');
      const livre = await page.evaluate(() => [...document.querySelectorAll('.modo-card')].some(c => /PREMIUM/i.test(c.textContent) && c.id === 'modoAleatorio'));
      L.ok(livre, 'selo Premium continua visível no card');
      await L.clickSel(page, '#segJogos .seg-btn[data-v="33"]', { wait: 250 });
      L.ok(await L.activeScreen(page) === 'screen-gerador', 'Premium pode escolher 33 jogos sem paywall');
      await L.clickSel(page, '#btnMotor', { wait: 2000 });
      const nova = await L.matrizNova(page);
      L.ok(!!nova && nova.jogos.length === 33, `33 jogos gerados no modo aleatório (${nova ? nova.jogos.length : 0})`);
      if (!nova) { await ctx.close(); break mot4; }
      L.ok(nova.modo === 'aleatorio', `matriz marcada com modo ${nova.modo}`);
      const erros = nova.jogos.flatMap(j => validarJogo(j, [], []));
      L.ok(erros.length === 0, 'todos os 33 jogos válidos' + (erros.length ? ' → ' + erros.slice(0, 2).join(' / ') : ''));
      L.ok(new Set(nova.jogos.map(j => j.join(','))).size === 33, 'sem jogos repetidos nos 33');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Motor: configuração restritiva (6 filtros + 6 fixas + 5 bloqueadas) não trava', 'MOT');
    {
      const storage = {
        fixas: JSON.stringify([1, 2, 3, 4, 5, 6]),
        bloqueadas: JSON.stringify([21, 22, 23, 24, 25]),
        filtrosAtivos: JSON.stringify(['impares', 'moldura', 'primos', 'foco14', 'soma', 'fibonacci']),
        qtdJogos: '10'
      };
      const { page, errors, ctx } = await bootDashboard(browser, { storage });
      await goto(page, 'gerador');
      L.ok((await page.textContent('#filtrosAtivosBadge')).trim() === '6 ativos', 'todos os 6 filtros ativos');
      await L.clickSel(page, '#btnMotor', { wait: 2500 });
      const btn = await page.evaluate(() => ({ dis: document.getElementById('btnMotor').disabled }));
      L.ok(!btn.dis, 'botão liberado (motor não fica travado em GERANDO)');
      const nova = await L.matrizNova(page);
      const aviso = (await L.toastText(page)).text + ' ' + (await page.evaluate(() => [...document.querySelectorAll('#logArea .log-line')].slice(-6).map(l => l.textContent).join(' ')));
      const gerou = nova && nova.jogos && nova.jogos.length > 0;
      L.ok(gerou, `gerou jogos mesmo com configuração restritiva (${nova ? nova.jogos.length : 0} jogos)`);
      if (gerou) {
        const erros = nova.jogos.flatMap(j => validarJogo(j, [1, 2, 3, 4, 5, 6], [21, 22, 23, 24, 25]));
        L.ok(erros.length === 0, 'fixas/bloqueadas respeitadas na config restritiva' + (erros.length ? ' → ' + erros[0] : ''));
        const somaOk = nova.jogos.every(j => { const s = j.reduce((a, b) => a + b, 0); return s >= 180 && s <= 200; });
        L.ok(somaOk || /relax|imposs|ajust|aviso|conflit/i.test(aviso), `filtro de SOMA respeitado ou usuário avisado quando impossível (soma ok=${somaOk})`);
      }
      const toast = await L.toastText(page);
      L.ok(toast.shown && !/^$/.test(toast.text), `usuário recebe feedback: "${toast.text}"`);
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  // ============================================================ INTELIGÊNCIA ARTIFICIAL
  if (run('IA')) {
    T('IA: 5 modelos (Atrasômetro/Markov/Ensemble/Apriori/Auto-Piloto) com Top5 real', 'IA');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'inteligencia');
      const modelos = [['atrasometro', 'ATRASÔMETRO'], ['markov', 'MARKOV'], ['ensemble', 'ENSEMBLE'], ['apriori', 'APRIORI'], ['autopiloto', 'AUTO-PILOTO']];
      const norm = t => String(t).replace(/[\u0300-\u036f]/g, '').toUpperCase();
      const detalhes = [];
      for (const [tipo, label] of modelos) {
        await page.evaluate(t => window.rodarIA(t), tipo);
        await page.waitForTimeout(220);
        const lbl = (await page.textContent('#iaModeLabel')).trim();
        L.ok(norm(lbl) === norm(label), `aba ${tipo} → label "${lbl}"`);
        const rows = await page.evaluate(() => [...document.querySelectorAll('#top5IAList .top5-row')].map(r => r.textContent.replace(/\s+/g, ' ').trim()));
        L.ok(rows.length === 5, `Top5 com 5 linhas (${rows.length})`);
        L.ok(rows.every(r => /^\d+º\d{2}/.test(r)), `linhas com posição + dezena 2 dígitos: ex "${rows[0]}"`);
        const det = (await page.textContent('#iaDetalhes')).trim();
        detalhes.push(det);
        L.ok(det.length > 40, `detalhes reais do modelo ${tipo} (${det.length} chars)`);
        const tabActive = await page.evaluate(t => {
          const map = { atrasometro: 0, markov: 1, ensemble: 2, apriori: 3, autopiloto: 4 };
          const tabs = document.querySelectorAll('#screen-inteligencia .bottom-tabs .tab');
          return tabs[map[t]]?.classList.contains('active');
        }, tipo);
        L.ok(tabActive, `aba correspondente marcada como ativa em ${tipo}`);
      }
      L.ok(new Set(detalhes).size >= 4, `textos de detalhes diferentes por modelo (${new Set(detalhes).size} distintos)`);
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('IA: heatmap da tela de IA + estrela fixa dezena + anomalias', 'IA');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'inteligencia');
      const heat = await page.evaluate(() => document.querySelectorAll('#heatmapIntel .cell').length);
      L.ok(heat === 25, `grid de calor da IA com 25 células (${heat})`);
      await page.evaluate(() => rodarIA('atrasometro'));
      await page.waitForTimeout(200);
      const anom = await page.evaluate(() => document.querySelectorAll('#anomaliasList .anom-row').length);
      L.ok(anom >= 1, `anomalias renderizadas na tela de IA (${anom})`);
      const antes = JSON.parse((await L.ls(page, 'fixas')) || '[]');
      await page.evaluate(() => document.querySelector('#top5IAList .top5-row .star').click());
      await page.waitForTimeout(250);
      const depois = JSON.parse((await L.ls(page, 'fixas')) || '[]');
      L.ok(JSON.stringify(antes) !== JSON.stringify(depois), `estrela ★ fixa a dezena sugerida [${antes.join(',')}] → [${depois.join(',')}]`);
      L.ok((await L.toastText(page)).shown, 'toast de confirmação ao fixar');
      await ctx.close();
    }
  }

  // ============================================================ RANKING
  if (run('RANK')) {
    T('Ranking: 8 matrizes iniciais com posições, medalhas, score, modo e base 20', 'RANK');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'ranking');
      const cards = await page.evaluate(() => [...document.querySelectorAll('#rankingList .rank-card')].map(c => ({
        pos: c.querySelector('.rank-pos')?.textContent.replace(/\s/g, ''),
        cls: c.querySelector('.rank-pos')?.className,
        score: c.querySelector('.score')?.textContent.trim(),
        g: c.querySelector('.g')?.textContent.trim(),
        modo: c.querySelector('.rank-info div div:nth-child(3)')?.textContent.trim(),
        base: c.querySelector('.base')?.textContent.trim(),
        chips: [...c.querySelectorAll('.rank-chip')].map(x => x.textContent.trim())
      })));
      L.ok(cards.length === 8, `8 cards iniciais (${cards.length})`);
      L.ok(/gold/.test(cards[0].cls) && /silver/.test(cards[1].cls) && /bronze/.test(cards[2].cls), 'pódio com gold/silver/bronze');
      L.ok(cards.slice(0, 3).every(c => /👑/.test(c.pos)), 'coroa 👑 nas 3 primeiras posições');
      L.ok(cards.every(c => /^R\$ [\d.]+,\d{2}$/.test(c.score)), `scores em R$: ex "${cards[0].score}"`);
      L.ok(cards.every(c => /^G\d+$/.test(c.g)), `badge de geração: ex "${cards[0].g}"`);
      L.ok(cards.every(c => /ANTIGOS|ALEATÓRIO/.test(c.modo)), `badge de modo: ex "${cards[0].modo}"`);
      L.ok(cards.every(c => /Base: \d/.test(c.base)), `base 20 exibida: ex "${cards[0].base.slice(0, 40)}"`);
      L.ok(cards[0].chips.join(',') === '11,12,13,14,15', 'chips de acertos 11/12/13/14/15');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Ranking: abrir detalhes, favoritar, tabs Top50/Top3/Favoritos e atualizar', 'RANK');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'ranking');
      const navPrem = await page.evaluate(() => document.getElementById('bottomNav').className);
      L.ok(/tab-premium/.test(navPrem), `barra inferior do ranking com estilo premium ("${navPrem}")`);
      // favoritar primeiro card
      await L.clickSel(page, '#rankingList .rank-card:first-child .rank-star', { wait: 300 });
      L.ok((await L.toastText(page)).shown, 'favoritar dá feedback (toast)');
      L.ok(await L.ls(page, 'favoritos') !== null, 'favoritos gravados no localStorage');
      // tabs
      for (const [tb, esperado] of [['top3', 3], ['top50', null], ['fav', null]]) {
        await page.evaluate(t => window.setRankingTab(t), tb);
        await page.waitForTimeout(250);
        const info = await page.evaluate(() => ({
          n: document.querySelectorAll('#rankingList .rank-card').length,
          ativo: [...document.querySelectorAll('#screen-ranking .bottom-tabs .tab')].findIndex(t => t.classList.contains('active'))
        }));
        L.ok(info.ativo >= 0, `tab ${tb} fica marcada como ativa (índice ${info.ativo})`);
        if (esperado != null) L.ok(info.n === esperado, `tab Top3 mostra ${info.n} cards (esperado ${esperado})`);
        else L.ok(info.n > 0, `tab ${tb} mostra ${info.n} cards`);
      }
      await page.evaluate(() => window.setRankingTab('top50'));
      await page.waitForTimeout(200);
      L.ok(await page.evaluate(() => document.querySelectorAll('#rankingList .rank-card').length) === 8, 'tab Top50 volta a mostrar todos');
      await L.clickSel(page, '#rankingList .rank-card:first-child', { wait: 400 });
      L.ok(await L.activeScreen(page) === 'screen-detalhes', 'clique no card abre Detalhes');
      L.ok(await L.navDisplay(page) === 'none', 'barra inferior escondida nos Detalhes');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Ranking: botão atualizar re-renderiza', 'RANK');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'ranking');
      const n0 = await page.evaluate(() => document.querySelectorAll('#rankingList .rank-card').length);
      await page.evaluate(() => { document.getElementById('rankingList').innerHTML = ''; });
      await L.clickSel(page, '#screen-ranking .icon-btn, #screen-ranking [onclick="atualizarRanking()"]', { wait: 350 });
      const n1 = await page.evaluate(() => document.querySelectorAll('#rankingList .rank-card').length);
      L.ok(n1 === n0 && n1 > 0, `atualizar re-renderiza os ${n1} cards`);
      L.ok((await L.toastText(page)).shown, 'toast "Ranking atualizado"');
      await ctx.close();
    }
  }

  // ============================================================ DETALHES
  if (run('DET')) {
    T('Detalhes: posição, score, ID, data, 20 dezenas de ouro e apostas reais', 'DET');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'ranking');
      await page.evaluate(() => document.querySelector('#rankingList .rank-card').click());
      await page.waitForTimeout(400);
      const d = await page.evaluate(() => ({
        pos: document.getElementById('detPos').textContent.trim(),
        score: document.getElementById('detScore').textContent.trim(),
        id: document.getElementById('detId').textContent.trim(),
        data: document.getElementById('detData').textContent.trim(),
        pontos: document.getElementById('detPontos').textContent.trim(),
        apostas: document.getElementById('detApostas').textContent.trim(),
        count: document.getElementById('detApostasCount').textContent.trim(),
        rank: document.getElementById('detRank').textContent.trim(),
        acertos: document.getElementById('detAcertos').textContent.trim(),
        dezenas: [...document.querySelectorAll('#dezenasOuro .dez-ouro')].map(x => x.textContent.trim()),
        apostasRows: [...document.querySelectorAll('#apostasList .aposta-row')].map(r => r.textContent.replace(/\s+/g, ' ').trim())
      }));
      L.ok(/^1/.test(d.pos), `badge de posição = "${d.pos.replace(/\s/g, '')}"`);
      L.ok(/^R\$ [\d.]+,?\d*/.test(d.score), `score em R$: "${d.score}"`);
      L.ok(/^#\d+/.test(d.id), `ID com timestamp: ${d.id}`);
      L.ok(/\d{2}\/\d{2}\/\d{4}/.test(d.data), `data em pt-BR: ${d.data}`);
      L.ok(d.dezenas.length === 20, `20 dezenas de ouro (${d.dezenas.length})`);
      L.ok(new Set(d.dezenas).size === 20, 'dezenas de ouro sem repetição');
      L.ok(d.dezenas.every(x => /^\d{2}$/.test(x)), 'dezenas com 2 dígitos (01..25)');
      L.ok(d.apostasRows.length === 5, `5 primeiras apostas listadas (${d.apostasRows.length})`);
      L.ok(d.apostasRows.every(r => (r.match(/\d{2}/g) || []).length >= 15), 'cada aposta com 15 dezenas');
      L.ok(/apostas/.test(d.count), `contador de apostas: ${d.count}`);
      L.ok(d.rank !== '', `rank exibido: ${d.rank}`);
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Detalhes: copiar, stress test, histórico, caos, WhatsApp e voltar', 'DET');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await page.evaluate(() => { window.__opens = []; window.open = (u) => { window.__opens.push(u); return null; }; });
      await goto(page, 'ranking');
      await page.evaluate(() => document.querySelector('#rankingList .rank-card').click());
      await page.waitForTimeout(350);
      await page.evaluate(() => document.querySelector('#apostasList .aposta-row div[onclick^="copiarAposta"]').click());
      await page.waitForTimeout(400);
      const tCop = await L.toastText(page);
      L.ok(tCop.shown && /Copiado/i.test(tCop.text), `copiar aposta dá feedback: "${tCop.text}"`);
      await L.clickText(page, '.btns-row .btn-outline', 'Stress Test', { wait: 300 });
      L.ok(/Stress/i.test((await L.toastText(page)).text), 'Stress Test responde: ' + (await L.toastText(page)).text.slice(0, 60));
      await L.clickText(page, '.btns-row .btn-outline', 'Histórico', { wait: 300 });
      L.ok(/3675/.test((await L.toastText(page)).text), 'Histórico informa 3675 sorteios');
      await L.clickText(page, '.btns-row .btn-outline', 'Caos', { wait: 300 });
      L.ok(/Caos/i.test((await L.toastText(page)).text), 'Teste de Caos responde');
      await L.clickText(page, '.btn-whats', 'WhatsApp', { wait: 400 });
      const opens = await page.evaluate(() => window.__opens || []);
      if (!opens.length) {
        // o app pode não ter conseguido abrir popup: checa o toast de feedback
        const t = await L.toastText(page);
        L.note('toast após compartilhar: ' + t.text);
      }
      L.ok(opens.some(u => /wa\.me/.test(u)), `compartilhamento abre wa.me (${opens.length} tentativa(s))`);
      L.ok(await L.visible(page, '.privacy'), 'aviso de privacidade presente');
      await L.clickSel(page, '#screen-detalhes .menu', { wait: 300 });
      L.ok(await L.activeScreen(page) === 'screen-ranking', 'botão ← volta para o Ranking');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  // ============================================================ PREMIUM
  if (run('PREM')) {
    T('Premium: comparação, 3 planos, trial, restaurar e desbloqueio efetivo', 'PREM');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'premium');
      const linhas = await page.evaluate(() => document.querySelectorAll('.compare-row').length);
      L.ok(linhas === 7, `tabela comparativa com 7 linhas (${linhas})`);
      const planos = await page.evaluate(() => [...document.querySelectorAll('.price-card')].map(c => c.textContent.replace(/\s+/g, ' ').trim().slice(0, 40)));
      L.ok(planos.length === 3, `3 planos exibidos: ${planos.map(p => p.split(' ')[0]).join(' / ')}`);
      L.ok(planos.some(p => /58% OFF/.test(p)), 'desconto anual 58% OFF');
      L.ok(await L.visible(page, '.btn-premium-cta'), 'CTA de 3 dias grátis presente');
      L.ok(await L.visible(page, '.secure-row'), 'selos de segurança presentes');
      L.ok(await page.evaluate(() => [...document.querySelectorAll('button')].some(b => /Restaurar compras/.test(b.textContent))), 'botão Restaurar compras presente');
      // compra do plano anual
      await L.clickText(page, '.price-card', 'Anual', { wait: 500 });
      L.ok(await L.ls(page, 'isPremium') === 'true', 'compra ativa isPremium no localStorage');
      const t = await L.toastText(page);
      L.ok(t.shown && /Premium/i.test(t.text), `toast de ativação: "${t.text}"`);
      await page.waitForTimeout(1100);
      L.ok(await L.activeScreen(page) === 'screen-gerador', 'após comprar, volta automaticamente ao Gerador');
      await L.clickSel(page, '#modoAleatorio', { wait: 300 });
      L.ok(!(await L.visible(page, '.premium-lock')), 'Aleatório desbloqueado (sem cadeado)');
      L.ok(await L.ls(page, 'modoGeracao') === 'aleatorio', 'modo Aleatório selecionável após compra');
      // 33 jogos liberados
      await page.evaluate(() => window.showScreen('gerador'));
      await L.clickSel(page, '#segJogos .seg-btn[data-v="33"]', { wait: 250 });
      L.ok(await L.activeScreen(page) === 'screen-gerador', '33 jogos liberados para Premium');
      L.ok(await page.evaluate(() => document.querySelector('#segJogos .seg-btn.active')?.dataset.v) === '33', 'opção 33 jogos selecionada');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Premium: trial de 3 dias e restaurar compras também desbloqueiam', 'PREM');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'premium');
      await L.clickSel(page, '.btn-premium-cta', { wait: 900 });
      L.ok(await L.ls(page, 'isPremium') === 'true', 'CTA "3 dias grátis" ativa Premium');
      await ctx.close();
      const app2 = await bootDashboard(browser);
      await goto(app2.page, 'premium');
      await L.clickText(app2.page, 'button', 'Restaurar compras', { wait: 400 });
      const t2 = await L.toastText(app2.page);
      L.ok(t2.shown, `Restaurar compras responde: "${t2.text}"`);
      await app2.ctx.close();
    }

    T('Premium: cadeado do modo Aleatório persiste após recarregar (Free)', 'PREM');
    {
      const { page, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      await L.clickSel(page, '#modoAleatorio', { wait: 300 });
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(600);
      await goto(page, 'gerador');
      L.ok(await page.evaluate(() => document.querySelector('.modo-card.active')?.id) === 'modoAntigos', 'após reload segue no modo grátis');
      await L.clickSel(page, '#modoAleatorio', { wait: 300 });
      L.ok(await L.visible(page, '.premium-lock'), 'cadeado continua bloqueando o Aleatório para usuário Free');
      await ctx.close();
    }
  }

  // ============================================================ HEATMAP SENSORIAL
  if (run('HM')) {
    T('Heatmap Sensorial: grid 5x5 colorido, legenda, Top5 real e fixar', 'HM');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'heatmap');
      const g = await page.evaluate(() => {
        const cells = [...document.querySelectorAll('#gridSensor .cell-sensor')];
        return { n: cells.length, classes: [...new Set(cells.map(c => c.className))], nums: cells.slice(0, 3).map(c => c.textContent) };
      });
      L.ok(g.n === 25, `grid sensorial 25 células (${g.n})`);
      L.ok(g.classes.length >= 3, `gradiente de cores aplicado (${g.classes.length} faixas: ${g.classes.join(' / ').slice(0, 80)})`);
      L.ok(g.nums.join(',') === '01,02,03', 'numeração das dezenas correta');
      const leg = await page.evaluate(() => [...document.querySelectorAll('.legend-sensor .item')].map(i => i.textContent.trim()));
      L.ok(leg.length === 4, `legenda com 4 faixas: ${leg.join(' / ')}`);
      const top5 = await page.evaluate(() => [...document.querySelectorAll('#top5SensorList .top5-sensor-row')].map(r => r.textContent.replace(/\s+/g, ' ').trim()));
      L.ok(top5.length === 5, `Top5 real listado (${top5.length})`);
      L.ok(top5.every(t => /Freq: \d+/.test(t)), `cada linha com frequência real: ex "${top5[0]}"`);
      L.ok(await page.evaluate(() => !!document.querySelector('#top5SensorList .pin')), 'pino 📌 em cada dezena do Top5');
      await page.evaluate(() => { localStorage.setItem('fixas', '[]'); window.fixas = []; window.renderFixasBloqueadas(); });
      await L.clickText(page, '.btn-fixar', 'Fixar todas', { wait: 400 });
      const fx = JSON.parse(await L.ls(page, 'fixas'));
      L.ok(fx.length > 0 && fx.length <= 6, `"Fixar todas no volante" atualiza fixas → [${fx.join(', ')}]`);
      const iaTxt = await page.textContent('.ia-card .desc');
      L.ok(/Markov|atras[oô]metro|frequ[êe]ncia/i.test(iaTxt), 'card de IA descreve a análise real');
      await page.evaluate(() => document.querySelector('#gridSensor .cell-sensor:nth-child(2)').click());
      await page.waitForTimeout(250);
      L.ok((await L.toastText(page)).shown, 'clique no grid sensorial fixa dezena com feedback');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  // ============================================================ CONFIGURAÇÕES
  if (run('CFG')) {
    T('Configurações: 11 itens, feedback de todos os clicáveis e banca editável', 'CFG');
    {
      const { page, errors, ctx, dialogsCfg } = await bootDashboard(browser);
      await goto(page, 'config');
      const itens = await page.evaluate(() => [...document.querySelectorAll('#screen-config .config-item')].map(i => i.querySelector('.t')?.textContent.trim()));
      L.ok(itens.length === 11, `11 itens de configuração (${itens.length}): ${itens.join(' / ')}`);
      L.ok(itens.includes('Tema Escuro') && itens.includes('Deletar Dados') && itens.includes('Premium'), 'itens essenciais presentes');
      L.ok(await page.evaluate(() => !!document.querySelector('#screen-config .footer-legal')), 'rodapé legal (+18 / educacional / dual modo) presente');
      L.ok(/1\.0\.0/.test(await page.textContent('#screen-config')), 'versão 1.0.0 exibida');
      // banca
      dialogsCfg.promptValue = '2500';
      await L.clickText(page, '#screen-config .config-item', 'Gestão de Banca', { wait: 400 });
      L.ok(await L.ls(page, 'banca') === '2500', 'banca editada e salva (R$ 2500)');
      L.ok(/2\.500,00/.test(await page.textContent('#bancaVal')), 'valor exibido na tela: ' + (await page.textContent('#bancaVal')).trim());
      // notificações
      const on0 = await page.evaluate(() => document.querySelector('#screen-config .toggle').classList.contains('on'));
      await page.click('#screen-config .toggle');
      await page.waitForTimeout(200);
      const on1 = await page.evaluate(() => document.querySelector('#screen-config .toggle').classList.contains('on'));
      L.ok(on0 !== on1, `toggle de notificações alterna (${on0} → ${on1})`);
      // feedback dos itens com toast
      for (const label of ['Tema Escuro', 'Privacidade', 'Termos', 'Avaliar App', 'Contato']) {
        await L.clickText(page, '#screen-config .config-item', label, { wait: 250 });
        const t = await L.toastText(page);
        L.ok(t.shown && t.text.length > 3, `item "${label}" responde: "${t.text.slice(0, 45)}..."`);
      }
      // premium
      await L.clickText(page, '#screen-config .config-item', 'Premium', { wait: 350 });
      L.ok(await L.activeScreen(page) === 'screen-premium', 'item Premium abre a tela Premium');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Configurações: deletar dados limpa tudo e reinicia o app', 'CFG');
    {
      const { page, ctx } = await bootDashboard(browser);
      await page.evaluate(() => { localStorage.setItem('banca', '999'); localStorage.setItem('fixas', '[2,4]'); });
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(600);
      await L.clickSel(page, '#bottomNav .tab[data-screen="config"]', { wait: 250 });
      await page.evaluate(() => window.deletarDados());
      await page.waitForTimeout(900);
      const depois = await L.lsAll(page);
      // dados do usuário devem sumir; o app recria apenas o seed de demonstração (8 matrizes) e o modo padrão
      const restos = ['banca', 'fixas', 'bloqueadas', 'favoritos', 'qtdJogos', 'onboardDone', 'isPremium'].filter(k => depois[k] !== undefined);
      L.ok(restos.length === 0, `dados do usuário apagados (mantidos: ${restos.join(', ') || 'nenhum'})`);
      L.ok(depois.modoGeracao === 'antigos', `modo volta ao padrão grátis (${depois.modoGeracao})`);
      L.ok(!depois.onboardDone, 'onboarding volta a aparecer para o usuário (dados zerados)');
      L.ok(await L.activeScreen(page) === 'screen-onboarding', 'app reinicia no onboarding após apagar dados');
      await ctx.close();
    }
  }

  // ============================================================ UX / COMPONENTES
  if (run('UX')) {
    T('UX: toast aparece, texto correto e desaparece sozinho (~3s)', 'UX');
    {
      const { page, ctx } = await bootDashboard(browser);
      await page.evaluate(() => showToast('🧪 Teste de toast'));
      await page.waitForTimeout(150);
      const t0 = await L.toastText(page);
      L.ok(t0.shown && t0.text === '🧪 Teste de toast', 'toast visível com a mensagem');
      const pos = await page.evaluate(() => { const r = document.getElementById('toast').getBoundingClientRect(); const p = document.querySelector('.phone').getBoundingClientRect(); return { baixo: Math.round(p.bottom - r.bottom), centro: Math.abs((r.left + r.right) / 2 - (p.left + p.right) / 2) }; });
      L.ok(pos.baixo > 60 && pos.baixo < 160, `toast posicionado acima da barra de navegação (${pos.baixo}px do fundo)`);
      await page.waitForTimeout(3300);
      const t1 = await L.toastText(page);
      L.ok(!t1.shown, 'toast desaparece sozinho após ~3s');
      await ctx.close();
    }

    T('UX: log com timestamp, cores por tipo e auto-scroll', 'UX');
    {
      const { page, errors, ctx } = await bootDashboard(browser);
      await goto(page, 'gerador');
      await page.evaluate(() => { window.log('teste info', 'info'); window.log('teste warn', 'warn'); window.log('teste error', 'error'); });
      await page.waitForTimeout(250);
      const l = await page.evaluate(() => {
        const lines = [...document.querySelectorAll('#logArea .log-line')];
        const area = document.getElementById('logArea');
        return {
          n: lines.length,
          ultima: lines[lines.length - 1].textContent,
          classes: lines.slice(-3).map(x => x.className),
          cores: lines.slice(-3).map(x => getComputedStyle(x).color),
          scrollado: Math.abs(area.scrollHeight - area.clientHeight - area.scrollTop) < 6,
          altura: area.clientHeight
        };
      });
      L.ok(/^\[\d{2}:\d{2}:\d{2}\]/.test(l.ultima), `linha com timestamp: "${l.ultima}"`);
      L.ok(l.classes.some(c => /log-warn/.test(c)) && l.classes.some(c => /log-error/.test(c)), 'tipos warn/error com classes próprias');
      L.ok(new Set(l.cores).size === 3, `3 cores distintas (verde/amarelo/vermelho): ${l.cores.join(' ')}`);
      L.ok(l.scrollado, 'área de log com auto-scroll para o fim');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('UX: persistência completa após recarregar o app', 'UX');
    {
      const storage = {
        isPremium: 'true', modoGeracao: 'aleatorio', fixas: '[3,7]', bloqueadas: '[25]',
        filtrosAtivos: '["impares","soma"]', qtdJogos: '15', mutacao: '12', severidade: '65',
        estrategia: 'agressivo', topScore: '4321.98', geracaoAtual: '77', banca: '1500', onboardDone: '1'
      };
      const { page, errors, ctx } = await bootDashboard(browser, { storage });
      await goto(page, 'gerador');
      const g = await page.evaluate(() => ({
        modo: document.querySelector('.modo-card.active')?.id,
        qtd: document.querySelector('#segJogos .seg-btn.active')?.dataset.v,
        chips: [...document.querySelectorAll('.filtro-chip:not(.inactive)')].map(c => c.dataset.f).sort(),
        badge: document.getElementById('filtrosAtivosBadge').textContent.trim(),
        mut: document.getElementById('mutacaoVal').textContent.trim(),
        sev: document.getElementById('severidadeVal').textContent.trim(),
        est: document.getElementById('estAgr').textContent.trim(),
        fixas: document.getElementById('fixasChips').textContent.replace(/\s+/g, ' ').trim(),
        bloq: document.getElementById('bloqChips').textContent.replace(/\s+/g, ' ').trim()
      }));
      L.ok(g.modo === 'modoAleatorio', 'modo Aleatório restaurado (Premium)');
      L.ok(g.qtd === '15', `quantidade 15 restaurada (${g.qtd})`);
      L.ok(g.chips.join(',') === 'impares,soma' && g.badge === '2 ativos', `filtros restaurados: [${g.chips.join(', ')}] / ${g.badge}`);
      L.ok(g.mut === '12%' && g.sev === '65%', `sliders restaurados: mutação ${g.mut}, severidade ${g.sev}`);
      L.ok(g.est === '✓', 'estratégia Agressivo marcada com ✓');
      L.ok(/03|07/.test(g.fixas) && /25/.test(g.bloq), `fixas/bloqueadas restauradas: fixas="${g.fixas}" bloqueadas="${g.bloq}"`);
      await goto(page, 'dashboard');
      L.ok((await page.textContent('#topScoreVal')).trim() === 'R$ 4.321,98', 'top score restaurado: ' + (await page.textContent('#topScoreVal')).trim());
      L.ok((await page.textContent('#genVal')).trim() === '77', 'geração atual restaurada: 77');
      await goto(page, 'config');
      L.ok(/1\.500,00/.test(await page.textContent('#bancaVal')), 'banca restaurada: ' + (await page.textContent('#bancaVal')).trim());
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  // ============================================================ MOBILE
  if (run('MOB')) {
    T('Mobile: layout sem estouro horizontal e navegação funcional em 390x844', 'MOB');
    {
      const { page, errors, ctx } = await bootDashboard(browser, { viewport: { width: 390, height: 844 } });
      const ov = await page.evaluate(() => ({
        docW: document.documentElement.scrollWidth, winW: window.innerWidth,
        phoneW: document.querySelector('.phone').getBoundingClientRect().width,
        overflow: [...document.querySelectorAll('.screen')].filter(s => s.scrollWidth > s.clientWidth + 2).map(s => s.id)
      }));
      L.ok(ov.docW <= ov.winW + 1, `sem rolagem horizontal (doc ${ov.docW} / janela ${ov.winW})`);
      L.ok(ov.phoneW <= 392, `moldura do app ocupa a largura da tela (${Math.round(ov.phoneW)}px)`);
      L.ok(ov.overflow.length === 0, `nenhuma tela com estouro horizontal (${ov.overflow.join(', ') || 'ok'})`);
      for (const s of ['dashboard', 'heatmap', 'gerador', 'ranking', 'config']) {
        await L.clickSel(page, `#bottomNav .tab[data-screen="${s}"]`, { wait: 200 });
        L.ok(await L.activeScreen(page) === 'screen-' + s, `navegação mobile funciona em ${s}`);
      }
      await goto(page, 'gerador');
      await L.clickSel(page, '#segJogos .seg-btn[data-v="10"]', { wait: 150 });
      await L.clickSel(page, '#btnMotor', { wait: 1800 });
      const nova = await L.matrizNova(page);
      L.ok(nova && nova.jogos.length === 10, `geração funciona no mobile (${nova ? nova.jogos.length : 0} jogos)`);
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }

    T('Mobile: tela pequena 360x640 mantém telas utilizáveis', 'MOB');
    {
      const { page, errors, ctx } = await bootDashboard(browser, { viewport: { width: 360, height: 640 } });
      const ov = await page.evaluate(() => ({ docW: document.documentElement.scrollWidth, winW: window.innerWidth }));
      L.ok(ov.docW <= ov.winW + 1, `sem estouro horizontal em 360px (${ov.docW}/${ov.winW})`);
      await L.clickSel(page, '#bottomNav .tab[data-screen="gerador"]', { wait: 250 });
      L.ok(await L.activeScreen(page) === 'screen-gerador', 'navegação OK em tela pequena');
      L.ok(await L.visible(page, '#btnMotor'), 'botão do motor visível e clicável');
      L.ok(errors.length === 0, 'sem erros de JS: ' + (errors.slice(0, 2).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  // ============================================================ FUZZ (varredura de todos os botões)
  if (run('FUZZ')) {
    T('Varredura: clique em TODOS os botões de TODAS as telas sem erro e com reação', 'FUZZ');
    {
      const { page, errors, ctx, dialogsCfg } = await bootDashboard(browser, { storage: { isPremium: 'true' } });
      dialogsCfg.promptValue = '1,5,10';
      const telas = ['dashboard', 'gerador', 'inteligencia', 'ranking', 'heatmap', 'config', 'premium', 'onboarding'];
      // gera uma matriz para existir a tela de detalhes
      await goto(page, 'gerador');
      await L.clickSel(page, '#segJogos .seg-btn[data-v="10"]', { wait: 120 });
      await L.clickSel(page, '#btnMotor', { wait: 1800 });
      let totalClicks = 0, semReacao = [], errosStr = [];
      const errsAntes = errors.length;
      for (const tela of telas) {
        await goto(page, tela);
        const n = await page.evaluate(() => document.querySelectorAll('.screen.active [onclick]').length);
        for (let i = 0; i < n; i++) {
          await goto(page, tela);
          const alvo = await page.evaluate(idx => {
            const els = [...document.querySelectorAll('.screen.active [onclick]')];
            const e = els[idx];
            if (!e) return null;
            const r = e.getBoundingClientRect();
            return { tag: e.tagName, txt: (e.textContent || '').trim().slice(0, 30), oc: e.getAttribute('onclick'), vis: r.width > 0 && r.height > 0 };
          }, i);
          if (!alvo || !alvo.vis) continue;
          const antes = await L.stateSnapshot(page);
          const err0 = errors.length;
          try {
            await page.evaluate(idx => {
              const els = [...document.querySelectorAll('.screen.active [onclick]')];
              els[idx].click();
            }, i);
          } catch (e) { errosStr.push(`${tela}#${i}: ${e.message}`); continue; }
          await page.waitForTimeout(180);
          const depois = await L.stateSnapshot(page);
          totalClicks++;
          if (antes === depois) semReacao.push(`${tela} › "${alvo.txt}" [${alvo.oc.slice(0, 45)}]`);
          if (errors.length > err0) errosStr.push(`${tela} › "${alvo.txt}": ${errors.slice(err0).join(' | ')}`);
        }
      }
      L.ok(totalClicks > 40, `botões efetivamente clicados: ${totalClicks}`);
      L.ok(semReacao.length === 0, `todo botão produziu reação visível` + (semReacao.length ? ` — SEM REAÇÃO (${semReacao.length}): ${semReacao.slice(0, 6).join(' ;; ')}` : ''));
      L.ok(errosStr.length === 0, `nenhum erro de JS disparado pelos cliques` + (errosStr.length ? ` — ${errosStr.slice(0, 4).join(' ;; ')}` : ''));
      L.ok(errors.length === errsAntes, 'nenhum erro novo no console durante a varredura');
      // detalhes também
      await goto(page, 'ranking');
      await page.evaluate(() => document.querySelector('#rankingList .rank-card').click());
      await page.waitForTimeout(400);
      const nDet = await page.evaluate(() => document.querySelectorAll('#screen-detalhes [onclick]').length);
      let okDet = 0;
      for (let i = 0; i < nDet; i++) {
        await page.evaluate(() => { const c = document.querySelector('#rankingList .rank-card'); if (typeof abrirDetalhes === 'function' && document.querySelector('#screen-detalhes').classList.contains('active') === false) c.click(); });
        await page.waitForTimeout(120);
        const r = await page.evaluate(idx => {
          const els = [...document.querySelectorAll('#screen-detalhes [onclick]')];
          const e = els[idx]; if (!e) return 'skip';
          e.click(); return 'ok';
        }, i);
        if (r === 'ok') okDet++;
        await page.waitForTimeout(150);
      }
      L.ok(okDet >= 5, `botões da tela de Detalhes clicados (${okDet}) sem quebrar`);
      L.ok(errors.length === errsAntes, 'nenhum erro novo após varrer Detalhes');
      await ctx.close();
    }
  }

  // ============================================================ JORNADA COMPLETA
  if (run('JORNADA')) {
    T('Jornada completa do usuário novo: onboarding → IA → gerar → ranking → premium', 'JORNADA');
    jor1: {
      const { page, errors, ctx } = await bootOnboard(browser);
      // onboarding
      await L.clickSel(page, '#btnOnboard', { wait: 200 });
      await L.clickSel(page, '#btnOnboard', { wait: 200 });
      await L.clickSel(page, '#btnOnboard', { wait: 400 });
      L.ok(await L.activeScreen(page) === 'screen-dashboard', '1) usuário novo entra no Dashboard');
      // dashboard
      L.ok((await page.textContent('#totalSorteios')).trim() === '3675', '2) vê 3675 concursos reais e o último concurso');
      // IA
      await page.waitForFunction(() => typeof window.rodarIA === 'function', null, { timeout: 15000 });
      await page.evaluate(() => window.showScreen('inteligencia'));
      await page.waitForTimeout(250);
      await page.evaluate(() => window.rodarIA('ensemble'));
      await page.waitForTimeout(250);
      L.ok((await page.textContent('#iaModeLabel')).trim() === 'ENSEMBLE', '3) roda análise de IA (Ensemble)');
      // gerador free
      await page.evaluate(() => window.showScreen('gerador'));
      await page.waitForTimeout(200);
      await L.clickSel(page, '#modoAleatorio', { wait: 250 });
      L.ok(await L.visible(page, '.premium-lock'), '4) descobre que Aleatório é Premium');
      await L.clickText(page, '.premium-lock .btn-unlock', 'Desbloquear', { wait: 400 });
      L.ok(await L.activeScreen(page) === 'screen-premium', '5) vai para a tela Premium');
      await L.clickSel(page, '.btn-premium-cta', { wait: 1200 });
      L.ok(await L.ls(page, 'isPremium') === 'true', '6) ativa Premium (3 dias grátis)');
      await L.clickSel(page, '#modoAleatorio', { wait: 250 });
      await L.clickSel(page, '#segJogos .seg-btn[data-v="33"]', { wait: 200 });
      await L.clickSel(page, '#btnMotor', { wait: 2200 });
      const nova = await L.matrizNova(page);
      L.ok(nova && nova.jogos.length === 33, `7) gera 33 jogos no modo aleatório (${nova ? nova.jogos.length : 0})`);
      if (!nova) { await ctx.close(); break jor1; }
      // ranking + detalhes
      await page.evaluate(() => window.showScreen('ranking'));
      await page.waitForTimeout(250);
      const card = await page.evaluate(() => document.querySelector('#rankingList .rank-card .rank-info').textContent.replace(/\s+/g, ' ').trim());
      L.ok(/ALEATÓRIO/.test(card), '8) ranking mostra a matriz nova marcada como ALEATÓRIO');
      await page.evaluate(() => document.querySelector('#rankingList .rank-card').click());
      await page.waitForTimeout(350);
      L.ok(await L.activeScreen(page) === 'screen-detalhes' && (await page.evaluate(() => document.querySelectorAll('#dezenasOuro .dez-ouro').length)) === 20, '9) detalhes do jogo com 20 dezenas de ouro');
      await page.evaluate(() => document.querySelector('#screen-detalhes .menu').click());
      await page.waitForTimeout(250);
      L.ok(await L.activeScreen(page) === 'screen-ranking', '10) volta ao ranking');
      await L.clickSel(page, '#bottomNav .tab[data-screen="dashboard"]', { wait: 300 });
      L.ok((await page.textContent('#genVal')).trim() === '43', '11) dashboard mostra a nova geração (43)');
      L.ok(errors.length === 0, '12) jornada inteira sem nenhum erro de JS: ' + (errors.slice(0, 3).join(' | ') || 'ok'));
      await ctx.close();
    }
  }

  await browser.close();
  L.report(require('path').join(__dirname, 'results.json'));
  const fails = L.results.filter(r => r.status === 'FAIL');
  process.exit(fails.length ? 1 : 0);
})();
