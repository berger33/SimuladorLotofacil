# Kivy MVP - Lotofácil Pro

MVP rápido para validar mercado em 1 semana.

## Arquivos

- `main.py` - MVP mock, 5 telas, motor mockado, rápido para testar UI
- `main_real.py` - REAL com core_shared, motor genético de verdade, sorteios Caixa
- `buildozer.spec` - gera APK/AAB

## Rodar desktop

```bash
pip install kivy kivymd
python main.py
python main_real.py
```

## Gerar APK

Linux/WSL:
```bash
pip install buildozer cython
buildozer android debug
# bin/lotofacilpro-0.1-debug.apk
```

## Features

- ✅ 5 telas BottomNavigation: Dashboard, Gerador, IA, Ranking, Premium
- ✅ Dashboard: top score, geração, gráfico mock, anomalias, logs
- ✅ Gerador: qtd jogos, fixas, bloqueadas, filtros (ímpar, moldura, foco14, apriori), sliders mutação/severidade
- ✅ IA: atrasômetro, markov, ensemble com resultados reais (main_real)
- ✅ Ranking: lista matrizes geradas
- ✅ Premium: paywall mock

## Diferença mock vs real

- `main.py` - 100% mock, sem dependência, roda em qualquer lugar, geração fake rápida
- `main_real.py` - usa core_shared real, precisa 3675 sorteios, geração real com Sharpe, mais lento mas fiel ao desktop

## Próximos passos

- [ ] Adicionar AdMob banner/interstitial (plyer + kivmob)
- [ ] Salvar ranking em JSON local (já faz em memória, precisa persistir)
- [ ] Export CSV
- [ ] Compartilhar WhatsApp via plyer
- [ ] Tema claro/escuro
- [ ] Buildozer AAB release assinado
