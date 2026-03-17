#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SANDKASSE-PROTOKOLLEN v3.0 - OPTIMAL EDITION
Kombinerer GSD's beste med vår selvhelbredende arkitektur
6-fase flyt: INIT → DISCUSS → PLAN → EXECUTE → VALIDATE → DEPLOY
"""

import os
import sys
import json
import shutil
import subprocess
import ast
import hashlib
import inspect
import re
import threading
import queue
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable, Any
from dataclasses import dataclass, asdict, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile

# Konfigurasjon
CONFIG = {
    "base_path": Path.home() / "sandkasse_produksjon",
    "archive_path": Path("/mnt/Bygg_Arkiv/Kode_arkiv"),  # Z: drive mount
    "log_path": Path("logs"),
    "max_iterations": 10,
    "safety_checks": True,
    "required_tests_pass": 90,
    "server_port": 8765,
    "tailscale_ip": "100.108.91.44",
    "fresh_context_enabled": True,  # GSD: Fresh context per plan
    "parallel_execution": True,      # GSD: Parallel tasks
}

@dataclass
class Prosjekt:
    """Struktur for hvert kodeprosjekt"""
    navn: str
    beskrivelse: str
    sprak: str = "python"
    mappe: Path = None
    status: str = "initiert"
    iterasjon: int = 0
    test_dekning: float = 0.0
    fase: int = 0
    context: Dict = field(default_factory=dict)  # GSD: Context per fase
    sist_sjekket: Optional[datetime] = None
    feil_log: List[Dict] = field(default_factory=list)
    fixes: List[Dict] = field(default_factory=list)
    git_commits: List[str] = field(default_factory=list)  # GSD: Track commits
    
    def to_dict(self):
        return {
            "navn": self.navn,
            "beskrivelse": self.beskrivelse,
            "sprak": self.sprak,
            "status": self.status,
            "fase": self.fase,
            "iterasjon": self.iterasjon,
            "test_dekning": self.test_dekning,
            "context_keys": list(self.context.keys()),
            "sist_sjekket": self.sist_sjekket.isoformat() if self.sist_sjekket else None
        }

class ContextManager:
    """GSD: Fresh context management - unngå context rot"""
    
    def __init__(self, max_context_size: int = 50000):
        self.max_size = max_context_size
        self.context_history = []
        self.summaries = []
    
    def create_fresh_context(self, phase: str, project: Prosjekt) -> str:
        """Lag fresh context for en ny fase (GSD pattern)"""
        summary = self._generate_summary(project)
        
        fresh_context = f"""
=== FRESH CONTEXT: {phase} ===
Prosjekt: {project.navn}
Status: Fase {project.fase}
Sist oppdatering: {datetime.now().isoformat()}

=== SUMMARY (autogenerert) ===
{summary}

=== VIKTIGE BESLUTNINGER ===
"""
        # Legg til låste beslutninger fra context
        for key, value in project.context.items():
            if key.startswith('LOCKED_'):
                fresh_context += f"\n{key}: {value}"
        
        return fresh_context
    
    def _generate_summary(self, project: Prosjekt) -> str:
        """Generer kortfattet summary av prosjektet"""
        summary = f"""
- Navn: {project.navn}
- Beskrivelse: {project.beskrivelse[:100]}...
- Fase: {project.fase} ({self._fase_name(project.fase)})
- Iterasjoner: {project.iterasjon}
- Test-dekning: {project.test_dekning:.1f}%
- Git commits: {len(project.git_commits)}
"""
        return summary
    
    def _fase_name(self, fase: int) -> str:
        faser = ["Init", "Init", "Discuss", "Plan", "Execute", "Validate", "Deploy"]
        return faser[fase] if fase < len(faser) else "Unknown"
    
    def archive_old_context(self, project: Prosjekt):
        """Arkiver gammel context for å holde vinduet rent"""
        archive_dir = Path(".planning/contexts")
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_dir / f"{project.navn}_fase{project.fase}_{timestamp}.md"
        
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(f"# Arkivert Context: {project.navn}\n")
            f.write(f"Fase: {project.fase}\n")
            f.write(f"Tid: {timestamp}\n\n")
            f.write(json.dumps(project.context, indent=2, default=str))
        
        # Tøm aktiv context (behold kun låste beslutninger)
        locked = {k: v for k, v in project.context.items() if k.startswith('LOCKED_')}
        project.context = locked

class ParallelRunner:
    """GSD: Kjør uavhengige oppgaver parallelt"""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def run_parallel(self, tasks: List[Callable], project: Prosjekt) -> List[Any]:
        """Kjør oppgaver parallelt og samle resultater"""
        results = []
        futures = []
        
        for task in tasks:
            future = self.executor.submit(task)
            futures.append(future)
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        
        return results
    
    def research_parallel(self, topics: List[str], project: Prosjekt) -> Dict[str, str]:
        """GSD: Parallell research av flere topics"""
        results = {}
        
        def research_topic(topic):
            # Simulert research - i produksjon ville dette kalle AI
            return f"Research om {topic}: Patterns identifisert, best practices funnet"
        
        with ThreadPoolExecutor(max_workers=len(topics)) as executor:
            future_to_topic = {executor.submit(research_topic, topic): topic for topic in topics}
            
            for future in as_completed(future_to_topic):
                topic = future_to_topic[future]
                try:
                    results[topic] = future.result()
                except Exception as e:
                    results[topic] = f"Error: {str(e)}"
        
        return results

class GitIntegration:
    """GSD: Atomic commits per task/fase"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.initialized = False
    
    def init_repo(self):
        """Initialiser git repo hvis ikke eksisterer"""
        git_dir = self.project_path / ".git"
        if not git_dir.exists():
            subprocess.run(["git", "init"], cwd=self.project_path, capture_output=True)
            self._create_gitignore()
            self.initialized = True
    
    def _create_gitignore(self):
        """Lag .gitignore for prosjektet"""
        gitignore_content = """
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
*.log
logs/*.log
backups/*.bak
fixes/*.py
.planning/
*.tmp
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
"""
        (self.project_path / ".gitignore").write_text(gitignore_content)
    
    def commit(self, message: str, project: Prosjekt) -> bool:
        """Lag atomic commit"""
        try:
            # Stage all
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_path,
                capture_output=True
            )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Track commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True
                )
                if hash_result.returncode == 0:
                    commit_hash = hash_result.stdout.strip()
                    project.git_commits.append(f"{commit_hash}: {message}")
                return True
            
            return False
        except Exception as e:
            print(f"Git commit feilet: {e}")
            return False

class SandkasseProtokoll:
    """Hovedklasse - 6-fase optimal sandkasse"""
    
    def __init__(self, event_queue=None):
        self.config = CONFIG
        self._setup_directories()
        
        # GSD komponenter
        self.context_manager = ContextManager()
        self.parallel_runner = ParallelRunner()
        
        # Tilstand
        self.aktive_prosjekter: Dict[str, Prosjekt] = {}
        self.current_prosjekt: Optional[Prosjekt] = None
        self.is_running = False
        self.should_stop = False
        self.event_queue = event_queue or queue.Queue()
    
    def _setup_directories(self):
        """Sikre at nødvendige mapper finnes"""
        self.config["base_path"].mkdir(parents=True, exist_ok=True)
        self.config["log_path"].mkdir(parents=True, exist_ok=True)
        self.config["archive_path"].mkdir(parents=True, exist_ok=True)
        
        # GSD: Planleggingsmappe
        (Path(".planning") / "research" / "contexts").mkdir(parents=True, exist_ok=True)
    
    def _log(self, message: str, level: str = "INFO"):
        """Logg til fil og event-kø"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "fase": self.current_prosjekt.fase if self.current_prosjekt else 0
        }
        
        # Skriv til fil
        log_file = self.config["log_path"] / f"protokoll_{datetime.now():%Y%m%d}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} [{level}] {message}\n")
        
        # Send til event-kø
        self.event_queue.put({"type": "log", "data": log_entry})
        
        print(f"{timestamp} [{level}] {message}")
    
    def _update_status(self, status: str, fase: int = None, progress: int = None):
        """Oppdater status og send til monitor"""
        if self.current_prosjekt:
            self.current_prosjekt.status = status
            if fase is not None:
                self.current_prosjekt.fase = fase
        
        status_data = {
            "type": "status",
            "data": {
                "prosjekt": self.current_prosjekt.navn if self.current_prosjekt else None,
                "status": status,
                "fase": fase or (self.current_prosjekt.fase if self.current_prosjekt else 0),
                "progress": progress,
                "is_running": self.is_running
            }
        }
        self.event_queue.put(status_data)
    
    def _send_code(self, code: str, filename: str = "main.py"):
        """Send kode til monitor for visning"""
        self.event_queue.put({
            "type": "code",
            "data": {"filename": filename, "code": code}
        })
    
    # ═══════════════════════════════════════════════════════════
    # FASE 1: INIT (GSD: Initialize Project)
    # ═══════════════════════════════════════════════════════════
    def fase_1_init(self, prosjektnavn: str, krav: str) -> Prosjekt:
        """
        FASE 1: INIT
        - Omfattende spørsmål for å forstå idé
        - Research (valgfritt)
        - Requirements (v1, v2, out-of-scope)
        - Roadmap
        """
        self._log(f"[FASE 1] INIT: '{prosjektnavn}'")
        self._update_status("initialiserer", fase=1, progress=10)
        
        prosjekt_mappe = self.config["base_path"] / prosjektnavn
        prosjekt_mappe.mkdir(parents=True, exist_ok=True)
        
        # GSD: Opprett mappestruktur
        struktur = {
            "src": prosjekt_mappe / "src",
            "tests": prosjekt_mappe / "tests",
            "docs": prosjekt_mappe / "docs",
            ".planning": prosjekt_mappe / ".planning",
            ".planning/research": prosjekt_mappe / ".planning/research",
            ".planning/contexts": prosjekt_mappe / ".planning/contexts",
        }
        for mappe in struktur.values():
            mappe.mkdir(exist_ok=True)
        
        self._update_status("initialiserer", fase=1, progress=30)
        
        # Lag PROJECT.md (GSD-stil)
        project_md = f"""# {prosjektnavn}

## Beskrivelse
{krav}

## Mål
- [ ] MVP (Minimum Viable Product)
- [ ] V1: Full funksjonalitet
- [ ] V2: Avanserte features

## Out of Scope
- V3+ features (planlegges senere)

## Teknologi
- Språk: Python 3.12
- Testing: pytest
- Linting: black, flake8
- Security: bandit

## Opprettet
{datetime.now().isoformat()}
"""
        (prosjekt_mappe / "docs" / "PROJECT.md").write_text(project_md)
        
        # Lag REQUIREMENTS.md (GSD-stil)
        requirements_md = f"""# Requirements

## V1 (MVP)
- Basisfunksjonalitet
- Kjerne-features

## V2
- Utvidet funksjonalitet
- Integrasjoner

## Out of Scope
- Features utsatt til senere
"""
        (prosjekt_mappe / "docs" / "REQUIREMENTS.md").write_text(requirements_md)
        
        # Lag ROADMAP.md (GSD-stil)
        roadmap_md = f"""# Roadmap

## Fase 1: DISCUSS
Diskutere kontekst og beslutninger

## Fase 2: PLAN
Planlegge implementasjon

## Fase 3: EXECUTE
Kode generering med @heal

## Fase 4: VALIDATE
Testing og verifisering

## Fase 5: DEPLOY
Arkivering og dokumentasjon
"""
        (prosjekt_mappe / "docs" / "ROADMAP.md").write_text(roadmap_md)
        
        # Lag STATE.md for tracking
        state_md = f"""# State
Prosjekt: {prosjektnavn}
Status: Init
Sist oppdatert: {datetime.now().isoformat()}
Fase: 1
"""
        (prosjekt_mappe / "STATE.md").write_text(state_md)
        
        # Initialiser Git
        git = GitIntegration(prosjekt_mappe)
        git.init_repo()
        
        self._update_status("init_ferdig", fase=1, progress=100)
        
        # Opprett prosjekt-objekt
        prosjekt = Prosjekt(
            navn=prosjektnavn,
            beskrivelse=krav,
            mappe=prosjekt_mappe,
            status="init_ferdig",
            fase=1
        )
        
        self.aktive_prosjekter[prosjektnavn] = prosjekt
        self.current_prosjekt = prosjekt
        
        self._log(f"[FASE 1] Fullført: Prosjekt initialisert")
        return prosjekt
    
    # ═══════════════════════════════════════════════════════════
    # FASE 2: DISCUSS (GSD: Discuss Phase)
    # ═══════════════════════════════════════════════════════════
    def fase_2_discuss(self, prosjektnavn: str) -> bool:
        """
        FASE 2: DISCUSS - NY! (Fra GSD)
        - Shape implementation
        - Visual features → layout, density, interactions
        - API/CLI → response format, flags, error handling
        - Content → structure, tone, depth
        - Output: CONTEXT.md med låste beslutninger
        """
        self._log(f"[FASE 2] DISCUSS: Forme implementasjon")
        self._update_status("diskuterer", fase=2, progress=20)
        
        prosjekt = self.aktive_prosjekter[prosjektnavn]
        
        # Analyser prosjekt-type
        beskrivelse = prosjekt.beskrivelse.lower()
        
        # Identifiser grå områder basert på type
        gray_areas = []
        
        if any(word in beskrivelse for word in ["gui", "interface", "web", "app"]):
            gray_areas.extend([
                ("visual", "Layout og design"),
                ("visual", "Interaksjonsmønstre"),
                ("visual", "Empty states")
            ])
        
        if any(word in beskrivelse for word in ["api", "cli", "server"]):
            gray_areas.extend([
                ("api", "Response format"),
                ("api", "Error handling"),
                ("api", "Flags og options")
            ])
        
        if not gray_areas:
            gray_areas = [
                ("general", "Arkitektur-pattern"),
                ("general", "Datastrukturer"),
                ("general", "Feilhåndtering")
            ]
        
        self._update_status("diskuterer", fase=2, progress=50)
        
        # Lag CONTEXT.md
        context_md = f"""# Context: {prosjektnavn}

## Grå områder identifisert
"""
        for area_type, area_desc in gray_areas:
            context_md += f"\n### {area_desc} ({area_type})\n"
            context_md += "- Beslutning: [Fylles ut i GUI/Dialog]\n"
        
        context_md += f"""

## Låste beslutninger (LOCKED_*)
- [ ] Ingen ennå - diskuter med bruker

## Notater
Opprettet: {datetime.now().isoformat()}
"""
        
        context_path = prosjekt.mappe / ".planning" / "CONTEXT.md"
        context_path.write_text(context_md)
        
        # Lagre i prosjekt-context
        prosjekt.context['gray_areas'] = gray_areas
        prosjekt.context['discussion_pending'] = True
        
        # Request diskusjon fra Acer
        self.event_queue.put({
            "type": "discussion_request",
            "data": {
                "prosjekt": prosjektnavn,
                "gray_areas": gray_areas,
                "context_file": str(context_path)
            }
        })
        
        # Vent på at bruker fullfører diskusjon
        self._update_status("venter_diskusjon", fase=2, progress=80)
        
        # I en full implementasjon ville vi ventet på brukerinput her
        # For nå simulerer vi at diskusjon er fullført
        prosjekt.context['LOCKED_architecture'] = "Modular"
        prosjekt.context['LOCKED_testing'] = "pytest with >90% coverage"
        prosjekt.context['LOCKED_style'] = "PEP8 with black formatter"
        prosjekt.context['discussion_pending'] = False
        
        # Oppdater CONTEXT.md med låste beslutninger
        context_md += f"""

## Låste beslutninger (etter diskusjon)
"""
        for key, value in prosjekt.context.items():
            if key.startswith('LOCKED_'):
                context_md += f"- {key}: {value}\n"
        
        context_path.write_text(context_md)
        
        prosjekt.status = "discuss_ferdig"
        prosjekt.fase = 2
        
        self._update_status("discuss_ferdig", fase=2, progress=100)
        self._log("[FASE 2] Fullført: Kontekst etablert")
        return True
    
    # ═══════════════════════════════════════════════════════════
    # FASE 3: PLAN (GSD: Plan Phase)
    # ═══════════════════════════════════════════════════════════
    def fase_3_plan(self, prosjektnavn: str) -> bool:
        """
        FASE 3: PLAN (GSD: Plan Phase)
        - Research: Hvordan implementere
        - Gitt CONTEXT.md, planlegg løsning
        - Lag 2-3 atomic planer med XML struktur
        - Verifiser planer mot krav
        """
        self._log(f"[FASE 3] PLAN: Planlegger implementasjon")
        self._update_status("planlegger", fase=3, progress=20)
        
        prosjekt = self.aktive_prosjekter[prosjektnavn]
        
        # GSD: Fresh context før planlegging
        if self.config["fresh_context_enabled"]:
            self.context_manager.create_fresh_context("PLAN", prosjekt)
        
        # Identifiser research-topics basert på kontekst
        research_topics = [
            "Python best practices",
            "Testing patterns",
            "Error handling strategies"
        ]
        
        # GSD: Parallell research
        if self.config["parallel_execution"]:
            self._update_status("forsker", fase=3, progress=40)
            research_results = self.parallel_runner.research_parallel(
                research_topics, prosjekt
            )
            
            # Lagre research
            research_md = "# Research\n\n"
            for topic, result in research_results.items():
                research_md += f"## {topic}\n{result}\n\n"
            
            (prosjekt.mappe / ".planning" / "research" / "RESEARCH.md").write_text(research_md)
        
        self._update_status("planlegger", fase=3, progress=70)
        
        # Lag atomic planer (GSD-stil)
        planer = [
            {
                "id": "plan-1",
                "name": "Setup og struktur",
                "tasks": [
                    "Opprette mappestruktur",
                    "Sette opp pytest",
                    "Lage main.py skelett"
                ]
            },
            {
                "id": "plan-2",
                "name": "Kjerneimplementasjon",
                "tasks": [
                    "Implementere kjerneklasser",
                    "Legge til @heal dekorator",
                    "Teste grunnleggende funksjonalitet"
                ]
            },
            {
                "id": "plan-3",
                "name": "Validering og dokumentasjon",
                "tasks": [
                    "Kjøre pytest",
                    "Sjekk linting",
                    "Oppdatere dokumentasjon"
                ]
            }
        ]
        
        # Lag plan-filer
        for i, plan in enumerate(planer, 1):
            plan_xml = f"""<plan id="{plan['id']}">
    <name>{plan['name']}</name>
    <phase>3</phase>
    <project>{prosjektnavn}</project>
    <tasks>
"""
            for task in plan['tasks']:
                plan_xml += f"        <task>{task}</task>\n"
            
            plan_xml += """    </tasks>
</plan>
"""
            plan_path = prosjekt.mappe / ".planning" / f"PLAN-{i}.xml"
            plan_path.write_text(plan_xml)
        
        # Git commit
        git = GitIntegration(prosjekt.mappe)
        git.commit("fase-3-plan: Atomic planer opprettet", prosjekt)
        
        prosjekt.status = "plan_ferdig"
        prosjekt.fase = 3
        
        self._update_status("plan_ferdig", fase=3, progress=100)
        self._log("[FASE 3] Fullført: Planer klare")
        return True
    
    # ═══════════════════════════════════════════════════════════
    # FASE 4-6: Fortsettelse i neste fil (delt for lesbarhet)
    # ═══════════════════════════════════════════════════════════
    
    def kjør_full_protokoll(self, prosjektnavn: str, krav: str) -> bool:
        """Kjør alle 6 faser i sekvens"""
        self._log(f"[START] Optimal Sandkasse for '{prosjektnavn}'")
        self.is_running = True
        self.should_stop = False
        
        try:
            # Fase 1-3: Setup og planlegging (GSD-inspirert)
            if not self.fase_1_init(prosjektnavn, krav):
                return False
            
            if not self.fase_2_discuss(prosjektnavn):
                return False
            
            if not self.fase_3_plan(prosjektnavn):
                return False
            
            self._log("[FERDIG] Fase 1-3 fullført - klar for Execute!")
            self.is_running = False
            return True
            
        except Exception as e:
            self._log(f"[KRITISK] Feil: {e}", "ERROR")
            self.is_running = False
            return False


# Entry point for testing
if __name__ == "__main__":
    print("Sandkasse-Protokollen v3.0 - Optimal Edition")
    print("Kjør: protokoll_server.py for full funksjonalitet")
