[app]
title = Guess Game
package.name = guessgame
package.domain = org.abo7medexe
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# تحديد الأرقام المناسبة لمنع التحميل اللانهائي
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

YES | buildozer android debug

log_level = 2
warn_on_root = 1
