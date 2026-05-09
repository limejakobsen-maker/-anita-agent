#!/usr/bin/env python3
"""
Self-Healing Main - Hovedprogram som lærer av feil
Dette programmet blir bedre og bedre jo mer det feiler!
"""
import os
import sys
import time
import random
from datetime import datetime
from self_healing_wrapper import heal, SelfHealingSystem
from error_handler import ErrorHandler

# Initialiser systemet
healing_system = SelfHealingSystem()

print("""
╔══════════════════════════════════════════════════════════╗
║     [AI] SELVHELBREDENDE AI-SYSTEM v1.0                    ║
║     "Hver feil er en mulighet til aa bli bedre"          ║
╚══════════════════════════════════════════════════════════╝
""")

# ============================================
# EKSEMPEL-FUNKSJONER SOM KAN FEILE
# ============================================

@heal
def prosess_data(data_list):
    """
    Prosesserer en dataliste
    Kan feile med IndexError hvis listen er tom
    """
    print(f"[DATA] Prosesserer {len(data_list)} elementer...")
    
    # Risikabel operasjon: henter første og siste element
    first = data_list[0]  # Kan feile hvis tom
    last = data_list[-1]  # Kan feile hvis tom
    
    return {"first": first, "last": last, "count": len(data_list)}

@heal
def del_numbers(a, b):
    """
    Deling av tall
    Kan feile med ZeroDivisionError
    """
    print(f"[MATH] Beregner {a} / {b}...")
    return a / b

@heal
def hent_konfig(nøkkel):
    """
    Henter konfigurasjonsverdi
    Kan feile med KeyError
    """
    config = {
        "database_url": "postgresql://localhost/db",
        "timeout": 30,
        "retry_count": 3
    }
    
    print(f"[CONF] Henter konfig for '{nøkkel}'...")
    return config[nøkkel]  # Kan feile hvis nøkkel ikke finnes

@heal
def parse_json(json_string):
    """
    Parser JSON-data
    Kan feile med ulike exceptions
    """
    import json
    print("[JSON] Parser JSON...")
    return json.loads(json_string)

@heal
def kjør_ekstern_kommando(kommando):
    """
    Simulerer kjøring av ekstern kommando
    Kan feile med fil ikke funnet, tilgangsfeil, etc.
    """
    print(f"[CMD] Kjorer: {kommando}")
    
    # Simuler ulike feilscenarier
    if random.random() < 0.3:  # 30% sjanse for feil
        feil_type = random.choice([
            FileNotFoundError,
            PermissionError,
            TimeoutError
        ])
        raise feil_type(f"Simulert feil for {kommando}")
    
    return f"Resultat av {kommando}"

# ============================================
# HOVEDPROGRAM
# ============================================

def main():
    """Hovedprogram med test-scenarier"""
    
    print("\n" + "="*60)
    print("🧪 TESTER SELVHELBREDING MED FORSJELLIGE FEIL")
    print("="*60 + "\n")
    
    test_scenarios = [
        ("Tom liste (IndexError)", lambda: prosess_data([])),
        ("Gyldig liste", lambda: prosess_data([1, 2, 3, 4, 5])),
        ("Deling med null (ZeroDivisionError)", lambda: del_numbers(10, 0)),
        ("Normal deling", lambda: del_numbers(10, 2)),
        ("Ugyldig config-nøkkel (KeyError)", lambda: hent_konfig("finnes_ikke")),
        ("Gyldig config-nøkkel", lambda: hent_konfig("timeout")),
        ("Ugyldig JSON", lambda: parse_json("{invalid json}")),
        ("Gyldig JSON", lambda: parse_json('{"key": "value"}')),
        ("Ekstern kommando (kan feile)", lambda: kjør_ekstern_kommando("ls -la")),
    ]
    
    results = []
    
    for beskrivelse, test_func in test_scenarios:
        print(f"\n[TEST] Test: {beskrivelse}")
        print("-" * 40)
        
        try:
            resultat = test_func()
            print(f"[OK] SUKSess: {resultat}")
            results.append((beskrivelse, "OK", resultat))
        except Exception as e:
            print(f"[FEIL] FEILET: {e}")
            results.append((beskrivelse, "FEIL", str(e)))
        
        time.sleep(0.5)  # Pause mellom tester
    
    # Vis statistikk
    print("\n" + "="*60)
    healing_system.print_stats()
    
    # Vis oppsummering
    print("\n📊 TEST-OPPSummering:")
    print("-" * 60)
    suksess = sum(1 for _, status, _ in results if status == "OK")
    feil = sum(1 for _, status, _ in results if status == "FEIL")
    print(f"[OK] Vellykkede: {suksess}/{len(results)}")
    print(f"[FEIL] Feil (noen kan være fikset): {feil}/{len(results)}")
    
    # Lagre resultater
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"test_result_{timestamp}.txt", "w") as f:
        f.write("Selvhelbredende System - Test Resultater\n")
        f.write("="*60 + "\n\n")
        for beskrivelse, status, resultat in results:
            f.write(f"{beskrivelse}: {status}\n")
            f.write(f"  Resultat: {resultat}\n\n")
    
    print(f"\n[LOG] Resultater lagret i: test_result_{timestamp}.txt")
    print("\n[NEXT] Neste steg:")
    print("   1. Sjekk logs/ mappen for feildetaljer")
    print("   2. Les AGENTS.md for lærdommer")
    print("   3. Se på fixes/ for genererte fikser")
    print("   4. Kjør på nytt for å se forbedringer!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[STOP] Avbrutt av bruker")
        healing_system.print_stats()
    except Exception as e:
        print(f"\n[CRASH] Uventet feil: {e}")
        import traceback
        traceback.print_exc()
