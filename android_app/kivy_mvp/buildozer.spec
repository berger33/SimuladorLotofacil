[app]
title = Lotofácil Pro
package.name = lotofacilpro
package.domain = com.berger33.lotofacilpro.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,webp
source.include_patterns = assets/*,images/*,core_shared/*
source.exclude_exts = spec,md,log
source.exclude_dirs = tests, bin, venv, __pycache__, .git, .github, docs, flutter_pro, api, playstore, scripts
source.exclude_patterns = tests/*,docs/*
version = 1.0.0
version.regex = __version__ = ['"]([^'"]*)['"]
version.filename = %(source.dir)s/main.py
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,numpy,requests,python-dateutil
icon.filename = %(source.dir)s/icon.png
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

# Android
[app:android]
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b
android.accept_sdk_license_agreements = True
android.ant_path = 
p4a.bootstrap = sdl2
p4a.arch = arm64-v8a
android.release_artifact = aab
android.debug_artifact = apk
p4a.download_retries = 5
p4a.branch = master
p4a.fork = kivy
