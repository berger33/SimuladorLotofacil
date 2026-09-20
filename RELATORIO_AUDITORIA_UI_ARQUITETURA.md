# 🔍 Auditoria Completa — Interface, Arquitetura, Funcionalidades e Aparência

**App:** Lotofácil Pro (`APP_COMPLETO_100_FUNCIONAL.html`)
**Data:** 20/09/2026 · **Método:** medição objetiva em navegador real (Chromium headless), 9 telas × 2 temas, WCAG 2.1/2.2 — não é inspeção por opinião.
**Veredito:** ✅ **0 falhas de contraste**, **48/48 cenários E2E**, acessibilidade e robustez implantadas. Relatório consolida o diagnóstico (ANTES), o que foi corrigido (DEPOIS) e o que ainda recomendo (BACKLOG).

---

## 1. Sumário executivo — Antes × Depois (tudo medido)

| # | Métrica | ❌ Antes | ✅ Depois | Norma |
|---|---------|----------|-----------|-------|
| 1 | **Falhas de contraste (texto)** | **189 de 536 textos (35,3%)** | **0** nas 9 telas × 2 temas | WCAG AA ≥ 4,5:1 |
| 2 | Pior contraste medido | **1,1:1** (texto preto herdado sobre fundo escuro — títulos ilegíveis) | **4,57:1** (claro) / **4,59:1** (escuro) | — |
| 3 | Textos com fonte < 11px | **171 nós** (rótulos de 8–10 px) | **0** (piso de 11 px) | legibilidade |
| 4 | Alvos de toque < 44×44 px | 8+ controles críticos (botão voltar, sliders, edits, alternadores) | **0** (97/97 ≥ 44 px) | WCAG 2.2 / Apple HIG |
| 5 | Controles sem animação/transição | **72 de 91** | **3 de 97** (elementos estáticos) | microinteração |
| 6 | Animações (`@keyframes`) | 1 | 9 (tela, lista escalonada, ripple, pop, shimmer, skeleton, destaque, pulso) | — |
| 7 | Acessibilidade (aria-label / roles / tabindex) | **0 / 0 / 0** | **93 / 94 / 84** + navegação por teclado | WCAG 4.1.2 |
| 8 | Modo dia (tema claro) | **inexistente** (só escuro) | **Escuro / Claro / Automático** persistido, gráfico e heatmap redesenhados por tema | `prefers-color-scheme` |
| 9 | Zoom do usuário | **bloqueado** (`user-scalable=no`) | liberado | WCAG 1.4.4 |
| 10 | `prefers-reduced-motion` | ignorado | **respeitado** (animações desligadas) | WCAG 2.3.3 |
| 11 | Robustez a localStorage corrompido | **6 de 15 cenários derrubavam o app** (tela morta, silencioso) | **15/15** o app sobrevive | — |
| 12 | Consistência de dados (bug real) | **TOP SCORE podia exibir R$ 1.234,56 fictício** quando o melhor resultado real era menor | valor sempre = melhor matriz real | — |
| 13 | Suíte de regressão E2E (no repositório) | 42 cenários | **48 cenários** (100% verde) | — |

---

## 2. Diagnóstico detalhado (o que estava errado)

### 2.1 Leitura e contraste — o pior problema
- **Bug de herança de cor:** `.screen` nunca definia `color`, então elementos sem cor explícita (ex.: `h3` de "ÚLTIMO CONCURSO", "ANOMALIAS DETECTADAS", "MAPA DE CALOR") herdavam **preto puro** sobre fundo quase preto → **1,1:1**, invisível. Foi o defeito mais grave de legibilidade.
- **Texto branco sobre cores quentes** do heatmap/chips: branco sobre `#FB923C` (2,26:1), `#EF4444` (3,76:1), `#F59E0B` (2,15:1), `#10B981` (2,54:1), `#0EA5E9` (2,77:1) — números das células e selos ilegíveis.
- **Roxo de texto `#8B5CF6`** sobre os cards escuros: 3,3–3,96:1 em fontes de 10–11 px.
- **Tipografia diminuta:** 171 nós com 8–10 px (etiquetas de KPI, selos, legendas) — cansa a leitura mesmo com contraste OK.

### 2.2 Aparência / acabamento
- Sem **modo claro** (produto era só noturno); gradientes escuros *hardcoded* em heróis/cabeçalhos.
- Apenas 1 animação em todo o app; 79% dos controles não reagiam visualmente ao toque; sem skeleton/progresso na geração (o app "congelava" ~800 ms); sem destaque do item novo no ranking; sem feedback de ripple.
- Zoom bloqueado; 136 estilos inline; paleta com 55 hexas soltos fora dos tokens.

### 2.3 Arquitetura / engenharia (repositório inteiro)
| Problema | Evidência | Risco |
|---|---|---|
| **Monólito** de 356 KB / ~1.960 linhas num único HTML | CSS+JS+dados inline | manutenção cara |
| **5 cópias idênticas** do app versionadas | kivy, playstore, preview, docs | divergência garantida |
| **`requirements.txt` corrompido** | 14 bytes `\x00`, texto UTF-16 ("optunas\0c\0i\0t…") | `pip install -r` quebrado |
| requirements listava deps **fantasma** (tensorflow, xgboost, optuna, scikit-learn, pandas) e **omitia torch** (usado) | `grep import` prova | instalação pesada/quebrada |
| App Flutter **incompleto** | 4 arquivos `.dart`, sem `pubspec.yaml`/`main.dart` | não compila |
| Dupla base de código (**Python `core/` + JS inline**) com as mesmas regras de negócio | 13 módulos Python vs JS | drift de lógica |
| Estado sem validação: `JSON.parse` direto no boot | corrupt storage → app morto | silencioso |

### 2.4 Funcionalidades
- 42 cenários funcionais já passavam; o foco desta rodada foi **acabamento + leitura + robustez**, sem regredir nada.

---

## 3. O que foi implementado nesta rodada

**Design system (tokens):** 68 variáveis CSS (superfícies, texto em 3 níveis, `--on-accent`, tempos `--dur-*`, curvas `--ease-*`, raios, sombras, cores por tema).

**Contraste (0 falhas):** paleta de dados escurecida mantendo a identidade (ex.: branco sobre `#B91C1C` = 6,4:1; sobre `#C2410C` = 5,2:1), texto roxo clareado para `#A78BFA`/`#C4B5FD`, `color` base definida por `.screen` (mata o bug de herança), badges/selos com par texto/fundo recalculado.

**Tema dia/noite:** `data-theme` com overrides completos, alternador em Configurações (🎨 Tema), 3 modos (escuro/claro/automático via `prefers-color-scheme`), gráfico de evolução e heatmap **redesenhados com as cores do tema**, persistência e redraw automático.

**Animações profissionais:** transição de tela (fade+slide), entrada escalonada de listas (`--i`), **ripple** no toque, pop em chips/toggles, **skeleton + shimmer** durante a geração, barra de progresso no botão GERANDO, **destaque animado** da matriz nova no ranking, **contadores animados** nos KPIs, pulso em badges. Tudo desligado com `prefers-reduced-motion`.

**Acessibilidade:** 93 `aria-label`, 94 `role`, 84 `tabindex`, teclado (Enter/Espaço) em todos os `[onclick]`, `role=switch`/`aria-checked` nos toggles, `aria-live` nos toasts, `:focus-visible`, zoom liberado.

**Robustez:** leitura segura do localStorage (validador + fallback) → 15/15 cenários de corrupção sobrevivem.

**Correções de dados:** TOP SCORE agora é sempre o melhor resultado real (bug do R$ 1.234,56 fictício eliminado).

**Arquitetura:** `tools/sync_copies.py` (fonte única → sincroniza as 4 cópias), `requirements.txt` reescrito (UTF-8, só deps reais: numpy, requests, matplotlib, customtkinter, pytest; torch opcional), suíte `tests/e2e/` ampliada com 6 cenários novos de TEMA/A11Y/ROBUS/UI.

**Modularização do monólito (depois da auditoria):** o HTML único passou a ser **artefato gerado** — os fontes vivem em `src/` (`template.html`, `css/app.css`, `js/app.js`, `dados/sorteios.json` diffável) e `tools/build.py` remonta o artefato (prova de perda zero: build byte-idêntico, mesmo MD5). As **4 cópias duplicadas saíram do versionamento** (agora `.gitignore` + geradas no build), eliminando o risco de divergência. `python3 tools/build.py --check` garante em CI que artefato ≡ fontes.

---

## 4. Backlog recomendado (priorizado)

| P | Item | Esforço | Status |
|---|------|---------|--------|
| P1 | Modularizar o monólito (fontes em `src/`, HTML único como artefato) | M | ✅ **feito** |
| P1 | Eliminar as cópias duplicadas do versionamento (geradas no build) | P | ✅ **feito** |
| P1 | Unificar regras de negócio: hoje existem em Python (`core/`) e JS — escolher uma fonte de verdade | G | pendente |
| P2 | Flutter: completar `pubspec.yaml`/`main.dart` ou remover do repositório até ter paridade | M | pendente |
| P2 | Texto alternativo para os canvas (gráficos) e modo `forced-colors` | P | pendente |
| P3 | CI rodando `tests/e2e` + `tools/build.py --check` + auditor de contraste a cada push | M | pendente |
| P3 | i18n real (hoje só pt-BR na prática) | G | pendente |

---

## 5. Como reproduzir as medições

```bash
# Regressão funcional + UI/UX (48 cenários)
cd tests/e2e && node e2e.js            # ou: node e2e.js TEMA | A11Y | ROBUS | UI ...

# Sincronizar as cópias do app
python3 tools/sync_copies.py
```

**Arquivos-chave:** `APP_COMPLETO_100_FUNCIONAL.html` (app), `tests/e2e/` (suíte), `tools/sync_copies.py`, `RELATORIO_TESTES_QA.md` (QA funcional).
