[app]
title = H2O Pro
package.name = h2opro
package.domain = org.silas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,kivymd,jnius,android

orientation = portrait
fullscreen = 0

android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_CONNECT, BLUETOOTH_SCAN, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

android.api = 33
android.minapi = 24
android.ndk = 25b

# Alterado para incluir as duas arquiteturas e resolver conflitos de bibliotecas
android.archs = armeabi-v7a, arm64-v8a

android.add_gradle_dependencies = True
android.gradle_dependencies = 
android.allow_backup = True
android.accept_catch_all = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
