#!/usr/bin/env python3
"""
Self-Healing Wrapper - Dekorator for selvreparerende kode
"""

import functools
import traceback
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

class SelfHealingWrapper:
    """Wrapper som gir selvhelbredende egenskaper til funksjoner"""
    
    def __init__(self):
        self.log_dir = Path.home() / "AI_System" / "logs" / "self_healing"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.error_history = []
        
    def heal(self, max_attempts=3, log_errors=True, notify_monitor=True):
        """
        Dekorator som fanger feil og forsøker reparasjon
        
        Args:
            max_attempts: Maks antall forsøk før feil kastes
            log_errors: Om feil skal logges til fil
            notify_monitor: Om monitor skal varsles
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                attempts = 0
                last_error = None
                
                while attempts < max_attempts:
                    try:
                        result = func(*args, **kwargs)
                        # Suksess - logg hvis vi hadde retry
                        if attempts > 0:
                            self._log_recovery(func.__name__, attempts)
                        return result
                        
                    except Exception as e:
                        attempts += 1
                        last_error = e
                        
                        if log_errors:
                            self._log_error(func.__name__, e, attempts)
                        
                        if attempts < max_attempts:
                            # Forsøk reparasjon
                            if self._attempt_fix(func.__name__, e, args, kwargs):
                                continue
                        else:
                            # Alle forsøk brukt opp
                            break
                
                # Feil kunne ikke repareres
                if notify_monitor and hasattr(self, 'monitor_callback'):
                    self.monitor_callback(func.__name__, last_error)
                    
                raise last_error
            
            return wrapper
        return decorator
    
    def _log_error(self, func_name, error, attempt):
        """Logg feil til fil"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "function": func_name,
            "error": str(error),
            "error_type": type(error).__name__,
            "attempt": attempt,
            "traceback": traceback.format_exc()
        }
        
        self.error_history.append(error_entry)
        
        # Lagre til fil
        log_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.json"
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(error_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except:
            pass
    
    def _log_recovery(self, func_name, attempts):
        """Logg vellykket reparasjon"""
        recovery_entry = {
            "timestamp": datetime.now().isoformat(),
            "function": func_name,
            "attempts_needed": attempts,
            "status": "recovered"
        }
        
        log_file = self.log_dir / f"recoveries_{datetime.now().strftime('%Y%m%d')}.json"
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(recovery_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except:
            pass
    
    def _attempt_fix(self, func_name, error, args, kwargs):
        """
        Forsøk å fikse feilen automatisk
        
        Returnerer True hvis fiks ble anvendt og vi skal prøve igjen
        """
        error_type = type(error).__name__
        error_msg = str(error).lower()
        
        # Fil ikke funnet - sjekk om path kan korrigeres
        if error_type == "FileNotFoundError":
            if len(args) > 0 and isinstance(args[0], (str, Path)):
                original_path = Path(args[0])
                # Prøv alternative lokasjoner
                alternatives = [
                    Path.home() / original_path.name,
                    Path.cwd() / original_path.name,
                    Path(__file__).parent / original_path.name,
                ]
                for alt in alternatives:
                    if alt.exists():
                        args = (str(alt),) + args[1:]
                        return True
        
        # Tillatelsesfeil - prøv å fikse
        if error_type == "PermissionError":
            if len(args) > 0 and isinstance(args[0], (str, Path)):
                try:
                    import stat
                    os.chmod(args[0], stat.S_IRUSR | stat.S_IWUSR)
                    return True
                except:
                    pass
        
        # Modul ikke funnet - prøv å installere
        if error_type == "ModuleNotFoundError" or "No module named" in error_msg:
            import re
            match = re.search(r"'([^']+)'", str(error))
            if match:
                module_name = match.group(1)
                # Logg forslag til fiks
                print(f"💡 Mangler modul: {module_name}")
                print(f"   Kjør: pip install {module_name}")
        
        # Type/feilverdi - prøv konvertering
        if error_type == "TypeError":
            if "must be" in error_msg or "expected" in error_msg:
                # Prøv å konvertere argumenter
                return False  # Krever manuell fiks
        
        return False
    
    def get_error_summary(self):
        """Returner oppsummering av feil"""
        if not self.error_history:
            return "Ingen feil registrert"
        
        total = len(self.error_history)
        by_type = {}
        for err in self.error_history:
            et = err["error_type"]
            by_type[et] = by_type.get(et, 0) + 1
        
        summary = f"Totalt {total} feil registrert:\n"
        for et, count in sorted(by_type.items(), key=lambda x: -x[1]):
            summary += f"  - {et}: {count}\n"
        
        return summary


# Global instans
_healer = SelfHealingWrapper()

# Convenience funksjon for enkel bruk
def heal(max_attempts=3, log_errors=True, notify_monitor=True):
    """Dekorator for selvhelbredende funksjoner"""
    return _healer.heal(max_attempts, log_errors, notify_monitor)


if __name__ == "__main__":
    # Test
    @heal(max_attempts=2)
    def test_function():
        import random
        if random.random() < 0.5:
            raise ValueError("Tilfeldig feil!")
        return "Suksess!"
    
    print("Tester self-healing wrapper...")
    for i in range(5):
        try:
            result = test_function()
            print(f"  Kjøring {i+1}: {result}")
        except Exception as e:
            print(f"  Kjøring {i+1}: Feil - {e}")
    
    print("\n" + _healer.get_error_summary())
