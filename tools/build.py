#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build do app — gera o HTML único de distribuição a partir dos fontes modulares.

Fontes (edite aqui):
    src/template.html        casca HTML (com placeholders @@CSS@@, @@DADOS@@, @@APP@@)
    src/css/app.css          estilos
    src/js/app.js            lógica do app
    src/dados/sorteios.json  histórico de sorteios (1 por linha, diffável)

Artefatos gerados (NÃO editar à mão):
    APP_COMPLETO_100_FUNCIONAL.html                      (canônico, versionado)
    PREVIEW_100_PORCENTO_IDENTICO.html                   (gerada; fora do git)
    android_app/kivy_mvp/app_final_100_identico.html     (gerada; fora do git)
    android_app/playstore/assets/APP_FINAL_100_IDENTICO.html (gerada; fora do git)
    docs/app_preview.html                                (gerada; fora do git)

Uso:
    python3 tools/build.py            # gera o canônico e sincroniza as cópias
    python3 tools/build.py --check    # CI: falha se o canônico estiver desatualizado
"""
import hashlib
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ / 'src'
TEMPLATE = SRC / 'template.html'
CSS = SRC / 'css' / 'app.css'
APP_JS = SRC / 'js' / 'app.js'
DADOS = SRC / 'dados' / 'sorteios.json'
CANONICO = RAIZ / 'APP_COMPLETO_100_FUNCIONAL.html'

sys.path.insert(0, str(RAIZ / 'tools'))
import sync_copies  # noqa: E402  (fonte única da lista de cópias)


def gerar_html() -> str:
    """Monta o HTML único a partir dos fontes modulares."""
    for f in (TEMPLATE, CSS, APP_JS, DADOS):
        if not f.exists():
            sys.exit(f'[erro] fonte não encontrada: {f.relative_to(RAIZ)}')

    sorteios = json.loads(DADOS.read_text(encoding='utf-8'))
    assert all(len(s) == 15 and all(1 <= n <= 25 for n in s) for s in sorteios), \
        'sorteios.json inválido (cada sorteio deve ter 15 dezenas de 1 a 25)'

    dados_js = ('const SORTEIOS_EMBEDDED = ['
                + ', '.join('[' + ', '.join(map(str, s)) + ']' for s in sorteios)
                + '];')

    tpl = TEMPLATE.read_text(encoding='utf-8')
    html = (tpl
            .replace('@@CSS@@', CSS.read_text(encoding='utf-8'))
            .replace('@@DADOS@@', dados_js)
            .replace('@@APP@@', APP_JS.read_text(encoding='utf-8')))
    if '@@' in html:
        sys.exit('[erro] placeholder não substituído no template')
    return html


def main() -> None:
    verificar = '--check' in sys.argv
    html = gerar_html()
    md5 = hashlib.md5(html.encode('utf-8')).hexdigest()

    if verificar:
        if not CANONICO.exists() or CANONICO.read_text(encoding='utf-8') != html:
            sys.exit('[falha] canônico desatualizado — rode: python3 tools/build.py')
        print(f'[ok] canônico atualizado ({md5})')
        sync_copies.main()
        return

    CANONICO.write_text(html, encoding='utf-8')
    print(f'[build] {CANONICO.name}: {len(html)} chars ({md5})')
    sync_copies.main()  # regenera as 4 cópias (artefatos fora do git)


if __name__ == '__main__':
    main()
