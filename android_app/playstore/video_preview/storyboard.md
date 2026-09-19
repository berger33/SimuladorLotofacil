# 🎬 Vídeo Preview 30s - Storyboard Lotofácil Pro

**Formato:** 1080x1920 (9:16 vertical) ou 1920x1080 (16:9 horizontal) - Play Store aceita ambos, vertical melhor para phone
**Duração:** 30 segundos
**Música:** Royalty-free upbeat tech (YouTube Audio Library - "Innovation" ou "Tech Talk")
**Narração:** Voz IA ou texto overlay (sem narração também funciona)

## Roteiro 30s

### 0-3s - Hook
- **Visual:** Splash screen com logo roxo + estrela dourada animada (Lottie)
- **Texto overlay:** "Lotofácil Pro" grande + "IA & Estatística"
- **Efeito:** Zoom in suave, partículas roxas
- **Música:** Começa beat

### 3-8s - Problema
- **Visual:** Pessoa olhando volante lotofácil confusa, depois dashboard com gráfico subindo
- **Texto:** "Cansado de jogar no escuro?"
- **Transição:** Slide left

### 8-15s - Solução - 3 features rápidas (2s cada)
- **8-10s - Algoritmo Genético:**
  - Visual: Tela Gerador com Qtd Jogos 33, animação de evolução G0→G42, score subindo R$0→R$380
  - Texto: "🧬 Algoritmo Genético evolui matrizes"
- **10-12s - IA:**
  - Visual: Tela Inteligência com TabBar, heatmap 5x5 animando cores fria→quente, Top 5 dezenas com estrelas
  - Texto: "🤖 6 IAs analisam 3675 sorteios"
- **12-15s - Fechamento:**
  - Visual: Tela Detalhes com base 20 ouro e lista 33 jogos, botão Compartilhar WhatsApp
  - Texto: "🎯 Desdobramento inteligente 20→15"

### 15-22s - Prova Social
- **Visual:** Ranking Top 50 com cards subindo, stress test resultado ROI 25%, confetti quando 14 pontos
- **Texto:** "📊 Testado contra histórico real"
- **Efeito:** Confetti Lottie quando 15 pontos

### 22-27s - Premium
- **Visual:** Tela Premium paywall com comparativo Free vs Pro, preços R$99/ano 58% OFF
- **Texto:** "👑 Pro: 33 jogos, IA completa, sem ads"
- **Efeito:** Badge "MAIS POPULAR" pulsa

### 27-30s - CTA
- **Visual:** Logo grande + botão Play Store + QR code
- **Texto:** "Baixe agora - Ferramenta educacional +18"
- **Disclaimer pequeno:** "Não garante prêmios. Jogue com responsabilidade."
- **Música:** Fade out

## Como gravar

### Opção 1: Screen Recording + Edição (Recomendado)
```bash
# Android device conectado
adb shell screenrecord /sdcard/lotofacil_demo.mp4 --time-limit 30
# Ou usar AZ Screen Recorder app

# Depois editar no CapCut, DaVinci Resolve, ou Premiere
# Adicionar textos overlay, música, transições
```

### Opção 2: Flutter Screenshot + Animação
- Usar screenshots 01-09 que já temos
- Criar slideshow com Ken Burns (zoom pan)
- Adicionar Lottie animações por cima
- Exportar com ffmpeg

### Opção 3: IA Video (Runway, Pika)
- Prompt: "App demo of lottery AI analysis tool, purple theme, charts, heatmap, smooth transitions"
- Mais rápido mas menos fiel ao app real

## Script ffmpeg para juntar screenshots em vídeo 30s

```bash
# Criar video a partir de screenshots com zoom
ffmpeg -framerate 1/3 -i android_app/playstore/assets/screenshots/%02d_*.png -c:v libx264 -r 30 -pix_fmt yuv420p -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,zoompan=d=1:s=1080x1920:fps=1/3" video_preview.mp4

# Adicionar música
ffmpeg -i video_preview.mp4 -i music.mp3 -c:v copy -c:a aac -shortest video_preview_music.mp4

# Cortar para 30s
ffmpeg -i video_preview_music.mp4 -t 30 video_preview_30s.mp4
```

## Checklist Play Store Vídeo

- [ ] Duração 30s-2min (recomendado 30-60s)
- [ ] Formato 16:9 ou 9:16, mínimo 1080p
- [ ] Sem promessa "ganhe dinheiro", usar "análise estatística"
- [ ] Mostrar app real, não mock genérico
- [ ] Incluir disclaimer +18 no final 3s
- [ ] Upload YouTube não listado, link no Play Console > Recursos gráficos > Vídeo de prévia
- [ ] Thumbnail atraente (usar feature graphic)

## Ferramentas

- **Gravação:** AZ Screen Recorder (Android), OBS (desktop emulator)
- **Edição:** CapCut (grátis, mobile/desktop), DaVinci Resolve (grátis pro)
- **Lottie:** LottieFiles.com - buscar "rocket", "chart", "confetti", "AI brain"
- **Música:** YouTube Audio Library, Uppbeat, Pixabay Music (royalty-free)
- **Voz IA:** ElevenLabs, Murf.ai para narração PT-BR

## Exemplo narração PT-BR (se usar voz)

> "Lotofácil Pro. Onde a matemática encontra a sorte. Algoritmo genético evolui matrizes, seis inteligências artificiais analisam milhares de sorteios, e o fechamento inteligente transforma 20 dezenas em 15 jogos. Testado contra histórico real, com ranking, heatmap e export. Baixe agora, ferramenta educacional, jogue com responsabilidade, mais dezoito."

## Entregável

- `video_preview_30s.mp4` 1080x1920 <100MB
- `video_preview_thumbnail.png` 1024x500
- YouTube link não listado
