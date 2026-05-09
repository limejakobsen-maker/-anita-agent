#!/usr/bin/env python3
"""
AI Fixer - Integrasjon med AI for automatiske kodefikser
"""

import json
import re
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class FixProposal:
    """Forslag til kodefiks fra AI"""
    original_code: str
    fixed_code: str
    explanation: str
    confidence: float  # 0.0 - 1.0
    requires_approval: bool
    line_start: int
    line_end: int


class AIFixer:
    """
    Håndterer AI-baserte kodefikser.
    
    I produksjon ville denne koble til faktisk AI-API.
    For nå simulerer vi med lokale regler.
    """
    
    def __init__(self):
        self.fix_rules = self._load_fix_rules()
        self.approval_queue: List[FixProposal] = []
        self.fixed_count = 0
        self.rejected_count = 0
        
    def _load_fix_rules(self) -> List[Dict]:
        """Last inn regler for automatiske fikser"""
        return [
            {
                "name": "missing_colon",
                "pattern": r'(if|for|while|def|class|elif|else|try|except|finally)\s+.*[^:\s]$',
                "description": "Mangler kolon etter utsagn",
                "fix_type": "append",
                "fix_value": ":",
                "auto_apply": True,
                "confidence": 0.95,
            },
            {
                "name": "print_python2",
                "pattern": r'^\s*print\s+[^(]',
                "description": "Python 2 print setning",
                "fix_type": "regex",
                "fix_value": (r'print\s+(.+)$', r'print(\1)'),
                "auto_apply": True,
                "confidence": 0.90,
            },
            {
                "name": "except_bare",
                "pattern": r'^\s*except\s*:$',
                "description": "Tom except-blokk (fanger alle feil)",
                "fix_type": "replace",
                "fix_value": "except Exception:",
                "auto_apply": False,  # Krever godkjenning
                "confidence": 0.85,
            },
            {
                "name": "missing_self",
                "pattern": r'^\s+def\s+\w+\(self[^)]*\)(?!.*self\.)',
                "description": "Metode uten self (sjekk om instansmetode)",
                "fix_type": "warning",
                "fix_value": None,
                "auto_apply": False,
                "confidence": 0.70,
            },
            {
                "name": "unused_import",
                "pattern": r'^import\s+(\w+)|^from\s+\S+\s+import\s+(\w+)',
                "description": "Sjekk om import er i bruk",
                "fix_type": "warning",
                "fix_value": None,
                "auto_apply": False,
                "confidence": 0.60,
            },
        ]
    
    def analyze_code(self, code: str, filename: str = "<unknown>") -> List[FixProposal]:
        """Analyser kode og finn potensielle fikser"""
        proposals = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for rule in self.fix_rules:
                if re.search(rule["pattern"], line):
                    proposal = self._create_proposal(line, i, rule, lines)
                    if proposal:
                        proposals.append(proposal)
        
        # Sjekk for vanlige mønstre
        proposals.extend(self._check_common_issues(code, lines))
        
        return proposals
    
    def _create_proposal(self, line: str, line_num: int, rule: Dict, all_lines: List[str]) -> Optional[FixProposal]:
        """Opprett et fix-forslag basert på regel"""
        
        fix_type = rule["fix_type"]
        
        if fix_type == "append":
            fixed = line + rule["fix_value"]
        elif fix_type == "replace":
            fixed = rule["fix_value"]
        elif fix_type == "regex":
            pattern, replacement = rule["fix_value"]
            fixed = re.sub(pattern, replacement, line)
        elif fix_type == "warning":
            fixed = line  # Ingen automatisk fiks
        else:
            return None
        
        return FixProposal(
            original_code=line,
            fixed_code=fixed,
            explanation=rule["description"],
            confidence=rule["confidence"],
            requires_approval=not rule["auto_apply"],
            line_start=line_num,
            line_end=line_num,
        )
    
    def _check_common_issues(self, code: str, lines: List[str]) -> List[FixProposal]:
        """Sjekk for vanlige problemer som ikke matcher enkle regex"""
        proposals = []
        
        # Sjekk for TODO/FIXME uten kontekst
        for i, line in enumerate(lines, 1):
            if re.search(r'#\s*(TODO|FIXME)\s*$', line, re.IGNORECASE):
                proposals.append(FixProposal(
                    original_code=line,
                    fixed_code=line + " [Trenger beskrivelse]",
                    explanation="TODO/FIXME uten beskrivelse",
                    confidence=0.80,
                    requires_approval=True,
                    line_start=i,
                    line_end=i,
                ))
        
        # Sjekk for hardkodede IP-adresser
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        for i, line in enumerate(lines, 1):
            if re.search(ip_pattern, line) and not re.search(r'#.*IP', line):
                if "localhost" not in line and "127.0.0.1" not in line:
                    proposals.append(FixProposal(
                        original_code=line,
                        fixed_code=line + "  # FIXME: Hardkodet IP",
                        explanation="Hardkodet IP-adresse funnet",
                        confidence=0.75,
                        requires_approval=True,
                        line_start=i,
                        line_end=i,
                    ))
        
        return proposals
    
    def apply_fix(self, proposal: FixProposal, code: str) -> str:
        """Anvend et fix-forslag på koden"""
        lines = code.split('\n')
        
        # Erstatt linje(r)
        lines[proposal.line_start - 1] = proposal.fixed_code
        
        return '\n'.join(lines)
    
    def request_ai_fix(self, error_message: str, code_snippet: str, context: str = "") -> Optional[FixProposal]:
        """
        Be ekstern AI om å fikse en feil.
        
        I produksjon ville dette kalle faktisk AI API.
        """
        # Simuler AI-respons basert på feilmelding
        
        # SyntaxError
        if "SyntaxError" in error_message:
            if "invalid syntax" in error_message:
                # Prøv å finne problemet
                if "print " in code_snippet and "print(" not in code_snippet:
                    return FixProposal(
                        original_code=code_snippet,
                        fixed_code=code_snippet.replace("print ", "print(").rstrip() + ")",
                        explanation="Python 2 print - oppdatert til Python 3",
                        confidence=0.95,
                        requires_approval=True,
                        line_start=1,
                        line_end=1,
                    )
        
        # NameError
        if "NameError" in error_message:
            match = re.search(r"name '(\w+)' is not defined", error_message)
            if match:
                var_name = match.group(1)
                return FixProposal(
                    original_code=code_snippet,
                    fixed_code=f"# TODO: Definer '{var_name}' før bruk\n{code_snippet}",
                    explanation=f"Variabel '{var_name}' er ikke definert",
                    confidence=0.70,
                    requires_approval=True,
                    line_start=1,
                    line_end=1,
                )
        
        # ImportError
        if "ImportError" in error_message or "ModuleNotFoundError" in error_message:
            match = re.search(r"No module named '(\w+)'", error_message)
            if match:
                module = match.group(1)
                return FixProposal(
                    original_code=code_snippet,
                    fixed_code=f"# Kjør: pip3 install {module}\n{code_snippet}",
                    explanation=f"Manglende modul: {module}",
                    confidence=0.90,
                    requires_approval=True,
                    line_start=1,
                    line_end=1,
                )
        
        return None
    
    def get_stats(self) -> Dict:
        """Returner statistikk"""
        return {
            "fixes_applied": self.fixed_count,
            "fixes_rejected": self.rejected_count,
            "pending_approval": len(self.approval_queue),
            "total_analyzed": self.fixed_count + self.rejected_count + len(self.approval_queue),
        }


class MockAIClient:
    """
    Mock klient for testing uten ekstern AI.
    Kan erstattes med faktisk API-kall.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.calls_made = 0
    
    def get_fix(self, error: str, code: str) -> str:
        """Simuler AI-respons"""
        self.calls_made += 1
        return f"# AI-forslag for: {error}\n# (Mock-respons - erstatt med faktisk AI-API)"


# Global instans
_ai_fixer = AIFixer()

def analyze(code: str, filename: str = "<unknown>") -> List[FixProposal]:
    """Analyser kode for potensielle fikser"""
    return _ai_fixer.analyze_code(code, filename)

def fix_error(error_message: str, code: str) -> Optional[FixProposal]:
    """Be om AI-fiks for en feil"""
    return _ai_fixer.request_ai_fix(error_message, code)


def get_stats() -> Dict:
    """Få statistikk"""
    return _ai_fixer.get_stats()


if __name__ == "__main__":
    print("Tester AI Fixer...\n")
    
    test_code = '''
def hei
    print "Hei verden"
    x = 5
    print x

try:
    noe()
except:
    pass
'''
    
    print("Testkode:")
    print(test_code)
    print("\n" + "="*50)
    print("Analyse:")
    
    proposals = analyze(test_code, "test.py")
    
    for p in proposals:
        print(f"\n📍 Linje {p.line_start}: {p.explanation}")
        print(f"   Konfidens: {p.confidence:.0%}")
        print(f"   Krever godkjenning: {'Ja' if p.requires_approval else 'Nei'}")
        print(f"   Original: {p.original_code.strip()}")
        print(f"   Forslag:  {p.fixed_code.strip()}")
    
    print("\n" + "="*50)
    print("Statistikk:", get_stats())
