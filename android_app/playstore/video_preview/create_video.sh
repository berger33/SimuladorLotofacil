#!/bin/bash
# Cria vídeo preview 30s a partir de screenshots com ffmpeg

set -e

SCREENSHOTS_DIR="../assets/screenshots"
OUTPUT="video_preview_30s.mp4"
MUSIC="music.mp3" # colocar música royalty-free aqui

echo "🎬 Criando vídeo preview Lotofácil Pro..."

# Verifica ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg não encontrado. Instalar: sudo apt install ffmpeg"
    exit 1
fi

# Verifica screenshots
if [ ! -d "$SCREENSHOTS_DIR" ]; then
    echo "❌ Screenshots não encontradas em $SCREENSHOTS_DIR"
    exit 1
fi

# Lista screenshots em ordem
echo "📸 Screenshots encontradas:"
ls -1 $SCREENSHOTS_DIR/*.png | sort

# Cria vídeo slideshow com zoompan (Ken Burns)
# Cada imagem 3 segundos, total ~27s para 9 imagens
ffmpeg -y -framerate 1/3 -pattern_type glob -i "$SCREENSHOTS_DIR/*.png" \
  -c:v libx264 -r 30 -pix_fmt yuv420p \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=#121212,zoompan=d=1:s=1080x1920:fps=1/3" \
  -t 27 \
  temp_video.mp4

# Se tem música, adiciona
if [ -f "$MUSIC" ]; then
    echo "🎵 Adicionando música..."
    ffmpeg -y -i temp_video.mp4 -i "$MUSIC" -c:v copy -c:a aac -shortest -t 30 "$OUTPUT"
else
    echo "⚠️ Sem música, usando vídeo silencioso"
    # Adiciona 3s finais com logo
    ffmpeg -y -i temp_video.mp4 -vf "tpad=stop_mode=clone:stop_duration=3" -t 30 "$OUTPUT"
fi

# Limpa temp
rm -f temp_video.mp4

# Info
SIZE=$(du -h "$OUTPUT" | cut -f1)
echo "✅ Vídeo criado: $OUTPUT ($SIZE)"
echo "📤 Upload no YouTube não listado e link no Play Console > Recursos gráficos > Vídeo"

# Thumbnail
echo "🖼️ Criando thumbnail..."
ffmpeg -y -i "$OUTPUT" -ss 00:00:05 -vframes 1 thumbnail.png
echo "✅ Thumbnail: thumbnail.png"

echo ""
echo "Próximos passos:"
echo "1. Revisar $OUTPUT"
echo "2. Upload YouTube não listado"
echo "3. Play Console > Recursos gráficos > Vídeo de prévia > Adicionar YouTube link"
