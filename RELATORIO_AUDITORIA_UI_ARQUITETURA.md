# Auditoria de Interface, Arquitetura e Experiência — Lotofácil Pro

**Data:** 19/09/2026
**Escopo auditado:** `APP_COMPLETO_100_FUNCIONAL.html` (app único, aberto como `file://` no Chrome — uso real do usuário final)
**Método:** medição automatizada com navegador real (Chromium headless via Playwright) **clicando como usuário**, em viewport de celular (390×844 e 360×640), em **modo escuro e claro** — complementada por inspeção de código. Nada foi avaliado "no olho": todos os números abaixo são medidos.

---

## 1. Resumo executivo

| Área | Situação encontrada | Situação após as correções |
|---|---|---|
| **Contraste (WCAG AA)** | **189 de 536 textos reprovados (35,3%)** — havia título com texto **preto puro sobre fundo escuro (1,1:1)** | **0 falhas nas 9 telas × 2 temas** (pior caso 4,59:1 no escuro / 4,57:1 no claro) |
| **Modo dia/noite** | Não existia. Gradientes escuros "chumbados" no HTML quebravam qualquer tema claro | **3 modos (Escuro / Claro / Automático)**, persistidos, com gráfico e heatmap redesenhados nas cores do tema |
| **Legibilidade** | Piso de fonte **8–10 px** em **171 textos** (35% dos textos) | Piso de **11 px** + hierarquia tipográfica — **0 textos abaixo de 11 px** |
| **Alvos de toque** | 8 controles abaixo de 44 px (só na tela inicial) e sliders com 6 px de área real | **0 violações** em 97 controles interativos (97/97 ≥ 44 px) |
| **Feedback/animações** | 72 de 91 controles **sem** transição; **1** `@keyframes` em todo o app | **3 de 97** sem transição (só os que não devem animar); **9** animações; ripple, esqueleto, progresso, contador, stagger |
| **Acessibilidade** | **0** `aria-label`, **0** `role`, **0** `tabindex`; zoom **bloqueado** (`user-scalable=no`) | **93 labels / 94 roles / 84 tabindex**, foco visível, teclado (Enter/Espaço), `role=switch`, `aria-live`, zoom **liberado** |
| **Robustez de estado** | **6 de 15** cenários de `localStorage` corrompido quebravam o app (ranking ficava vazio) | **15/15** recuperados, com validação de tipos/tamanhos |
| **Dados exibidos** | TOP SCORE podia mostrar **R$ 1.234,56 fictício** (valor-semente) enquanto o melhor resultado real era menor | KPIs sempre derivados de resultado real; valor-semente eliminado |
| **Regressão funcional** | 24 defeitos funcionais já corrigidos na etapa anterior | **48 cenários / 359 verificações / 0 falhas** contra o arquivo final |

**Resultado:** 100% do app (9 telas, 2 temas) passou a cumprir contraste AA, com tema claro real, animações profissionais de interação, acessibilidade básica de teclado/leitor de tela e recuperação de dados corrompidos — sem perder nenhuma funcionalidade (a suíte de 42 cenários da etapa anterior foi ampliada para 48 e continua verde).

---

## 2. Diagnóstico detalhado (o que estava errado)

### 2.1 Cores e contraste

* **189 falhas** de contraste em **536 textos** medidos (35,3%).
* Casos graves: `<h3>` renderizado em **preto puro `rgb(0,0,0)` sobre `#1a1d29`** (razão ≈ **1,1:1**, exigido 4,5:1). Também cinzas `#6B7280` e `#4B5563` sobre fundos escuros, textos dourados `#F59E0B` sobre gradiente âmbar, e textos primários claros usados como texto (roxo `#8B5CF6` como cor de texto sobre azul).
* **Cores sem sistema:** 43 cores de fundo e 55 hexadecimais distintos espalhados pelo CSS, sem *design tokens*.
* **Modo claro inviável:** `.card-topscore`, `.card-ia`, `.ia-card` e `.premium-hero` tinham gradiente escuro em `style=""` dentro do próprio HTML — em tema claro o texto branco continuaria sobre fundo escuro e textos escuros sumiriam.

### 2.2 Legibilidade e acabamento

* **171 nós** de texto com fonte entre 8 e 10 px (rótulos, badges, legendas, chips) — abaixo do mínimo confortável em celular.
* Sem hierarquia: 320 textos em 11–12 px contra 68 em 18 px, sem escala definida.
* **Vazamento de layout no card de TOP SCORE**: o rótulo "GERAÇÃO ATUAL" e o selo "Em andamento" terminavam **exatamente na borda** do card (folga de 0 px do padding de 20 px), porque o valor `R$ …` usa `white-space:nowrap` e empurrava a coluna direita para fora da caixa de conteúdo em telas de 390 px. Corrigido com `min-width:0`/`flex:0 0 auto`/`gap` e uma faixa dedicada para telas ≤ 385 px (trophy e fontes reduzidos). Hoje: **0 elementos vazando contêiner** em 390 px e 360 px (verificado e agora coberto pela suíte).
* 237 atributos `style=""` inline, muitos fixando tamanho e cor fora do CSS.

### 2.3 Interação e animações

* **72 de 91** elementos clicáveis sem nenhuma transição — o app parecia "travado" mesmo funcionando.
* Nenhum feedback no gesto: sem efeito de toque (ripple), sem estado de carregamento no botão do motor, sem esqueleto enquanto o ranking carrega, sem destaque para a matriz recém-gerada.
* Nenhuma animação de transição entre as 9 telas; o KPI aparecia pronto, sem animação de contador.
* **Zoom bloqueado** (`maximum-scale=1.0, user-scalable=no`) — impedia o usuário com baixa visão de ampliar (falha WCAG 1.4.4).

### 2.4 Acessibilidade

* **0** `aria-label`, **0** `role`, **0** `tabindex`: leitor de tela lia apenas "div", botões sem nome, e **nenhum** controle era alcançável por teclado.
* Toasts/avisos não eram anunciados (sem `aria-live`).

### 2.5 Dados e robustez (auditoria de dados)

* **`localStorage` corrompido derrubava o app:** com `rankingMatrizes: "not-json"`, `fixas: "abc"` (texto), `banca: "-500"`, `qtdJogos: "muitos"` etc., **6 de 15 cenários** terminavam com ranking vazio/tela quebrada e erro no console.
* **Valor fictício exibido como dado real:** o TOP SCORE era inicializado com a constante `1234.56`. Quando o ranking inicial gerava um resultado menor (ex.: R$ 1.010,00), o painel exibia **R$ 1.234,56** e derivava `MÉDIA = 617,28` e `MÁXIMO = 1.234,56` desse número inventado. Corrigido: o KPI agora é sempre o melhor resultado **real** (era o caso mais sério encontrado nos dados).

---

## 3. O que foi implementado

### 3.1 Design System com tokens (fim das cores soltas)

* **68 variáveis CSS** (eram 24) centralizando cores, superfícies, bordas, raios, sombras, tempos e curvas de animação: `--dur-1..4`, `--ease`, `--red-soft`, `--success-text`, `--gold-text`, `--blue-text`, `--chip-11..15`.
* **Variantes de texto para AA**: onde a cor de marca (`--primary`, `--gold`, `--blue`) não alcançava 4,5:1, o texto passou a usar a variante clara correspondente — preservando a identidade visual.
* 522 regras CSS (eram 337), com nomes semânticos, e **piso de fonte de 11 px** aplicado globalmente.

### 3.2 Tema Escuro / Claro / Automático

* Botão em Configurações cicla **Escuro → Claro → Automático**, com descrição dinâmica ("Claro") e persistência (`localStorage.tema`).
* O **modo automático** segue o sistema (`prefers-color-scheme`).
* Os **4 blocos com gradiente escuro inline** foram substituídos por CSS que respeita o tema (no claro, superfície escura com texto branco coerente — nada de texto invisível).
* **Gráfico de convergência** e **heatmap** redesenhados a cada troca de tema (cores lidas dos tokens; medido: 11.743 pixels pintados no canvas no tema claro).
* `theme-color` do navegador acompanha o tema.

### 3.3 Interações e animações profissionais

| Efeito | Onde |
|---|---|
| **Onda no toque (ripple)** | todos os botões/controles clicáveis |
| **Transição de tela** (`telaIn`) | entrada das 9 telas |
| **Entrada escalonada** (`itemIn` + `--i`) | listas, cards, ranking |
| **Esqueleto de carregamento** (`skeleton` + shimmer) | ranking enquanto gera |
| **Estado "GERANDO…"** com **barra de progresso** e `aria-busy` | botão INICIAR MOTOR |
| **Contador animado** (`animarValor`) | TOP SCORE, MÉDIA, MÁXIMO, banca |
| **Destaque da matriz nova** (`rank-card--novo` + brilho) | ranking |
| **Pop / pulsar / subir de valor** | medalhas, chips, feedbacks |

  Medido: 94 de 97 controles com transição (3 sem, por escolha — elementos estáticos), 9 animações `@keyframes` (era 1).
  **`prefers-reduced-motion` respeitado**: com "reduzir movimento" ativo, transições caem para ~0 s e o valor é aplicado imediatamente (testado).

### 3.4 Acessibilidade

* `melhorarAcessibilidade()` + `MutationObserver` aplicam, a **todo elemento com `onclick`** (inclusive os criados dinamicamente): `role`, `aria-label` descritivo (ex.: *"Matriz 1º lugar, score R$ 1.040,00, modo antigos"*), `tabindex=0` e acionamento por **Enter/Espaço**.
* Toggles viram `role="switch"` com `aria-checked` sincronizado.
* Toasts com `role="status"` e `aria-live="polite"`.
* `:focus-visible` com anel de foco consistente; `lang="pt-BR"`; hierarquia de títulos corrigida (1 `h1`, sem saltos).
* **Zoom liberado** (viewport sem `maximum-scale`/`user-scalable=no`).
* Resultado medido: **93 `aria-label`, 94 `role`, 84 `tabindex`** (antes: 0/0/0) e **0 alvos de toque abaixo de 44 px**.

### 3.5 Robustez e integridade dos dados

* Funções de leitura segura: `getJSON`, `getBool`, `getNum`, `soDezenasValidas`, `matrizesValidas` — validam tipo, faixa e formato antes de usar.
* Estado validado na inicialização: `qtdJogos ∈ {10,15,20,33}`, estratégia em lista branca, banca ≥ 0, tema ∈ {escuro, claro, automático}, ranking saneado (item sem jogos é descartado).
* Suíte dedicada de **15 cenários de corrupção** → **15/15 recuperados**, 0 erros no console, ranking com 8 cards e heatmap 5×5 sempre renderizados.
* **TOP SCORE nunca mais fictício** (ver 2.5).

### 3.6 Testes automatizados (regressão)

A suíte E2E foi ampliada de 42 para **48 cenários / 360 verificações**, agora cobrindo também as novas áreas:

* `TEMA` — ciclo escuro/claro/automático, persistência, redesidnho do gráfico e **medição de contraste WCAG AA em runtime nas 9 telas nos 2 temas** (falha o teste se qualquer texto cair abaixo de 4,5:1).
* `A11Y` — rótulos/roles/tabindex, `aria-live`, zoom liberado, navegação por teclado, `role=switch`, alvos ≥ 44 px, e respeito a `prefers-reduced-motion` (com e sem a preferência).
* `ROBUS` — 15 casos de `localStorage` corrompido + geração de matriz funcionando depois da recuperação.
* `UI` — animação de tela, ripple, estado GERANDO + barra + esqueleto + `aria-busy`, destaque da matriz nova e limpeza do estado.
* `MOB` — ampliado com a checagem de que **nenhum conteúdo vaza do próprio contêiner** em 360 px.

**Resultado final: `TOTAL: 48 | PASSOU: 48 | FALHOU: 0`** (360 verificações ✅, 0 ❌), executado contra o arquivo `file://` final.

---

## 4. Arquitetura e engenharia — análise

### 4.1 Como está hoje

```
APP_COMPLETO_100_FUNCIONAL.html   354 KB — 1.944 linhas, CSS ~35 KB + 2 blocos <script>
├── 4 cópias espelho ...     (PREVIEW_100_PORCENTO_IDENTICO.html, android_app/kivy_mvp/…,
│                             android_app/playstore/assets/…, docs/app_preview.html)
├── tools/sync_copies.py    ← NOVO: sincroniza as 4 cópias a partir do canônico
├── tests/e2e/              ← NOVO: 48 cenários Playwright
├── app.py + ui/ + core/    app desktop Python (Tkinter/CustomTkinter) — base de código separada
└── android_app/flutter_pro projeto Flutter incompleto (4 .dart, sem pubspec.yaml/main.dart)
```

### 4.2 Pontos de melhoria identificados (prioridade)

| # | Achado | Risco | Recomendação |
|---|---|---|---|
| 1 | **App em arquivo único (monólito)**: 354 KB, 1.944 linhas, HTML+CSS+JS+237 estilos inline no mesmo arquivo | Manutenção cara, merge difícil, qualquer erro de sintaxe derruba tudo | Separar em `app.html + styles.css + app.js` **durante o desenvolvimento** e gerar o arquivo único por build (o requisito de "1 arquivo para o usuário" continua atendido) |
| 2 | **4 cópias duplicadas** do mesmo HTML versionadas | Divergência garantida (as cópias já estavam desatualizadas antes desta tarefa) | Automatizado com `tools/sync_copies.py` (modo `--check` para CI); ideal é **não versionar** as cópias e gerá-las no build |
| 3 | **Duas bases de código** (HTML/JS e Python desktop) com regras de negócio reimplementadas | Correção aplicada em uma não vale para a outra | Definir o HTML como referência e congelar/aposentar o desktop, **ou** extrair o núcleo (sorteios, score, filtros) para um arquivo de dados/regras compartilhado |
| 4 | **`requirements.txt` corrompido** (`optunas\0c\0i\0…` — mojibake com bytes nulos; falta `scikit-learn` legível) | `pip install -r` falha: o app desktop não instala | Reescrever o arquivo (UTF-8) com `optuna`, `scikit-learn`, `customtkinter`, `pandas`, `numpy`, `matplotlib`, `requests`, `xgboost`, `tensorflow`, `pytest`; adicionar `python_requires` |
| 5 | **Projeto Flutter incompleto**: nenhum `pubspec.yaml`/`main.dart`, 4 telas soltas e imports ausentes | Não é paridade com o app HTML, como sugere a documentação | Ou completar (pubspec, `main.dart`, `android/`, assets) ou remover a alegação de paridade da documentação até existir |
| 6 | **Sem CI**: nenhum workflow roda os testes | Regressão volta silenciosamente | GitHub Action rodando `tests/e2e` (Chromium já é instalável) + `tools/sync_copies.py --check` |
| 7 | Dados de sorteios vêm de `fetch` local com fallback sintético | Com cache ausente o app usa dados simulados sem sinalizar ao usuário | Marcar na UI quando estiver em modo simulado (o selo "educacional" já existe; falta indicar a origem dos dados) |
| 8 | Sem `Content-Security-Policy` / integridade | Distribuição em WebView/Play Store sem política de origem | Adicionar CSP no wrapper Android e assinar os ativos gerados |

### 4.3 Débitos intencionais (documentados, não corrigidos)

* **App desktop Python** e **projeto Flutter** não foram modificados nesta tarefa (fora do escopo do arquivo canônico) — as correções de UI valem para o HTML entregue.
* **Idioma**: o item "Idioma" em Configurações é apenas informativo (não há i18n real) — permanece como está, com feedback ao usuário.

---

## 5. Impacto medido (antes → depois)

Medições com o mesmo navegador, mesmo viewport e mesmos critérios:

| Indicador | Antes | Depois |
|---|---|---|
| Textos com contraste reprovado (AA) | **189** / 536 (35,3%) | **0** (9 telas × 2 temas) |
| Pior contraste medido | **1,1:1** | 4,59:1 (escuro) / 4,57:1 (claro) |
| Textos com fonte < 11 px | **171** | **0** |
| Controles abaixo de 44 px | **8** | **0** (de 97) |
| Conteúdo vazando do contêiner (390/360 px) | **1** (card TOP SCORE, folga 0 px) | **0** |
| Controles sem transição/animação | **72** / 91 | **3** / 97 |
| Animações (`@keyframes`) | **1** | **9** |
| `aria-label` / `role` / `tabindex` | **0 / 0 / 0** | **93 / 94 / 84** |
| Temas disponíveis | 1 (escuro fixo) | **3** (escuro, claro, automático) |
| Zoom do usuário | bloqueado | **liberado** |
| `localStorage` corrompido | **6/15 quebravam** | **15/15 recuperados** |
| TOP SCORE | podia exibir **R$ 1.234,56 fictício** | sempre o melhor resultado **real** |
| Cenários de regressão E2E | 42 | **48** (360 verificações, 0 falhas) |
| Tamanho do app | 323.346 bytes | 355.160 bytes (+9,8% — todo o design system, temas, animações e acessibilidade) |

---

## 6. Como reproduzir as medições

```bash
# abre o app como o usuário (arquivo local, sem servidor)
google-chrome APP_COMPLETO_100_FUNCIONAL.html

# regressão completa (48 cenários) — precisa de Chromium do Playwright
cd tests/e2e && node e2e.js

# auditoria de contraste/alvos/tipografia/ARIA (uma tela por vez, tema escolhido)
TEMA=claro node ui_audit.js

# manter as cópias espelho iguais ao canônico
python3 tools/sync_copies.py          # sincroniza
python3 tools/sync_copies.py --check  # falha se divergirem (uso em CI)
```

---

## 7. Arquivos alterados nesta auditoria

| Arquivo | O que mudou |
|---|---|
| `APP_COMPLETO_100_FUNCIONAL.html` | Design system, temas, animações, acessibilidade, robustez de estado, correção do TOP SCORE, alvos de toque |
| `PREVIEW_100_PORCENTO_IDENTICO.html` · `android_app/kivy_mvp/app_final_100_identico.html` · `android_app/playstore/assets/APP_FINAL_100_IDENTICO.html` · `docs/app_preview.html` | Sincronizadas com o canônico |
| `tests/e2e/e2e.js` | +6 cenários (TEMA, A11Y, ROBUS, UI), verificação de transbordo de layout e correções de assert (MOT-01, DASH, CFG-02) |
| `tools/sync_copies.py` | **Novo** — sincronização/verificação das 4 cópias |
| `RELATORIO_AUDITORIA_UI_ARQUITETURA.md` | **Novo** — este relatório |
| `RELATORIO_TESTES_QA.md` | Atualizado com a suíte de 48 cenários |
