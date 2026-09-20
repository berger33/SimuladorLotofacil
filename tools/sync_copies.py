#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincroniza as cópias do app a partir da fonte única de verdade.

Canônico : APP_COMPLETO_100_FUNCIONAL.html
Cópias   : PREVIEW_100_PORCENTO_IDENTICO.html
           android_app/kivy_mvp/app_final_100_identico.html
           android_app/playstore/assets/APP_FINAL_100_IDENTICO.html
           docs/app_preview.html

Uso:
    python3 tools/sync_copies.py            # sincroniza
    python3 tools/sync_copies.py --check    # apenas verifica (exit 1 se divergirem)
"""
import hashlib
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CANONICO = RAIZ / 'APP_COMPLETO_100_FUNCIONAL.html'
COPIAS = [
    RAIZ / 'PREVIEW_100_PORCENTO_IDENTICO.html',
    RAIZ / 'android_app/kivy_mvp/app_final_100_identico.html',
    RAIZ / 'android_app/playstore/assets/APP_FINAL_100_IDENTICO.html',
    RAIZ / 'docs/app_preview.html',
]


def hash_arquivo(caminho):
    return hashlib.md5(caminho.read_bytes()).hexdigest()


def main():
    verificar = '--check' in sys.argv
    if not CANONICO.exists():
        sys.exit(f'[erro] canônico não encontrado: {CANONICO}')
    conteudo = CANONICO.read_bytes()
    origem = hash_arquivo(CANONICO)
    print(f'canônico: {CANONICO.name} ({origem}) {len(conteudo)} bytes')
    divergentes, sincronizadas = [], []
    for copia in COPIAS:
        if copia.exists() and hash_arquivo(copia) == origem:
            sincronizadas.append(copia.name)
            print(f'  = já sincronizada: {copia.relative_to(RAIZ)}')
            continue
        if verificar:
            divergentes.append(str(copia.relative_to(RAIZ)))
            print(f'  ! divergente: {copia.relative_to(RAIZ)}')
            continue
        copia.parent.mkdir(parents=True, exist_ok=True)
        copia.write_bytes(conteudo)
        print(f'  → copiada para {copia.relative_to(RAIZ)}')
    if verificar and divergentes:
        sys.exit(f'[falha] {len(divergentes)} cópia(s) divergente(s): {", ".join(divergentes)}')
    print(f'ok: {len(COPIAS)} cópias conferidas ({len(sincronizadas)} já idênticas)')


if __name__ == '__main__':
    main()
