#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Viewer GUI - Et lite vindu som viser selvhelbredende systemet i aksjon
For Acer PC - Windows
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import queue
import time
import sys
import os
from datetime import datetime

# Farger for dark mode
COLORS = {
    'bg': '#1e1e1e',
    'fg': '#d4d4d4',
    'accent': '#007acc',
    'success': '#4ec9b0',
    'error': '#f44747',
    'warning': '#cca700',
    'code': '#ce9178',
    'info': '#569cd6'
}

class CodeViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Self-Healing Code Viewer")
        self.root.geometry("900x650")
        self.root.configure(bg=COLORS['bg'])
        self.root.minsize(700, 500)
        
        # Message queue for thread-safe updates
        self.msg_queue = queue.Queue()
        
        self.setup_ui()
        self.running = False
        self.system_thread = None
        
        # Start queue checker
        self.check_queue()
        
    def setup_ui(self):
        """Sett opp GUI komponenter"""
        # Header
        header = tk.Frame(self.root, bg=COLORS['bg'], height=40)
        header.pack(fill='x', padx=10, pady=5)
        
        self.title_label = tk.Label(
            header, 
            text="🔄 Self-Healing System - Live Code Viewer",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['info']
        )
        self.title_label.pack(side='left')
        
        self.status_label = tk.Label(
            header,
            text="⏹️ STOPPET",
            font=('Segoe UI', 10),
            bg=COLORS['bg'],
            fg=COLORS['error']
        )
        self.status_label.pack(side='right')
        
        # Hovedområde med to paneler
        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Venstre panel - Kodevisning
        left_frame = tk.LabelFrame(
            main_frame,
            text="📝 Live Kode & Handlinger",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        )
        left_frame.pack(side='left', fill='both', expand=True)
        
        self.code_text = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#252526',
            fg=COLORS['fg'],
            insertbackground=COLORS['fg'],
            height=25
        )
        self.code_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Høyre panel - Status & Logger
        right_frame = tk.Frame(main_frame, bg=COLORS['bg'], width=250)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Statistikk
        stats_frame = tk.LabelFrame(
            right_frame,
            text="📊 Statistikk",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        )
        stats_frame.pack(fill='x', pady=(0, 10))
        
        self.stats_labels = {}
        stats = [
            ('runs', 'Kjøringer:', '0'),
            ('errors', 'Feil:', '0'),
            ('fixed', 'Fikset:', '0'),
            ('learning', 'Lært:', '0')
        ]
        
        for key, label, default in stats:
            row = tk.Frame(stats_frame, bg=COLORS['bg'])
            row.pack(fill='x', padx=5, pady=2)
            tk.Label(row, text=label, bg=COLORS['bg'], fg=COLORS['fg'], 
                    font=('Segoe UI', 9)).pack(side='left')
            lbl = tk.Label(row, text=default, bg=COLORS['bg'], fg=COLORS['info'],
                          font=('Segoe UI', 9, 'bold'))
            lbl.pack(side='right')
            self.stats_labels[key] = lbl
        
        # Logg-visning
        log_frame = tk.LabelFrame(
            right_frame,
            text="📋 Siste Hendelser",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        )
        log_frame.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(
            log_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#252526',
            fg=COLORS['fg'],
            height=15,
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # AI Status
        ai_frame = tk.LabelFrame(
            right_frame,
            text="🤖 AI Status",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['fg']
        )
        ai_frame.pack(fill='x', pady=(10, 0))
        
        self.ai_status = tk.Label(
            ai_frame,
            text="Sjekker...",
            bg=COLORS['bg'],
            fg=COLORS['warning'],
            font=('Segoe UI', 9)
        )
        self.ai_status.pack(pady=5)
        
        # Kontroll-knapper
        button_frame = tk.Frame(self.root, bg=COLORS['bg'])
        button_frame.pack(fill='x', padx=10, pady=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶️  Start System",
            command=self.start_system,
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['success'],
            fg='white',
            relief='flat',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️  Stopp",
            command=self.stop_system,
            font=('Segoe UI', 10),
            bg=COLORS['error'],
            fg='white',
            relief='flat',
            padx=20,
            pady=5,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️  Tøm",
            command=self.clear_display,
            font=('Segoe UI', 10),
            bg='#3c3c3c',
            fg=COLORS['fg'],
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.clear_btn.pack(side='right', padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            button_frame,
            mode='indeterminate',
            length=150
        )
        self.progress.pack(side='right', padx=10)
        
    def check_queue(self):
        """Sjekk etter meldinger fra worker thread"""
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                self.handle_message(msg)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def handle_message(self, msg):
        """Håndter innkommende meldinger"""
        msg_type = msg.get('type', 'info')
        content = msg.get('content', '')
        
        if msg_type == 'code':
            self.append_code(content, msg.get('highlight', False))
        elif msg_type == 'log':
            self.append_log(content, msg.get('level', 'info'))
        elif msg_type == 'stats':
            self.update_stats(msg.get('stats', {}))
        elif msg_type == 'ai_status':
            self.ai_status.config(
                text=content,
                fg=COLORS['success'] if 'Klar' in content else COLORS['error']
            )
        elif msg_type == 'status':
            self.status_label.config(
                text=content,
                fg=COLORS['success'] if 'KJØRER' in content else COLORS['error']
            )
    
    def append_code(self, text, highlight=False):
        """Legg til tekst i kodevinduet"""
        self.code_text.insert('end', text + '\n')
        if highlight:
            # Highlight siste linje
            end_idx = self.code_text.index('end-1c')
            start_idx = self.code_text.index('end-2l')
            self.code_text.tag_add('highlight', start_idx, end_idx)
            self.code_text.tag_config('highlight', background='#264f78')
        self.code_text.see('end')
        self.code_text.update()
    
    def append_log(self, text, level='info'):
        """Legg til logg-melding"""
        self.log_text.config(state='normal')
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        color = {
            'info': COLORS['info'],
            'success': COLORS['success'],
            'error': COLORS['error'],
            'warning': COLORS['warning']
        }.get(level, COLORS['fg'])
        
        self.log_text.insert('end', f'[{timestamp}] ', 'timestamp')
        self.log_text.tag_config('timestamp', foreground='#808080')
        
        self.log_text.insert('end', f'{text}\n', level)
        self.log_text.tag_config(level, foreground=color)
        
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.log_text.update()
    
    def update_stats(self, stats):
        """Oppdater statistikk-labels"""
        for key, value in stats.items():
            if key in self.stats_labels:
                self.stats_labels[key].config(text=str(value))
    
    def clear_display(self):
        """Tøm alle visninger"""
        self.code_text.delete(1.0, 'end')
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, 'end')
        self.log_text.config(state='disabled')
    
    def start_system(self):
        """Start selvhelbredende system i egen thread"""
        if self.running:
            return
        
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress.start(10)
        
        self.msg_queue.put({
            'type': 'status',
            'content': '▶️ KJØRER'
        })
        
        # Start system i egen thread
        self.system_thread = threading.Thread(target=self.run_system, daemon=True)
        self.system_thread.start()
    
    def stop_system(self):
        """Stopp systemet"""
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress.stop()
        
        self.msg_queue.put({
            'type': 'status',
            'content': '⏹️ STOPPET'
        })
        
        self.append_log('System stoppet av bruker', 'warning')
    
    def run_system(self):
        """Hovedsystem-loop (kjører i egen thread)"""
        try:
            # Simuler selvhelbredende system
            self.simulate_self_healing()
        except Exception as e:
            self.msg_queue.put({
                'type': 'log',
                'content': f'Feil i system: {e}',
                'level': 'error'
            })
        finally:
            self.running = False
            self.msg_queue.put({
                'type': 'status',
                'content': '⏹️ FERDIG'
            })
    
    def simulate_self_healing(self):
        """Simuler selvhelbredende prosess"""
        import random
        
        # Test scenarier
        scenarios = [
            {
                'name': 'prosess_data()',
                'code': 'def prosess_data(data):\n    return data[0] + data[-1]',
                'error': 'IndexError: list index out of range',
                'input': '[]',
                'fix': 'def prosess_data(data):\n    if not data:\n        return 0\n    return data[0] + data[-1]'
            },
            {
                'name': 'del_numbers()',
                'code': 'def del_numbers(a, b):\n    return a / b',
                'error': 'ZeroDivisionError: division by zero',
                'input': 'del_numbers(10, 0)',
                'fix': 'def del_numbers(a, b):\n    if b == 0:\n        return None\n    return a / b'
            },
            {
                'name': 'hent_config()',
                'code': 'def hent_config(key):\n    return config[key]',
                'error': 'KeyError: timeout',
                'input': 'hent_config("timeout")',
                'fix': 'def hent_config(key):\n    return config.get(key)'
            }
        ]
        
        stats = {'runs': 0, 'errors': 0, 'fixed': 0, 'learning': 0}
        
        while self.running:
            scenario = random.choice(scenarios)
            stats['runs'] += 1
            
            # Vis kode
            self.msg_queue.put({
                'type': 'code',
                'content': f'\n{"="*50}\n>>> Kjører: {scenario["name"]}'
            })
            self.msg_queue.put({
                'type': 'code',
                'content': scenario['code']
            })
            self.msg_queue.put({
                'type': 'log',
                'content': f'Starter {scenario["name"]}',
                'level': 'info'
            })
            
            time.sleep(1.5)
            
            # Simuler feil
            stats['errors'] += 1
            self.msg_queue.put({
                'type': 'code',
                'content': f'[FEIL] {scenario["error"]}',
                'highlight': True
            })
            self.msg_queue.put({
                'type': 'log',
                'content': f'Fanget: {scenario["error"]}',
                'level': 'error'
            })
            
            time.sleep(0.5)
            
            # Aktiver healing
            self.msg_queue.put({
                'type': 'code',
                'content': '[HEAL] Aktiverer selvhelbreding...'
            })
            self.msg_queue.put({
                'type': 'log',
                'content': 'Analyserer feil med AI...',
                'level': 'warning'
            })
            
            time.sleep(1.5)
            
            # Generer fiks
            stats['fixed'] += 1
            stats['learning'] += 1
            self.msg_queue.put({
                'type': 'code',
                'content': f'[FIX] Generert fiks:\n{scenario["fix"]}',
                'highlight': True
            })
            self.msg_queue.put({
                'type': 'log',
                'content': f'Fiks generert for {scenario["name"]}',
                'level': 'success'
            })
            
            time.sleep(0.5)
            
            # Backup og anvend
            self.msg_queue.put({
                'type': 'code',
                'content': '[BACKUP] Lagrer backup...\n[APPLY] Anvender fiks...'
            })
            
            time.sleep(0.5)
            
            # Suksess
            self.msg_queue.put({
                'type': 'code',
                'content': f'[OK] {scenario["name"]} vellykket!\n{"="*50}'
            })
            self.msg_queue.put({
                'type': 'log',
                'content': f'{scenario["name"]} fikset og fullført',
                'level': 'success'
            })
            
            # Oppdater stats
            self.msg_queue.put({
                'type': 'stats',
                'stats': stats
            })
            
            time.sleep(2)
            
            # Sjekk om vi skal fortsette
            if not self.running:
                break

def main():
    """Hovedfunksjon"""
    root = tk.Tk()
    
    # Sett dark mode
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = CodeViewerGUI(root)
    
    # Center vindu
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == '__main__':
    main()
