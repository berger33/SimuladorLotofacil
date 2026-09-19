# Screenshots Play Store

## 9 Screenshots 1080x1920 gerados com IA

1. **01_dashboard.png** - Dashboard com Top Score R$1.234, gráfico fl_chart convergência Top vs Média, último sorteio bolas roxas, anomalias, heatmap 5x5
2. **02_gerador.png** - Gerador com segmented control 10/15/20/33, fixas/bloqueadas chips, filtros chips (ímpar, moldura, primos, foco14), sliders mutação/severidade, botão Iniciar Motor Híbrido
3. **03_inteligencia.png** - Inteligência com TabBar 5 abas (atrasômetro, markov, ensemble, apriori, autopiloto), lista Top 5 dezenas scores, heatmap
4. **04_ranking.png** - Ranking Top 50 com cards posição/score/base20/stats chips 11-15
5. **05_detalhes.png** - Detalhes bottom sheet com 20 Dezenas Ouro, lista jogos com copy, stress tests histórico/caos, share WhatsApp
6. **06_premium.png** - Premium paywall com comparativo Free vs Pro, 3 price cards anual popular 58% OFF com trial, mensal, vitalício
7. **07_onboarding.png** - Onboarding com emoji foguete 80px, título Bem-vindo ao Lab, disclaimer +18
8. **08_heatmap.png** - Heatmap 5x5 grid fria→quente, Top 5 dezenas
9. **09_config.png** - Configurações com tema, idioma, banca, notificações, premium, privacy, deletar dados

## Como tirar screenshots reais do app (recomendado para produção)

Screenshots IA são ótimas para MVP e teste interno, mas para produção final, tirar screenshots reais do app Flutter rodando:

```bash
cd android_app/flutter_pro
flutter run -d <device_id>
# Navegar para cada tela e tirar screenshot:
# Android: Power + Volume Down
# Ou
adb exec-out screencap -p > screenshot.png

# Ou usar Fastlane Screengrab para automatizar
cd android
fastlane screenshots
```

## Device Frame (deixar mais profissional)

Usar https://www.previewed.app/ ou Figma com frame Pixel 7, iPhone, etc.

- Upload screenshot 1080x1920
- Escolher frame Pixel 7 Pro, cor preta
- Background gradiente roxo #6F42C1 → #4A1A8B
- Exportar com frame

## Otimização

```bash
cd android_app
./scripts/optimize_images.sh      # TinyPNG ou pngquant
./scripts/convert_webp.sh         # PNG → WebP ~30% menor
```

## Upload Play Console

Play Console > Seu app > Crescimento > Recursos gráficos > Capturas de tela de smartphone

- Mínimo 2, máximo 8 para phone
- 1080x1920 ou 1440x2560, PNG/JPEG/WebP, até 8MB cada
- Recomendado: usar 01-08 (8 screenshots) + 09_config como bônus se couber

## Ordem recomendada upload

1. 01_dashboard - mais impactante, mostra valor
2. 02_gerador - mostra funcionalidade principal
3. 03_inteligencia - diferencial IA
4. 04_ranking - prova social
5. 06_premium - monetização (mostra que tem Pro)
6. 05_detalhes - detalhes técnicos
7. 07_onboarding - bem-vindo
8. 08_heatmap - visual bonito

## Vídeo Preview

- Usar `../video_preview/create_video.sh` para gerar vídeo 30s a partir desses screenshots com Ken Burns zoom
- Upload YouTube não listado + link no Play Console > Vídeo de prévia
