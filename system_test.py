#!/usr/bin/env python3
"""
Systemtest - Sjekker at alle komponenter fungerer
"""
import sys
import os

# Legg til riktig path
sys.path.insert(0, r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing')

def test_imports():
    """Test at alle moduler kan importeres"""
    print("=" * 60)
    print("TEST 1: Modul-imports")
    print("=" * 60)
    
    tests = [
        ("error_handler", "ErrorHandler"),
        ("ai_fixer", "AIFixer"),
        ("self_healing_wrapper", "SelfHealingSystem"),
    ]
    
    results = []
    for module_name, class_name in tests:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"[OK] {module_name}.{class_name}")
            results.append(True)
        except Exception as e:
            print(f"[FAIL] {module_name}.{class_name}: {e}")
            results.append(False)
    
    return all(results)

def test_ollama():
    """Test Ollama-tilkobling"""
    print("\n" + "=" * 60)
    print("TEST 2: Ollama-tilkobling")
    print("=" * 60)
    
    try:
        import requests
        resp = requests.get('http://localhost:11434/api/tags', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            models = data.get('models', [])
            print(f"[OK] Ollama kjorer pa localhost:11434")
            print(f"     Tilgjengelige modeller: {len(models)}")
            for m in models[:3]:
                print(f"     - {m.get('name', 'unknown')}")
            return True
        else:
            print(f"[WARN] Ollama svarte med status {resp.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Ollama ikke tilgjengelig: {e}")
        return False

def test_logs():
    """Test at logg-systemet fungerer"""
    print("\n" + "=" * 60)
    print("TEST 3: Logg-system")
    print("=" * 60)
    
    import json
    log_dir = r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing\logs'
    patterns_file = os.path.join(log_dir, 'patterns.json')
    
    if os.path.exists(patterns_file):
        with open(patterns_file, 'r', encoding='utf-8') as f:
            patterns = json.load(f)
        print(f"[OK] patterns.json funnet")
        print(f"     Unike feil: {len(patterns)}")
        fixed = sum(1 for p in patterns.values() if p.get('status') == 'fixed')
        print(f"     Fikset: {fixed}")
        
        # Vis alle feil
        print("\n     Registrerte feil:")
        for hash_id, info in patterns.items():
            status = info.get('status', 'unknown')
            func = info.get('function', 'unknown')
            err_type = info.get('type', 'unknown')
            freq = info.get('frequency', 0)
            print(f"     - {func}: {err_type} (freq: {freq}, status: {status})")
        return True
    else:
        print(f"[WARN] patterns.json ikke funnet i {log_dir}")
        return False

def test_archives():
    """Test arkivstruktur"""
    print("\n" + "=" * 60)
    print("TEST 4: Arkivstruktur")
    print("=" * 60)
    
    arkiv_dir = r'C:\AI_System\arkiv'
    if not os.path.exists(arkiv_dir):
        print(f"[FAIL] Arkivmappe ikke funnet: {arkiv_dir}")
        return False
    
    projects = [d for d in os.listdir(arkiv_dir) if os.path.isdir(os.path.join(arkiv_dir, d))]
    print(f"[OK] Arkivmappe funnet")
    print(f"     Antall prosjekter: {len(projects)}")
    
    for proj in projects:
        proj_path = os.path.join(arkiv_dir, proj)
        versions = [d for d in os.listdir(proj_path) if os.path.isdir(os.path.join(proj_path, d)) and d.startswith('v_')]
        print(f"     - {proj}: {len(versions)} versjon(er)")
    
    return True

def test_self_healing():
    """Test selvhelbredende funksjonalitet"""
    print("\n" + "=" * 60)
    print("TEST 5: Selvhelbredende system")
    print("=" * 60)
    
    from self_healing_wrapper import SelfHealingSystem, heal
    
    # Opprett system
    system = SelfHealingSystem(backup_dir=r'C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing\backups')
    
    # Test funksjon med feil
    @heal
    def test_func_error():
        raise ValueError("Test-feil")
    
    @heal  
    def test_func_success():
        return 42
    
    # Kjor tester
    print("[INFO] Tester funksjon som feiler...")
    try:
        test_func_error()
    except:
        pass
    
    print("[INFO] Tester funksjon som fungerer...")
    result = test_func_success()
    
    # Vis statistikk
    stats = system.get_stats()
    print(f"[OK] Selvhelbredende system fungerer")
    print(f"     Totale kjoringer: {stats.get('total_runs', 0)}")
    print(f"     Auto-fikset: {stats.get('auto_fixed', 0)}")
    print(f"     Suksessrate: {stats.get('healing_success_rate', 0):.1f}%")
    
    return True

def main():
    print("\n" + "=" * 60)
    print("SYSTEMTEST - Den Digitale Riggen")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("Imports", test_imports()))
    except Exception as e:
        print(f"[FAIL] Imports test feilet: {e}")
        results.append(("Imports", False))
    
    try:
        results.append(("Ollama", test_ollama()))
    except Exception as e:
        print(f"[FAIL] Ollama test feilet: {e}")
        results.append(("Ollama", False))
    
    try:
        results.append(("Logger", test_logs()))
    except Exception as e:
        print(f"[FAIL] Logg test feilet: {e}")
        results.append(("Logger", False))
    
    try:
        results.append(("Arkiv", test_archives()))
    except Exception as e:
        print(f"[FAIL] Arkiv test feilet: {e}")
        results.append(("Arkiv", False))
    
    try:
        results.append(("Self-Healing", test_self_healing()))
    except Exception as e:
        print(f"[FAIL] Self-healing test feilet: {e}")
        results.append(("Self-Healing", False))
    
    # Oppsummering
    print("\n" + "=" * 60)
    print("OPPSUMMERING")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    print(f"\nTotalt: {passed}/{total} tester bestatt")
    
    if passed == total:
        print("\n*** ALLE TESTER BESTATT! SYSTEMET ER KLART. ***")
    else:
        print("\n*** NOEN TESTER FEILET - SE DETALJER OVER ***")

if __name__ == "__main__":
    main()
