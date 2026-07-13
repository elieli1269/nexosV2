#!/bin/bash
set -e
cd "$(dirname "$0")"

UI_SRC="index.html"
UI_DST="config/includes.chroot/usr/share/nexos-ui/index.html"

mkdir -p "$(dirname "$UI_DST")"
cp -r -f "$UI_SRC" "$(dirname "$UI_DST")"
cp -f nexos-launch.sh config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/usr/local/bin/nexos-launch.sh

lb config \
  --distribution jammy \
  --architecture amd64 \
  --archive-areas "main universe multiverse" \
  --binary-images iso-hybrid \
  --apt-indices true \
  --debian-installer false \
  --bootappend-live "boot=live components persistence"

# Remove any leftover build chroot or stray ISO files that can confuse live-build
if [ -d "chroot" ]; then
  echo "Removing stale chroot/ directory to avoid invalid include patterns"
  rm -rf chroot || true
fi
find . -maxdepth 2 -type f -name "memtest86+.iso" -print -delete || true

sudo lb build

echo "Build complete: $(pwd)/live-image-amd64.hybrid.iso"
