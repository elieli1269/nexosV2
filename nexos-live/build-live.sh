#!/bin/bash
set -e
cd "$(dirname "$0")"

mkdir -p config/includes.chroot/usr/share/nexos-ui
cp -f index.html config/includes.chroot/usr/share/nexos-ui/index.html
cp -f nexos-launch.sh config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/etc/profile.d/nexos-live.sh

echo "=== Listing config structure ==="
find config -type f | head -30 | sort

if command -v lb >/dev/null 2>&1; then
  echo "=== Starting lb config ==="
  lb config --distribution jammy --architecture amd64 --archive-areas "main universe multiverse" --binary-images iso-hybrid --apt-indices true --debian-installer false --bootappend-live "boot=live components persistence"
  
  echo "=== Pre-cleanup: checking for problematic files ==="
  if [ -d "chroot" ]; then
    echo "Found stale chroot/ directory - removing"
    rm -rf chroot || true
  fi
  
  echo "=== Searching for problematic memtest files ==="
  find . -maxdepth 2 -type f -name "memtest86+.iso" -print -delete -v || true
  
  echo "=== Checking config after cleanup ==="
  find config -name "*.iso" -o -name "*.chroot" | head -20 || true
  
  echo "=== Starting sudo lb build with debug ==="
  set -x
  sudo lb build
else
  echo "live-build n'est pas installé. Installez-le avec : sudo apt update && sudo apt install live-build"
  exit 1
fi
