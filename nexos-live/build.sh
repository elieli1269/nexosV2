#!/bin/bash
set -e
cd "$(dirname "$0")"

UI_SRC="index.html"
UI_DST="config/includes.chroot/usr/share/nexos-ui/index.html"

mkdir -p "$(dirname "$UI_DST")"
cp -r -f "$UI_SRC" "$(dirname "$UI_DST")"
cp -f nexos-launch.sh config/includes.chroot/usr/local/bin/nexos-launch.sh
chmod +x config/includes.chroot/usr/local/bin/nexos-launch.sh

echo "=== System diagnostics ==="
whoami
id
df -h .
free -m || true
ls -la config/ 

# Clean up any existing artifacts
echo "=== Cleaning up old builds ==="
rm -rf chroot/ build/ live-image-amd64.hybrid.iso live-image-amd64.iso cache/ || true
sudo apt-get clean -y || true

echo "=== Creating minimal live-build config ==="
# Reset to fresh state
lb clean --all || true
lb config \
  --distribution jammy \
  --architecture amd64 \
  --archive-areas "main universe multiverse" \
  --binary-images iso-hybrid \
  --apt-indices false \
  --debian-installer false \
  --bootappend-live "boot=live components" \
  --memtest none

echo "=== Building with verbose logging ==="
set -x
sudo lb build 2>&1 | tee build.log || {
  BUILD_EXIT=$?
  echo ""
  echo "=== BUILD FAILED with exit code: $BUILD_EXIT ==="
  echo ""
  echo "=== Last 100 lines of build.log ==="
  tail -n 100 build.log || true
  exit $BUILD_EXIT
}

echo "Build complete: $(pwd)/live-image-amd64.hybrid.iso"
ls -lh live-image-amd64.hybrid.iso || echo "ERROR: ISO not found!"
