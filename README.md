# TowerMadness 1.0 : mise à jour de compatibilité Android

APK à installer : `release/TowerMadness-v1.0-android-moderne.apk`

Le gameplay, les graphismes, les sons et les ressources sont ceux d'origine.
Seules les couches techniques ont été modifiées pour que le jeu s'installe et se
lance sur les Android récents.

## Ce qui a été modifié

| Problème | Correctif |
|---|---|
| Android 14 et plus refusent d'installer une application qui vise une version trop ancienne (ici targetSdk 17) | Version visée passée à **24** (au-dessus du minimum exigé par Android 14/15, sous les seuils qui ajoutent d'autres restrictions) |
| Les 18 bibliothèques natives Apportable contiennent des « text relocations », refusées par le chargeur d'Android dès que la version visée est ≥ 23 | Retrait du marqueur `DT_TEXTREL`/`DF_TEXTREL` et segment de code rendu modifiable pendant le chargement (`patch/patch_elf.py`) |
| Le son chargeait `/system/lib/libOpenSLES.so` par son chemin absolu, bloqué depuis Android 7 | Chargement par nom (`libOpenSLES.so`) |
| Certains téléphones récents n'acceptent plus le dossier `lib/armeabi` | Bibliothèques placées dans `lib/armeabi-v7a`, et `apportable.abi_list=armv7a` pour que le chargeur Apportable les trouve |
| Liaisons de services implicites (achats intégrés, licence, Google Play Services) : plantage dès que la version visée est ≥ 21 | Ajout de `setPackage(...)` (`patch/patch_smali.py`) |
| Signature v1 de 2013 | Nouvelle signature v1, v2 et v3 après zipalign |

## Installation

1. **Désinstaller l'ancienne version** du jeu : la signature a changé, donc
   l'installation par-dessus échoue.
2. Installer `release/TowerMadness-v1.0-android-moderne.apk`, en autorisant les
   « sources inconnues ».

## Limite : téléphones sans support 32 bits

Le jeu ne contient que du code natif ARM **32 bits**, et on n'a pas son code
source pour le recompiler en 64 bits. Il ne peut donc pas tourner sur les
téléphones qui n'exécutent plus du tout le 32 bits (Google Pixel 7 et plus
récents, et une partie des modèles haut de gamme récents). Sur ces appareils,
Android affiche « application non compatible ».

## Reconstruire

```
APKTOOL=/chemin/apktool.jar SIGNER=/chemin/uber-apk-signer.jar ./build.sh
```

Outils utilisés : apktool 2.10.0 et uber-apk-signer 1.3.0. La clé de signature
est `patch/towermadness.jks` (mot de passe `towermadness`). Gardez-la pour que
les prochaines versions s'installent par-dessus celle-ci.
