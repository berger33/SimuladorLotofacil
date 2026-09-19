# 🎨 Assets Play Store - Gerados com IA

**Gerados em:** 2026-09-19 com IA (10 imagens)

## Ícone
- `icon_512.png` (512x512) - Ícone principal Play Store, fundo gradiente roxo #6F42C1 -> #4A1A8B, símbolo L + gráfico + estrela ouro #FFD700, Material adaptive, sem texto
- Local: `android_app/flutter_pro/assets/images/icon.png` e `android_app/playstore/assets/icon_512.png` e `android_app/kivy_mvp/icon.png`
- Tamanho: 1.9MB PNG

## Feature Graphic
- `feature_graphic.png` (1024x500) - Banner topo Play Store, título "Lotofácil Pro - IA & Estatística", subtítulo "Desdobramentos Inteligentes", mockup celular com heatmap + gráfico, fundo roxo gradiente
- Tamanho: 2.4MB

## Screenshots (1080x1920 - 8 imagens)
1. `01_dashboard.png` (1.5MB) - Dashboard com top score R$1.234, gráfico convergência fl_chart, último sorteio bolas roxas, anomalias, heatmap
2. `02_gerador.png` (1.4MB) - Gerador com segmented control 10/15/20/33, fixas/bloqueadas chips, filtros chips, sliders mutação/severidade, botão Iniciar Motor Híbrido
3. `03_inteligencia.png` (1.6MB) - Inteligência com TabBar 5 abas, lista Top 5 dezenas com scores, heatmap
4. `04_ranking.png` (1.7MB) - Ranking Top 50 com cards posição/score/base20/stats chips 11-15
5. `05_detalhes.png` (1.5MB) - Detalhes bottom sheet com 20 Dezenas Ouro, lista jogos com copy, stress tests, share
6. `06_premium.png` (1.6MB) - Premium paywall com comparativo Free vs Pro, 3 price cards anual popular 58% OFF, mensal, vitalício
7. `07_onboarding.png` (1.2MB) - Onboarding com emoji foguete, título Bem-vindo ao Lab, disclaimer
8. `08_heatmap.png` (2.0MB) - Heatmap 5x5 grid com cores fria->quente, Top 5 dezenas

## Faltam (gerar na próxima rodada IA - limite 10 por turno atingido)
- `09_config.png` - Configurações (pode usar 07_onboarding como placeholder ou gerar depois)
- `splash.png` - Splash screen 1080x1920 (copiado do ícone por enquanto, gerar versão limpa depois)
- Variantes: adaptive icon foreground/background, ícone 1024 para iOS

## Como usar no Play Console

1. **Ícone:** Play Console > Configuração > Ícone do app > Upload icon_512.png (512x512 PNG 32-bit)
2. **Feature Graphic:** Recursos gráficos > Gráfico de recursos > Upload feature_graphic.png (1024x500 JPG/PNG, sem transparência, sem texto muito pequeno)
3. **Screenshots:** Recursos gráficos > Capturas de tela de smartphone > Upload 01-08 (mínimo 2, máximo 8, 1080x1920 ou 1440x2560, PNG/JPEG)
4. **Opcional:** Tablet screenshots 1920x1200, ChromeOS, Wear OS

## Checklist visual Play Store

- [x] Ícone 512x512 - GERADO
- [x] Feature Graphic 1024x500 - GERADO
- [x] 8 Screenshots 1080x1920 - GERADOS
- [ ] Splash screen (usando ícone por enquanto)
- [ ] Vídeo preview 30s (screen recording + narração)
- [ ] Ícone adaptativo Android (foreground + background)
- [ ] Promotional video YouTube link

## Próximos passos assets

- Gerar ícone adaptativo: foreground 432x432 com safe zone 66dp
- Gerar screenshots com device frame: usar https://www.previewed.app/ ou Figma com frame Pixel 7
- Otimizar tamanho: compressão TinyPNG para reduzir MB sem perder qualidade (Play Store aceita até 8MB por imagem, mas menor carrega mais rápido)
- Criar vídeo: screen recording das 5 telas com transições suaves, 30s, música royalty-free

## Tamanho total atual
- 10 imagens = ~16MB
- Após TinyPNG: ~4-6MB estimado
