#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOMPLETT SYSTEMTEST - Den Digitale Riggen
Sjekker alle komponenter for websider, apper, rapporter, grafer, bilder, videoer
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path

# Farger for output (Windows-kompatibel)
class Colors:
    OK = "[OK]"
    FAIL = "[FAIL]"
    WARN = "[WARN]"
    INFO = "[INFO]"

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_result(status, text, detail=""):
    if detail:
        print(f"{status} {text}")
        print(f"     {detail}")
    else:
        print(f"{status} {text}")

# ============================================================================
# TEST 1: SELVHELBREDENDE SYSTEM
# ============================================================================

def test_self_healing():
    print_header("TEST 1: SELVHELBREDENDE SYSTEM")
    
    sys.path.insert(0, r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing')
    
    results = []
    
    # Test imports
    try:
        from error_handler import ErrorHandler
        from ai_fixer import AIFixer
        from ai_integrasjon import AIAgent
        from self_healing_wrapper import SelfHealingSystem, heal
        print_result(Colors.OK, "Alle moduler importert")
        results.append(True)
    except Exception as e:
        print_result(Colors.FAIL, f"Import-feil: {e}")
        results.append(False)
    
    # Test config
    try:
        import yaml
        config_path = r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing\config.yaml'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print_result(Colors.OK, "Konfigurasjon lest", 
                    f"Max attempts: {config['healing']['max_attempts']}, "
                    f"Auto-apply: {config['safety']['allow_auto_apply']}")
        results.append(True)
    except Exception as e:
        print_result(Colors.FAIL, f"Konfigurasjon: {e}")
        results.append(False)
    
    # Test error handler
    try:
        handler = ErrorHandler(log_dir=r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing\logs')
        print_result(Colors.OK, "ErrorHandler initialisert")
        
        # Sjekk patterns
        patterns = handler._load_patterns()
        print_result(Colors.INFO, f"Lagrede feil: {len(patterns)}")
        results.append(True)
    except Exception as e:
        print_result(Colors.FAIL, f"ErrorHandler: {e}")
        results.append(False)
    
    return all(results)

# ============================================================================
# TEST 2: KUBERNETES TJENESTER
# ============================================================================

def test_kubernetes_services():
    print_header("TEST 2: KUBERNETES TJENESTER (anita-agent)")
    
    results = []
    
    # Sjekk kubectl
    try:
        result = subprocess.run(['kubectl', 'get', 'pods', '-n', 'anita-agent'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_result(Colors.OK, "Kubernetes tilkoblet")
            results.append(True)
        else:
            print_result(Colors.FAIL, "Kubernetes ikke tilgjengelig")
            results.append(False)
    except Exception as e:
        print_result(Colors.FAIL, f"Kubernetes-feil: {e}")
        return False
    
    # Sjekk tjenester
    services = {
        'anita-agent': {'port': 30007, 'path': '/health', 'desc': 'AI Agent'},
        'anythingllm': {'port': 30006, 'path': '/api/v1/ping', 'desc': 'AnythingLLM'},
        'comfyui': {'port': 30005, 'path': '/', 'desc': 'ComfyUI (bildegenerering)'},
        'telegram-webhook': {'port': 30002, 'path': '/health', 'desc': 'Telegram Bot'}
    }
    
    import requests
    
    for svc_name, svc_info in services.items():
        try:
            # Sjekk pod status
            result = subprocess.run(
                ['kubectl', 'get', 'pods', '-n', 'anita-agent', '-l', f'app={svc_name}', 
                 '-o', 'jsonpath={.items[0].status.phase}'],
                capture_output=True, text=True, timeout=5
            )
            status = result.stdout.strip()
            
            if status == 'Running':
                ready_result = subprocess.run(
                    ['kubectl', 'get', 'pods', '-n', 'anita-agent', '-l', f'app={svc_name}',
                     '-o', 'jsonpath={.items[0].status.containerStatuses[0].ready}'],
                    capture_output=True, text=True, timeout=5
                )
                ready = ready_result.stdout.strip() == 'true'
                
                if ready:
                    print_result(Colors.OK, f"{svc_info['desc']}", f"Pod: Running, Ready")
                else:
                    print_result(Colors.WARN, f"{svc_info['desc']}", f"Pod: Running, ikke Ready")
                results.append(ready)
            elif status:
                print_result(Colors.WARN, f"{svc_info['desc']}", f"Status: {status}")
                results.append(False)
            else:
                print_result(Colors.FAIL, f"{svc_info['desc']}", "Pod ikke funnet")
                results.append(False)
                
        except Exception as e:
            print_result(Colors.FAIL, f"{svc_info['desc']}: {e}")
            results.append(False)
    
    return any(results)  # Minst en tjeneste må fungere

# ============================================================================
# TEST 3: WEBUTVIKLINGSVERKTØY
# ============================================================================

def test_web_dev_tools():
    print_header("TEST 3: WEBUTVIKLINGSVERKTØY")
    
    results = []
    
    # Sjekk Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_result(Colors.OK, f"Node.js", result.stdout.strip())
            results.append(True)
        else:
            print_result(Colors.WARN, "Node.js ikke installert")
            results.append(False)
    except:
        print_result(Colors.WARN, "Node.js ikke tilgjengelig")
        results.append(False)
    
    # Sjekk npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_result(Colors.OK, f"npm", f"v{result.stdout.strip()}")
    except:
        pass
    
    # Sjekk Python web-rammeverk
    web_libs = [
        ('flask', 'Flask'),
        ('django', 'Django'),
        ('fastapi', 'FastAPI'),
        ('requests', 'Requests (HTTP)'),
        ('websockets', 'WebSockets'),
    ]
    
    for lib, name in web_libs:
        try:
            __import__(lib)
            print_result(Colors.OK, name)
            results.append(True)
        except ImportError:
            print_result(Colors.WARN, f"{name} ikke installert")
            results.append(False)
    
    return any(results)

# ============================================================================
# TEST 4: DATAVISUALISERING OG RAPPORTER
# ============================================================================

def test_data_visualization():
    print_header("TEST 4: DATAVISUALISERING OG RAPPORTER")
    
    results = []
    
    viz_libs = [
        ('matplotlib', 'Matplotlib', 'Grafer og plots'),
        ('plotly', 'Plotly', 'Interaktive grafer'),
        ('pandas', 'Pandas', 'Dataanalyse'),
        ('numpy', 'NumPy', 'Numerisk computing'),
        ('PIL', 'Pillow', 'Bildebehandling'),
    ]
    
    for lib, name, desc in viz_libs:
        try:
            module = __import__(lib)
            version = getattr(module, '__version__', 'ukjent')
            print_result(Colors.OK, name, f"{desc} (v{version})")
            results.append(True)
        except ImportError:
            print_result(Colors.WARN, name, f"{desc} - ikke installert")
            results.append(False)
    
    # Sjekk om vi kan generere grafer
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        
        # Lag test-graf
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_title('Test-graf')
        
        test_file = r'C:\Users\Emil\Desktop\test_graph.png'
        plt.savefig(test_file)
        plt.close()
        
        if os.path.exists(test_file):
            os.remove(test_file)
            print_result(Colors.OK, "Matplotlib fungerer", "Kan generere PNG-grafer")
            results.append(True)
    except Exception as e:
        print_result(Colors.WARN, f"Matplotlib test feilet: {e}")
        results.append(False)
    
    return any(results)

# ============================================================================
# TEST 5: MEDIA GENERERING
# ============================================================================

def test_media_generation():
    print_header("TEST 5: MEDIA GENERERING")
    
    results = []
    
    # Sjekk bildegenerering (ComfyUI/Kubernetes)
    try:
        result = subprocess.run(
            ['kubectl', 'get', 'pods', '-n', 'anita-agent', '-l', 'app=comfyui',
             '-o', 'jsonpath={.items[0].status.phase}'],
            capture_output=True, text=True, timeout=5
        )
        status = result.stdout.strip()
        
        if status == 'Running':
            print_result(Colors.OK, "ComfyUI (Kubernetes)", "Tilgjengelig på port 30005")
            results.append(True)
        else:
            print_result(Colors.WARN, "ComfyUI", f"Status: {status} - installerer fortsatt?")
            results.append(False)
    except Exception as e:
        print_result(Colors.WARN, f"ComfyUI: {e}")
        results.append(False)
    
    # Sjekk om Stable Diffusion er tilgjengelig lokalt
    try:
        import requests
        resp = requests.get('http://localhost:7860/sdapi/v1/sd-models', timeout=2)
        if resp.status_code == 200:
            print_result(Colors.OK, "Stable Diffusion (lokal)", "Tilgjengelig på port 7860")
            results.append(True)
    except:
        print_result(Colors.INFO, "Stable Diffusion (lokal)", "Ikke tilgjengelig på localhost:7860")
    
    # Sjekk OpenCV for video
    try:
        import cv2
        version = cv2.__version__
        print_result(Colors.OK, "OpenCV", f"Video/behandling (v{version})")
        results.append(True)
    except ImportError:
        print_result(Colors.WARN, "OpenCV", "Ikke installert - trengs for video")
        results.append(False)
    
    return any(results)

# ============================================================================
# TEST 6: 6-FASE PROTOKOLL
# ============================================================================

def test_6fase_protokoll():
    print_header("TEST 6: 6-FASE UTVIKLINGSPROTOKOLL")
    
    results = []
    
    # Sjekk at sandkasse_protokoll finnes
    protokoll_files = [
        r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\sandkasse_protokoll_NY.py',
        r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\enkel_server_NY.py',
        r'C:\AI_System\protokoll\enkel_server.py',
    ]
    
    for f in protokoll_files:
        if os.path.exists(f):
            print_result(Colors.OK, os.path.basename(f))
            results.append(True)
        else:
            print_result(Colors.WARN, f"Mangler: {f}")
            results.append(False)
    
    # Sjekk arkivstruktur
    arkiv_dir = r'C:\AI_System\arkiv'
    if os.path.exists(arkiv_dir):
        projects = [d for d in os.listdir(arkiv_dir) if os.path.isdir(os.path.join(arkiv_dir, d))]
        print_result(Colors.OK, f"Arkivmappe", f"{len(projects)} prosjekter")
        for p in projects:
            p_path = os.path.join(arkiv_dir, p)
            versions = len([d for d in os.listdir(p_path) if d.startswith('v_')])
            print(f"     - {p}: {versions} versjon(er)")
        results.append(True)
    else:
        print_result(Colors.FAIL, "Arkivmappe ikke funnet")
        results.append(False)
    
    return any(results)

# ============================================================================
# HOVEDFUNKSJON
# ============================================================================

def main():
    print("\n" + "="*70)
    print("  KOMPLETT SYSTEMTEST - Den Digitale Riggen v2.0")
    print("  Tester alle komponenter for websider, apper, rapporter, media")
    print("="*70)
    
    all_results = {}
    
    try:
        all_results['Self-Healing'] = test_self_healing()
    except Exception as e:
        print(f"{Colors.FAIL} Self-Healing test feilet: {e}")
        all_results['Self-Healing'] = False
    
    try:
        all_results['Kubernetes'] = test_kubernetes_services()
    except Exception as e:
        print(f"{Colors.FAIL} Kubernetes test feilet: {e}")
        all_results['Kubernetes'] = False
    
    try:
        all_results['Web Dev'] = test_web_dev_tools()
    except Exception as e:
        print(f"{Colors.FAIL} Web Dev test feilet: {e}")
        all_results['Web Dev'] = False
    
    try:
        all_results['Data Viz'] = test_data_visualization()
    except Exception as e:
        print(f"{Colors.FAIL} Data Viz test feilet: {e}")
        all_results['Data Viz'] = False
    
    try:
        all_results['Media Gen'] = test_media_generation()
    except Exception as e:
        print(f"{Colors.FAIL} Media Gen test feilet: {e}")
        all_results['Media Gen'] = False
    
    try:
        all_results['6-Fase Protokoll'] = test_6fase_protokoll()
    except Exception as e:
        print(f"{Colors.FAIL} 6-Fase test feilet: {e}")
        all_results['6-Fase Protokoll'] = False
    
    # OPPSUMMERING
    print_header("OPPSUMMERING")
    
    passed = sum(1 for v in all_results.values() if v)
    total = len(all_results)
    
    for name, result in all_results.items():
        status = Colors.OK if result else Colors.FAIL
        print(f"{status} {name}")
    
    print(f"\nTotalt: {passed}/{total} hovedkategorier fungerer")
    
    print("\n" + "="*70)
    if passed == total:
        print("  *** ALLE SYSTEMER OPERATIVE! ***")
        print("  Du kan lage: websider, apper, rapporter, grafer, bilder, videoer")
    elif passed >= total * 0.7:
        print("  *** SYSTEMET ER FUNKSJONELT ***")
        print("  De fleste komponenter fungerer. Se detaljer over.")
    else:
        print("  *** FLERE KOMPONENTER MANGLER ***")
        print("  Se detaljer over for hva som må fikses.")
    print("="*70)
    
    # Lag rapport
    report_file = r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\system_test_rapport.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("SYSTEMTEST RAPPORT\n")
        f.write("="*50 + "\n\n")
        for name, result in all_results.items():
            f.write(f"{'[OK]' if result else '[FAIL]'} {name}\n")
        f.write(f"\nTotalt: {passed}/{total}\n")
        f.write(f"\nGenerert: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"\n[INFO] Rapport lagret til: {report_file}")

if __name__ == "__main__":
    main()
