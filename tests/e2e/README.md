# Testes E2E — Lotofácil Pro (APP_COMPLETO_100_FUNCIONAL.html)

Suíte de testes **funcionais, regressivos e de fumaça** que simula um usuário real
navegando pelo app (Chromium headless via Playwright): clica, arrasta, digita,
recarrega, instala/limpa dados e confere cada tela contra os dados reais de
3675 concursos.

Resultado da última execução completa: **42 cenários / 319 verificações / 0 falhas**.

## Como rodar

```bash
# 1) dependências (uma vez)
npm i -D playwright-core
npx playwright install chromium        # ou informe CHROMIUM_PATH=/caminho/do/chrome

# 2) executar tudo
cd tests/e2e
node e2e.js

# 3) executar apenas uma área
node e2e.js NAV      # navegação
node e2e.js GER      # gerador (modo dual, fixas, filtros, sliders)
node e2e.js MOT      # motor de geração / ranking
node e2e.js IA       # atrasômetro, markov, ensemble, apriori, auto-piloto
node e2e.js RANK     # ranking, abas, favoritos
node e2e.js DET      # detalhes do jogo
node e2e.js PREM     # premium / paywall
node e2e.js HM       # heatmap sensorial
node e2e.js CFG      # configurações
node e2e.js UX       # toast, logs, persistência
node e2e.js MOB      # mobile 390x844 e 360x640
node e2e.js FUZZ     # clique em TODOS os botões de TODAS as telas
node e2e.js JORNADA  # jornada completa do usuário novo
```

Variáveis de ambiente:

| Variável | Descrição |
|---|---|
| `APP_FILE` | caminho do HTML a testar (padrão: `APP_COMPLETO_100_FUNCIONAL.html` da raiz) |
| `CHROMIUM_PATH` | binário do Chromium/Chrome quando não usar o do Playwright |

Saídas: `results.json` (evidências por cenário) e `screenshots/` (capturas).

## Áreas cobertas

| Área | Cenários | O que é verificado |
|---|---|---|
| BOOT | 2 | app abre sem erro de JS; as 52 funções públicas existem |
| ONB | 2 | onboarding 1/3→2/3→3/3, botão "Começar", "Pular", persistência |
| NAV | 3 | 5 abas inferiores, botões voltar, 12 navegações seguidas, acesso à tela de IA |
| DASH | 5 | top score, geração, 4 KPIs, gráfico canvas 2x, último concurso 3675, anomalias reais, heatmap 5x5, estatísticas |
| GER | 6 | modo dual (grátis × Premium), paywall de quantidade, fixas/bloqueadas com limites, edição por texto, 6 filtros, sliders, toggles, estratégias |
| MOT | 4 | geração real (10 e 33 jogos), validação de cada jogo, duplicatas, 3 gerações seguidas, config restritiva |
| IA | 2 | 5 modelos com Top5 real e textos distintos; heatmap da IA; ☆ fixa dezena |
| RANK | 3 | 8 matrizes iniciais, pódio, score/modo/base, abas Top50/Top3/Favoritos, favoritar, atualizar |
| DET | 2 | posição, score, ID, data, 20 dezenas, apostas reais, stats, copiar, stress test, caos, WhatsApp, privacidade |
| PREM | 3 | 7 linhas comparativas, 3 planos, trial, restaurar compras, desbloqueio efetivo, cadeado persistente |
| HM | 1 | grid 5x5 com gradiente, legenda, Top5 real, fixar todas, IA |
| CFG | 2 | 11 itens, banca validada, toggles, feedback de todos os clicáveis, deletar dados |
| UX | 3 | toast (posição/duração), log (timestamp, cores, auto-scroll), persistência completa |
| MOB | 2 | sem estouro horizontal, navegação e geração em telas pequenas |
| FUZZ | 1 | clica em todos os elementos com `onclick` de todas as telas sem erro e com reação |
| JORNADA | 1 | onboarding → IA → paywall → Premium → 33 jogos → ranking → detalhes → dashboard |

## Regras de validação aplicadas a cada jogo gerado

- exatamente 15 dezenas, inteiras, entre 01 e 25, sem repetição e ordenadas;
- todas as dezenas **fixas** presentes;
- nenhuma dezena **bloqueada** presente;
- filtros ativos respeitados (ímpares, moldura, primos, Foco 14, soma 180–200, Fibonacci);
- sem jogos duplicados dentro da mesma geração.
