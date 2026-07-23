#!/bin/sh
set -e

export DISPLAY=:0
export XDG_RUNTIME_DIR="/tmp/runtime-live"
mkdir -p "$XDG_RUNTIME_DIR"

# Start local backend for UI actions if Python is available
if command -v python3 >/dev/null 2>&1 && [ -x /usr/local/bin/nexos-backend.py ]; then
  python3 /usr/local/bin/nexos-backend.py &
fi

if command -v chromium >/dev/null 2>&1; then
  exec chromium --no-first-run --disable-translate --disable-infobars --kiosk "file:///usr/share/nexos-ui/index.html"
elif command -v google-chrome >/dev/null 2>&1; then
  exec google-chrome --no-first-run --disable-translate --disable-infobars --kiosk "file:///usr/share/nexos-ui/index.html"
elif command -v firefox >/dev/null 2>&1; then
  exec firefox --kiosk "file:///usr/share/nexos-ui/index.html"
else
  exec x-www-browser "file:///usr/share/nexos-ui/index.html"
fi
