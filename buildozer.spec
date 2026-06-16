[app]
title = H2O Pro
package.name = h2opro
package.domain = org.silas
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivymd,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 24
android.ndk = 25b
# Focando apenas em uma arquitetura para economizar RAM
android.archs = arm64-v8a
android.gradle_dependencies = 
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 1
warn_on_root = 1
