# NEXOS Live USB

Prototype de Live USB Linux avec interface NEXOS.

## Objectif
Créer une image bootable Linux basée sur Lubuntu qui démarre en mode Live USB et lance automatiquement l'interface NEXOS en plein écran.

## Structure
- `build.sh` : script de génération de l'ISO Debian live.
- `config/package-lists/nexos.list.chroot` : packages inclus dans l'image, avec un environnement Lubuntu réel.
- `config/includes.chroot/usr/local/bin/nexos-launch.sh` : script de lancement de l'UI.
- `config/includes.chroot/etc/xdg/openbox/autostart` : autostart Openbox.
- `config/includes.chroot/etc/lightdm/lightdm.conf.d/50-nexos.conf` : autologin LightDM.
- `ui/index.html` : interface NEXOS prototype.

## Prérequis
- Linux ou WSL2 avec accès aux commandes `bash`, `cp`, `chmod`, `lb`.
- Package `live-build` installé :
  - Debian/Ubuntu : `sudo apt update && sudo apt install live-build`
- Clé USB 8GB+ pour écrire l'ISO.

## Construire l'image
1. Ouvrir un terminal Linux depuis le dossier `nexos-live`.
2. Rendre le script exécutable :
   ```bash
   chmod +x build.sh
   ```
3. Lancer la génération :
   ```bash
   ./build.sh
   ```
4. L'image ISO finale sera produite dans `nexos-live/live-image-amd64.hybrid.iso`.

## Écrire sur la clé USB
Sur Linux, remplacer `/dev/sdX` par l'identifiant de votre clé USB :

```bash
sudo dd if=live-image-amd64.hybrid.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

## Sur Windows
1. Installez WSL si nécessaire :
   ```powershell
   wsl --install
   ```
2. Ouvrez une distribution Linux (Debian ou Ubuntu).
3. Accédez au dossier de projet via `/mnt/c/Users/.../Downloads/nexos/nexos-live`.
4. Exécutez :
   ```bash
   chmod +x build.sh
   ./build.sh
   ```
5. Une fois l'image créée, écrivez-la sur la clé USB depuis Linux :
   ```bash
   sudo dd if=live-image-amd64.hybrid.iso of=/dev/sdX bs=4M status=progress conv=fsync
   ```

> L'image créée est une image ISO-hybrid bootable. Elle peut être écrite directement sur une clé USB et démarrée en mode Live USB.

## Personnalisation
- Remplacer `ui/index.html` par la version complète de l'interface NEXOS.
- Ajouter des fichiers CSS/JS complémentaires dans `ui/` et référencer dans `index.html`.
- Modifier `config/package-lists/nexos.list.chroot` pour installer des outils supplémentaires.

## NEXOS EXT et compte global
- Cette version prototype simule un compte unifié `NEXOS EXT` qui fonctionne partout.
- L'identifiant NEXOS EXT est enregistré localement dans le navigateur via `localStorage`.
- Dans un vrai déploiement, `NEXOS EXT` serait le même compte sur plusieurs clés USB, appareils et instances NEXOS.
- La localisation NEXOS EXT signifie que l'expérience et les paramètres sont liés à ce compte global.

## NEXA et NEX Store
- `NEXA` n'est pas encore disponible et reste en développement.
- Aucune fonctionnalité cloud NEXA n'est simulée dans cette version.
- `NEX Store` gère uniquement les applications locales installées : activation, désactivation et désinstallation.
- Il n'y a pas de téléchargement ou d'installation cloud dans ce prototype.

## Notes
- Cette structure utilise Debian live-build comme base réaliste pour un Live USB Linux.
- Le vrai système NEXOS sera une surcouche graphique sur un Linux live, pas un noyau réécrit à partir de zéro.
