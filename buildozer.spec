[app]

title = لعبة تخمين الرقم
package.name = guessnumber
package.domain = org.example
source.dir = .
source.include_exts = py,ttf,png,jpg
version = 1.0

requirements = python3,kivy,arabic-reshaper

orientation = portrait
fullscreen = 0

icon.filename = icon.png


[buildozer]

log_level = 2


[android]

android.api = 35
android.minapi = 23
android.archs = arm64-v8a