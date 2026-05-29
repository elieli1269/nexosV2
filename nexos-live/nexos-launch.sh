#!/bin/sh
set -e

export DISPLAY=:0
export XDG_RUNTIME_DIR="/tmp/runtime-live"
mkdir -p "$XDG_RUNTIME_DIR"

if command -v chromium >/dev/null 2>&1; then
  exec chromium --no-first-run --disable-translate --disable-infobars --kiosk "file:///usr/share/nexos-ui/index.html"
elif command -v google-chrome >/dev/null 2>&1; then
  exec google-chrome --no-first-run --disable-translate --disable-infobars --kiosk "file:///usr/share/nexos-ui/index.html"
elif command -v firefox >/dev/null 2>&1; then
  exec firefox --kiosk "file:///usr/share/nexos-ui/index.html"
else
  exec x-www-browser "file:///usr/share/nexos-ui/index.html"
fi
