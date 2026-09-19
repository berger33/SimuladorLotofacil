# 📱 Android App - Lotofácil Pro

Esta pasta contém a transformação do Simulador Lotofácil Pro Desktop para App Android Comercial.

## Estrutura

```
android_app/
  README.md (este arquivo)
  ROADMAP.md - roadmap detalhado 8 semanas
  core_shared/ - core puro desacoplado (Python)
    domain/
    engine/
    ml/
    data/
    utils/
  kivy_mvp/ - MVP rápido com KivyMD + Buildozer (Semana 1-2)
    main.py
    buildozer.spec
    kivymd_ui/
  flutter_pro/ - Versão campeã Flutter + FastAPI (Semana 3-8)
    lib/
    android/
    pubspec.yaml
    README_FLUTTER.md
  api/ - FastAPI backend
    main.py
    routers/
    services/
  playstore/
    privacy_policy.md
    listing/
    assets/
  monetization/
    admob_config.md
    iap_config.md
```

## Como rodar cada versão

### Kivy MVP (Rápido)
```bash
cd android_app/kivy_mvp
pip install kivy kivymd buildozer numpy pandas requests
python main.py  # testa desktop

# Gerar APK (Linux ou WSL)
buildozer android debug
# APK em bin/
```

### Flutter Pro
```bash
cd android_app/flutter_pro
flutter pub get
flutter run

# Build AAB
flutter build appbundle --release
```

### API Backend
```bash
cd android_app/api
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8000
# Docs em http://localhost:8000/docs
```

## Decisão Arquitetural

- **MVP Kivy:** Para validar mercado em 1 semana, reaproveita 90% Python, APK ~80MB
- **Flutter Pro:** Para Play Store campeão, APK ~40MB, UI Material 3, monetização completa

Recomendado: Lançar Kivy como beta fechado enquanto desenvolve Flutter.

## Próximos Passos

Ver `ROADMAP.md` e `docs/PLANO_APP_ANDROID.md` na raiz.
