#!/usr/bin/env python3
"""
SANDKASSE-PROTOKOLLEN v3.0 - DEL 2: Fase 4-6
Fase 4: EXECUTE (vår styrke med @heal)
Fase 5: VALIDATE (vår strenge standard)
Fase 6: DEPLOY (vår arkivering)
"""

# Denne filen inneholder metoder som skal legges til hovedklassen
# Dette er en utvidelse av sandkasse_protokoll.py

# ═══════════════════════════════════════════════════════════
# FASE 4: EXECUTE (GSD + vår @heal teknologi)
# ═══════════════════════════════════════════════════════════

def fase_4_execute(self, prosjektnavn: str, iterasjon: int = 0) -> Tuple[bool, str]:
    """
    FASE 4: EXECUTE
    - Kjør planer i bølger (parallelt hvor mulig)
    - Fresh context per plan (GSD)
    - @heal dekorator (vår styrke!)
    - Commits per task (GSD)
    """
    self._log(f"[FASE 4] EXECUTE: Iterasjon {iterasjon}")
    self._update_status("eksekverer", fase=4, progress=10)
    
    prosjekt = self.aktive_prosjekter[prosjektnavn]
    
    if iterasjon >= self.config["max_iterations"]:
        return False, "Maks iterasjoner nådd"
    
    # GSD: Fresh context før eksekvering
    if self.config["fresh_context_enabled"]:
        fresh_ctx = self.context_manager.create_fresh_context("EXECUTE", prosjekt)
        self._log("[CONTEXT] Fresh context generert")
    
    # Les planer
    planning_dir = prosjekt.mappe / ".planning"
    plan_files = list(planning_dir.glob("PLAN-*.xml"))
    
    self._update_status("eksekverer", fase=4, progress=30)
    
    # GSD: Kjør planer i bølger
    for i, plan_file in enumerate(plan_files, 1):
        self._log(f"[EXECUTE] Kjører plan {i}/{len(plan_files)}")
        
        # Generer kode for denne planen
        # I full implementasjon: Kall AI med fresh context
        
        # Lag main.py med @heal dekorator
        main_code = f'''#!/usr/bin/env python3
"""
{prosjektnavn} - Plan {i}
Generert av Sandkasse-Protokollen v3.0
"""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from self_healing_wrapper import heal

@heal
def main():
    """Hovedfunksjon for {prosjektnavn}"""
    print(f"[START] {prosjektnavn} - Plan {i}")
    
    # TODO: Implementer basert på plan
    return True

if __name__ == "__main__":
    main()
'''
        
        src_dir = prosjekt.mappe / "src"
        src_dir.mkdir(exist_ok=True)
        
        main_file = src_dir / "main.py"
        main_file.write_text(main_code)
        
        self._send_code(main_code, "main.py")
        
        # GSD: Atomic commit per plan
        git = GitIntegration(prosjekt.mappe)
        git.commit(f"fase-4-execute: Plan {i} implementert", prosjekt)
        
        progress = 30 + (i / len(plan_files)) * 40
        self._update_status("eksekverer", fase=4, progress=int(progress))
    
    # Lag test-fil
    test_code = f'''"""
Tester for {prosjektnavn}
"""
import pytest
from src.main import main

class TestKjerne:
    def test_main_returns_true(self):
        assert main() is True
    
    def test_main_no_exceptions(self):
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised {e}")
'''
    
    tests_dir = prosjekt.mappe / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_main.py").write_text(test_code)
    
    prosjekt.status = "execute_ferdig"
    prosjekt.fase = 4
    prosjekt.iterasjon = iterasjon
    
    self._update_status("execute_ferdig", fase=4, progress=100)
    self._log("[FASE 4] Fullført: Kode eksekvert")
    return True, "Kode eksekvert"


# ═══════════════════════════════════════════════════════════
# FASE 5: VALIDATE (vår strenge standard)
# ═══════════════════════════════════════════════════════════

def fase_5_validate(self, prosjektnavn: str) -> Tuple[bool, str]:
    """
    FASE 5: VALIDATE
    - pytest med >90% dekning (vår standard!)
    - Linting: black, flake8
    - Sikkerhet: bandit
    - Manuelle sjekker
    """
    self._log(f"[FASE 5] VALIDATE: Streng validering")
    self._update_status("validerer", fase=5, progress=20)
    
    prosjekt = self.aktive_prosjekter[prosjektnavn]
    mappe = prosjekt.mappe
    
    # 1. Kjør tester
    self._log("[TEST] Kjører pytest...")
    self._update_status("validerer", fase=5, progress=40)
    
    test_resultat = self._kjør_tester(mappe)
    
    if not test_resultat["success"]:
        self._log(f"[FEIL] Tester feilet: {test_resultat['output']}", "ERROR")
        return False, f"Tester feilet"
    
    dekning = test_resultat.get("coverage", 0)
    prosjekt.test_dekning = dekning
    
    # Vår standard: >90% dekning!
    if dekning < self.config["required_tests_pass"]:
        msg = f"Testdekning for lav: {dekning:.1f}% (krever {self.config['required_tests_pass']}%)"
        self._log(f"[FEIL] {msg}", "ERROR")
        return False, msg
    
    self._log(f"[OK] Testdekning: {dekning:.1f}%")
    
    # 2. Linting
    self._log("[LINT] Sjekker kodekvalitet...")
    self._update_status("validerer", fase=5, progress=60)
    
    lint_resultat = self._kjør_linting(mappe)
    if not lint_resultat["success"]:
        self._log(f"[ADVARSEL] Linting: {lint_resultat['output']}", "WARNING")
    else:
        self._log("[OK] Linting: All kode følger PEP8")
    
    # 3. Sikkerhetsskanning
    self._log("[SIKKERHET] Skanner med bandit...")
    self._update_status("validerer", fase=5, progress=80)
    
    security_resultat = self._kjør_sikkerhetsskanning(mappe)
    if security_resultat["high_severity"] > 0:
        msg = f"Kritiske sikkerhetsfunnet: {security_resultat['issues']}"
        self._log(f"[FEIL] {msg}", "ERROR")
        return False, msg
    
    self._log("[OK] Sikkerhet: Ingen kritiske funn")
    
    # Git commit
    git = GitIntegration(mappe)
    git.commit(f"fase-5-validate: Alle tester OK ({dekning:.1f}% coverage)", prosjekt)
    
    prosjekt.status = "validate_ferdig"
    prosjekt.fase = 5
    prosjekt.sist_sjekket = datetime.now()
    
    # Send valideringsrapport
    self.event_queue.put({
        "type": "validation_report",
        "data": {
            "test_coverage": dekning,
            "lint_success": lint_resultat["success"],
            "security_issues": security_resultat["high_severity"],
            "git_commits": len(prosjekt.git_commits)
        }
    })
    
    self._update_status("validate_ferdig", fase=5, progress=100)
    self._log("[FASE 5] Fullført: All validering bestått")
    return True, "All validering bestått"


def _kjør_tester(self, mappe: Path) -> Dict:
    """Kjør pytest med dekning"""
    try:
        resultat = subprocess.run(
            ["python3", "-m", "pytest", "tests/", "-v", "--cov=src", "--cov-report=json"],
            cwd=mappe,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse dekning fra JSON
        cov_json = mappe / "coverage.json"
        dekning = 0
        if cov_json.exists():
            import json
            with open(cov_json) as f:
                cov_data = json.load(f)
                dekning = cov_data.get("totals", {}).get("percent_covered", 0)
        
        return {
            "success": resultat.returncode == 0,
            "output": resultat.stdout[-500:] if resultat.stdout else "",
            "coverage": dekning
        }
    except Exception as e:
        return {"success": False, "output": str(e), "coverage": 0}


def _kjør_linting(self, mappe: Path) -> Dict:
    """Kjør black og flake8"""
    try:
        # Black check
        black_res = subprocess.run(
            ["python3", "-m", "black", "--check", "src/", "tests/"],
            cwd=mappe,
            capture_output=True,
            text=True
        )
        
        # Flake8
        flake_res = subprocess.run(
            ["python3", "-m", "flake8", "src/", "tests/", "--max-line-length=88"],
            cwd=mappe,
            capture_output=True,
            text=True
        )
        
        return {
            "success": black_res.returncode == 0 and flake_res.returncode == 0,
            "output": (black_res.stdout + flake_res.stdout)[-500:]
        }
    except Exception as e:
        return {"success": False, "output": str(e)}


def _kjør_sikkerhetsskanning(self, mappe: Path) -> Dict:
    """Kjør bandit"""
    try:
        resultat = subprocess.run(
            ["python3", "-m", "bandit", "-r", "src/", "-f", "json"],
            cwd=mappe,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        import json
        funn = json.loads(resultat.stdout) if resultat.stdout else {"results": []}
        high_sev = sum(1 for issue in funn.get("results", []) if issue.get("issue_severity") == "HIGH")
        
        return {
            "success": high_sev == 0,
            "high_severity": high_sev,
            "issues": funn.get("results", [])[:3]
        }
    except Exception as e:
        return {"success": False, "high_severity": 1, "issues": [str(e)]}


# ═══════════════════════════════════════════════════════════
# FASE 6: DEPLOY (vår arkivering på Z:)
# ═══════════════════════════════════════════════════════════

def fase_6_deploy(self, prosjektnavn: str) -> bool:
    """
    FASE 6: DEPLOY
    - Git tag for release
    - Kopier til Z: (Bygg_Arkiv/Kode_arkiv)
    - Generer manifest
    """
    self._log(f"[FASE 6] DEPLOY: Arkiverer prosjekt")
    self._update_status("deployer", fase=6, progress=20)
    
    prosjekt = self.aktive_prosjekter[prosjektnavn]
    mappe = prosjekt.mappe
    
    # Git tag
    self._update_status("deployer", fase=6, progress=40)
    try:
        subprocess.run(
            ["git", "tag", "-a", f"v1.0-{datetime.now():%Y%m%d}", "-m", "Release v1.0"],
            cwd=mappe,
            capture_output=True
        )
    except:
        pass
    
    # Kopier til arkiv
    self._update_status("deployer", fase=6, progress=60)
    
    arkiv_dest = self.config["archive_path"] / prosjektnavn
    arkiv_dest.mkdir(parents=True, exist_ok=True)
    
    versjon = datetime.now().strftime("%Y%m%d_%H%M%S")
    versjon_mappe = arkiv_dest / f"v_{versjon}"
    
    # Kopier (ignore patterns)
    import shutil
    ignore = shutil.ignore_patterns(
        '__pycache__', '*.pyc', '.pytest_cache', '.git', 
        '*.egg-info', '.coverage', 'htmlcov'
    )
    shutil.copytree(mappe, versjon_mappe, ignore=ignore)
    
    self._update_status("deployer", fase=6, progress=80)
    
    # Generer manifest
    manifest = {
        "prosjekt": {
            "navn": prosjekt.navn,
            "beskrivelse": prosjekt.beskrivelse,
            "sprak": prosjekt.sprak,
            "test_dekning": prosjekt.test_dekning,
            "git_commits": prosjekt.git_commits,
        },
        "versjon": versjon,
        "sjekksum": self._generer_sjekksum(versjon_mappe),
        "deploy_dato": datetime.now().isoformat(),
    }
    
    import json
    with open(versjon_mappe / "manifest.json", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    prosjekt.status = "deploy_ferdig"
    prosjekt.fase = 6
    
    # Send ferdig-melding
    self.event_queue.put({
        "type": "completed",
        "data": {
            "prosjekt": prosjektnavn,
            "versjon": versjon,
            "lokasjon": str(versjon_mappe),
            "test_coverage": prosjekt.test_dekning,
            "git_commits": len(prosjekt.git_commits)
        }
    })
    
    self._update_status("deploy_ferdig", fase=6, progress=100)
    self._log(f"[FASE 6] Fullført: Arkivert til {versjon_mappe}")
    return True


def _generer_sjekksum(self, mappe: Path) -> str:
    """Generer hash av alle filer"""
    import hashlib
    sha256 = hashlib.sha256()
    
    for fil in sorted(mappe.rglob("*")):
        if fil.is_file() and fil.name != "manifest.json":
            sha256.update(fil.read_bytes())
    
    return sha256.hexdigest()[:16]


# Integrer disse metodene i SandkasseProtokoll klassen
# I hovedfilen: from sandkasse_protokoll_part2 import *
