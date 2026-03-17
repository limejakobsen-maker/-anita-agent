#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protokoll Server - Kommunikasjon med GUI Monitor
Kjører lokalt på port 8765
"""

import asyncio
import websockets
import json
import threading
import queue
import sys
from pathlib import Path
from datetime import datetime

from sandkasse_protokoll import SandkasseProtokoll

class ProtokollServer:
    """WebSocket-server for kommunikasjon med Acer-monitor"""
    
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.event_queue = queue.Queue()
        self.clients = set()
        self.protokoll = None
        self.is_running = False
        
    async def register(self, websocket):
        """Registrer ny klient (Acer)"""
        self.clients.add(websocket)
        print(f"[CONNECT] Acer tilkoblet fra {websocket.remote_address}")
        
        # Send velkomstmelding
        await websocket.send(json.dumps({
            "type": "connected",
            "data": {
                "server": "Lokal Sandkasse",
                "ip": "localhost",
                "status": "ready"
            }
        }))
    
    async def unregister(self, websocket):
        """Fjern klient"""
        self.clients.discard(websocket)
        print(f"[DISCONNECT] Acer frakoblet")
    
    async def handle_client(self, websocket, path):
        """Håndter klient-tilkobling"""
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def process_message(self, websocket, message):
        """Prosesser melding fra GUI monitor"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "start_protokoll":
                # Start ny protokoll
                prosjektnavn = data["data"]["navn"]
                krav = data["data"]["krav"]
                
                print(f"[KOMMANDO] Start protokoll: {prosjektnavn}")
                
                # Start protokoll i egen tråd
                thread = threading.Thread(
                    target=self.run_protokoll,
                    args=(prosjektnavn, krav),
                    daemon=True
                )
                thread.start()
                
                await websocket.send(json.dumps({
                    "type": "protokoll_started",
                    "data": {"navn": prosjektnavn}
                }))
            
            elif msg_type == "stopp_protokoll":
                if self.protokoll:
                    self.protokoll.stopp()
                    print("[KOMMANDO] Stopp protokoll")
                
                await websocket.send(json.dumps({
                    "type": "protokoll_stopped"
                }))
            
            elif msg_type == "approval_response":
                # Bruker har godkjent/avvist fiks
                approved = data["data"]["approved"]
                if self.protokoll:
                    self.protokoll.set_approval_result(approved)
                    print(f"[GODKJENNING] {'Godkjent' if approved else 'Avvist'}")
            
            elif msg_type == "get_status":
                # Send nåværende status
                status = {
                    "is_running": self.protokoll.is_running if self.protokoll else False,
                    "fase": self.protokoll.current_prosjekt.fase if self.protokoll and self.protokoll.current_prosjekt else 0,
                    "prosjekt": self.protokoll.current_prosjekt.navn if self.protokoll and self.protokoll.current_prosjekt else None
                }
                await websocket.send(json.dumps({
                    "type": "status",
                    "data": status
                }))
            
            elif msg_type == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
                
        except Exception as e:
            print(f"[FEIL] Kunne ikke prosessere melding: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "data": {"message": str(e)}
            }))
    
    def run_protokoll(self, navn: str, krav: str):
        """Kjør protokoll i egen tråd"""
        self.protokoll = SandkasseProtokoll(event_queue=self.event_queue)
        self.protokoll.kjør_full_protokoll(navn, krav)
    
    async def broadcast_events(self):
        """Send hendelser fra kø til alle tilkoblede klienter"""
        while True:
            try:
                # Sjekk event-kø (ikke-blokkerende)
                event = self.event_queue.get_nowait()
                
                # Send til alle klienter
                if self.clients:
                    disconnected = []
                    for client in self.clients:
                        try:
                            await client.send(json.dumps(event))
                        except:
                            disconnected.append(client)
                    
                    # Fjern frakoblede klienter
                    for client in disconnected:
                        self.clients.discard(client)
                        
            except queue.Empty:
                pass
            
            await asyncio.sleep(0.1)  # 100ms delay
    
    async def start(self):
        """Start serveren"""
        self.is_running = True
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║  [LOKAL] Sandkasse-Protokoll Server v3.0                   ║
║                                                           ║
║  Lytter på: {self.host}:{self.port}                          ║
║  Lokalt: ws://localhost:{self.port}                        ║
║                                                           ║
║  GUI kan koble til med:                                   ║
║  ws://localhost:{self.port}                                  ║
╚═══════════════════════════════════════════════════════════╝
        """)
        
        # Start WebSocket-server
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10
        )
        
        # Start broadcast-task
        broadcast_task = asyncio.create_task(self.broadcast_events())
        
        try:
            await server.wait_closed()
        except asyncio.CancelledError:
            print("[STOPP] Server avsluttet")
            broadcast_task.cancel()


def main():
    """Hovedfunksjon"""
    # Sjekk avhengigheter
    try:
        import websockets
    except ImportError:
        print("[INSTALLER] Installerer websockets...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "websockets"])
        import websockets
    
    server = ProtokollServer()
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n[STOPP] Avbrutt av bruker")


if __name__ == "__main__":
    main()
