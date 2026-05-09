#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protokoll Monitor - Overvåkingsvindu for Acer
Viser sanntidsstatus fra Lenovo Sandkasse
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import asyncio
import websockets
import json
import queue
import time
from datetime import datetime

class ProtokollMonitor:
    """GUI for overvåking av Sandkasse-Protokollen på Lenovo"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("[ACER] → [LENOVO] Sandkasse Protokoll Monitor")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        self.root.minsize(900, 600)
        
        # Tailscale-konfigurasjon
        self.lenovo_ip = "100.108.91.44"
        self.lenovo_port = 8765
        self.ws_url = f"ws://{self.lenovo_ip}:{self.lenovo_port}"
        
        # Tilstand
        self.websocket = None
        self.is_connected = False
        self.message_queue = queue.Queue()
        self.current_fase = 0
        self.current_prosjekt = None
        
        # GUI-oppsett
        self.setup_ui()
        
        # Start bakgrunnstråder
        self.running = True
        self.start_websocket_thread()
        self.start_ui_updater()
        
        # Dark mode på Windows
        self._setup_dark_mode()
    
    def _setup_dark_mode(self):
        """Aktiver mørk modus på Windows 10/11"""
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
            windll.dwmapi.DwmSetWindowAttribute(
                windll.user32.GetParent(self.root.winfo_id()),
                20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                1, 4
            )
        except:
            pass
    
    def setup_ui(self):
        """Sett opp brukergrensesnittet"""
        # ===== TOPP-PANEL (Status og tilkobling) =====
        top_frame = tk.Frame(self.root, bg='#252526', height=50)
        top_frame.pack(fill='x', padx=5, pady=5)
        top_frame.pack_propagate(False)
        
        # Tilkoblingsstatus
        self.conn_label = tk.Label(
            top_frame,
            text="🔗 Kobler til Lenovo...",
            font=('Segoe UI', 10, 'bold'),
            bg='#252526',
            fg='#ffcc00'
        )
        self.conn_label.pack(side='left', padx=10, pady=10)
        
        # Prosjekt-status
        self.status_label = tk.Label(
            top_frame,
            text="Venter på prosjekt...",
            font=('Segoe UI', 10),
            bg='#252526',
            fg='#d4d4d4'
        )
        self.status_label.pack(side='right', padx=10, pady=10)
        
        # ===== HOVEDPANEL (Faser) =====
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Venstre: Fase-visning
        left_frame = tk.Frame(main_frame, bg='#1e1e1e', width=250)
        left_frame.pack(side='left', fill='y', padx=5)
        left_frame.pack_propagate(False)
        
        tk.Label(
            left_frame,
            text="FASE-OVERSIKT",
            font=('Segoe UI', 11, 'bold'),
            bg='#1e1e1e',
            fg='#569cd6'
        ).pack(pady=10)
        
        # Fase-indikatorer
        self.fase_labels = {}
        faser = [
            (1, "1. SPECS", "Definer krav"),
            (2, "2. SKELETT", "Opprett struktur"),
            (3, "3. KODE", "Generer kode"),
            (4, "4. VALIDER", "Test & sjekk"),
            (5, "5. DEPLOY", "Arkiver")
        ]
        
        for fase_num, fase_navn, fase_desc in faser:
            frame = tk.Frame(left_frame, bg='#1e1e1e')
            frame.pack(fill='x', pady=5, padx=10)
            
            # Fase-nummer (sirkel)
            self.fase_labels[fase_num] = tk.Label(
                frame,
                text=str(fase_num),
                font=('Segoe UI', 14, 'bold'),
                bg='#3c3c3c',
                fg='#808080',
                width=2
            )
            self.fase_labels[fase_num].pack(side='left', padx=5)
            
            # Fase-tekst
            tk.Label(
                frame,
                text=fase_navn,
                font=('Segoe UI', 10, 'bold'),
                bg='#1e1e1e',
                fg='#d4d4d4'
            ).pack(anchor='w')
            tk.Label(
                frame,
                text=fase_desc,
                font=('Segoe UI', 8),
                bg='#1e1e1e',
                fg='#808080'
            ).pack(anchor='w')
        
        # Fremdriftsindikator
        tk.Label(
            left_frame,
            text="FREMDRIFT",
            font=('Segoe UI', 10, 'bold'),
            bg='#1e1e1e',
            fg='#569cd6'
        ).pack(pady=(20, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            left_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress.pack(fill='x', padx=10, pady=5)
        
        self.progress_label = tk.Label(
            left_frame,
            text="0%",
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#4ec9b0'
        )
        self.progress_label.pack()
        
        # Midten: Kode-visning
        center_frame = tk.Frame(main_frame, bg='#1e1e1e')
        center_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(
            center_frame,
            text="KODE (SANNTID)",
            font=('Segoe UI', 11, 'bold'),
            bg='#1e1e1e',
            fg='#569cd6'
        ).pack(anchor='w', pady=(0, 5))
        
        self.code_box = scrolledtext.ScrolledText(
            center_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='#252526',
            fg='#d4d4d4',
            insertbackground='white',
            height=20
        )
        self.code_box.pack(fill='both', expand=True)
        
        # Syntax highlighting tags
        self.code_box.tag_config('keyword', foreground='#569cd6')
        self.code_box.tag_config('string', foreground='#ce9178')
        self.code_box.tag_config('comment', foreground='#6a9955')
        self.code_box.tag_config('function', foreground='#dcdcaa')
        
        # Høyre: Logg
        right_frame = tk.Frame(main_frame, bg='#1e1e1e', width=300)
        right_frame.pack(side='left', fill='y', padx=5)
        right_frame.pack_propagate(False)
        
        tk.Label(
            right_frame,
            text="LOGG & HENDELSER",
            font=('Segoe UI', 11, 'bold'),
            bg='#1e1e1e',
            fg='#569cd6'
        ).pack(anchor='w', pady=(0, 5))
        
        self.log_box = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#252526',
            fg='#d4d4d4',
            height=15
        )
        self.log_box.pack(fill='both', expand=True)
        
        # Statistikk under logg
        tk.Label(
            right_frame,
            text="STATISTIKK",
            font=('Segoe UI', 10, 'bold'),
            bg='#1e1e1e',
            fg='#569cd6'
        ).pack(anchor='w', pady=(10, 5))
        
        self.stats_text = tk.Text(
            right_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#252526',
            fg='#4ec9b0',
            height=5,
            state='disabled'
        )
        self.stats_text.pack(fill='x')
        
        # ===== BUNNPANEL (Kontroller) =====
        bottom_frame = tk.Frame(self.root, bg='#252526', height=60)
        bottom_frame.pack(fill='x', padx=5, pady=5)
        bottom_frame.pack_propagate(False)
        
        # Prosjekt-input
        input_frame = tk.Frame(bottom_frame, bg='#252526')
        input_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(
            input_frame,
            text="Prosjektnavn:",
            font=('Segoe UI', 9),
            bg='#252526',
            fg='#d4d4d4'
        ).pack(side='left')
        
        self.project_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 9),
            bg='#3c3c3c',
            fg='white',
            insertbackground='white',
            width=20
        )
        self.project_entry.pack(side='left', padx=5)
        self.project_entry.insert(0, "TestProsjekt")
        
        tk.Label(
            input_frame,
            text="Krav:",
            font=('Segoe UI', 9),
            bg='#252526',
            fg='#d4d4d4'
        ).pack(side='left', padx=(10, 0))
        
        self.requirement_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 9),
            bg='#3c3c3c',
            fg='white',
            insertbackground='white',
            width=40
        )
        self.requirement_entry.pack(side='left', padx=5)
        self.requirement_entry.insert(0, "Et enkelt program som beregner areal av rektangel")
        
        # Knapper
        btn_frame = tk.Frame(bottom_frame, bg='#252526')
        btn_frame.pack(side='right', padx=10, pady=10)
        
        self.start_btn = tk.Button(
            btn_frame,
            text="▶ START",
            command=self.start_protokoll,
            bg='#4ec9b0',
            fg='black',
            font=('Segoe UI', 9, 'bold'),
            relief='flat',
            cursor='hand2',
            width=10
        )
        self.start_btn.pack(side='left', padx=2)
        
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ STOPP",
            command=self.stopp_protokoll,
            bg='#f44747',
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2',
            width=10,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=2)
        
        self.clear_btn = tk.Button(
            btn_frame,
            text="🗑 TØM",
            command=self.clear_log,
            bg='#3c3c3c',
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2',
            width=8
        )
        self.clear_btn.pack(side='left', padx=2)
        
        # Godkjennings-knapper (skjult som standard)
        self.approval_frame = tk.Frame(bottom_frame, bg='#252526')
        
        tk.Label(
            self.approval_frame,
            text="GODKJENN FJKS:",
            font=('Segoe UI', 9, 'bold'),
            bg='#252526',
            fg='#ffcc00'
        ).pack(side='left', padx=5)
        
        self.approve_btn = tk.Button(
            self.approval_frame,
            text="✅ GODKJENN",
            command=lambda: self.send_approval(True),
            bg='#4ec9b0',
            fg='black',
            font=('Segoe UI', 9, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        self.approve_btn.pack(side='left', padx=2)
        
        self.reject_btn = tk.Button(
            self.approval_frame,
            text="❌ AVVIS",
            command=lambda: self.send_approval(False),
            bg='#f44747',
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2'
        )
        self.reject_btn.pack(side='left', padx=2)
    
    def start_websocket_thread(self):
        """Start WebSocket-klient i egen tråd"""
        def run_websocket():
            asyncio.run(self.websocket_loop())
        
        self.ws_thread = threading.Thread(target=run_websocket, daemon=True)
        self.ws_thread.start()
    
    async def websocket_loop(self):
        """Hovedloop for WebSocket-kommunikasjon"""
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    self.websocket = ws
                    self.is_connected = True
                    self.update_connection_status(True)
                    
                    # Lytt på meldinger fra server
                    async for message in ws:
                        await self.handle_message(message)
                        
            except Exception as e:
                self.is_connected = False
                self.update_connection_status(False)
                print(f"[WS FEIL] {e}")
                time.sleep(5)  # Vent før reconnect
    
    async def handle_message(self, message):
        """Håndter melding fra Lenovo"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            # Legg i kø for UI-oppdatering
            self.message_queue.put(data)
            
        except Exception as e:
            print(f"[FEIL] Kunne ikke parse melding: {e}")
    
    def start_ui_updater(self):
        """Start UI-oppdateringsloop"""
        self.update_ui()
    
    def update_ui(self):
        """Oppdater UI fra meldingskø"""
        try:
            while True:
                msg = self.message_queue.get_nowait()
                self.process_ui_message(msg)
        except queue.Empty:
            pass
        finally:
            if self.running:
                self.root.after(100, self.update_ui)
    
    def process_ui_message(self, msg):
        """Prosesser melding og oppdater UI"""
        msg_type = msg.get("type")
        data = msg.get("data", {})
        
        if msg_type == "connected":
            self.log("Tilkoblet Lenovo Sandkasse!")
            
        elif msg_type == "log":
            level = data.get("level", "INFO")
            message = data.get("message", "")
            self.log(f"[{level}] {message}")
            
        elif msg_type == "status":
            self.update_status(data)
            
        elif msg_type == "code":
            self.update_code(data.get("code", ""), data.get("filename", "main.py"))
            
        elif msg_type == "stats":
            self.update_stats(data)
            
        elif msg_type == "approval_request":
            self.show_approval_dialog(data)
            
        elif msg_type == "validation_report":
            self.show_validation_report(data)
            
        elif msg_type == "completed":
            self.log(f"✅ Prosjekt fullført: {data.get('prosjekt')}")
            self.log(f"   Versjon: {data.get('versjon')}")
            self.log(f"   Lokasjon: {data.get('lokasjon')}")
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
    
    def update_connection_status(self, connected):
        """Oppdater tilkoblingsstatus i UI"""
        if connected:
            self.conn_label.config(
                text=f"🔗 Tilkoblet Lenovo ({self.lenovo_ip})",
                fg='#4ec9b0'
            )
        else:
            self.conn_label.config(
                text=f"⏳ Kobler til Lenovo...",
                fg='#ffcc00'
            )
    
    def update_status(self, data):
        """Oppdater status-visning"""
        status = data.get("status", "ukjent")
        fase = data.get("fase", 0)
        progress = data.get("progress", 0)
        
        self.current_fase = fase
        self.status_label.config(text=f"Status: {status.upper()}")
        
        # Oppdater fase-indikatorer
        for num, label in self.fase_labels.items():
            if num < fase:
                label.config(bg='#4ec9b0', fg='white')  # Fullført
            elif num == fase:
                label.config(bg='#007acc', fg='white')  # Aktiv
            else:
                label.config(bg='#3c3c3c', fg='#808080')  # Venter
        
        # Oppdater fremdrift
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{int(progress)}%")
    
    def update_code(self, code, filename):
        """Oppdater kode-visning"""
        self.code_box.delete(1.0, tk.END)
        self.code_box.insert(1.0, code)
        
        # Enkel syntax highlighting
        self.apply_syntax_highlighting()
    
    def apply_syntax_highlighting(self):
        """Bruk enkel syntax highlighting"""
        text = self.code_box.get(1.0, tk.END)
        
        # Highlight keywords (enkel versjon)
        keywords = ['def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'with']
        for keyword in keywords:
            start = 1.0
            while True:
                start = self.code_box.search(r'\b' + keyword + r'\b', start, tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(keyword)}c"
                self.code_box.tag_add('keyword', start, end)
                start = end
    
    def update_stats(self, data):
        """Oppdater statistikk"""
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        
        stats_str = f"""Kjøringer: {data.get('runs', 0)}
Feil: {data.get('errors', 0)}
Fikset: {data.get('fixed', 0)}
Suksessrate: {data.get('success_rate', 0):.1f}%"""
        
        self.stats_text.insert(1.0, stats_str)
        self.stats_text.config(state='disabled')
    
    def show_approval_dialog(self, data):
        """Vis godkjenningsforespørsel"""
        self.log("⚠️ GODKJENNING KREVES!")
        self.log(f"   {data.get('description', '')}")
        
        # Vis godkjenningsknapper
        self.approval_frame.pack(side='left', padx=10, pady=10)
        
        # Vis popup
        messagebox.showinfo(
            "Godkjenning kreves",
            f"En fiks har blitt foreslått og krever din godkjenning.\n\n"
            f"Beskrivelse: {data.get('description', '')}\n\n"
            f"Bruk knappene nederst for å godkjenne eller avvise."
        )
    
    def send_approval(self, approved):
        """Send godkjenningsrespons til Lenovo"""
        if self.websocket:
            msg = {
                "type": "approval_response",
                "data": {"approved": approved}
            }
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps(msg)),
                asyncio.get_event_loop()
            )
        
        # Skjul godkjenningsknapper
        self.approval_frame.pack_forget()
        
        self.log(f"{'✅ Godkjent' if approved else '❌ Avvist'}")
    
    def show_validation_report(self, data):
        """Vis valideringsrapport"""
        self.log("📊 VALIDERINGSRAPPORT:")
        self.log(f"   Testdekning: {data.get('test_coverage', 0):.1f}%")
        self.log(f"   Lint: {'✅ OK' if data.get('lint_success') else '⚠️ Advarsler'}")
        self.log(f"   Sikkerhet: {data.get('security_issues', 0)} kritiske funn")
    
    def log(self, message):
        """Legg til logg-melding"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_box.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_box.see(tk.END)
    
    def start_protokoll(self):
        """Start protokoll på Lenovo"""
        if not self.is_connected:
            messagebox.showerror("Ikke tilkoblet", 
                f"Kan ikke koble til Lenovo på {self.lenovo_ip}:{self.lenovo_port}\n"
                f"Sjekk at:\n"
                f"1. Lenovo er påslått\n"
                f"2. Tailscale kjører på begge maskiner\n"
                f"3. protokoll_server.py kjører på Lenovo")
            return
        
        navn = self.project_entry.get().strip()
        krav = self.requirement_entry.get().strip()
        
        if not navn or not krav:
            messagebox.showerror("Mangler input", "Fyll inn prosjektnavn og krav")
            return
        
        # Send start-melding
        msg = {
            "type": "start_protokoll",
            "data": {
                "navn": navn,
                "krav": krav
            }
        }
        
        if self.websocket:
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps(msg)),
                asyncio.get_event_loop()
            )
        
        self.log(f"🚀 Starter protokoll: {navn}")
        self.log(f"   Krav: {krav}")
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.current_prosjekt = navn
    
    def stopp_protokoll(self):
        """Stopp pågående protokoll"""
        if self.websocket:
            msg = {"type": "stopp_protokoll"}
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps(msg)),
                asyncio.get_event_loop()
            )
        
        self.log("⏹ Stopp-signal sendt")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
    
    def clear_log(self):
        """Tøm logg"""
        self.log_box.delete(1.0, tk.END)
        self.code_box.delete(1.0, tk.END)


def main():
    """Hovedfunksjon"""
    # Sjekk avhengigheter
    try:
        import websockets
    except ImportError:
        print("Installerer websockets...")
        import subprocess
        subprocess.run(["pip", "install", "websockets"])
    
    root = tk.Tk()
    app = ProtokollMonitor(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nAvslutter...")
    finally:
        app.running = False


if __name__ == "__main__":
    main()
