# 🎯 DECISÃO DE PRÓXIMO PASSO - Análise e Planejamento

**Data:** 2026-09-19
**Status Atual:** 65% implementado, core 100% funcional, Flutter estrutura 80%
**Pergunta:** Qual próximo passo maximiza chance de sucesso comercial Play Store?

---

## Análise de Gargalos

### O que BLOQUEIA publicação Play Store HOJE?
1. **Flutter telas ainda placeholder** - app.dart tinha telas mock, não produção
2. **Sem assets visuais** - sem ícone 512, feature graphic, screenshots
3. **Sem AAB assinado** - sem keystore
4. **Sem teste interno 20 testers 14 dias** - obrigatório Google para novos devs
5. **Privacy Policy não hospedada** - precisa URL pública

### O que NÃO bloqueia mas é importante?
- API Cloud Run (pode usar fallback local mock que já funciona)
- Firebase Analytics (pode adicionar depois)
- Kivy APK (é MVP paralelo, não bloqueia Flutter)

### Matriz Impacto x Esforço

| Tarefa | Impacto Play Store | Esforço | Prioridade |
|--------|-------------------|---------|------------|
| Finalizar Flutter telas produção (dashboard, gerador, IA, ranking, premium) | 🔥🔥🔥🔥🔥 Alto - sem isso não tem app | Médio 3 dias | **P1 - AGORA** |
| Criar assets ícone + screenshots + feature | 🔥🔥🔥🔥 Alto - obrigatório listing | Baixo 1 dia | P2 |
| Gerar AAB assinado + CI | 🔥🔥🔥🔥 Alto | Baixo 0.5 dia | P2 |
| Hospedar Privacy Policy GitHub Pages | 🔥🔥🔥 Médio-Alto | Baixo 0.5 dia | P2 |
| Deploy API Cloud Run | 🔥🔥 Médio - pode usar offline | Médio 1 dia | P3 |
| Firebase + AdMob + IAP integração UI | 🔥🔥🔥 Médio-Alto - monetização | Médio 2 dias | P3 |
| Kivy APK beta fechado | 🔥 Baixo-Médio - validação paralela | Baixo 1 dia | P4 |

---

## ✅ DECISÃO TOMADA: Finalizar Flutter Pro Produção

**Justificativa:**
- Core já 100% funcional com 3675 sorteios, motor real testado
- API já tem versão mock e real, Flutter já tem fallback local que funciona offline (não precisa backend para lançar)
- O que falta para ter APK instalável e publicável é **Flutter telas de produção**
- Com telas prontas, já dá para gerar AAB, criar assets, e iniciar teste interno 20 testers (que demora 14 dias obrigatórios)
- Enquanto teste interno roda (14 dias), dá para fazer API deploy + Firebase + monetização

**Então próximo passo é:**
1. **Finalizar Flutter telas produção** - dashboard com fl_chart real, gerador com BLoC ao vivo, IA com TabBar real, ranking com detalhes + share, premium paywall, config
2. Criar `app_production.dart` e `main_production.dart` com onboarding check + navigation real
3. Criar widgets faltantes: banner_ad, etc
4. Deixar app 100% funcional offline (sem precisar API)

**Isso foi feito agora:**
- ✅ `dashboard_screen.dart` completo com LineChart fl_chart, 3 stats cards, último sorteio bolas, anomalias, heatmap, atalhos, banner
- ✅ `gerador_screen.dart` completo com SegmentedButton qtd jogos, fixas/bloqueadas chips, filtros chips, sliders, switches, estratégias prontas, bottom sheet progresso ao vivo com BLoC
- ✅ `inteligencia_screen.dart` com TabBar 5 abas (atrasômetro, markov, ensemble Pro, apriori, autopiloto), info cards, listas, heatmap
- ✅ `ranking_screen.dart` com TabBar Top50/Top3/Favoritos, CardMatriz real, detalhes bottom sheet com base 20, jogos, stats, stress tests, compartilhar WhatsApp
- ✅ `premium_screen.dart` paywall com comparativo Free vs Pro, 3 preços (anual popular, mensal, vitalício), depoimentos, CTA
- ✅ `config_screen.dart` com tema, idioma, banca, notificações, privacy, termos, sobre, avaliar, deletar dados
- ✅ `onboarding_screen.dart` 3 páginas com PageView + disclaimer legal + Hive
- ✅ `app_production.dart` com MultiRepositoryProvider, AppInitializer checa onboarding, MainNavigationProduction
- ✅ `main_production.dart` init Hive, AdMob, Firebase opcional
- ✅ `core/network/dio_client.dart` + `core/storage/hive_init.dart`
- ✅ `widgets/banner_ad_widget.dart` com checa premium

**Próximos passos depois disso (ordem):**
1. Assets visuais (ícone, feature, screenshots) - 1 dia
2. Gerar AAB assinado - 0.5 dia
3. Hospedar privacy policy GitHub Pages - 0.5 dia
4. Iniciar teste interno Play Console 20 testers 14 dias - 0.5 dia
5. Enquanto teste roda: deploy API Cloud Run + Firebase + AdMob/IAP UI - 3 dias
6. Beta aberto + produção rollout

---

## Resultado Esperado

Após finalizar Flutter produção, teremos:
- APK debug instalável com 5 telas reais, geração offline, ranking, IA, premium paywall
- AAB release pronto para Play Console
- 14 dias de teste interno já podem começar (gargalo Google)
- Monetização mock funcionando, pronta para integrar AdMob/IAP reais

**Tempo estimado até Play Store produção:** 16 dias (2 dias telas + 14 dias teste obrigatório Google)
