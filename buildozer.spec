[app]

title = Кофе и Чай
package.name = brewbook
package.domain = org.brewbook

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav
source.include_patterns = app/data/*.json

version = 1.0.0

# Kivy + plyer (вибрация, выбор фото), android — для Intent «Поделиться»
requirements = python3,kivy==2.3.0,plyer,android

orientation = portrait
fullscreen = 0

# Разрешения: чтение галереи для фото рецептов + вибрация
android.permissions = VIBRATE,READ_EXTERNAL_STORAGE,READ_MEDIA_IMAGES

android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = 1

# presplash.filename = %(source.dir)s/assets/presplash.png
# icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
