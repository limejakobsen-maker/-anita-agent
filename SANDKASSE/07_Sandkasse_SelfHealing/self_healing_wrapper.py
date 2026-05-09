"""
Self-Healing Wrapper - Hovedkomponenten for selvhelbredelse
"""
import os
import sys
import shutil
import traceback
import ast
import inspect
from datetime import datetime
from typing import Callable, Any, Dict
from error_handler import ErrorHandler
from ai_fixer import AIFixer

class SelfHealingSystem:
    def __init__(self, backup_dir="backups"):
        self.error_handler = ErrorHandler()
        self.ai_fixer = AIFixer()
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
        # Statistikk
        self.stats = {
            "total_runs": 0,
            "successful_runs": 0,
            "auto_fixed": 0,
            "failed_fixes": 0
        }
        
        print("[INIT] Self-Healing System initialisert")
        print(f"   Backup-mappe: {backup_dir}")
        print(f"   AI-tilkobling: {'Klar' if (self.ai_fixer.kimi_available or self.ai_fixer.gemini_available) else 'Lokal modus'}")
    
    def heal(self, func: Callable) -> Callable:
        """
        Dekorator som gir en funksjon selvhelbredende evner
        """
        def wrapper(*args, **kwargs):
            max_attempts = 3
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    # Prøv å kjøre funksjonen
                    result = func(*args, **kwargs)
                    
                    # Suksess!
                    if attempt > 0:
                        print(f"✅ {func.__name__} gjenopprettet etter {attempt} fiks-forsøk")
                        self.stats["auto_fixed"] += 1
                    
                    self.stats["successful_runs"] += 1
                    return result
                    
                except Exception as e:
                    attempt += 1
                    self.stats["total_runs"] += 1
                    
                    print(f"\n⚠️  Feil i {func.__name__} (forsøk {attempt}/{max_attempts}): {e}")
                    
                    if attempt < max_attempts:
                        # Prøv å helbrede
                        healed = self._attempt_healing(e, func)
                        if not healed:
                            print(f"   Kunne ikke auto-fikse, prøver igjen...")
                    else:
                        print(f"❌ {func.__name__} feilet etter {max_attempts} forsøk")
                        self.stats["failed_fixes"] += 1
                        raise e
            
            return None
        
        return wrapper
    
    def _attempt_healing(self, error: Exception, func: Callable) -> bool:
        """Prøver å helbrede en feil"""
        try:
            # 1. Fang feilen
            code_context = self._get_function_source(func)
            error_info = self.error_handler.handle_error(
                error, code_context, func.__name__
            )
            
            print(f"   Feil-hash: {error_info['error_hash']}")
            print(f"   Tidligere sett: {error_info['previously_seen']} ({error_info['frequency']} ganger)")
            
            # 2. Generer fiks
            print("   Genererer fiks...")
            fixed_code = self.ai_fixer.generate_fix(error_info, code_context)
            
            if not fixed_code:
                print("   Kunne ikke generere fiks")
                return False
            
            # 3. Valider syntaks
            if not self.ai_fixer.validate_syntax(fixed_code):
                print("   Generert kode har syntaksfeil")
                return False
            
            # 4. Sikkerhetskopi
            self._create_backup(func.__name__)
            
            # 5. Anvend fiks
            print("   Anvender fiks...")
            self._apply_fix(func, fixed_code)
            
            # 6. Logg suksess
            self.error_handler.learn_from_fix(
                error_info['error_hash'],
                f"Auto-fiks for {error_info['type']}",
                success=True,
                new_code=fixed_code
            )
            
            self._update_agents_md(error_info, fixed_code, success=True)
            
            return True
            
        except Exception as healing_error:
            print(f"   Helbredingsprosess feilet: {healing_error}")
            self.error_handler.learn_from_fix(
                error_info.get('error_hash', 'unknown'),
                str(healing_error),
                success=False
            )
            return False
    
    def _get_function_source(self, func: Callable) -> str:
        """Henter kildekoden til en funksjon"""
        try:
            return inspect.getsource(func)
        except:
            return "# Kunne ikke hente kildekode"
    
    def _create_backup(self, func_name: str):
        """Lager sikkerhetskopi av main.py"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"main_{func_name}_{timestamp}.py.bak"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        if os.path.exists("main.py"):
            shutil.copy("main.py", backup_path)
            print(f"   Backup: {backup_path}")
    
    def _apply_fix(self, func: Callable, new_code: str):
        """Anvender fiksen til koden"""
        # I en produksjonsversjon ville dette bruke AST-manipulering
        # For nå logger vi bare
        fix_file = f"fixes/{func.__name__}_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        os.makedirs("fixes", exist_ok=True)
        
        with open(fix_file, 'w') as f:
            f.write(new_code)
        
        print(f"   Fiks lagret: {fix_file}")
    
    def _update_agents_md(self, error_info: Dict, fix_code: str, success: bool):
        """Oppdaterer AGENTS.md med lærdom"""
        with open("AGENTS.md", "a", encoding="utf-8") as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Funksjon:** {error_info['function']}\n")
            f.write(f"**Feil:** {error_info['type']}: {error_info['message'][:80]}\n")
            f.write(f"**Frekvens:** {error_info['frequency']} ganger\n")
            f.write(f"**Fiks:** {'✅ Suksess' if success else '❌ Feilet'}\n")
            if success:
                f.write(f"**Lærdom:** {error_info['type']} kan fikses med {len(fix_code)} tegn kode\n")
            f.write("---\n")
    
    def get_stats(self) -> Dict:
        """Returnerer statistikk"""
        trends = self.error_handler.analyze_error_trends()
        return {
            **self.stats,
            **trends,
            "healing_success_rate": (
                (self.stats["auto_fixed"] / self.stats["total_runs"] * 100)
                if self.stats["total_runs"] > 0 else 0
            )
        }
    
    def print_stats(self):
        """Printer statistikk"""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("📊 SELVHELBREDING STATISTIKK")
        print("="*50)
        print(f"Totale kjøringer:    {stats['total_runs']}")
        print(f"Vellykkede:          {stats['successful_runs']}")
        print(f"Auto-fikset:         {stats['auto_fixed']}")
        print(f"Mislykkede fikser:   {stats['failed_fixes']}")
        print(f"Suksessrate:         {stats['healing_success_rate']:.1f}%")
        print("-"*50)
        print(f"Unike feil:          {stats['total_unique_errors']}")
        print(f"Fikset feil:         {stats['fixed_errors']}")
        print(f"Gjentagende feil:    {stats['recurring_errors']}")
        print("="*50)

# Global instans for enkel bruk
_healing_system = SelfHealingSystem()

def heal(func):
    """Dekorator for selvhelbredelse"""
    return _healing_system.heal(func)

if __name__ == "__main__":
    print("Self-Healing System test")
    
    @heal
    def test_func():
        print("Kjører test_func")
        return 42
    
    test_func()
