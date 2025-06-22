[app]
title = NiftyRSIAnalyzer
package.name = niftyrsianalyzer
package.domain = org.karthik.nifty
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd,yfinance,numpy

android.archs = armeabi-v7a, arm64-v8a
orientation = portrait
osx.kivy_version = 2.1.0

android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
android.build_tools_version = 31.0.0

android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
