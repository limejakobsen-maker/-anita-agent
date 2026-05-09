#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENKEL HTTP SERVER v2.0 - Threadripper
Integrert med sandkasse_protokoll.py
Port: 8765
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Importér protokollen
try:
    from sandkasse_protokoll import SandkasseProtokoll, LenovoOllamaClient
    PROTOKOLL_TILGJENGELIG = True
except ImportError as e:
    print(f"ADVARSEL: Kunne ikke importere sandkasse_protokoll: {e}")
    PROTOKOLL_TILGJENGELIG = False

# Global state
protokoll = None
server_status = {
    "siste_prosjekt": None,
    "fase": 0,
    "prosent": 0,
    "status": "idle",
    "logg": [],
    "lenovo_tilkoblet": False
}

class SandkasseHandler(BaseHTTPRequestHandler):
    """HTTP Handler for sandkasse-forespørsler"""
    
    def log_message(self, format, *args):
        """Custom logging - skriv til fil i stedet for stdout"""
        log_file = Path("C:/AI_System/logs/server.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{self.log_date_time_string()} - {format % args}\n")
    
    def _send_json(self, data, status=200):
        """Send JSON-respons"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    
    def do_GET(self):
        """Håndter GET-forespørsler"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/status":
            # Returner nåværende status
            global server_status
            if protokoll:
                server_status.update(protokoll.get_status())
            self._send_json(server_status)
        
        elif path == "/health":
            # Sjekk at serveren lever
            self._send_json({
                "status": "ok",
                "protokoll_tilgjengelig": PROTOKOLL_TILGJENGELIG,
                "lenovo_tilkoblet": server_status.get("lenovo_tilkoblet", False)
            })
        
        elif path == "/models":
            # List tilgjengelige modeller på Lenovo
            try:
                client = LenovoOllamaClient()
                models = client.list_models()
                self._send_json({"models": models, "lenovo_url": client.base_url})
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
        
        else:
            self._send_json({"error": "Ukjent endepunkt"}, status=404)
    
    def do_POST(self):
        """Håndter POST-forespørsler"""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        try:
            data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            data = parse_qs(post_data)
            # Flatten single-value lists
            data = {k: v[0] if len(v) == 1 else v for k, v in data.items()}
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/start":
            # Start ny protokoll
            prosjektnavn = data.get("project") or data.get("prosjekt")
            beskrivelse = data.get("description") or data.get("beskrivelse")
            
            if not prosjektnavn or not beskrivelse:
                self._send_json({
                    "error": "Mangler 'project' eller 'description'"
                }, status=400)
                return
            
            # Start protokoll i egen tråd
            def run_protokoll():
                global protokoll
                try:
                    protokoll = SandkasseProtokoll()
                    result = protokoll.kjør_full_protokoll(prosjektnavn, beskrivelse)
                    print(f"Protokoll fullført: {result}")
                except Exception as e:
                    print(f"Feil i protokoll: {e}")
                    server_status["status"] = f"feil: {e}"
            
            thread = threading.Thread(target=run_protokoll, daemon=True)
            thread.start()
            
            self._send_json({
                "message": "Protokoll startet",
                "prosjekt": prosjektnavn,
                "status": "running"
            })
        
        elif path == "/stopp":
            # Stopp pågående protokoll
            if protokoll:
                protokoll.stopp()
                self._send_json({"message": "Stopp-signal sendt"})
            else:
                self._send_json({"message": "Ingen protokoll kjører"})
        
        else:
            self._send_json({"error": "Ukjent endepunkt"}, status=404)
    
    def do_OPTIONS(self):
        """Håndter CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def check_lenovo_connection():
    """Sjekk tilkobling til Lenovo i bakgrunnen"""
    global server_status
    while True:
        try:
            client = LenovoOllamaClient()
            server_status["lenovo_tilkoblet"] = client.is_available()
        except:
            server_status["lenovo_tilkoblet"] = False
        time.sleep(30)  # Sjekk hvert 30. sekund


def main():
    """Start serveren"""
    host = "0.0.0.0"
    port = 8765
    
    # Opprett logg-mappe
    Path("C:/AI_System/logs").mkdir(parents=True, exist_ok=True)
    
    # Sjekk protokoll-tilgjengelighet
    if PROTOKOLL_TILGJENGELIG:
        print("✅ sandkasse_protokoll.py funnet og lastet")
    else:
        print("⚠️  sandkasse_protokoll.py ikke funnet - server kjører i begrenset modus")
        print("    Kopier sandkasse_protokoll.py til samme mappe som denne serveren")
    
    # Start Lenovo-monitorering
    monitor_thread = threading.Thread(target=check_lenovo_connection, daemon=True)
    monitor_thread.start()
    
    # Start HTTP-server
    server = HTTPServer((host, port), SandkasseHandler)
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  ENKEL HTTP SERVER v2.0 - Threadripper                     ║
║                                                            ║
║  Lytter på: http://{host}:{port}                         ║
║                                                            ║
║  Endepunkter:                                              ║
║    GET  /status   - Se prosjektstatus                     ║
║    GET  /health   - Sjekk serverhelse                     ║
║    GET  /models   - List Lenovos modeller                 ║
║    POST /start    - Start prosjekt (JSON: project, desc)  ║
║    POST /stopp    - Stopp pågående prosjekt               ║
║                                                            ║
║  Trykk Ctrl+C for å stoppe                                ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stoppet av bruker")
        server.shutdown()


if __name__ == "__main__":
    main()
