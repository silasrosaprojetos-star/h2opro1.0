[app]

title = H2O Pro
package.name = h2opro
package.domain = org.silasrosa

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = hostpython3==3.11.6,python3==3.11.6,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,certifi,chardet,idna,six,filetype

orientation = portrait
fullscreen = 0

android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
