#!/usr/bin/env python3
import http.server
import json
import os
import socketserver
import subprocess
from urllib.parse import urlparse

PORT = 9876
BACKEND_PATH = "/usr/local/bin/nexos"

class NexosHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

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
