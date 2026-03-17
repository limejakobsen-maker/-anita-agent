"""
AI Fixer - Bruker Kimi eller Gemini til å generere fikser
"""
import os
import sys
import re
from typing import Optional, Dict
from pathlib import Path

# Legg til lokale paths for AI-integrasjon
sys.path.insert(0, str(Path.home() / 'AI_System' / 'protokoll'))
sys.path.insert(0, str(Path.home() / 'Desktop' / 'PROSJEKTMAPPE AI' / 'SANDKASSE' / '07_Sandkasse_SelfHealing'))

class AIFixer:
    def __init__(self):
        self.kimi_available = False
        self.gemini_available = False
        self._init_ai()
        
    def _init_ai(self):
        """Initialiserer AI-tilkobling"""
        try:
            from ai_integrasjon import AIAgent
            self.agent = AIAgent()
            self.kimi_available = self.agent.kimi.er_tilgjengelig()
            self.gemini_available = self.agent.gemini.er_tilgjengelig()
            print(f"AI Status - Kimi: {self.kimi_available}, Gemini: {self.gemini_available}")
        except Exception as e:
            print(f"Kunne ikke laste ekstern AI: {e}")
            print("Bruker lokal Ollama-fallback for fikser")
            self._init_local_ollama()
    
    def _init_local_ollama(self):
        """Initialiser lokal Ollama som fallback"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Lokal Ollama tilgjengelig som AI-fallback")
                self.ollama_available = True
            else:
                self.ollama_available = False
        except:
            self.ollama_available = False
    
    def generate_fix(self, error_info: Dict, current_code: str) -> Optional[str]:
        """
        Genererer en fiks basert på feilinformasjon
        """
        error_type = error_info['type']
        error_message = error_info['message']
        
        # Først: Sjekk om vi har en kjent feiltype med standardfiks
        standard_fix = self._get_standard_fix(error_type, error_message, current_code)
        if standard_fix:
            print(f"Bruker standardfiks for {error_type}")
            return standard_fix
        
        # Hvis AI er tilgjengelig, bruk den
        if self.kimi_available or self.gemini_available:
            return self._generate_ai_fix(error_info, current_code)
        else:
            return self._generate_local_fix(error_info, current_code)
    
    def _get_standard_fix(self, error_type: str, error_message: str, code: str) -> Optional[str]:
        """Standardfikser for vanlige feil"""
        
        # AttributeError: NoneType
        if error_type == "AttributeError" and "NoneType" in error_message:
            # Finn hvilken variabel som er None
            match = re.search(r"'NoneType' object has no attribute '(\w+)'", error_message)
            if match:
                attr = match.group(1)
                # Finn linjen med problemet
                lines = code.split('\n')
                for i, line in enumerate(lines):
                    if attr in line and '.' in line:
                        # Inject sjekk før bruk
                        indent = len(line) - len(line.lstrip())
                        var_name = line.strip().split('.')[0]
                        check_line = ' ' * indent + f"if {var_name} is not None:"
                        lines.insert(i, check_line)
                        lines[i+1] = '    ' + lines[i+1]
                        return '\n'.join(lines)
        
        # IndexError
        elif error_type == "IndexError":
            if "list index out of range" in error_message:
                # Erstatt direkte index med .get() eller sjekk
                fixed_code = re.sub(
                    r'(\w+)\[(\d+)\]',
                    r'\1[\2] if len(\1) > \2 else None',
                    code
                )
                return fixed_code
        
        # KeyError
        elif error_type == "KeyError":
            match = re.search(r"'(.+?)'", error_message)
            if match:
                key = match.group(1)
                # Erstatt dict[key] med dict.get(key, default)
                fixed_code = re.sub(
                    rf'(\w+)\[\s*[\'"]?{key}[\'"]?\s*\]',
                    rf'\1.get("{key}", None)',
                    code
                )
                return fixed_code
        
        # ZeroDivisionError
        elif error_type == "ZeroDivisionError":
            # Finn divisjonen og legg til sjekk
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if '/' in line and not line.strip().startswith('#'):
                    indent = len(line) - len(line.lstrip())
                    # Finn denominator
                    parts = line.split('/')
                    if len(parts) >= 2:
                        denom = parts[1].strip().split()[0].rstrip(')')
                        check = ' ' * indent + f"if {denom} != 0:"
                        lines.insert(i, check)
                        lines[i+1] = '    ' + lines[i+1]
                        lines.insert(i+2, ' ' * indent + 'else:')
                        lines.insert(i+3, ' ' * indent + '    result = 0  # Avoid division by zero')
                        return '\n'.join(lines)
        
        return None
    
    def _generate_ai_fix(self, error_info: Dict, current_code: str) -> Optional[str]:
        """Bruker AI til å generere fiks"""
        prompt = f"""
Jeg har en Python-feil som må fikses. Vær konsis og returner KUN koden.

FEILTYPE: {error_info['type']}
FEILMELDING: {error_info['message']}
FUNKSJON: {error_info['function']}
FREKVENS: {error_info['frequency']} forekomster

NÅVÆRENDE KODE:
```python
{current_code}
```

Din oppgave:
1. Fiks feilen på en robust måte
2. Returner KUN den korrigerte koden (ingen forklaring)
3. Behold all original funksjonalitet
"""
        
        try:
            if self.kimi_available:
                fix_code = self.agent.kimi.generer_kode(prompt)
            else:
                fix_code = self.agent.gemini.analyser_kode(prompt)
            
            return self._clean_code(fix_code)
            
        except Exception as e:
            print(f"AI-fiks generering feilet: {e}")
            return self._generate_local_fix(error_info, current_code)
    
    def _generate_local_fix(self, error_info: Dict, code: str) -> Optional[str]:
        """Lokal fallback for fikser når AI ikke er tilgjengelig"""
        error_type = error_info['type']
        
        # Wrap koden i try-except som siste utvei
        wrapped = f'''
try:
    {code.replace(chr(10), chr(10) + "    ")}
except {error_type} as e:
    print(f"Håndtert feil: {{e}}")
    # TODO: Legg til passende fallback
    pass
'''
        return wrapped
    
    def _clean_code(self, code: str) -> str:
        """Fjerner markdown-formattering"""
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
        return code.strip()
    
    def validate_syntax(self, code: str) -> bool:
        """Sjekker at koden er gyldig Python"""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            print(f"Syntaksfeil i generert kode: {e}")
            return False

if __name__ == "__main__":
    fixer = AIFixer()
    print("AI Fixer klar")
