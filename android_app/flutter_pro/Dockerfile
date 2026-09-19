# Dockerfile para build AAB 100% reproduzível - Lotofácil Pro
# Uso: docker build -t lotofacil-build . && docker run --rm -v $(pwd)/build:/app/build lotofacil-build

FROM cirrusci/flutter:stable

# Instalar dependências extras
RUN apt-get update && apt-get install -y \
    pngquant \
    webp \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar pubspec e baixar deps primeiro (cache layer)
COPY pubspec.yaml pubspec.lock ./
RUN flutter pub get

# Copiar resto do projeto
COPY . .

# Otimizar imagens se tiver API key
# ARG TINYPNG_API_KEY
# RUN if [ -n "$TINYPNG_API_KEY" ]; then ../scripts/optimize_images.sh; fi

# Build AAB release
RUN flutter build appbundle --release --no-tree-shake-icons

# Mostrar tamanho
RUN ls -lh build/app/outputs/bundle/release/app-release.aab && \
    echo "✅ AAB pronto para Play Store"

# O AAB estará em build/app/outputs/bundle/release/
