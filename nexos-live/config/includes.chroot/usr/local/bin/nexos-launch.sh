#!/bin/sh
set -eu

export DISPLAY="${DISPLAY:-:0}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp/runtime-live}"
mkdir -p "$XDG_RUNTIME_DIR"

if command -v xset >/dev/null 2>&1; then
  xset s off -dpms >/dev/null 2>&1 || true
fi

if command -v dbus-launch >/dev/null 2>&1; then
  eval "$(dbus-launch --auto-syntax 2>/dev/null)" || true
fi

sleep 2

if command -v firefox >/dev/null 2>&1; then
  exec firefox --kiosk --new-window "file:///usr/share/nexos-ui/index.html"
elif command -v chromium >/dev/null 2>&1; then
  exec chromium --no-first-run --disable-translate --disable-infobars --kiosk "file:///usr/share/nexos-ui/index.html"
elif command -v google-chrome >/dev/null 2>&1; then
  exec google-chrome --no-first-run --disable-translate --disable-infobars --kiosk "file:///usr/share/nexos-ui/index.html"
elif command -v xdg-open >/dev/null 2>&1; then
  exec xdg-open "file:///usr/share/nexos-ui/index.html"
else
  echo "NEXOS: no supported browser found for kiosk launch" >&2
  exit 1
fi
