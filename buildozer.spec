[app]
title = Guess Game
package.name = guessgame
package.domain = org.abo7medexe
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1

# المكاتب المطلوبة لتشغيل مشروعك
requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 0

# إعدادات الأندرويد الأساسية والسيرفر
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 1
