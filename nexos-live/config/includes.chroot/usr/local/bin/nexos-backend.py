#!/usr/bin/env python3
import glob
import http.server
import json
import os
import socketserver
import subprocess
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import base64

PORT = 9876
BACKEND_PATH = "/usr/local/bin/nexos"
HOME = os.path.expanduser("~")
SEARCH_PATHS = [HOME, "/usr/share", "/opt", "/home"]
ICON_PATHS = [
    "/usr/share/pixmaps",
    "/usr/share/icons/hicolor",
    "/usr/share/icons/ubuntu",
    "/usr/local/share/pixmaps",
    f"{HOME}/.local/share/icons",
]

def detect_zram_status():
    """Detect if ZRAM is installed and running"""
    try:
        result = subprocess.run(['zramctl'], capture_output=True, text=True, check=False)
        if result.returncode == 0 and 'ALGORITHM' in result.stdout:
            return {"installed": True, "status": "active", "info": result.stdout.strip()}
    except:
        pass
    
    # Check /proc/swaps for zram
    try:
        with open('/proc/swaps', 'r') as f:
            content = f.read()
            if '/dev/zram' in content:
                return {"installed": True, "status": "active", "info": content}
    except:
        pass
    
    return {"installed": False, "status": "inactive", "info": "ZRAM not detected"}


def find_app_icon(app_name):
    """Find and return base64-encoded icon for an app"""
    app_lower = app_name.lower().replace(' ', '').replace('.', '')
    
    # Common icon names mapping
    icon_mappings = {
        'chrome': 'google-chrome',
        'chromium': 'chromium-browser',
        'firefox': 'firefox',
        'vscode': 'code',
        'vlc': 'vlc',
        'libreoffice': 'libreoffice-writer',
    }
    
    search_names = [icon_mappings.get(app_lower, app_lower), app_lower, app_name.lower()]
    
    for icon_dir in ICON_PATHS:
        if not os.path.isdir(icon_dir):
            continue
        
        # Search for icons recursively
        for root, dirs, files in os.walk(icon_dir):
            for file in files:
                if file.endswith(('.png', '.svg', '.jpg')):
                    file_lower = file.lower().replace('.png', '').replace('.svg', '').replace('.jpg', '')
                    for name in search_names:
                        if name in file_lower or file_lower in name:
                            icon_path = os.path.join(root, file)
                            try:
                                with open(icon_path, 'rb') as f:
                                    icon_data = f.read()
                                    if len(icon_data) < 500000:  # Max 500KB
                                        return f"data:image/png;base64,{base64.b64encode(icon_data).decode()}"
                            except:
                                pass
            # Don't go too deep
            if root.count(os.sep) - icon_dir.count(os.sep) > 4:
                break
    
    return None


def list_pc_apps():
    apps = []
    seen = set()
    for directory in ["/usr/share/applications", "/usr/local/share/applications", "~/.local/share/applications"]:
        directory = os.path.expanduser(directory)
        if not os.path.isdir(directory):
            continue
        for path in glob.glob(os.path.join(directory, "*.desktop")):
            try:
                name = None
                exec_cmd = None
                no_display = False
                with open(path, encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("Name=") and name is None:
                            name = line.split("=", 1)[1].strip()
                        elif line.startswith("Exec="):
                            exec_cmd = line.split("=", 1)[1].strip()
                        elif line.startswith("NoDisplay="):
                            no_display = line.split("=", 1)[1].strip().lower() == "true"
                if not name or no_display or name in seen:
                    continue
                seen.add(name)
                apps.append({"name": name, "exec": exec_cmd or "", "desktop": os.path.basename(path)})
            except Exception:
                continue
    apps.sort(key=lambda x: x["name"].lower())
    return apps


def list_files(search_path="/home", max_depth=2, current_depth=0, max_items=100):
    """Explore filesystem and return files/folders with metadata"""
    items = []
    
    if current_depth >= max_depth or not os.path.isdir(search_path):
        return items
    
    try:
        entries = sorted(os.listdir(search_path))[:max_items]
    except (PermissionError, OSError):
        return items
    
    for entry in entries:
        if entry.startswith('.'):
            continue
        
        full_path = os.path.join(search_path, entry)
        try:
            stat = os.stat(full_path)
            is_dir = os.path.isdir(full_path)
            
            item = {
                "name": entry,
                "path": full_path,
                "type": "folder" if is_dir else "file",
                "size": stat.st_size if not is_dir else 0,
                "mtime": int(stat.st_mtime),
            }
            items.append(item)
        except (PermissionError, OSError):
            continue
    
    return items


def build_apps_index():
    """Build semantic index of all apps (both NEX and system)"""
    apps = list_pc_apps()
    
    nex_apps = [
        {
            "name": "NEX Editor", 
            "category": "texte", 
            "icon": "✍️", 
            "desc": "Éditeur texte intégré avec IA collaborative",
            "keywords": ["edit", "text", "write", "document"]
        },
        {
            "name": "NEX AI", 
            "category": "ia", 
            "icon": "🤖", 
            "desc": "Copilote IA Groq pour coding et assistance",
            "keywords": ["ai", "assistant", "groq", "code"]
        },
        {
            "name": "NEX Console", 
            "category": "system", 
            "icon": "⌨️", 
            "desc": "Terminal intégré pour commandes shell",
            "keywords": ["terminal", "shell", "bash", "command"]
        },
        {
            "name": "NEX Files", 
            "category": "files", 
            "icon": "📁", 
            "desc": "Gestionnaire de fichiers avec recherche sémantique",
            "keywords": ["files", "folders", "browse", "manager"]
        },
        {
            "name": "NEX Store", 
            "category": "packages", 
            "icon": "📦", 
            "desc": "Gestionnaire de paquets NEXOS",
            "keywords": ["install", "package", "app", "store"]
        },
        {
            "name": "NEX Search", 
            "category": "search", 
            "icon": "⌕", 
            "desc": "Moteur de recherche intégré",
            "keywords": ["search", "find", "query"]
        },
    ]
    
    # Extended categorization with semantic keywords
    categorized = {
        "browser": {
            "keywords": ["chrome", "firefox", "chromium", "safari", "edge", "opera"],
            "icon": "🌐"
        },
        "media": {
            "keywords": ["vlc", "mpv", "kodi", "plex", "ffmpeg"],
            "icon": "🎬"
        },
        "office": {
            "keywords": ["libreoffice", "onlyoffice", "word", "excel", "writer", "calc"],
            "icon": "📑"
        },
        "dev": {
            "keywords": ["code", "vscode", "atom", "sublime", "intellij", "vim", "git", "python", "node"],
            "icon": "👨‍💻"
        },
        "messaging": {
            "keywords": ["discord", "telegram", "slack", "thunderbird", "mail", "irc"],
            "icon": "💬"
        },
        "audio": {
            "keywords": ["spotify", "audacity", "rhythmbox", "pulseaudio"],
            "icon": "🎵"
        },
        "graphics": {
            "keywords": ["gimp", "krita", "blender", "imagemagick"],
            "icon": "🎨"
        },
        "system": {
            "keywords": ["gnome", "kde", "xfce", "systemd", "kernel"],
            "icon": "⚙️"
        },
        "gaming": {
            "keywords": ["steam", "lutris", "wine", "proton"],
            "icon": "🎮"
        },
    }
    
    indexed = {"nex": nex_apps, "system": {}, "total": len(apps) + len(nex_apps)}
    
    for app in apps:
        category = "other"
        app_lower = app["name"].lower()
        
        for cat, config in categorized.items():
            if any(kw in app_lower for kw in config["keywords"]):
                category = cat
                break
        
        if category not in indexed["system"]:
            indexed["system"][category] = []
        
        icon = categorized.get(category, {}).get("icon", "⚙️")
        indexed["system"][category].append({
            "name": app["name"],
            "category": category,
            "icon": icon,
            "desc": f"Application système: {app['name']}",
            "keywords": app["name"].lower().split()
        })
    
    return indexed


class NexosHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        
        if parsed.path == "/pc-apps":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            apps = list_pc_apps()
            # Add icon data for each app
            for app in apps:
                icon = find_app_icon(app["name"])
                app["icon"] = icon
            self.wfile.write(json.dumps({"apps": apps}).encode("utf-8"))
            return
        
        if parsed.path == "/icon":
            app_name = query.get("app", [""])[0]
            if app_name:
                icon = find_app_icon(app_name)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"icon": icon, "app": app_name}).encode("utf-8"))
                return
        
        if parsed.path == "/files":
            search_path = query.get("path", [HOME])[0]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            items = list_files(search_path, max_depth=2)
            self.wfile.write(json.dumps({"path": search_path, "items": items}).encode("utf-8"))
            return
        
        if parsed.path == "/apps-index":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            index = build_apps_index()
            self.wfile.write(json.dumps(index).encode("utf-8"))
            return
        
        if parsed.path == "/system-info":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            zram_status = detect_zram_status()
            system_info = {
                "zram": zram_status,
                "hostname": os.uname().nodename,
                "platform": os.uname().sysname,
            }
            self.wfile.write(json.dumps(system_info).encode("utf-8"))
            return
        
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/uninstall":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Endpoint inconnu"}).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if not os.path.exists(BACKEND_PATH):
            self.wfile.write(json.dumps({"status": "error", "message": "Commande de désinstallation introuvable"}).encode("utf-8"))
            return

        try:
            result = subprocess.run([BACKEND_PATH, "uninstall"], capture_output=True, text=True, check=False)
            if result.returncode != 0:
                self.wfile.write(json.dumps({"status": "error", "message": result.stderr.strip() or "Erreur de désinstallation"}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"status": "ok", "message": "Désinstallation Nexos terminée"}).encode("utf-8"))
        except Exception as e:
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), NexosHandler) as httpd:
        httpd.serve_forever()
