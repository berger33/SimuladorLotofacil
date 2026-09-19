# Flutter Pro - Lotofácil Pro

Versão campeã para Play Store.

## Estrutura
```
lib/
  main.dart - init Hive, Firebase, AdMob
  app.dart - Material 3 + 5 telas placeholder (Dashboard, Gerador, IA, Ranking, Premium)
  core/
    constants/ - colors.dart, strings.dart
    theme/ - app_theme.dart
    utils/ - helpers
    network/ - dio
    storage/ - hive
  data/
    datasources/ - local (Hive) + remote (Dio)
    models/ - matriz_model.dart
    repositories/ - matriz_repository_impl.dart (com fallback local mock)
  domain/
    entities/ - matriz.dart
    repositories/ - interfaces
    usecases/ - gerar_matriz.dart
  presentation/
    screens/
      onboarding/ - onboarding_screen.dart (3 páginas + disclaimer)
      dashboard/ - futuro
      gerador/ - futuro
      inteligencia/ - futuro
      ranking/ - futuro
      premium/ - futuro
    widgets/ - heatmap_widget.dart, card_matriz.dart
    blocs/ - gerador_bloc.dart (com AdMob + IAP check)
  services/ - ads_service.dart, iap_service.dart
```

## Rodar
```bash
flutter pub get
flutter run
```

## O que já está pronto
- ✅ Design system Material 3 com cores roxo/ciano/ouro
- ✅ Theme dark/light
- ✅ Models e entities tipadas
- ✅ Repository pattern com local Hive + remote Dio + fallback mock
- ✅ UseCases com validação freemium
- ✅ BLoC Gerador com AdMob interstitial check + IAP premium check
- ✅ Services AdMob (banner, interstitial, rewarded) e IAP (monthly/yearly/lifetime)
- ✅ Widgets: heatmap 5x5 animado, card_matriz com stats
- ✅ Onboarding 3 telas com disclaimer legal
- ✅ Android build.gradle e AndroidManifest com permissões mínimas + AdMob App ID

## Falta implementar (próximos passos)
- [ ] Telas completas: dashboard com fl_chart, gerador com inputs reais, inteligencia com TabBar, ranking com lista + detalhes, premium paywall
- [ ] Blocs para cada tela (inteligencia_bloc, ranking_bloc)
- [ ] Integração Firebase Analytics + Crashlytics
- [ ] Testes widget + integration
- [ ] Ícone e splash
- [ ] Conectar com API real (main_real.py)

## Diferença mock vs real
- Atualmente repository_impl usa `_gerarLocalMock` se remote falha
- Quando API Cloud Run estiver no ar, trocar baseUrl e implementar SSE stream
