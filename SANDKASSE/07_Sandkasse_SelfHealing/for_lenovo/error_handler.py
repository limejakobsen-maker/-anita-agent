#!/usr/bin/env python3
"""
Error Handler - Avansert feilhåndtering og klassifisering
"""

import re
import traceback
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List, Dict, Callable


class ErrorSeverity(Enum):
    LOW = auto()      # Advarsel, kan fortsette
    MEDIUM = auto()   # Problem, bør fikses
    HIGH = auto()     # Alvorlig, krever handling
    CRITICAL = auto() # Systemkritisk, stopp alt


class ErrorCategory(Enum):
    SYNTAX = auto()
    RUNTIME = auto()
    LOGIC = auto()
    NETWORK = auto()
    IO = auto()
    PERMISSION = auto()
    RESOURCE = auto()
    UNKNOWN = auto()


@dataclass
class ErrorRecord:
    """Represents a captured error"""
    error_type: str
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    file: Optional[str] = None
    line: Optional[int] = None
    context: Optional[str] = None
    traceback_str: Optional[str] = None
    suggested_fix: Optional[str] = None


class ErrorHandler:
    """Intelligent feilhåndterer"""
    
    def __init__(self):
        self.error_patterns = self._compile_patterns()
        self.error_history: List[ErrorRecord] = []
        self.fix_handlers: Dict[ErrorCategory, List[Callable]] = {}
        
    def _compile_patterns(self) -> Dict[ErrorCategory, List[re.Pattern]]:
        """Kompiler regex-mønstre for feilklassifisering"""
        return {
            ErrorCategory.SYNTAX: [
                re.compile(r"SyntaxError|IndentationError"),
                re.compile(r"unexpected EOF|invalid syntax"),
            ],
            ErrorCategory.RUNTIME: [
                re.compile(r"RuntimeError|RecursionError|NotImplementedError"),
                re.compile(r"maximum recursion depth exceeded"),
            ],
            ErrorCategory.NETWORK: [
                re.compile(r"ConnectionError|TimeoutError|socket\\.error"),
                re.compile(r"HTTPError|URLError|requests\\.exceptions"),
                re.compile(r"Connection refused|Connection reset|timed out"),
            ],
            ErrorCategory.IO: [
                re.compile(r"FileNotFoundError|IsADirectoryError"),
                re.compile(r"IOError|OSError.*file"),
                re.compile(r"No such file or directory"),
            ],
            ErrorCategory.PERMISSION: [
                re.compile(r"PermissionError|Access denied"),
                re.compile(r"Unauthorized|Forbidden"),
            ],
            ErrorCategory.RESOURCE: [
                re.compile(r"MemoryError|ResourceExhausted"),
                re.compile(r"disk full|out of memory"),
            ],
            ErrorCategory.LOGIC: [
                re.compile(r"ValueError|TypeError|KeyError|IndexError"),
                re.compile(r"AttributeError|AssertionError"),
            ],
        }
    
    def classify_error(self, exception: Exception) -> ErrorCategory:
        """Klassifiser en feil basert på type og melding"""
        error_type = type(exception).__name__
        error_msg = str(exception)
        error_str = f"{error_type}: {error_msg}"
        
        for category, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern.search(error_str):
                    return category
        
        return ErrorCategory.UNKNOWN
    
    def assess_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Vurder alvorlighetsgraden til en feil"""
        error_type = type(exception).__name__
        error_msg = str(exception).lower()
        
        # Kritiske feiler
        if error_type in ["SystemExit", "KeyboardInterrupt"]:
            return ErrorSeverity.CRITICAL
        
        if category == ErrorCategory.RESOURCE:
            if "disk full" in error_msg or "memory" in error_msg:
                return ErrorSeverity.CRITICAL
        
        # Høy alvorlighet
        if category == ErrorCategory.PERMISSION:
            return ErrorSeverity.HIGH
        
        if category == ErrorCategory.NETWORK:
            if "refused" in error_msg or "reset" in error_msg:
                return ErrorSeverity.HIGH
        
        # Medium - de fleste logikkfeil
        if category in [ErrorCategory.LOGIC, ErrorCategory.IO]:
            return ErrorSeverity.MEDIUM
        
        # Lav - syntaksfeil (fanges ved start)
        if category == ErrorCategory.SYNTAX:
            return ErrorSeverity.HIGH  # Men stopp før kjøring
        
        return ErrorSeverity.MEDIUM
    
    def parse_traceback(self, tb_str: str) -> Dict[str, Optional[str]]:
        """Parser traceback for å finne fil, linje og kontekst"""
        lines = tb_str.strip().split('\n')
        info = {
            'file': None,
            'line': None,
            'context': None,
            'function': None,
        }
        
        # Finn siste filreferanse
        for i, line in enumerate(lines):
            match = re.search(r'File "([^"]+)", line (\d+), in (\w+)', line)
            if match:
                info['file'] = match.group(1)
                info['line'] = int(match.group(2))
                info['function'] = match.group(3)
                
                # Se om det er kode på neste linje
                if i + 1 < len(lines):
                    code_line = lines[i + 1].strip()
                    if code_line and not code_line.startswith('File'):
                        info['context'] = code_line
        
        return info
    
    def suggest_fix(self, error: ErrorRecord) -> str:
        """Foreslå en fiks basert på feiltypen"""
        
        if error.category == ErrorCategory.IO:
            if "FileNotFoundError" in error.error_type:
                return f"Sjekk at filen '{error.context}' eksisterer, eller opprett den."
        
        if error.category == ErrorCategory.PERMISSION:
            return "Sjekk filrettigheter. Kjør: chmod +x filnavn eller kjør med sudo."
        
        if error.category == ErrorCategory.NETWORK:
            return "Sjekk nettverkstilkobling og at tjenesten kjører på målmaskin."
        
        if error.category == ErrorCategory.LOGIC:
            if "KeyError" in error.error_type:
                return "Sjekk at nøkkelen eksisterer i ordboken før bruk."
            if "IndexError" in error.error_type:
                return "Sjekk at indeksen er innenfor listens lengde."
            if "TypeError" in error.error_type:
                return "Sjekk at datatypene stemmer (f.eks. ikke streng + tall)."
            if "AttributeError" in error.error_type:
                return "Sjekk at objektet har attributten du prøver å bruke."
        
        if error.category == ErrorCategory.SYNTAX:
            return "Sjekk syntaks - mangler kolon, parenteser eller anførselstegn?"
        
        return "Se dokumentasjon og stack trace for mer informasjon."
    
    def handle(self, exception: Exception, context: Optional[str] = None) -> ErrorRecord:
        """Håndter en feil og returner ErrorRecord"""
        
        category = self.classify_error(exception)
        severity = self.assess_severity(exception, category)
        
        # Få traceback
        tb_str = traceback.format_exc()
        tb_info = self.parse_traceback(tb_str)
        
        # Lag record
        record = ErrorRecord(
            error_type=type(exception).__name__,
            message=str(exception),
            severity=severity,
            category=category,
            file=tb_info.get('file'),
            line=tb_info.get('line'),
            context=tb_info.get('context') or context,
            traceback_str=tb_str,
            suggested_fix=None
        )
        
        # Generer fiksforslag
        record.suggested_fix = self.suggest_fix(record)
        
        # Lagre i historikk
        self.error_history.append(record)
        
        # Logg
        self._log_error(record)
        
        return record
    
    def _log_error(self, record: ErrorRecord):
        """Logg feil til konsoll (kan utvides til fil)"""
        emoji = {
            ErrorSeverity.LOW: "⚪",
            ErrorSeverity.MEDIUM: "🟡",
            ErrorSeverity.HIGH: "🔴",
            ErrorSeverity.CRITICAL: "💥",
        }.get(record.severity, "❓")
        
        print(f"\n{emoji} FEIL [{record.severity.name}] - {record.error_type}")
        print(f"   Melding: {record.message}")
        print(f"   Kategori: {record.category.name}")
        if record.file:
            print(f"   Sted: {record.file}:{record.line}")
        if record.suggested_fix:
            print(f"   💡 Forslag: {record.suggested_fix}")
    
    def get_stats(self) -> Dict:
        """Returner statistikk over feil"""
        if not self.error_history:
            return {"total": 0}
        
        stats = {
            "total": len(self.error_history),
            "by_category": {},
            "by_severity": {},
        }
        
        for err in self.error_history:
            cat = err.category.name
            sev = err.severity.name
            stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
            stats["by_severity"][sev] = stats["by_severity"].get(sev, 0) + 1
        
        return stats


# Global handler
_handler = ErrorHandler()

def handle_error(exception: Exception, context: Optional[str] = None) -> ErrorRecord:
    """Håndter en feil"""
    return _handler.handle(exception, context)

def get_error_stats() -> Dict:
    """Få feilstatistikk"""
    return _handler.get_stats()


if __name__ == "__main__":
    # Test
    print("Tester ErrorHandler...\n")
    
    test_errors = [
        FileNotFoundError("fil.txt ikke funnet"),
        PermissionError("Tilgang nektet"),
        ValueError("Ugyldig verdi: -5"),
        ConnectionError("Connection refused"),
    ]
    
    for err in test_errors:
        try:
            raise err
        except Exception as e:
            handle_error(e, "test_context")
    
    print("\n" + "="*50)
    print("Statistikk:")
    print(get_error_stats())
