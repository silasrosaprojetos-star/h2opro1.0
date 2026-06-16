[app]
title = H2O Pro
package.name = h2opro
package.domain = org.silas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Bibliotecas necessárias (Kivy, KivyMD e Pyjnius para o Bluetooth)
requirements = python3,kivy,kivymd,jnius,android

orientation = portrait
fullscreen = 0

# Permissões exigidas pelo Android moderno para o HC-06
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_CONNECT, BLUETOOTH_SCAN, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# Configurações de API e travamento do NDK (A SOLUÇÃO DO ERRO)
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.accept_catch_all = True

[buildozer]
log_level = 2
warn_on_root = 1
