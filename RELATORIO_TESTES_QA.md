# Relatório de QA — Lotofácil Pro (app HTML `APP_COMPLETO_100_FUNCIONAL.html`)

**Data:** 20/09/2026
**Escopo:** teste funcional, regressivo, de interface, de persistência, de responsividade (mobile) e varredura total de cliques — simulado como usuário real em navegador (Chromium headless).
**Resultado final:** **42 cenários / 319 verificações / 0 falhas.**

---

## 1. Resumo executivo

O sintoma relatado — *"tentei navegar entre os botões e não funcionou"* — tinha **uma causa única e total**:
um **erro de sintaxe JavaScript** que impedia o `<script>` inteiro de carregar. Como
consequência, **nenhuma função existia** na página: nenhum botão, aba, chip, slider ou
toast funcionava. O app exibia a interface "pintada", mas morta.

Além disso, a auditoria linha a linha do código revelou **17 defeitos funcionais**
adicionais (incluindo o motor que **não gerava nenhum jogo**, o onboarding que **não
avançava**, a tela de IA **inalcançável**, abas do ranking e botões "favoritar",
"ver todas as apostas", "stress test" e "caos" que **não faziam nada**) e um problema
de **desempenho grave** (o app levava mais de 2 minutos para ficar utilizável; agora
fica pronto em ~0,23 s).

Todos foram corrigidos, o app foi testado de ponta a ponta e está com **42 cenários
automatizados aprovados**, disponíveis em `tests/e2e/` para rodar a qualquer momento.

---

## 2. Causa raiz do "não funciona nenhum botão"

**Defeito #1 — CRÍTICO — erro de sintaxe em `renderAnomalias()`**

```js
// ANTES (linha com template literal inválido) — o parser abortava o script TODO:
`${i===0?'Intervalo longo sem: '+n:', '+Object.keys(dados).filter(k=>dados[k].atual>20).slice(0,3).join(', '):'Números em atraso: '+n}`
//            └─ abre um ternário sem fechar e ainda injeta  ', '  dentro da expressão de template
```

O erro reportado pelo navegador era `SyntaxError: Missing } in template expression`.
Como o script é carregado em um único bloco, **tudo** era descartado:

| Evidência | Antes | Depois |
|---|---|---|
| Erro no console | `SyntaxError: Missing } in template expression` | nenhum |
| `typeof showScreen` | `undefined` | `function` |
| Botões no HTML ligados a funções | 87 elementos `onclick` → **todos** geravam `ReferenceError` | 100% funcionando |
| Ranking inicial | nunca renderizado | 8 matrizes |

**Correção:** expressão corrigida para `${i===0?'Intervalo longo sem: '+n:'Números em atraso: '+n}`.
O arquivo foi replicado nas 4 cópias idênticas do repositório (mesmo MD5).

---

## 3. Defeitos encontrados e corrigidos

### Críticos

| # | Defeito | Sintoma para o usuário | Correção |
|---|---|---|---|
| 1 | Erro de sintaxe em `renderAnomalias` | **nenhum botão funcionava** | expressão corrigida |
| 2 | `nextOnboard()` usava `querySelectorAll('.dot')` — que também capturava os *dots* do gráfico/legenda (9 elementos em vez de 3) | botão **"Próximo" não avançava** (1/3 → travava); só "Pular" funcionava | escopo em `#screen-onboarding .onboard-dots .dot`, botão vira "Começar" na 3ª página e avanço explícito |
| 3 | Motor de geração **não produzia jogos**: `gerarJogoBaseadoEmAntigos` era determinístico (o mesmo jogo sempre) e esse jogo violava o filtro "Moldura" (11 dezenas > 10) → 500 tentativas idênticas e rejeitadas, × cálculo Markov 25×25 | clicar "INICIAR MOTOR HÍBRIDO" **não gerava nada**, sem erro, sem toast, sem log; ranking vazio | gerador estocástico ponderado (atraso + frequência + Markov + estratégia + sliders), **reparo local de filtros** por hill-climbing, cache das análises, dedupe e feedback explícito |
| 4 | Desempenho: cada tentativa recalculava atrasômetro + Markov + frequência; ranking inicial (8 matrizes) multiplicava isso | app levava **>120 s** para ficar utilizável (medido: nunca "pronto") | cache `iaDados()` validado por geração → **app pronto em ~0,23 s**, geração de 10 jogos em ~0,85 s |

### Altos

| # | Defeito | Sintoma | Correção |
|---|---|---|---|
| 5 | Tela **Inteligência (IA)** inalcançável (nenhum elemento chamava `showScreen('inteligencia')`) | usuário nunca chegava ao Atrasômetro/Markov/Ensemble/Apriori/Auto-Piloto | card "Lotofácil Pro Intelligence" no Dashboard + botão **←** na tela |
| 6 | `rodarIA()` removia a classe `active` de **todas** as abas da página e `showScreen` marcava abas `[data-screen]` de telas internas | estado visual inconsistente entre telas | escopo em `#bottomNav` e `#screen-inteligencia .bottom-tabs` |
| 7 | Abas do ranking **Top 50 / Top 3 / Favoritos** não filtravam nada (só toast) e `setRankingTab` dependia de `window.event` | clicar nas abas não mudava nada | filtros reais + estado persistido + `{this}` no HTML |
| 8 | Botão **☆ favoritar** não gravava nada | favorito "sumia" ao recarregar | persistência em `localStorage` + estado visual ★/☆ |
| 9 | Paywall do modo Aleatório: `showPremiumLock(); return []` no meio da geração + cadeado auto-removido em 5 s | usuário sem explicação do que aconteceu | toast + log + redirecionamento explícito; cadeado com `z-index` correto |
| 10 | `gerarSistema` podia entrar em *dead-end* silencioso | "nada acontece" ao gerar com filtros rigorosos | limite de tentativas com aviso, ajuste parcial avisado e mensagem de erro quando impossível |

### Médios

| # | Defeito | Correção |
|---|---|---|
| 11 | Filtros **Foco 14** e **Fibonacci** existiam na UI mas não eram aplicados (só moldura/primos/soma) | lógica real dos 6 filtros em `filtrarJogo` + reparo em `ajustarAosFiltros` |
| 12 | `editarFixas/editarBloqueadas` ignoravam os limites (6 fixas / 5 bloqueadas), aceitavam duplicatas e permitiam fixar dezena bloqueada | validação em **todos** os caminhos (clique, texto, heatmap, ★ da IA, "Fixar todas") |
| 13 | Sliders (mutação/severidade) com apenas **6 px** de altura clicável | área de toque ampliada para 34 px sem alterar o visual |
| 14 | Detalhes exibiam números **fictícios**: "Acertos 15 / 100%", "Rank de 1.842", "Aproveitamento 100%" | acertos = melhor resultado real nos últimos 100 concursos; rank real; aproveitamento calculado |
| 15 | "Ver todas as apostas" só mostrava toast; lista sempre limitada a 5 | alterna 5 ↔ todas com contador atualizado |
| 16 | **Stress Test** e **Teste Caos** eram `Math.random()` disfarçado de simulação | simulações reais sobre as apostas da matriz (1.000 e 300 sorteios), com log |
| 17 | `copiarAposta` só usava `navigator.clipboard` (indisponível em `file://`) | fallback com `textarea` + sempre com feedback ao usuário |
| 18 | Ranking inicial: 8 matrizes **idênticas**, não persistidas; `topScore` congelado no mock "1.234,56" (podendo ficar **menor** que o melhor score real) | matrizes distintas e persistidas; `topScore` = melhor matriz |
| 19 | KPIs do dashboard não sincronizados no boot ("Geração 41" com geração 42; MÁXIMO/ MÉDIA divergentes) e sem separador de milhar | `atualizarKPIs()` + `fmtMoeda()` pt-BR (`R$ 1.234,56`) |

### Baixos (acabamento)

| # | Defeito | Correção |
|---|---|---|
| 20 | 2 botões "hambúrguer" sem `onclick` (Gerador e Heatmap) | passam a abrir Configurações (todos os cabeçalhos respondem) |
| 21 | Logs com hora em formato en-US e sem limite | `toLocaleTimeString('pt-BR')`, auto-scroll garantido e limite de 300 linhas |
| 22 | Vários `setTimeout` de toast podiam esconder a mensagem nova antes da hora | *timer* único |
| 23 | `compartilharWhats` usava o ranking global, não a matriz aberta; sem feedback | usa a matriz aberta, inclui base 20 + jogos e confirma no toast |
| 24 | Edição de banca aceitava `abc`/negativos e não dava retorno | validação numérica (aceita `2.500` ou `2500,00`) + toast |
| 25 | Rótulos de IA sem acento (`ATRASOMETRO`, `AUTOPILOTO`) | `ATRASÔMETRO` / `AUTO-PILOTO` |

---

## 4. Cobertura de testes (o que foi verificado)

Suíte em `tests/e2e/e2e.js` — 42 cenários, 319 verificações. Cada jogo gerado é
validado de forma independente: **15 dezenas, sem repetição, 01–25, ordenado, fixas
presentes, bloqueadas ausentes, filtros respeitados e sem duplicatas**.

| Área | Cenários | Destaques verificados |
|---|---|---|
| BOOT | 2 | app abre sem erro de JS; **as 52 funções públicas existem** |
| ONB | 2 | 1/3 → 2/3 → 3/3 → Começar; Pular; persistência (`onboardDone`) |
| NAV | 3 | 5 abas inferiores com estado ativo; botões ←; 12 navegações seguidas; **acesso e volta da tela de IA** |
| DASH | 5 | top score coerente com a melhor matriz; 4 KPIs; canvas 2× retina com as 2 linhas (pixels/cores conferidos); **Concurso 3675 [02,03,05,06,09,10,11,13,14,16,18,20,23,24,25]**; anomalias "Atual X vs Média Y" com severidade; heatmap 5×5 com cores de frequência; estatísticas reais (mais/menos frequente, média de ímpares 7,8) |
| GER | 6 | modo dual (Antigos grátis × Aleatório Premium com cadeado); paywall 15/20/33; fixas/bloqueadas com limites e validações cruzadas; edição por texto; 6 filtros com contador e persistência; sliders (clique em 50% ⇒ ~13%), toggles e 4 estratégias |
| MOT | 4 | 10 jogos no modo grátis com score, logs e toast; 3 gerações seguidas (43→44→45) com ranking ordenado; 33 jogos no modo Aleatório após Premium; **configuração restritiva (6 fixas + 5 bloqueadas + 6 filtros) não trava e avisa** |
| IA | 2 | 5 modelos com Top5 real, textos distintos e aba ativa correta; heatmap da IA; ★ fixa a dezena sugerida |
| RANK | 3 | 8 matrizes, pódio gold/silver/bronze com coroas, score/modo/base 20, chips 11–15; **abas Top50/Top3/Favoritos funcionando**; favoritar; atualizar |
| DET | 2 | posição, score em R$, ID, data pt-BR, 20 dezenas de ouro, 5 apostas de 15 dezenas, stats reais; copiar, stress test, histórico, caos, WhatsApp (`wa.me`), privacidade, voltar |
| PREM | 3 | tabela de 7 linhas, 3 planos, 58% OFF, trial, restaurar compras; **compra desbloqueia o Aleatório e libera 33 jogos**; cadeado persiste para usuário Free |
| HM | 1 | grid 5×5 com gradiente, legenda de 4 faixas, Top5 real com frequência, "Fixar todas", card de IA |
| CFG | 2 | 11 itens, banca validada, toggles, feedback de todos os clicáveis, deletar dados (volta ao onboarding, modo grátis padrão) |
| UX | 3 | toast (texto, posição acima da barra, auto-hide em 3 s); log (timestamp pt-BR, 3 cores, auto-scroll); persistência completa após reload |
| MOB | 2 | 390×844 e 360×640 sem estouro horizontal, navegação e geração funcionando |
| FUZZ | 1 | **clique em todos os elementos `onclick` de todas as telas** sem erro e com reação visível |
| JORNADA | 1 | usuário novo: onboarding → IA → paywall → Premium → 33 jogos → ranking → detalhes → dashboard |

### Comparativo antes/depois

| Métrica | Antes | Depois |
|---|---|---|
| Cenários aprovados | 0 (script não carregava) | **42 / 42** |
| App utilizável (medido) | > 120 s (timeout) | **0,23 s** |
| Geração de 10 jogos | não gerava | **0,85 s** |
| Jogos por geração (grátis) | 0 | 10 válidos e distintos |
| Erros de JS em uso | 1 fatal + dezenas de `ReferenceError` | 0 |

---

## 5. Como executar os testes

```bash
npm i -D playwright-core && npx playwright install chromium
cd tests/e2e && node e2e.js            # tudo (≈5 min)
node e2e.js NAV                        # ou só uma área: NAV DASH GER MOT IA RANK DET PREM HM CFG UX MOB FUZZ JORNADA
```

Saídas: `tests/e2e/results.json` (evidência por cenário) e `tests/e2e/screenshots/`.

Para testar outro arquivo: `APP_FILE=/caminho/app.html node e2e.js`.

---

## 6. Observações e pendências (transparência)

1. **Projeto Flutter (`android_app/flutter_pro`) não é compilável no estado atual.** Ele contém
   apenas 4 arquivos `.dart` e **não possui** `pubspec.yaml`, `lib/main.dart`, pasta `android/`
   nem as dependências importadas (`data/datasources/local_datasource.dart`,
   `domain/usecases/gerar_matriz.dart`, `presentation/widgets/heatmap_widget.dart`, pacote `fl_chart`).
   Portanto, `cd android_app/flutter_pro && flutter build apk --debug` falha de imediato — não
   porque o Flutter tenha problema, mas porque o projeto está incompleto no repositório.
   O app **100% funcional e testado hoje é o HTML** (`APP_COMPLETO_100_FUNCIONAL.html`).
2. **Sem PWA/Service Worker:** "Adicionar à tela inicial" cria um atalho do Chrome, mas não há
   `manifest.json`/service worker (sem instalação offline real). Posso implementar se quiser.
3. **Data do último concurso** exibida no card ("18/05/2025") é estática no HTML; o número
   (3675) e as 15 dezenas vêm dos dados reais embarcados.
4. **Valores ilustrativos:** `Stress Test`/`Caos` agora rodam simulação real, mas o "score R$"
   é uma métrica interna do simulador (prêmios teóricos), não um valor oficial da Caixa.
5. Um valor em `detalhes` ("Apostas/Sub") e o seletor de período do gráfico
   ("Últimas 50 gerações") permanecem decorativos — não afetam nenhuma funcionalidade.
