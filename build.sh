#!/usr/bin/env bash
# Rebuilds release/TowerMadness-v1.0-android-moderne.apk from original/.
# Needs: java, python3, apktool.jar and uber-apk-signer.jar (paths below).
set -euo pipefail
cd "$(dirname "$0")"
APKTOOL=${APKTOOL:-apktool.jar}
SIGNER=${SIGNER:-uber-apk-signer.jar}
W=$(mktemp -d)

java -jar "$APKTOOL" d -f -o "$W/dec" original/towermadness-v1-0.apk

# Java: make implicit service intents explicit (required when targetSdk >= 21)
python3 patch/patch_smali.py "$W/dec"

# Native: move libs to armeabi-v7a and strip text relocations
mkdir -p "$W/dec/lib/armeabi-v7a"
mv "$W/dec/lib/armeabi/"*.so "$W/dec/lib/armeabi-v7a/"
rmdir "$W/dec/lib/armeabi"
python3 patch/patch_elf.py "$W/dec/lib/armeabi-v7a/"*.so

# Manifest: targetSdk 24 (installable on Android 14+), tell Apportable to use armeabi-v7a
sed -i "s/targetSdkVersion: '\?17'\?/targetSdkVersion: 24/" "$W/dec/apktool.yml"
sed -i 's#android:name="apportable.abi_list" android:value=""#android:name="apportable.abi_list" android:value="armv7a"#' \
  "$W/dec/AndroidManifest.xml"

java -jar "$APKTOOL" b "$W/dec" -o "$W/unsigned.apk"
java -jar "$SIGNER" -a "$W/unsigned.apk" -o "$W/signed" \
  --ks patch/towermadness.jks --ksAlias towermadness --ksPass towermadness --ksKeyPass towermadness
mkdir -p release
cp "$W/signed/unsigned-aligned-signed.apk" release/TowerMadness-v1.0-android-moderne.apk
echo "OK: release/TowerMadness-v1.0-android-moderne.apk"
