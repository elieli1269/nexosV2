#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "=== Environment ==="
whoami
pwd
df -h
ls -la

UI_SRC="index.html"
UI_DST="config/includes.chroot/usr/share/nexos-ui/index.html"

echo "=== Preparing UI ==="
mkdir -p "$(dirname "$UI_DST")"
cp -r -f "$UI_SRC" "$(dirname "$UI_DST")"
cp -f nexos-launch.sh config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/usr/local/bin/nexos-launch.sh

echo "=== Cleaning previous builds ==="
rm -rf cache/ chroot/ build/ *.iso *.log 2>/dev/null || true

echo "=== Configuring live-build ==="
lb clean --all || true
lb config \
  --distribution jammy \
  --architecture amd64 \
  --archive-areas "main universe multiverse" \
  --binary-images iso-hybrid \
  --apt-indices true \
  --debian-installer false \
  --memtest none \
  --bootappend-live "boot=live components persistence"

echo "=== Running lb build ==="
set -x
sudo lb build
set +x

echo "=== Build complete, checking for ISO ==="
ls -lh
echo "=== Looking for .iso files (excluding protected SSL private dirs) ==="
find . \( -path './cache/bootstrap/etc/ssl/private' -o -path './cache/bootstrap/etc/ssl/private/*' \) -prune -o -type f -name '*.iso' -print -exec ls -lh {} \; 2>/dev/null
if [ -f "live-image-amd64.hybrid.iso" ]; then
  echo "SUCCESS: Found live-image-amd64.hybrid.iso"
  ls -lh live-image-amd64.hybrid.iso
else
  echo "ERROR: live-image-amd64.hybrid.iso not found!"
  exit 1
fi
