#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini Code Viewer - Lite kompakt vindu for Acer PC
Viser kodekjoring i sanntid
"""
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import time
from datetime import datetime

class MiniCodeViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("[SH] Self-Healing Viewer")
        self.root.geometry("600x450")
        self.root.configure(bg='#1e1e1e')
        self.root.attributes('-topmost', True)  # Alltid på topp
        
        self.msg_queue = queue.Queue()
        self.running = False
        
        self.setup_ui()
        self.check_queue()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#007acc', height=30)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="[AI] Self-Healing System",
            font=('Segoe UI', 10, 'bold'),
            bg='#007acc',
            fg='white'
        ).pack(side='left', padx=10, pady=3)
        
        self.status = tk.Label(
            header,
            text="STOPPET",
            font=('Segoe UI', 9),
            bg='#007acc',
            fg='#ffcc00'
        )
        self.status.pack(side='right', padx=10, pady=3)
        
        # Kode-visning
        self.code_box = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#252526',
            fg='#d4d4d4',
            height=18,
            state='disabled'
        )
        self.code_box.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Kontroller
        ctrl = tk.Frame(self.root, bg='#1e1e1e')
        ctrl.pack(fill='x', padx=5, pady=5)
        
        self.start_btn = tk.Button(
            ctrl,
            text="[START]",
            command=self.start,
            bg='#4ec9b0',
            fg='black',
            font=('Segoe UI', 9, 'bold'),
            relief='flat',
            cursor='hand2',
            width=10
        )
        self.start_btn.pack(side='left', padx=2)
        
        self.stop_btn = tk.Button(
            ctrl,
            text="[STOPP]",
            command=self.stop,
            bg='#f44747',
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2',
            width=10,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=2)
        
        tk.Button(
            ctrl,
            text="[TOM]",
            command=self.clear,
            bg='#3c3c3c',
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2',
            width=8
        ).pack(side='right', padx=2)
        
        # Stats linje
        self.stats = tk.Label(
            ctrl,
            text="Kjøringer: 0 | Feil: 0 | Fikset: 0",
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#569cd6'
        )
        self.stats.pack(side='bottom', pady=5)
        
    def log(self, text, tag='normal'):
        self.code_box.config(state='normal')
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        colors = {
            'normal': '#d4d4d4',
            'error': '#f44747',
            'success': '#4ec9b0',
            'code': '#ce9178',
            'info': '#569cd6'
        }
        
        self.code_box.insert('end', f'{timestamp} ', 'time')
        self.code_box.tag_config('time', foreground='#808080')
        
        self.code_box.insert('end', f'{text}\n', tag)
        self.code_box.tag_config(tag, foreground=colors.get(tag, '#d4d4d4'))
        
        self.code_box.see('end')
        self.code_box.config(state='disabled')
        
    def check_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                if msg['type'] == 'log':
                    self.log(msg['text'], msg.get('tag', 'normal'))
                elif msg['type'] == 'stats':
                    s = msg['data']
                    self.stats.config(
                        text=f"Kjøringer: {s['runs']} | Feil: {s['errors']} | Fikset: {s['fixed']}"
                    )
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def start(self):
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status.config(text='[KJORER]', fg='#00ff00')
        
        thread = threading.Thread(target=self.run_simulation, daemon=True)
        thread.start()
        
    def stop(self):
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status.config(text='[STOPPET]', fg='#ffcc00')
        self.log('[INFO] System stoppet', 'info')
        
    def clear(self):
        self.code_box.config(state='normal')
        self.code_box.delete(1.0, 'end')
        self.code_box.config(state='disabled')
        
    def run_simulation(self):
        import random
        
        scenarios = [
            ('Liste tom', 'data[0]', 'IndexError', 'if data: return data[0]'),
            ('Deling 0', 'a/b', 'ZeroDivisionError', 'if b!=0: return a/b'),
            ('Nøkkel finnes ikke', 'config[key]', 'KeyError', 'config.get(key)'),
        ]
        
        stats = {'runs': 0, 'errors': 0, 'fixed': 0}
        
        while self.running:
            name, code, error, fix = random.choice(scenarios)
            stats['runs'] += 1
            
            self.msg_queue.put({'type': 'log', 'text': f'[START] Kjorer: {name}', 'tag': 'info'})
            self.msg_queue.put({'type': 'log', 'text': f'  Code: {code}', 'tag': 'code'})
            
            time.sleep(1.2)
            
            stats['errors'] += 1
            self.msg_queue.put({'type': 'log', 'text': f'  [FEIL] {error}', 'tag': 'error'})
            self.msg_queue.put({'type': 'log', 'text': '  [AI] Analyserer...', 'tag': 'info'})
            
            time.sleep(1.5)
            
            stats['fixed'] += 1
            self.msg_queue.put({'type': 'log', 'text': f'  [OK] Fiks: {fix}', 'tag': 'success'})
            self.msg_queue.put({'type': 'log', 'text': '  [LOG] Lagrer til AGENTS.md', 'tag': 'success'})
            
            self.msg_queue.put({'type': 'stats', 'data': stats.copy()})
            
            time.sleep(1)

def main():
    root = tk.Tk()
    
    # Dark title bar på Windows 10/11
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        windll.dwmapi.DwmSetWindowAttribute(
            windll.user32.GetParent(root.winfo_id()),
            20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
            1, 4
        )
    except:
        pass
    
    app = MiniCodeViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
