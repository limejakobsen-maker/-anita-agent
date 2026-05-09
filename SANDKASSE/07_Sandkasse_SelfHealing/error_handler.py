"""
Error Handler - Logger og analyserer feil for selvhelbredelse
"""
import traceback
import json
import datetime
import hashlib
import os
from typing import Dict, List, Optional

class ErrorHandler:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        self.error_log = os.path.join(log_dir, "errors.log")
        self.learning_log = os.path.join(log_dir, "learning.log")
        self.fixes_log = os.path.join(log_dir, "fixes.log")
        self.error_patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict:
        """Laster tidligere feilmønstre"""
        patterns_file = os.path.join(self.log_dir, "patterns.json")
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_patterns(self):
        """Lagrer feilmønstre til fil"""
        patterns_file = os.path.join(self.log_dir, "patterns.json")
        with open(patterns_file, 'w') as f:
            json.dump(self.error_patterns, f, indent=2)
    
    def handle_error(self, error: Exception, code_context: str, function_name: str = "unknown") -> Dict:
        """
        Analyserer en feil og returnerer strukturert informasjon
        """
        error_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "function": function_name,
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "code_context": code_context[:500],  # Første 500 tegn
            "error_hash": self._hash_error(error, function_name),
            "frequency": 1,
            "status": "new"
        }
        
        # Sjekk om vi har sett denne feilen før
        if error_info["error_hash"] in self.error_patterns:
            self.error_patterns[error_info["error_hash"]]["frequency"] += 1
            error_info["frequency"] = self.error_patterns[error_info["error_hash"]]["frequency"]
            error_info["previously_seen"] = True
            error_info["previous_fixes"] = self.error_patterns[error_info["error_hash"]].get("fixes", [])
        else:
            self.error_patterns[error_info["error_hash"]] = error_info
            error_info["previously_seen"] = False
            
        self._log_error(error_info)
        self._save_patterns()
        
        return error_info
    
    def _hash_error(self, error: Exception, function_name: str) -> str:
        """Lager en hash av feilen for å identifisere unike feil"""
        error_str = f"{function_name}:{type(error).__name__}:{str(error)}"
        return hashlib.md5(error_str.encode()).hexdigest()[:12]
    
    def _log_error(self, error_info: Dict):
        """Logger feilen til fil"""
        with open(self.error_log, "a") as f:
            f.write(json.dumps(error_info) + "\n")
    
    def get_common_errors(self, n: int = 5) -> List[Dict]:
        """Returnerer de vanligste feilene"""
        sorted_errors = sorted(
            self.error_patterns.values(), 
            key=lambda x: x.get("frequency", 0), 
            reverse=True
        )
        return sorted_errors[:n]
    
    def learn_from_fix(self, error_hash: str, fix_description: str, success: bool, new_code: str = ""):
        """Lagrer at en fiks fungerte eller ikke"""
        learning_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "error_hash": error_hash,
            "fix": fix_description,
            "success": success,
            "new_code_hash": hashlib.md5(new_code.encode()).hexdigest()[:8] if new_code else ""
        }
        
        with open(self.learning_log, "a") as f:
            f.write(json.dumps(learning_entry) + "\n")
        
        # Oppdater patterns
        if error_hash in self.error_patterns:
            if "fixes" not in self.error_patterns[error_hash]:
                self.error_patterns[error_hash]["fixes"] = []
            
            self.error_patterns[error_hash]["fixes"].append({
                "description": fix_description,
                "success": success,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            if success:
                self.error_patterns[error_hash]["status"] = "fixed"
            
            self._save_patterns()
        
        if success:
            with open(self.fixes_log, "a") as f:
                f.write(json.dumps(learning_entry) + "\n")
    
    def get_error_history(self, error_hash: str) -> List[Dict]:
        """Henter historikk for en spesifikk feil"""
        if error_hash in self.error_patterns:
            return self.error_patterns[error_hash].get("fixes", [])
        return []
    
    def analyze_error_trends(self) -> Dict:
        """Analyserer feiltrender"""
        total_errors = len(self.error_patterns)
        fixed_errors = sum(1 for e in self.error_patterns.values() if e.get("status") == "fixed")
        recurring_errors = sum(1 for e in self.error_patterns.values() if e.get("frequency", 0) > 1)
        
        return {
            "total_unique_errors": total_errors,
            "fixed_errors": fixed_errors,
            "recurring_errors": recurring_errors,
            "success_rate": (fixed_errors / total_errors * 100) if total_errors > 0 else 0
        }

if __name__ == "__main__":
    # Test
    handler = ErrorHandler()
    try:
        1/0
    except Exception as e:
        info = handler.handle_error(e, "1/0", "test_function")
        print(f"Error logged: {info['error_hash']}")
