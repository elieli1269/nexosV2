#!/bin/bash
set -e
cd "$(dirname "$0")"

mkdir -p config/includes.chroot/usr/share/nexos-ui
cp -f index.html config/includes.chroot/usr/share/nexos-ui/index.html
cp -f nexos-launch.sh config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/etc/profile.d/nexos-live.sh

if command -v lb >/dev/null 2>&1; then
  lb config --distribution jammy --architecture amd64 --archive-areas "main universe multiverse" --binary-images iso-hybrid --apt-indices true --debian-installer false --bootappend-live "boot=live components persistence"
  sudo lb build
else
  echo "live-build n'est pas installé. Installez-le avec : sudo apt update && sudo apt install live-build"
  exit 1
fi
