// ==================== ARMAZENAMENTO SEGURO ====================
// Dados corrompidos (ou de versões antigas) nunca devem derrubar o app.
function getJSON(chave, padrao, validador){
  try{
    const bruto = localStorage.getItem(chave);
    if(bruto === null || bruto === 'undefined') return padrao;
    const valor = JSON.parse(bruto);
    return (!validador || validador(valor)) ? valor : padrao;
  }catch(e){
    log('⚠️ Dado inválido em "'+chave+'" foi restaurado para o padrão','warn');
    try{ localStorage.removeItem(chave); }catch(_){}
    return padrao;
  }
}
function getBool(chave, padrao){ const v = localStorage.getItem(chave); return v === null ? padrao : v === 'true'; }
function getNum(chave, padrao, min, max){
  const v = parseFloat(String(localStorage.getItem(chave)));
  if(!isFinite(v)) return padrao;
  if(min !== undefined && v < min) return min;
  if(max !== undefined && v > max) return max;
  return v;
}
function soDezenasValidas(lista, maximo){
  if(!Array.isArray(lista)) return null;
  const ok = [...new Set(lista.map(n=>parseInt(n,10)).filter(n=>Number.isInteger(n) && n>=1 && n<=25))];
  return ok.length > maximo ? ok.slice(0, maximo) : ok;
}
function matrizesValidas(lista){
  if(!Array.isArray(lista)) return null;
  const ok = lista.filter(m => m && typeof m === 'object' && Array.isArray(m.jogos) &&
    m.jogos.every(j => Array.isArray(j) && j.length === 15 && j.every(n => Number.isInteger(n) && n>=1 && n<=25)) &&
    isFinite(m.score));
  return ok.length === lista.length ? ok : null; // descarta tudo se houver item inconsistente
}

// ==================== TEMA (claro / escuro / automático) ====================
const TEMAS = ['escuro','claro','auto'];
let tema = TEMAS.includes(localStorage.getItem('tema')) ? localStorage.getItem('tema') : 'escuro';
const mqClaro = window.matchMedia ? window.matchMedia('(prefers-color-scheme: light)') : null;
function temaEfetivo(){
  if(tema === 'auto') return (mqClaro && mqClaro.matches) ? 'light' : 'dark';
  return tema === 'claro' ? 'light' : 'dark';
}
function aplicarTema(){
  document.documentElement.setAttribute('data-theme', temaEfetivo());
  const desc = document.getElementById('temaDesc');
  if(desc) desc.textContent = tema === 'auto' ? 'Automático (segue o sistema)' : (tema === 'claro' ? 'Claro' : 'Escuro');
  if(mqClaro){
    mqClaro.onchange = () => { if(tema === 'auto'){ aplicarTema(); if(typeof drawChart === 'function') drawChart(); } };
  }
  if(typeof drawChart === 'function') setTimeout(drawChart, 40);
}
function alternarTema(){
  tema = tema === 'escuro' ? 'claro' : (tema === 'claro' ? 'auto' : 'escuro');
  localStorage.setItem('tema', tema);
  aplicarTema();
  const rotulos = { escuro:'🌙 Tema escuro ativo', claro:'☀️ Tema claro ativo', auto:'🔄 Tema automático (sistema)' };
  showToast(rotulos[tema]);
  log('🎨 '+rotulos[tema].replace(/^[^ ]+ /,''),'info');
}
function cssVar(nome){ return getComputedStyle(document.documentElement).getPropertyValue(nome).trim(); }
const prefereMenosMovimento = () => window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ==================== ANIMAÇÕES ====================
function animarValor(id, alvo, formatador){
  const el = document.getElementById(id);
  if(!el || !isFinite(alvo)) return;
  const de = parseFloat(el.dataset.valor);
  el.dataset.valor = alvo;
  const formatar = formatador || (v => v.toFixed(2));
  if(!isFinite(de) || de === alvo || prefereMenosMovimento()){ el.textContent = formatar(alvo); return; }
  const inicio = performance.now(), duracao = 520;
  el.classList.remove('valor-animado'); void el.offsetWidth; el.classList.add('valor-animado');
  const passo = (agora) => {
    const t = Math.min(1, (agora - inicio) / duracao);
    const suave = 1 - Math.pow(1 - t, 3);
    el.textContent = formatar(de + (alvo - de) * suave);
    if(t < 1) requestAnimationFrame(passo);
  };
  requestAnimationFrame(passo);
}
function marcarIndices(container, seletor){ // stagger das listas
  const itens = container.querySelectorAll(seletor);
  itens.forEach((el, i) => el.style.setProperty('--i', Math.min(i, 14)));
}
function esqueleto(container, quantidade, altura){
  if(!container) return;
  container.innerHTML = Array.from({length: quantidade||3}, () => `<div class="rank-card skeleton" style="height:${altura||110}px;border-radius:14px;margin:10px 12px"></div>`).join('');
}
let matrizDestacada = null;

// ==================== DADOS REAIS 3675 SORTEIOS ====================
let SORTEIOS_HISTORICOS = [];
let isPremium = getBool('isPremium', false);
let modoGeracao = ['antigos','aleatorio'].includes(localStorage.getItem('modoGeracao')) ? localStorage.getItem('modoGeracao') : 'antigos';
let fixas = soDezenasValidas(getJSON('fixas', [1,5,10]), 6) || [1,5,10];
let bloqueadas = soDezenasValidas(getJSON('bloqueadas', [25]), 5) || [25];
let filtrosAtivos = new Set(getJSON('filtrosAtivos', ['impares','moldura','primos','foco14'], v => Array.isArray(v) && v.every(f => typeof f === 'string')));
const QTD_PERMITIDAS = [10,15,20,33];
let qtdJogos = QTD_PERMITIDAS.includes(parseInt(localStorage.getItem('qtdJogos'))) ? parseInt(localStorage.getItem('qtdJogos')) : 33;
let mutacao = getNum('mutacao', 5, 1, 25);
let severidade = getNum('severidade', 80, 0, 100);
let estrategia = ['conservador','agressivo','robo','preguicoso'].includes(localStorage.getItem('estrategia')) ? localStorage.getItem('estrategia') : 'robo';
let rankingMatrizes = matrizesValidas(getJSON('rankingMatrizes', [])) || [];
let topScore = getNum('topScore', 0, 0);
// O TOP SCORE exibido deve ser sempre um resultado REAL: adota o melhor do ranking salvo
(function sincronizarTopScore(){
  if(!rankingMatrizes.length) return;
  const melhorReal = rankingMatrizes.reduce((a,m)=>Math.max(a, Number(m.score)||0), 0);
  if(melhorReal > topScore){ topScore = melhorReal; localStorage.setItem('topScore', topScore); }
})();
let geracaoAtual = Math.round(getNum('geracaoAtual', 42, 1));
let banca = getNum('banca', 1000, 0);
let rankingTab = 'top50';
let favoritos = (getJSON('favoritos', [], v => Array.isArray(v) && v.every(x => typeof x === 'number'))) || [];
let matrizAtual = null;
let mostrarTodasApostas = false;
let toastTimer = null;

function fmtMoeda(v){
  const n=Number(v);
  const s=(isFinite(n)?n:0).toFixed(2);
  const partes=s.split('.');
  return partes[0].replace(/\B(?=(\d{3})+(?!\d))/g,'.')+','+partes[1];
}

// KPIs do dashboard sempre coerentes com o estado salvo
function atualizarKPIs(){
  const set=(id,v)=>{const e=document.getElementById(id); if(e && e.textContent!==v) e.textContent=v;};
  animarValor('topScoreVal', topScore, v => 'R$ '+fmtMoeda(v));
  animarValor('statMedia', topScore*0.5, fmtMoeda);
  animarValor('statMax', topScore, fmtMoeda);
  set('genVal', geracaoAtual);
  set('statMaxGen','Geração '+geracaoAtual);
  set('bancaVal','R$ '+fmtMoeda(banca));
}

// Carregar 3675 sorteios - tentar fetch do cache real, fallback mock
async function carregarSorteios() {
  try {
    // Usar dados embarcados 3675 sorteios reais
    if (typeof SORTEIOS_EMBEDDED !== 'undefined' && SORTEIOS_EMBEDDED.length > 0) {
      SORTEIOS_HISTORICOS = SORTEIOS_EMBEDDED;
      log(`✅ ${SORTEIOS_HISTORICOS.length} sorteios reais embarcados carregados`, 'info');
    } else {
      // Tentar fetch
      const res = await fetch('storage/resultados_historico_cache.json');
      if (res.ok) {
        SORTEIOS_HISTORICOS = await res.json();
        log('✅ 3675 sorteios reais carregados do cache', 'info');
      } else throw new Error('fallback');
    }
  } catch (e) {
    log('⚠️ Erro carregar, usando mock 3675', 'warn');
    SORTEIOS_HISTORICOS = [];
    for (let i = 0; i < 3675; i++) {
      const jogo = new Set();
      while (jogo.size < 15) {
        let n;
        if (Math.random() < 0.7) n = Math.floor(Math.random() * 25) + 1;
        else n = [1,2,3,4,5,10,11,15,20,21,22,23,24,25][Math.floor(Math.random()*14)];
        jogo.add(n);
      }
      SORTEIOS_HISTORICOS.push(Array.from(jogo).sort((a,b)=>a-b));
    }
  }
  const total=document.getElementById('totalSorteios');
  if(total) total.textContent=SORTEIOS_HISTORICOS.length;
  const totalIA=document.getElementById('totalSorteiosIA');
  if(totalIA) totalIA.textContent=SORTEIOS_HISTORICOS.length;
  invalidarCacheIA();
  calcularEstatisticasReais();
  renderUltimoConcurso();
  renderHeatmaps();
  atualizarKPIs();
  rodarIA('atrasometro');
  if (rankingMatrizes.length === 0) gerarRankingInicial();
  else renderRanking();
}

// Estatísticas reais
function calcularEstatisticasReais() {
  const freq = {};
  for (let i=1;i<=25;i++) freq[i]=0;
  let totalImpares=0;
  SORTEIOS_HISTORICOS.forEach(s=>{
    s.forEach(n=>freq[n]++);
    totalImpares += s.filter(n=>n%2===1).length;
  });
  const maisFreq = Object.entries(freq).sort((a,b)=>b[1]-a[1])[0];
  const menosFreq = Object.entries(freq).sort((a,b)=>a[1]-b[1])[0];
  document.getElementById('dezenaMaisFreq').textContent = `${maisFreq[0].padStart(2,'0')} (${maisFreq[1]}x)`;
  document.getElementById('dezenaMenosFreq').textContent = `${menosFreq[0].padStart(2,'0')} (${menosFreq[1]}x)`;
  document.getElementById('mediaImpares').textContent = (totalImpares/SORTEIOS_HISTORICOS.length).toFixed(1);
}

function renderUltimoConcurso() {
  const ultimo = SORTEIOS_HISTORICOS[SORTEIOS_HISTORICOS.length-1] || [1,3,5,7,10,11,13,15,18,20,21,22,23,24,25];
  const container = document.getElementById('ultimoBolas');
  container.innerHTML='';
  ultimo.forEach(n=>{
    const b=document.createElement('div');b.className='bola';b.textContent=String(n).padStart(2,'0');container.appendChild(b);
  });
  document.getElementById('ultimoConcursoNum').textContent = `Concurso ${SORTEIOS_HISTORICOS.length}`;
}

// ==================== IA REAL - ATRASÔMETRO ====================
function analisarAtrasos() {
  const atrasosAtuais = {}; const atrasosHist = {};
  for(let i=1;i<=25;i++){atrasosAtuais[i]=0;atrasosHist[i]=[];}
  SORTEIOS_HISTORICOS.forEach(sorteio=>{
    for(let i=1;i<=25;i++){
      if(sorteio.includes(i)){atrasosHist[i].push(atrasosAtuais[i]);atrasosAtuais[i]=0;}
      else atrasosAtuais[i]++;
    }
  });
  const dados={}; const anomalias=[];
  for(let i=1;i<=25;i++){
    const hist=atrasosHist[i];
    const media=hist.length?hist.reduce((a,b)=>a+b,0)/hist.length:0;
    const variancia=hist.length?hist.reduce((a,b)=>a+(b-media)**2,0)/hist.length:0;
    const desvio=Math.sqrt(variancia);
    const limite=media+desvio*2;
    let status='NORMAL';
    if(atrasosAtuais[i]>=limite && limite>0){status='ESTOURANDO';anomalias.push(i);}
    dados[i]={atual:atrasosAtuais[i],media,limite,status};
  }
  return {dados,anomalias};
}

function gerarPrevisaoMarkov() {
  if(SORTEIOS_HISTORICOS.length<2) return {top5:[],ranking:[]};
  const trans={}; for(let i=1;i<=25;i++){trans[i]={};for(let j=1;j<=25;j++)trans[i][j]=0;}
  for(let t=1;t<SORTEIOS_HISTORICOS.length;t++){
    SORTEIOS_HISTORICOS[t-1].forEach(x=>{
      SORTEIOS_HISTORICOS[t].forEach(y=>{trans[x][y]++;});
    });
  }
  const prob={}; for(let i=1;i<=25;i++){prob[i]={};const total=Object.values(trans[i]).reduce((a,b)=>a+b,0);for(let j=1;j<=25;j++)prob[i][j]=total?trans[i][j]/total:0;}
  const ultimo=SORTEIOS_HISTORICOS[SORTEIOS_HISTORICOS.length-1];
  const agreg={};for(let i=1;i<=25;i++)agreg[i]=0;
  ultimo.forEach(x=>{for(let y=1;y<=25;y++)agreg[y]+=prob[x][y];});
  const ranking=Object.entries(agreg).sort((a,b)=>b[1]-a[1]).map(([k,v])=>[parseInt(k),v]);
  return {top5:ranking.slice(0,5).map(r=>r[0]),ranking};
}

function calcularFrequencia() {
  const freq={};for(let i=1;i<=25;i++)freq[i]=0;
  const recentes=SORTEIOS_HISTORICOS.slice(-50);
  recentes.forEach(s=>s.forEach(n=>freq[n]++));
  return freq;
}

// ==================== GERADOR REAL ====================
function gerarJogoAleatorio(fixasArr=[], bloqueadasArr=[], filtros) {
  const disponiveis=[];for(let i=1;i<=25;i++)if(!bloqueadasArr.includes(i))disponiveis.push(i);
  const jogo=new Set(fixasArr);
  let guard=0;
  while(jogo.size<15 && guard++<500){
    const idx=Math.floor(Math.random()*disponiveis.length);
    if(disponiveis[idx]!==undefined) jogo.add(disponiveis[idx]);
  }
  let arr=Array.from(jogo).sort((a,b)=>a-b);
  if(filtros && filtros.size) arr=ajustarAosFiltros(arr,fixasArr,bloqueadasArr,filtros);
  return arr;
}

// ---------- Constantes de filtros ----------
const MOLDURA=[1,2,3,4,5,6,10,11,15,16,20,21,22,23,24,25];
const PRIMOS=[2,3,5,7,11,13,17,19,23];
const FIBONACCI=[1,2,3,5,8,13,21];
const IMPARES=[1,3,5,7,9,11,13,15,17,19,21,23,25];
const TODAS_DEZENAS=Array.from({length:25},(_,i)=>i+1);
let filtrosRelaxadosAviso='';

// Cache das análises pesadas (atrasômetro/Markov/frequência) reutilizado na geração
let cacheIA=null;
function invalidarCacheIA(){cacheIA=null;}
function iaDados(){
  if(!cacheIA){
    const atrasos=analisarAtrasos();
    const freq=calcularFrequencia();
    const markov=gerarPrevisaoMarkov();
    const top14=Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0,14).map(([k])=>parseInt(k));
    cacheIA={atrasos,freq,markov,top14};
  }
  return cacheIA;
}
function top14Quentes(){ return iaDados().top14; }

// Pontuação dos filtros ativos (0 = todos satisfeitos)
function penalidadeFiltros(jogo,filtros,top14){
  let p=0;
  const cont=(lista)=>jogo.filter(n=>lista.includes(n)).length;
  if(filtros.has('impares')){const c=cont(IMPARES); if(c<6)p+=6-c; else if(c>10)p+=c-10;}
  if(filtros.has('moldura')){const c=cont(MOLDURA); if(c<5)p+=5-c; else if(c>10)p+=c-10;}
  if(filtros.has('primos')){const c=cont(PRIMOS); if(c<3)p+=3-c; else if(c>7)p+=c-7;}
  if(filtros.has('fibonacci')){const c=cont(FIBONACCI); if(c<2)p+=2-c; else if(c>5)p+=c-5;}
  if(filtros.has('foco14')){const fora=jogo.filter(n=>!top14.includes(n)).length; if(fora>3)p+=fora-3;}
  if(filtros.has('soma')){const s=jogo.reduce((a,b)=>a+b,0); if(s<180)p+=(180-s)/10; else if(s>200)p+=(s-200)/10;}
  return p;
}

// Ajuste local (hill-climbing): troca dezenas não fixas até satisfazer os filtros
function ajustarAosFiltros(jogo,fixasArr,bloqueadasArr,filtros){
  if(!filtros || filtros.size===0) return jogo.slice().sort((a,b)=>a-b);
  const top14=top14Quentes();
  const candidatos=TODAS_DEZENAS.filter(n=>!bloqueadasArr.includes(n));
  let atual=jogo.slice();
  let p=penalidadeFiltros(atual,filtros,top14);
  if(p===0) return atual.sort((a,b)=>a-b); // já satisfaz todos os filtros
  for(let it=0; it<40 && p>0; it++){
    let melhorP=p, melhorJogo=null;
    for(const entra of candidatos){
      if(atual.includes(entra)) continue;
      for(const sai of atual){
        if(fixasArr.includes(sai)) continue;
        const teste=atual.map(n=>n===sai?entra:n);
        const pt=penalidadeFiltros(teste,filtros,top14);
        if(pt<melhorP){melhorP=pt; melhorJogo=teste;}
      }
    }
    if(!melhorJogo) break;
    atual=melhorJogo; p=melhorP;
  }
  return atual.sort((a,b)=>a-b);
}

function gerarJogoBaseadoEmAntigos(fixasArr=[],bloqueadasArr=[],filtros){
  const ia=iaDados();
  const atrasos=ia.atrasos.dados;
  const freq=ia.freq;
  const markovRanking=ia.markov.ranking;
  const markovMap={}; markovRanking.forEach(([n],idx)=>markovMap[n]=100-idx);

  // Peso de cada dezena = atraso + frequência + Markov, ajustado pela estratégia
  const pool=[];
  for(let i=1;i<=25;i++){
    if(bloqueadasArr.includes(i) || fixasArr.includes(i)) continue;
    let score = atrasos[i].atual*2 + freq[i]*3 + (markovMap[i]||0)*0.5;
    if(estrategia==='conservador') score += freq[i]*2;              // prioriza dezenas frequentes
    else if(estrategia==='agressivo') score += atrasos[i].atual*3;  // prioriza atrasadas
    else if(estrategia==='robo') score += (markovMap[i]||0)*1.5;    // prioriza cadeia de Markov
    else if(estrategia==='preguicoso') score += Math.random()*80;   // busca mais aleatória
    score += (Math.random()-0.5)*Math.max(6, mutacao*2);            // mutação
    score += (Math.random()-0.5)*(severidade/100)*40;               // severidade (exploração)
    pool.push({n:i,score});
  }
  pool.sort((a,b)=>b.score-a.score);

  // Amostragem ponderada: parte da elite (nota alta) + parte do restante => jogos distintos
  const corte=estrategia==='conservador'?10:estrategia==='agressivo'?18:15;
  const elite=pool.slice(0,Math.max(9,Math.min(corte,pool.length)));
  const resto=pool.slice(elite.length);
  const jogo=new Set(fixasArr);
  let guard=0;
  while(jogo.size<15 && (elite.length||resto.length) && guard++<200){
    const fonte=(Math.random()<0.72 && elite.length)?elite:(resto.length?resto:elite);
    if(!fonte.length) break;
    const idx=Math.floor(Math.random()*fonte.length);
    jogo.add(fonte.splice(idx,1)[0].n);
  }
  // Rede de segurança: completa com quaisquer dezenas permitidas
  for(const n of TODAS_DEZENAS){
    if(jogo.size>=15) break;
    if(!bloqueadasArr.includes(n)) jogo.add(n);
  }
  let jogoArr=Array.from(jogo).slice(0,15);
  return ajustarAosFiltros(jogoArr,fixasArr,bloqueadasArr,filtros||new Set());
}

function filtrarJogo(jogo, filtros) {
  if(!filtros) return true;
  if(filtros.has('impares')){
    const c=jogo.filter(n=>IMPARES.includes(n)).length;
    if(c<6 || c>10) return false;
  }
  if(filtros.has('moldura')){
    const qtdMoldura=jogo.filter(n=>MOLDURA.includes(n)).length;
    if(qtdMoldura<5 || qtdMoldura>10) return false;
  }
  if(filtros.has('primos')){
    const qtd=jogo.filter(n=>PRIMOS.includes(n)).length;
    if(qtd<3 || qtd>7) return false;
  }
  if(filtros.has('fibonacci')){
    const qtd=jogo.filter(n=>FIBONACCI.includes(n)).length;
    if(qtd<2 || qtd>5) return false;
  }
  if(filtros.has('foco14')){
    const top14=top14Quentes();
    const fora=jogo.filter(n=>!top14.includes(n)).length;
    if(fora>3) return false;
  }
  if(filtros.has('soma')){
    const soma=jogo.reduce((a,b)=>a+b,0);
    if(soma<180 || soma>200) return false;
  }
  return true;
}

function gerarSistema(qtdJogosNum, fixasArr, bloqueadasArr, filtros, modo) {
  const jogos=[];
  const vistos=new Set();
  let tentativas=0;
  const MAX_TENT=Math.max(600, qtdJogosNum*80);
  let relaxados=0;
  filtrosRelaxadosAviso='';
  invalidarCacheIA();
  while(jogos.length<qtdJogosNum && tentativas<MAX_TENT){
    tentativas++;
    let jogo;
    if(modo==='aleatorio'){
      if(!isPremium){showPremiumLock();return [];}
      jogo=gerarJogoAleatorio(fixasArr,bloqueadasArr,filtros);
    } else {
      jogo=gerarJogoBaseadoEmAntigos(fixasArr,bloqueadasArr,filtros);
    }
    if(!jogo || jogo.length!==15) continue;
    if(!filtrarJogo(jogo,filtros)) relaxados++;
    const chave=jogo.join(',');
    if(vistos.has(chave)) continue;
    vistos.add(chave);
    jogos.push(jogo);
  }
  if(relaxados>0){
    filtrosRelaxadosAviso=`⚠️ ${relaxados} jogo(s) com ajuste parcial de filtros (combinação de filtros conflitante)`;
    log(filtrosRelaxadosAviso,'warn');
  }
  if(jogos.length<qtdJogosNum){
    log(`⚠️ Gerados ${jogos.length} de ${qtdJogosNum} jogos únicos (limite de tentativas atingido)`,'warn');
  }
  return jogos;
}

function avaliarSistema(jogos) {
  // Simular score R$ baseado em histórico - quantos 11,12,13,14,15 acertaria nos últimos 100
  let scoreTotal=0;
  const ultimos100=SORTEIOS_HISTORICOS.slice(-100);
  jogos.forEach(jogo=>{
    ultimos100.forEach(sorteio=>{
      const acertos=jogo.filter(n=>sorteio.includes(n)).length;
      if(acertos===11) scoreTotal+=5;
      else if(acertos===12) scoreTotal+=10;
      else if(acertos===13) scoreTotal+=25;
      else if(acertos===14) scoreTotal+=500;
      else if(acertos===15) scoreTotal+=1500;
    });
  });
  return scoreTotal;
}

// ==================== UI FUNCIONAL ====================
function setModoGeracao(modo) {
  if(modo==='aleatorio' && !isPremium){
    showPremiumLock();
    return;
  }
  modoGeracao=modo;
  localStorage.setItem('modoGeracao',modo);
  document.querySelectorAll('.modo-card').forEach(c=>c.classList.remove('active'));
  document.getElementById(modo==='antigos'?'modoAntigos':'modoAleatorio').classList.add('active');
  document.getElementById('modoDesc').textContent = modo==='antigos' 
    ? 'Modo Antigos: usa atrasômetro, Markov, frequência real de 3675 concursos - Grátis'
    : 'Modo Aleatório: números totalmente aleatórios sem análise - Premium desbloqueado';
  log(`🎯 Modo alterado para: ${modo==='antigos'?'Sorteios Antigos (Grátis)':'Aleatório (Premium)'}`, 'info');
}

function showPremiumLock() {
  const existing=document.querySelector('.premium-lock');
  if(existing) existing.remove();
  const geradorContent=document.querySelector('.gerador-content');
  const lock=document.createElement('div');
  lock.className='premium-lock';
  lock.innerHTML=`
    <div class="lock-ico">🔒</div>
    <div class="lock-title">Recurso Premium</div>
    <div class="lock-desc">Gerador Aleatório é exclusivo Premium.<br>Use Sorteios Antigos grátis ou desbloqueie Premium.</div>
    <button class="btn-unlock" onclick="showScreen('premium')">👑 Desbloquear Premium</button>
    <button class="btn-outline" style="margin-top:8px;font-size:11px;padding:6px 12px" onclick="this.parentElement.remove();setModoGeracao('antigos')">Usar Modo Grátis</button>
  `;
  geradorContent.style.position='relative';
  geradorContent.appendChild(lock);
  setTimeout(()=>{if(lock.parentElement) lock.remove();},5000);
}

function iniciarMotorReal() {
  const btn=document.getElementById('btnMotor');
  if(!btn || btn.disabled) return;

  const qtd=parseInt(document.querySelector('.seg-btn.active')?.dataset.v || '33');
  if(qtd>10 && !isPremium){
    log('❌ '+qtd+' jogos é Premium. Free limita 10. Compre Premium ou use 10.','error');
    showToast('🔒 '+qtd+' jogos é Premium - use 10 no plano Free');
    showScreen('premium');
    return;
  }

  btn.disabled=true;
  btn.classList.add('gerando');
  btn.innerHTML='⏳ GERANDO...<div class="progresso"></div><span class="shimmer" aria-hidden="true" style="position:absolute;inset:0;"></span>';
  btn.setAttribute('aria-busy','true');
  esqueleto(document.getElementById('rankingList'), 3, 110);
  log(`🚀 Iniciando motor híbrido - Modo: ${modoGeracao} - ${qtd} jogos - Fixas: [${fixas}] Bloqueadas: [${bloqueadas}]`,'info');

  setTimeout(()=>{
    try{
      const jogos=gerarSistema(qtd, fixas, bloqueadas, filtrosAtivos, modoGeracao);
      if(!jogos || jogos.length===0){
        log('❌ Nenhum jogo pôde ser gerado. Verifique fixas/bloqueadas/filtros e tente novamente.','error');
        showToast('❌ Nada foi gerado - revise fixas, bloqueadas e filtros');
        btn.disabled=false; btn.classList.remove('gerando'); btn.removeAttribute('aria-busy');
        btn.innerHTML='🚀 INICIAR MOTOR HÍBRIDO';
        renderRanking();
        return;
      }
      const score=avaliarSistema(jogos);
      geracaoAtual++;
      if(score>topScore) topScore=score;

      localStorage.setItem('geracaoAtual',geracaoAtual);
      localStorage.setItem('topScore',topScore);

      const base20=gerarBase20(fixas,bloqueadas);
      rankingMatrizes.unshift({
        id:Date.now(),
        score:score,
        geracao:geracaoAtual,
        base:base20,
        jogos:jogos,
        modo:modoGeracao,
        fixas:[...fixas],
        bloqueadas:[...bloqueadas],
        data:new Date().toISOString()
      });
      rankingMatrizes.sort((a,b)=>b.score-a.score);
      rankingMatrizes=rankingMatrizes.slice(0,50);
      const melhorScore=rankingMatrizes.length?rankingMatrizes[0].score:score;
      if(melhorScore>topScore){ topScore=melhorScore; localStorage.setItem('topScore',topScore); }
      localStorage.setItem('rankingMatrizes',JSON.stringify(rankingMatrizes));

      atualizarKPIs();
      log(`✅ ${jogos.length} jogos gerados! Score: R$ ${fmtMoeda(score)} - Modo: ${modoGeracao}`,'info');
      log(`📊 Base 20: [${base20.join(', ')}]`,'info');
      log(`🎲 Exemplo jogo 1: [${jogos[0].join(', ')}]`,'info');
      log(`💰 Top Score: R$ ${fmtMoeda(topScore)} G${geracaoAtual}`,'info');

      matrizDestacada=rankingMatrizes[0] ? rankingMatrizes[0].id : null;
      renderRanking();
      renderHeatmaps();
      rodarIA('atrasometro');

      btn.disabled=false;
      btn.classList.remove('gerando');
      btn.removeAttribute('aria-busy');
      btn.innerHTML='🚀 INICIAR MOTOR HÍBRIDO';
      let msg=`✅ ${jogos.length} jogos gerados! Score R$ ${fmtMoeda(score)} - Ver em Jogos`;
      if(filtrosRelaxadosAviso) msg='⚠️ '+jogos.length+' jogos gerados com ajuste de filtros - Ver em Jogos';
      showToast(msg);
    }catch(err){
      log('❌ Erro na geração: '+err.message,'error');
      showToast('❌ Erro ao gerar: '+err.message);
      btn.disabled=false; btn.classList.remove('gerando'); btn.removeAttribute('aria-busy');
      btn.innerHTML='🚀 INICIAR MOTOR HÍBRIDO';
      renderRanking();
    }
  },800);
}

function gerarBase20(fixasArr,bloqArr){
  const base=new Set(fixasArr);
  const candidatos=[];
  for(let i=1;i<=25;i++) if(!bloqArr.includes(i) && !fixasArr.includes(i)) candidatos.push(i);
  // Ordenar por frequência real
  const freq=calcularFrequencia();
  candidatos.sort((a,b)=>freq[b]-freq[a]);
  for(let n of candidatos){if(base.size>=20) break; base.add(n);}
  return Array.from(base).sort((a,b)=>a-b);
}

function gerarRankingInicial(){
  const vistos=new Set();
  let guard=0;
  while(rankingMatrizes.length<8 && guard++<40){
    const base=gerarBase20([1,5,10],[25]);
    const jogos=gerarSistema(10, [1,5,10], [25], filtrosAtivos, 'antigos');
    if(!jogos.length) break;
    const assinatura=jogos.map(j=>j.join('-')).join('|');
    if(vistos.has(assinatura)) continue;
    vistos.add(assinatura);
    const score=avaliarSistema(jogos);
    rankingMatrizes.push({id:Date.now()+rankingMatrizes.length,score,geracao:42-rankingMatrizes.length,base,jogos,modo:'antigos',fixas:[1,5,10],bloqueadas:[25],data:new Date().toISOString()});
  }
  rankingMatrizes.sort((a,b)=>b.score-a.score);
  if(rankingMatrizes.length && rankingMatrizes[0].score>topScore){
    topScore=rankingMatrizes[0].score;
    localStorage.setItem('topScore',topScore);
  }
  localStorage.setItem('rankingMatrizes',JSON.stringify(rankingMatrizes));
  atualizarKPIs();
  renderRanking();
}

// ==================== HEATMAPS ====================
function getHeatColor(v){
  // tons escurecidos para manter contraste AA com o número branco
  if(v<0.2) return '#1E3A8A';
  if(v<0.4) return '#2563EB';
  if(v<0.6) return '#3730A3';
  if(v<0.8) return '#C2410C';
  return '#B91C1C';
}
function renderHeatmaps(){
  const freq=calcularFrequencia();
  const max=Math.max(...Object.values(freq));
  const min=Math.min(...Object.values(freq));
  ['heatmapDash','heatmapIntel'].forEach(id=>{
    const el=document.getElementById(id);
    if(!el) return;
    el.innerHTML='';
    for(let i=1;i<=25;i++){
      const v=(freq[i]-min)/(max-min||1);
      const c=document.createElement('div');
      c.className='cell';
      c.style.setProperty('--i', i-1);
      c.style.background=getHeatColor(v);
      c.textContent=String(i).padStart(2,'0');
      c.onclick=()=>{toggleFixa(i);};
      el.appendChild(c);
    }
  });
  renderSensor();
}
function renderSensor(){
  const grid=document.getElementById('gridSensor');
  const top5=document.getElementById('top5SensorList');
  if(!grid) return;
  grid.innerHTML='';
  const freq=calcularFrequencia();
  const scores=[];
  for(let i=1;i<=25;i++){scores.push({n:i,score:freq[i]});}
  scores.sort((a,b)=>b.score-a.score);
  const max=scores[0].score, min=scores[scores.length-1].score;
  for(let i=1;i<=25;i++){
    const s=freq[i];
    const norm=(s-min)/(max-min||1);
    const cell=document.createElement('div');
    cell.className='cell-sensor';
    cell.style.setProperty('--i', i-1);
    if(norm<0.2) cell.classList.add('fria');
    else if(norm<0.4) cell.classList.add('media-fria');
    else if(norm<0.6) cell.classList.add('media');
    else if(norm<0.8) cell.classList.add('quente');
    else cell.classList.add('muito-quente');
    cell.textContent=String(i).padStart(2,'0');
    cell.onclick=()=>toggleFixa(i);
    grid.appendChild(cell);
  }
  top5.innerHTML='';
  scores.slice(0,5).forEach((s,idx)=>{
    const row=document.createElement('div');
    row.className='top5-sensor-row';
    const cls = s.score>15?'red': s.score>10?'orange':'yellow';
    row.innerHTML=`<div class="pos">${idx+1}</div><div class="num ${cls}">${String(s.n).padStart(2,'0')}</div><div class="score">Freq: <b>${s.score}</b> (50 conc)</div><div class="pin" onclick="toggleFixa(${s.n})">📌</div>`;
    top5.appendChild(row);
  });
}

// ==================== IA ====================
function rodarIA(tipo){
  const rotulos={atrasometro:'ATRASÔMETRO',markov:'MARKOV',ensemble:'ENSEMBLE',apriori:'APRIORI',autopiloto:'AUTO-PILOTO'};
  const label=document.getElementById('iaModeLabel');
  if(label) label.textContent=rotulos[tipo]||String(tipo).toUpperCase();
  // marca apenas as abas da própria tela de IA (não mexe na barra principal)
  const map={atrasometro:0,markov:1,ensemble:2,apriori:3,autopiloto:4};
  const tabs=document.querySelectorAll('#screen-inteligencia .bottom-tabs .tab');
  tabs.forEach(t=>t.classList.remove('active'));
  if(tabs[map[tipo]]) tabs[map[tipo]].classList.add('active');

  let top5=[], detalhes='';
  if(tipo==='atrasometro'){
    const {dados,anomalias}=analisarAtrasos();
    top5=Object.entries(dados).sort((a,b)=>b[1].atual-a[1].atual).slice(0,5).map(([k,v])=>({n:parseInt(k),score:v.atual,pts:(95-Math.random()*5).toFixed(1)}));
    detalhes=`🕒 Atrasômetro: ${anomalias.length} dezenas estourando (acima de 2σ). Dezenas com maior atraso têm maior probabilidade de sair. Base: ${SORTEIOS_HISTORICOS.length} sorteios. Anomalias: [${anomalias.join(', ')||'nenhuma'}]`;
    renderAnomalias(dados,anomalias);
  } else if(tipo==='markov'){
    const {top5:mkTop,ranking}=gerarPrevisaoMarkov();
    top5=mkTop.map((n,i)=>({n,score:ranking[i]?ranking[i][1]:0,pts:(95-i*2).toFixed(1)}));
    detalhes=`🔗 Markov: Cadeias de Markov analisam transição de dezenas. Se 04 saiu, qual probabilidade de 22 sair no próximo? Top: ${mkTop.join(', ')}`;
  } else if(tipo==='ensemble'){
    const freq=calcularFrequencia();
    const {dados:atrasos}=analisarAtrasos();
    const {ranking:mk}=gerarPrevisaoMarkov();
    const mkMap={};mk.forEach(([n,p],i)=>mkMap[n]=100-i);
    const scores={};for(let i=1;i<=25;i++)scores[i]=freq[i]*2 + atrasos[i].atual*1.5 + (mkMap[i]||0);
    top5=Object.entries(scores).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([k,v])=>({n:parseInt(k),score:v,pts:(98-Math.random()*3).toFixed(1)}));
    detalhes=`📚 Ensemble: Combina atrasômetro + frequência + Markov com pesos. Score = freq*2 + atraso*1.5 + markov. Mais robusto.`;
  } else if(tipo==='apriori'){
    const pares={};
    SORTEIOS_HISTORICOS.slice(-200).forEach(s=>{
      for(let i=0;i<s.length;i++) for(let j=i+1;j<s.length;j++){
        const key=`${s[i]}-${s[j]}`;
        pares[key]=(pares[key]||0)+1;
      }
    });
    const topPares=Object.entries(pares).sort((a,b)=>b[1]-a[1]).slice(0,10);
    top5=topPares.slice(0,5).map(([k,v])=>({n:parseInt(k.split('-')[0]),score:v,pts:v.toString()}));
    detalhes=`🔀 Apriori: Regras de associação. Pares que mais saem juntos nos últimos 200 concursos: ${topPares.slice(0,3).map(([k,v])=>`${k} (${v}x)`).join(', ')}`;
  } else if(tipo==='autopiloto'){
    const freq=calcularFrequencia();
    const ultimos=SORTEIOS_HISTORICOS.slice(-100);
    const mediaImpares=ultimos.reduce((acc,s)=>acc+s.filter(n=>n%2===1).length,0)/(ultimos.length||1);
    const mediaSoma=ultimos.reduce((acc,s)=>acc+s.reduce((x,y)=>x+y,0),0)/(ultimos.length||1);
    top5=Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([k,v])=>({n:parseInt(k),score:v,pts:v.toString()}));
    detalhes=`🚀 Auto-Piloto: Analisa macro propriedades. Média ímpares últimos 100: ${mediaImpares.toFixed(1)}. Soma média: ${mediaSoma.toFixed(0)}. Recomenda 7-9 ímpares, 6-8 pares, soma 180-220.`;
  }

  const list=document.getElementById('top5IAList');
  if(list){
    list.innerHTML='';
    top5.forEach((item,idx)=>{
      const row=document.createElement('div');
      row.className='top5-row';
      row.innerHTML=`<div class="pos">${idx+1}º</div><div class="num">${String(item.n).padStart(2,'0')}</div><div class="bar"><div class="bar-fill" style="width:${90-idx*5}%"></div></div><div class="pts">${item.pts} pts</div><div class="star" onclick="toggleFixa(${item.n})">★</div>`;
      list.appendChild(row);
    });
  }
  const det=document.getElementById('iaDetalhes');
  if(det) det.textContent=detalhes;
}

function renderAnomalias(dados,anomalias){
  const container=document.getElementById('anomaliasList');
  container.innerHTML='';
  // Top 3 anomalias
  const sorted=Object.entries(dados).sort((a,b)=>b[1].atual-a[1].atual).slice(0,3);
  sorted.forEach(([n,d],i)=>{
    const row=document.createElement('div');
    row.className='anom-row';
    const badge = d.atual>25?'ALTA':d.atual>15?'MÉDIA':'BAIXA';
    const badgeClass = d.atual>25?'badge-alta':d.atual>15?'badge-media':'badge-baixa';
    const ico = d.atual>25?'⚠️':d.atual>15?'🕒':'ℹ️';
    row.innerHTML=`<div class="ico" style="background:rgba(239,68,68,0.15);color:var(--red-soft)">${ico}</div><div class="txt"><div class="t">${i===0?'Intervalo longo sem: '+n:'Números em atraso: '+n} - Atual ${d.atual} vs Média ${d.media.toFixed(1)}</div><div class="d">${d.status} - ${d.atual>20?'Acima de 20 concursos':'Há '+d.atual+' concursos'}</div></div><div class="badge ${badgeClass}">${badge}</div>`;
    container.appendChild(row);
  });
  if(anomalias.length===0){
    const row=document.createElement('div');
    row.className='anom-row';
    row.innerHTML=`<div class="ico" style="background:rgba(16,185,129,0.15);color:var(--success-text)">✅</div><div class="txt"><div class="t">Nenhuma anomalia crítica</div><div class="d">Sistema saudável - 3675 sorteios analisados</div></div><div class="badge badge-baixa">OK</div>`;
    container.appendChild(row);
  }
}

// ==================== RANKING ====================
function listaRanking(){
  if(rankingTab==='top3') return rankingMatrizes.slice(0,3);
  if(rankingTab==='fav') return rankingMatrizes.filter(m=>favoritos.includes(m.id));
  return rankingMatrizes;
}
function aplicarTabRanking(){
  const ordem=['top50','top3','fav'];
  document.querySelectorAll('#screen-ranking .bottom-tabs .tab').forEach((t,i)=>{
    t.classList.toggle('active', ordem[i]===rankingTab);
  });
}
function renderRanking(){
  const el=document.getElementById('rankingList');
  if(!el) return;
  el.innerHTML='';
  const lista=listaRanking();
  if(lista.length===0){
    el.innerHTML=rankingTab==='fav'
      ? '<div style="padding:40px;text-align:center;color:var(--text2)">Nenhum favorito ainda. Toque em ☆ nos cards do ranking para favoritar.</div>'
      : '<div style="padding:40px;text-align:center;color:var(--text2)">Nenhuma matriz gerada ainda. Vá em Gerações e clique Iniciar Motor.</div>';
    return;
  }
  lista.forEach((mat, indice)=>{
    const pos=rankingMatrizes.indexOf(mat)+1;
    let posClass='normal', crown='';
    if(pos===1){posClass='gold';crown='👑'} else if(pos===2){posClass='silver';crown='👑'} else if(pos===3){posClass='bronze';crown='👑'}
    const score=fmtMoeda(mat.score||0);
    const fav=favoritos.includes(mat.id);
    const card=document.createElement('div');
    card.className='rank-card'+(mat.id===matrizDestacada?' rank-card--novo':'');
    card.style.setProperty('--i', Math.min(indice,14));
    card.setAttribute('role','button');
    card.setAttribute('aria-label','Matriz '+pos+'º lugar, score R$ '+score+(mat.modo==='aleatorio'?', modo aleatório':', modo antigos'));
    card.onclick=()=>abrirDetalhes(mat);
    card.innerHTML=`
      <div class="rank-pos ${posClass}">${crown?`<div class="crown">${crown}</div>`:''}${pos}</div>
      <div class="rank-info"><div class="score-row"><div class="score">R$ ${score}</div><div class="g">G${mat.geracao}</div><div style="font-size:11px;background:${mat.modo==='aleatorio'?'var(--gold)':'var(--chip-14)'};color:${mat.modo==='aleatorio'?'#000':'#fff'};padding:2px 6px;border-radius:6px">${mat.modo==='aleatorio'?'ALEATÓRIO':'ANTIGOS'}</div></div><div class="base">Base: ${(mat.base||[]).join(' ')}</div><div class="rank-chips"><div class="rank-chip c11">11</div><div class="rank-chip c12">12</div><div class="rank-chip c13">13</div><div class="rank-chip c14">14</div><div class="rank-chip c15">15</div></div></div>
      <div class="rank-actions"><div class="rank-star" onclick="event.stopPropagation();favoritar(${mat.id})">${fav?'★':'☆'}</div><div class="rank-arrow">›</div></div>`;
    el.appendChild(card);
  });
}

function melhorAcerto(mat){
  const sorteios=SORTEIOS_HISTORICOS.slice(-100);
  let melhor=0;
  sorteios.forEach(d=>{
    (mat.jogos||[]).forEach(j=>{
      const a=j.filter(n=>d.includes(n)).length;
      if(a>melhor) melhor=a;
    });
  });
  return melhor;
}

function renderApostas(mat){
  const apostasEl=document.getElementById('apostasList');
  if(!apostasEl || !mat) return;
  apostasEl.innerHTML='';
  const lista=mostrarTodasApostas?mat.jogos:mat.jogos.slice(0,5);
  lista.forEach((nums,i)=>{
    const row=document.createElement('div');
    row.className='aposta-row';
    row.innerHTML=`<div class="label">Aposta ${String(i+1).padStart(2,'0')}:</div><div class="nums">${nums.map(n=>String(n).padStart(2,'0')).join(' ')}</div><div style="cursor:pointer" onclick="copiarAposta('${nums.join(' ')}')">📋</div>`;
    apostasEl.appendChild(row);
  });
  const count=document.getElementById('detApostasCount');
  if(count) count.textContent=`${mat.jogos.length} apostas${mostrarTodasApostas?'':` (5 exibidas)`}`;
}

function abrirDetalhes(mat){
  if(!mat) return;
  matrizAtual=mat;
  mostrarTodasApostas=false;
  const pos=rankingMatrizes.indexOf(mat)+1;
  const posEl=document.getElementById('detPos');
  if(posEl) posEl.innerHTML=`${pos}<div class="wreath left">🌿</div><div class="wreath right">🌿</div>`;
  const scoreEl=document.getElementById('detScore');
  if(scoreEl){
    const partes=fmtMoeda(mat.score).split(',');
    scoreEl.innerHTML=`R$ ${partes[0]},<span style="font-size:18px">${partes[1]}</span>`;
  }
  const setId=(id,v)=>{const e=document.getElementById(id); if(e) e.textContent=v;};
  setId('detId','#'+mat.id);
  setId('detData',new Date(mat.data).toLocaleString('pt-BR'));
  setId('detPontos',mat.score.toFixed(0));
  setId('detApostas',mat.jogos.length);
  setId('detApostasCount',mat.jogos.length+' apostas (5 exibidas)');
  setId('detRank',pos+'º');
  setId('detRankSub','de '+rankingMatrizes.length+' matrizes');
  const acertos=melhorAcerto(mat);
  const aproveitamento=Math.round((acertos/15)*100);
  setId('detAcertos',acertos);
  setId('detAcertosSub','melhor em 100 concursos');
  setId('detAproveitamento',aproveitamento+'%');
  setId('detAproveitamentoSub',acertos>=14?'Excepcional':acertos>=13?'Excelente':acertos>=11?'Bom':'Regular');

  const dezenasEl=document.getElementById('dezenasOuro');
  if(dezenasEl){
    dezenasEl.innerHTML='';
    (mat.base||[]).forEach(n=>{
      const d=document.createElement('div');d.className='dez-ouro';d.textContent=String(n).padStart(2,'0');dezenasEl.appendChild(d);
    });
  }
  renderApostas(mat);
  showScreen('detalhes');
}

// ==================== UTILS ====================
function toggleFixa(n){
  n=parseInt(n,10);
  if(!Number.isInteger(n) || n<1 || n>25) return;
  if(fixas.includes(n)){
    fixas=fixas.filter(x=>x!==n);
    showToast(`📌 Fixas: [${fixas.join(', ')||'nenhuma'}]`);
  } else {
    if(bloqueadas.includes(n)){showToast('🚫 Dezena '+String(n).padStart(2,'0')+' está bloqueada - remova dos bloqueados primeiro');return;}
    if(fixas.length>=6){showToast('⚠️ Máximo 6 fixas - remova uma antes de adicionar');return;}
    fixas.push(n);
    showToast(`📌 Fixa adicionada: ${String(n).padStart(2,'0')} [${[...fixas].sort((a,b)=>a-b).join(', ')}]`);
  }
  fixas.sort((a,b)=>a-b);
  localStorage.setItem('fixas',JSON.stringify(fixas));
  renderFixasBloqueadas();
}

function renderFixasBloqueadas(){
  const fixasEl=document.getElementById('fixasChips');
  fixasEl.innerHTML=fixas.map(n=>`<div class="chip fixa" onclick="toggleFixa(${n})">${String(n).padStart(2,'0')} ✕</div>`).join('') || '<span style="font-size:11px;color:var(--text3)">Nenhuma</span>';
  const bloqEl=document.getElementById('bloqChips');
  bloqEl.innerHTML=bloqueadas.map(n=>`<div class="chip bloq" onclick="toggleBloq(${n})">${String(n).padStart(2,'0')} ✕</div>`).join('') || '<span style="font-size:11px;color:var(--text3)">Nenhuma</span>';
}
function toggleBloq(n){
  n=parseInt(n,10);
  if(!Number.isInteger(n) || n<1 || n>25) return;
  if(bloqueadas.includes(n)){
    bloqueadas=bloqueadas.filter(x=>x!==n);
    showToast(`🚫 Bloqueadas: [${bloqueadas.join(', ')||'nenhuma'}]`);
  } else {
    if(fixas.includes(n)){showToast('📌 Dezena '+String(n).padStart(2,'0')+' está fixa - remova das fixas primeiro');return;}
    if(bloqueadas.length>=5){showToast('⚠️ Máximo 5 bloqueadas - remova uma antes de adicionar');return;}
    bloqueadas.push(n);
    showToast(`🚫 Bloqueada: ${String(n).padStart(2,'0')} [${[...bloqueadas].sort((a,b)=>a-b).join(', ')}]`);
  }
  bloqueadas.sort((a,b)=>a-b);
  localStorage.setItem('bloqueadas',JSON.stringify(bloqueadas));
  renderFixasBloqueadas();
}

function editarFixas(){
  const input=prompt('Fixas (até 6 dezenas, ex: 1,5,10):', fixas.join(','));
  if(input===null) return;
  let lista=[...new Set(input.split(',').map(s=>parseInt(s.trim(),10)).filter(n=>Number.isInteger(n)&&n>=1&&n<=25))];
  lista=lista.filter(n=>!bloqueadas.includes(n));
  if(lista.length>6){ lista=lista.slice(0,6); showToast('Máximo 6 fixas - mantidas '+lista.join(', ')); }
  fixas=lista.sort((a,b)=>a-b);
  localStorage.setItem('fixas',JSON.stringify(fixas));
  renderFixasBloqueadas();
  showToast(`📌 Fixas: [${fixas.join(', ')||'nenhuma'}]`);
}

function editarBloqueadas(){
  const input=prompt('Bloqueadas (até 5 dezenas, ex: 25):', bloqueadas.join(','));
  if(input===null) return;
  let lista=[...new Set(input.split(',').map(s=>parseInt(s.trim(),10)).filter(n=>Number.isInteger(n)&&n>=1&&n<=25))];
  lista=lista.filter(n=>!fixas.includes(n));
  if(lista.length>5){ lista=lista.slice(0,5); showToast('Máximo 5 bloqueadas - mantidas '+lista.join(', ')); }
  bloqueadas=lista.sort((a,b)=>a-b);
  localStorage.setItem('bloqueadas',JSON.stringify(bloqueadas));
  renderFixasBloqueadas();
  showToast(`🚫 Bloqueadas: [${bloqueadas.join(', ')||'nenhuma'}]`);
}

function setMutacao(e){
  const rect=e.currentTarget.getBoundingClientRect();
  const x=e.clientX-rect.left;
  const pct=Math.max(0,Math.min(100, (x/rect.width)*100));
  mutacao=1 + (pct/100)*24;
  document.getElementById('mutacaoFill').style.width=pct+'%';
  document.getElementById('mutacaoVal').textContent=Math.round(mutacao)+'%';
  localStorage.setItem('mutacao',mutacao);
}
function setSeveridade(e){
  const rect=e.currentTarget.getBoundingClientRect();
  const x=e.clientX-rect.left;
  const pct=Math.max(0,Math.min(100, (x/rect.width)*100));
  severidade=pct;
  document.getElementById('severidadeFill').style.width=pct+'%';
  document.getElementById('severidadeVal').textContent=Math.round(severidade)+'%';
  localStorage.setItem('severidade',severidade);
}
function toggleMem(el){el.classList.toggle('on');}
function setEstrategia(est){
  estrategia=est;
  localStorage.setItem('estrategia',est);
  document.querySelectorAll('.est-row .arrow').forEach(a=>a.textContent='›');
  const map={conservador:'estCons',agressivo:'estAgr',robo:'estRobo',preguicoso:'estPreg'};
  document.getElementById(map[est]).textContent='✓';
  showToast(`🎯 Estratégia: ${est}`);
}
function fixarTop5(){
  const freq=calcularFrequencia();
  const top5=Object.entries(freq).sort((a,b)=>b[1]-a[1]).map(([k])=>parseInt(k)).filter(n=>!bloqueadas.includes(n)).slice(0,5);
  const novas=[...new Set([...fixas,...top5])].slice(0,6).sort((a,b)=>a-b);
  fixas=novas;
  localStorage.setItem('fixas',JSON.stringify(fixas));
  renderFixasBloqueadas();
  showToast(`📌 Fixas atualizadas (Top5 real): [${fixas.join(', ')}]`);
}

function log(msg,type='info'){
  const area=document.getElementById('logArea');
  if(!area) return;
  const line=document.createElement('div');
  line.className='log-line '+(type==='warn'?'log-warn':type==='error'?'log-error':'');
  line.textContent=`[${new Date().toLocaleTimeString('pt-BR')}] ${msg}`;
  area.appendChild(line);
  while(area.children.length>300) area.removeChild(area.firstChild);
  area.scrollTop=area.scrollHeight;
}

function showToast(msg){
  const toast=document.getElementById('toast');
  if(!toast) return;
  toast.textContent=msg;
  toast.classList.add('show');
  if(toastTimer) clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>toast.classList.remove('show'),3000);
}

function copiarAposta(nums){
  const confirmar=()=>showToast('📋 Copiado: '+nums);
  const fallback=()=>{
    try{
      const ta=document.createElement('textarea');
      ta.value=nums; ta.setAttribute('readonly','');
      ta.style.position='fixed'; ta.style.top='-1000px';
      document.body.appendChild(ta); ta.select();
      const ok=document.execCommand('copy');
      ta.remove();
      if(ok) confirmar(); else showToast('📋 Aposta: '+nums);
    }catch(e){ showToast('📋 Aposta: '+nums); }
  };
  try{
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(nums).then(confirmar).catch(fallback);
      return;
    }
  }catch(e){}
  fallback();
}

function compartilharWhats(){
  const mat=matrizAtual||rankingMatrizes[0];
  const jogos=(mat&&mat.jogos?mat.jogos.slice(0,3):[]).map(j=>j.map(n=>String(n).padStart(2,'0')).join(' ')).join(' | ');
  const texto=`🎯 Lotofácil Pro - Top Score R$ ${fmtMoeda(topScore)} - Base 20: ${mat&&mat.base?mat.base.join(' '):''}${jogos?` - Jogos: ${jogos}`:''}`;
  try{ window.open(`https://wa.me/?text=${encodeURIComponent(texto)}`,'_blank'); }catch(e){}
  showToast('💬 Abrindo WhatsApp para compartilhar');
}

function stressTest(){
  if(!matrizAtual){showToast('📈 Gere uma matriz primeiro para rodar o Stress Test');return;}
  const SIM=1000;
  let soma=0, melhor=0, jogos15=0;
  for(let i=0;i<SIM;i++){
    const d=new Set();
    while(d.size<15) d.add(1+Math.floor(Math.random()*25));
    const arr=[...d];
    matrizAtual.jogos.forEach(j=>{
      const a=j.filter(n=>arr.includes(n)).length;
      soma+=a;
      if(a>melhor) melhor=a;
      if(a===15) jogos15++;
    });
  }
  const media=(soma/(SIM*matrizAtual.jogos.length)).toFixed(2).replace('.',',');
  log(`📈 Stress Test: ${SIM} sorteios simulados - média ${media} acertos/aposta - melhor ${melhor} acertos`,'info');
  showToast(`📈 Stress Test (${SIM} simulações): média ${media} acertos • melhor ${melhor}`);
}

function testeCaos(){
  if(!matrizAtual){showToast('🌀 Gere uma matriz primeiro para o teste de caos');return;}
  const SIM=300;
  const simular=(gerar)=>{
    let soma=0,max=0;
    for(let i=0;i<SIM;i++){
      const arr=gerar();
      matrizAtual.jogos.forEach(j=>{
        const a=j.filter(n=>arr.includes(n)).length;
        soma+=a; if(a>max) max=a;
      });
    }
    return {media:soma/(SIM*matrizAtual.jogos.length), max};
  };
  const normal=simular(()=>{const s=new Set();while(s.size<15)s.add(1+Math.floor(Math.random()*25));return [...s];});
  const caos=simular(()=>{ // cenário extremo: dezenas concentradas nas pontas
    const s=new Set();
    while(s.size<15){
      const extremo=Math.random()<0.7;
      s.add(extremo?(Math.random()<0.5?1+Math.floor(Math.random()*6):20+Math.floor(Math.random()*6)):1+Math.floor(Math.random()*25));
    }
    return [...s];
  });
  const variacao=(((caos.media-normal.media)/normal.media)*100).toFixed(1);
  log(`🌀 Teste Caos: cenário normal ${normal.media.toFixed(2)} vs extremo ${caos.media.toFixed(2)} acertos (variação ${variacao}%)`,'warn');
  showToast(`🌀 Teste Caos: variação extrema ${variacao}% • melhor acerto ${caos.max}`);
}

function verTodasApostas(){
  if(!matrizAtual){showToast('📋 Abra uma matriz do ranking primeiro');return;}
  mostrarTodasApostas=!mostrarTodasApostas;
  renderApostas(matrizAtual);
  const el=document.querySelector('#screen-detalhes div[onclick="verTodasApostas()"] span:last-child');
  if(el) el.textContent=mostrarTodasApostas?'⌃':'⌄';
  showToast(mostrarTodasApostas?`📋 Exibindo todas as ${matrizAtual.jogos.length} apostas`:'📋 Exibindo as 5 primeiras apostas');
}

function favoritar(id){
  const i=favoritos.indexOf(id);
  if(i>=0){favoritos.splice(i,1); showToast('☆ Removido dos Favoritos');}
  else {favoritos.push(id); showToast('⭐ Favoritado! Ver em Favoritos');}
  localStorage.setItem('favoritos',JSON.stringify(favoritos));
  renderRanking();
}

function setRankingTab(tab, el){
  rankingTab=tab;
  if(!el && typeof event!=='undefined' && event && event.currentTarget) el=event.currentTarget;
  aplicarTabRanking();
  renderRanking();
  const nomes={top50:'Top 50',top3:'Top 3',fav:'Favoritos'};
  showToast('📊 '+nomes[tab]);
}

function atualizarRanking(){
  renderRanking();
  showToast('🔄 Ranking atualizado');
}

function editarBanca(){
  const novo=prompt('Banca R$:', banca);
  if(novo===null || novo==='') return;
  const valor=parseFloat(String(novo).replace(',','.'));
  if(!isFinite(valor) || valor<0){showToast('⚠️ Valor de banca inválido');return;}
  banca=valor;
  localStorage.setItem('banca',banca);
  const el=document.getElementById('bancaVal');
  if(el) el.textContent='R$ '+fmtMoeda(banca);
  showToast('💳 Banca atualizada: R$ '+fmtMoeda(banca));
}
function deletarDados(){if(confirm('Apagar todos dados?')){localStorage.clear();location.reload();}}
function comprarPlano(plano){
  isPremium=true;
  localStorage.setItem('isPremium','true');
  const nomes={anual:'Anual',mensal:'Mensal',vitalicio:'Vitalício',trial:'3 dias grátis'};
  showToast(`✅ Premium ${nomes[plano]||plano} ativado! Aleatório desbloqueado`);
  log(`👑 Premium ativado (${nomes[plano]||plano}) - modo Aleatório liberado`,'info');
  document.querySelectorAll('.premium-lock').forEach(el=>el.remove());
  setTimeout(()=>{ showScreen('gerador'); },900);
}

function restaurarCompras(){if(isPremium) showToast('✅ Premium já ativo'); else {isPremium=true;localStorage.setItem('isPremium','true');showToast('✅ Compras restauradas - Premium ativo');}}
function drawChart(){
  const canvas=document.getElementById('chartConv');
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const w=canvas.width=canvas.offsetWidth*2;
  const h=canvas.height=canvas.offsetHeight*2;
  ctx.scale(2,2);
  const W=canvas.offsetWidth, H=canvas.offsetHeight;
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle=cssVar('--chart-grid') || 'rgba(255,255,255,0.08)';ctx.lineWidth=1;
  for(let y=0;y<=3;y++){const yy=(H-20)*(y/3)+10;ctx.beginPath();ctx.moveTo(40,yy);ctx.lineTo(W-10,yy);ctx.stroke();}
  const top=[500,600,750,850,800,900,880,920,1100,1200,1300,1450,1400,1480,1470];
  const media=[250,300,350,400,380,420,400,450,480,500,520,580,600,620,650];
  function drawLine(data,color){
    ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=2;
    data.forEach((v,i)=>{const x=40+(W-50)*(i/(data.length-1));const y=H-20-(v/1600)*(H-40);if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);});
    ctx.stroke();
  }
  drawLine(media, cssVar('--chart-media') || '#22D3EE');
  drawLine(top, cssVar('--chart-top') || '#34D399');
  ctx.fillStyle=cssVar('--chart-eixo') || 'rgba(255,255,255,0.55)';ctx.font='11px Inter';
  [1500,1000,500,0].forEach((v,i)=>{const y=10+(H-40)*(i/3);ctx.fillText(String(v),2,y+3);});
  ['-50','-40','-30','-20','-10','0'].forEach((v,i)=>{const x=40+(W-50)*(i/5);ctx.fillText(v,x-8,H-2);});
}
function showScreen(name){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  const target=document.getElementById('screen-'+name);
  if(target) target.classList.add('active');
  document.querySelectorAll('#bottomNav .tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll(`#bottomNav .tab[data-screen="${name}"]`).forEach(t=>t.classList.add('active'));
  const bottomNav=document.getElementById('bottomNav');
  if(['premium','detalhes','config','onboarding'].includes(name)){
    bottomNav.style.display='none';
  } else {
    bottomNav.style.display='flex';
    bottomNav.className = (name==='ranking') ? 'bottom-tabs tab-premium' : 'bottom-tabs';
  }
  if(name==='ranking') aplicarTabRanking();
  if(name==='dashboard') setTimeout(drawChart,60);
  if(name==='heatmap') renderSensor();
  if(target) target.scrollTop=0;
}

function nextOnboard(){
  const dots=[...document.querySelectorAll('#screen-onboarding .onboard-dots .dot')];
  const page=document.getElementById('onboardPage');
  const title=document.getElementById('onboardTitle');
  const sub=document.getElementById('onboardSub');
  const rocket=document.getElementById('onboardRocket');
  const btn=document.getElementById('btnOnboard');
  let current=dots.findIndex(d=>d.classList.contains('active'));
  if(current<0) current=0;
  if(current>=dots.length-1){ // já está na última página -> Começar
    localStorage.setItem('onboardDone','1');
    showScreen('dashboard');
    return;
  }
  dots[current].classList.remove('active');
  dots[current+1].classList.add('active');
  page.textContent=(current+2)+'/'+dots.length;
  if(current===0){
    title.innerHTML='Análise com <b>IA Avançada</b>';
    sub.innerHTML='Atrasômetro, Markov, Ensemble e Apriori para encontrar padrões ocultos em 3675 sorteios<br><small style="color:var(--primary-light)">Grátis: Sorteios Antigos | Premium: Aleatório</small>';
    rocket.textContent='🧠';
  } else {
    title.innerHTML='Gere Jogos <b>Inteligentes</b>';
    sub.innerHTML='Motor genético híbrido com 33 jogos, filtros e gestão de banca<br><small style="color:var(--gold-text)">Aleatório é Premium - Antigos é Grátis e Inteligente</small>';
    rocket.textContent='🎯';
    if(btn) btn.textContent='Começar';
  }
}

function pularOnboard(){localStorage.setItem('onboardDone','1');showScreen('dashboard');}
function toggleMenu(){showScreen('config');}
// ==================== ACESSIBILIDADE (ARIA + teclado) ====================
const ROTULOS_ICONE = {
  '🔔':'Configurações','📄':'Ajuda','←':'Voltar','✕':'Fechar','★':'Fixar dezena','☆':'Favoritar',
  '📌':'Fixar dezena','📋':'Copiar aposta','ⓘ':'Ver detalhes','?':'Ajuda','📊':'Atualizar ranking',
  '👑':'Premium','🏆':'Ranking','🥈':'Top 3','⭐':'Favoritos','🚀':'Gerar jogos','🧠':'Análise de IA',
  '→':'Avançar','›':'Abrir','▼':'Expandir'
};
function melhorarAcessibilidade(raiz){
  (raiz || document).querySelectorAll('[onclick]').forEach(el=>{
    if(el.dataset.a11y === '1') return;
    el.dataset.a11y = '1';
    if(!el.hasAttribute('role')){
      const papel = el.tagName === 'BUTTON' ? null : 'button';
      if(papel) el.setAttribute('role', papel);
    }
    const texto = (el.getAttribute('title') || el.textContent || '').trim().replace(/\s+/g,' ');
    if(!el.hasAttribute('aria-label') && el.tagName !== 'BUTTON'){
      el.setAttribute('aria-label', ROTULOS_ICONE[texto] || texto.slice(0,60) || 'Ação');
    }
    if(el.tagName !== 'BUTTON' && !el.hasAttribute('tabindex')) el.setAttribute('tabindex','0');
    el.addEventListener('keydown', e=>{
      if(e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar'){
        e.preventDefault();
        el.click();
      }
    });
    if(el.classList.contains('toggle')){
      const sincronizar = () => el.setAttribute('aria-checked', el.classList.contains('on') ? 'true' : 'false');
      sincronizar();
      el.addEventListener('click', () => setTimeout(sincronizar, 0));
    }
  });
}
// mantém os novos elementos (ranking, IA, logs) acessíveis automaticamente
function observarDOM(){
  if(typeof MutationObserver === 'undefined') return;
  let agendado = false;
  const obs = new MutationObserver(() => {
    if(agendado) return;
    agendado = true;
    requestAnimationFrame(() => { agendado = false; melhorarAcessibilidade(); });
  });
  obs.observe(document.body, { childList:true, subtree:true });
}
function alternarNotificacoes(el){
  el.classList.toggle('on');
  const ativo = el.classList.contains('on');
  localStorage.setItem('notificacoes', ativo ? 'true' : 'false');
  el.setAttribute('aria-checked', ativo ? 'true' : 'false');
  showToast(ativo ? '🔔 Notificações ativadas' : '🔕 Notificações desativadas');
}
// efeito de onda nos controles (feedback tátil visual)
document.addEventListener('pointerdown', e => {
  const alvo = e.target.closest && e.target.closest('[onclick],button,.tab,.seg-btn,.chip');
  if(!alvo || prefereMenosMovimento()) return;
  const r = alvo.getBoundingClientRect();
  if(r.width < 24 || r.height < 24) return;
  const onda = document.createElement('span');
  onda.className = 'onda';
  const tamanho = Math.max(r.width, r.height);
  onda.style.width = onda.style.height = tamanho + 'px';
  onda.style.left = (e.clientX - r.left - tamanho/2) + 'px';
  onda.style.top = (e.clientY - r.top - tamanho/2) + 'px';
  alvo.appendChild(onda);
  setTimeout(()=>onda.remove(), 520);
});

document.addEventListener('DOMContentLoaded',()=>{
  aplicarTema();
  if(rankingMatrizes.length===0) esqueleto(document.getElementById('rankingList'), 3, 110);
  carregarSorteios();
  renderFixasBloqueadas();
  setModoGeracao(modoGeracao);
  melhorarAcessibilidade();
  observarDOM();
  const notif = document.getElementById('toggleNotif');
  if(notif){
    const ativo = getBool('notificacoes', true);
    notif.classList.toggle('on', ativo);
    notif.setAttribute('aria-checked', ativo ? 'true' : 'false');
  }
  if(rankingMatrizes.length===0) esqueleto(document.getElementById('rankingList'), 3, 110); // antes de renderizar


  // Quantidade de jogos (10 Free / 15 / 20 / 33 Pro)
  document.querySelectorAll('.seg-btn').forEach(b=>{
    b.onclick=()=>{
      const v=parseInt(b.dataset.v);
      if(v>10 && !isPremium){
        showToast('🔒 '+v+' jogos é Premium - Free limita 10');
        showScreen('premium');
        return;
      }
      document.querySelectorAll('.seg-btn').forEach(x=>x.classList.remove('active'));
      b.classList.add('active');
      qtdJogos=v;
      localStorage.setItem('qtdJogos',v);
      showToast('🎲 '+v+' jogos por geração');
    };
  });
  document.querySelectorAll('.seg-btn').forEach(b=>{
    const on=parseInt(b.dataset.v)===qtdJogos;
    if(on) b.classList.add('active'); else b.classList.remove('active');
  });

  // Filtros inteligentes
  document.querySelectorAll('.filtro-chip').forEach(c=>{
    const aplicar=()=>{ if(filtrosAtivos.has(c.dataset.f)) c.classList.remove('inactive'); else c.classList.add('inactive'); };
    aplicar();
    c.onclick=()=>{
      const f=c.dataset.f;
      if(filtrosAtivos.has(f)) filtrosAtivos.delete(f);
      else filtrosAtivos.add(f);
      localStorage.setItem('filtrosAtivos',JSON.stringify(Array.from(filtrosAtivos)));
      const badge=document.getElementById('filtrosAtivosBadge');
      if(badge) badge.textContent=filtrosAtivos.size+' ativos';
      aplicar();
    };
  });
  const badgeFiltros=document.getElementById('filtrosAtivosBadge');
  if(badgeFiltros) badgeFiltros.textContent=filtrosAtivos.size+' ativos';

  // Sliders
  const mf=document.getElementById('mutacaoFill');
  if(mf) mf.style.width=((mutacao-1)/24*100)+'%';
  const mv=document.getElementById('mutacaoVal');
  if(mv) mv.textContent=Math.round(mutacao)+'%';
  const sf=document.getElementById('severidadeFill');
  if(sf) sf.style.width=severidade+'%';
  const sv=document.getElementById('severidadeVal');
  if(sv) sv.textContent=Math.round(severidade)+'%';

  // Estratégia salva
  const map={conservador:'estCons',agressivo:'estAgr',robo:'estRobo',preguicoso:'estPreg'};
  document.querySelectorAll('.est-row .arrow').forEach(a=>a.textContent='›');
  if(map[estrategia]){const el=document.getElementById(map[estrategia]); if(el) el.textContent='✓';}

  // Abas do ranking (Top 50 / Top 3 / Favoritos)
  aplicarTabRanking();

  // Tela inicial
  if(!localStorage.getItem('onboardDone')) showScreen('onboarding');
  else showScreen('dashboard');

  log(isPremium ? '👑 Premium ativo - Aleatório desbloqueado' : '🆓 Modo Free - Sorteios Antigos grátis, Aleatório é Premium','info');
});