#!/usr/bin/env python3
"""
AI Integrasjon - Kimi og Gemini API klienter
Forenklet versjon som støtter Ollama-fallback
"""
import os
import sys
import json
import requests
from typing import Optional, Dict, Any
from pathlib import Path

class KimiClient:
    """Kimi API klient (forenklet - bruker Ollama som fallback)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("KIMI_API_KEY", "")
        self.base_url = "https://api.moonshot.cn/v1"
        self._available = None
        
    def er_tilgjengelig(self) -> bool:
        """Sjekk om Kimi er tilgjengelig"""
        if self._available is not None:
            return self._available
            
        if not self.api_key:
            self._available = False
            return False
            
        try:
            # Sjekk om Ollama er tilgjengelig som fallback
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            self._available = resp.status_code == 200
            if self._available:
                print("[KimiClient] Bruker Ollama som fallback for Kimi")
        except:
            self._available = False
            
        return self._available
    
    def generer_kode(self, prompt: str, modell: str = None) -> str:
        """Generer kode via API eller Ollama"""
        if not self.er_tilgjengelig():
            return self._generer_med_ollama(prompt, modell)
        
        # Hvis vi har API-nøkkel, prøv Kimi API
        if self.api_key and self.api_key != "ollama-fallback":
            try:
                return self._generer_med_kimi(prompt, modell)
            except Exception as e:
                print(f"[KimiClient] Kimi API feilet: {e}, faller tilbake til Ollama")
                return self._generer_med_ollama(prompt, modell)
        
        return self._generer_med_ollama(prompt, modell)
    
    def _generer_med_kimi(self, prompt: str, modell: str = None) -> str:
        """Generer via Kimi API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": modell or "moonshot-v1-8k",
            "messages": [
                {"role": "system", "content": "Du er en ekspert Python-utvikler. Skriv konsis, produksjonsklar kode."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        
        return resp.json()["choices"][0]["message"]["content"]
    
    def _generer_med_ollama(self, prompt: str, modell: str = None) -> str:
        """Fallback til Ollama"""
        try:
            payload = {
                "model": modell or "deepseek-coder-v2:16b",
                "prompt": prompt,
                "stream": False,
                "system": "Du er en ekspert Python-utvikler. Skriv konsis, produksjonsklar kode.",
                "options": {
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            }
            
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=120
            )
            resp.raise_for_status()
            return resp.json().get("response", "")
        except Exception as e:
            return f"# Feil ved kodegenerering: {e}\n# Vennligst sjekk at Ollama kjører"


class GeminiClient:
    """Gemini API klient (forenklet - bruker Ollama som fallback)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        self._available = None
        
    def er_tilgjengelig(self) -> bool:
        """Sjekk om Gemini er tilgjengelig"""
        if self._available is not None:
            return self._available
            
        if not self.api_key:
            self._available = False
            return False
            
        # For nå bruker vi Ollama som fallback
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            self._available = resp.status_code == 200
        except:
            self._available = False
            
        return self._available
    
    def analyser_kode(self, kode: str, kontekst: str = "") -> Dict[str, Any]:
        """Analyser kode for feil og forbedringer"""
        prompt = f"""Analyser denne Python-koden for potensielle feil og forbedringer:

{kode}

{kontekst}

Gi svaret som JSON med følgende struktur:
{{
    "feil": ["liste over potensielle feil"],
    "forbedringer": ["liste over forslag"],
    "sikkerhet": ["sikkerhetsproblemer hvis noen"]
}}"""
        
        # Bruk Ollama for analyse
        try:
            payload = {
                "model": "qwen2.5:14b",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.3}
            }
            
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            
            result = resp.json().get("response", "{}")
            return json.loads(result)
        except Exception as e:
            return {
                "feil": [f"Kunne ikke analysere: {e}"],
                "forbedringer": [],
                "sikkerhet": []
            }


class AIAgent:
    """Hovedagent som koordinerer Kimi og Gemini"""
    
    def __init__(self):
        self.kimi = KimiClient()
        self.gemini = GeminiClient()
        self._prefer_kimi = True
        
    def er_tilgjengelig(self) -> bool:
        """Sjekk om minst en AI er tilgjengelig"""
        return self.kimi.er_tilgjengelig() or self.gemini.er_tilgjengelig()
    
    def generer_kode(self, prompt: str, bruk_kimi: bool = None) -> str:
        """Generer kode med foretrukket AI"""
        if bruk_kimi is None:
            bruk_kimi = self._prefer_kimi
            
        if bruk_kimi and self.kimi.er_tilgjengelig():
            return self.kimi.generer_kode(prompt)
        elif self.gemini.er_tilgjengelig():
            # Gemini kan også generere kode via Ollama
            return self.kimi._generer_med_ollama(prompt)  # Bruker Ollama
        else:
            # Fallback til lokal Ollama
            return self.kimi._generer_med_ollama(prompt)
    
    def analyser_feil(self, feil_melding: str, kode: str) -> Dict[str, Any]:
        """Analyser en feil og foreslå fiks"""
        return self.gemini.analyser_kode(kode, f"Feil: {feil_melding}")


if __name__ == "__main__":
    # Test
    print("Tester AI Integrasjon...")
    
    agent = AIAgent()
    
    print(f"Kimi tilgjengelig: {agent.kimi.er_tilgjengelig()}")
    print(f"Gemini tilgjengelig: {agent.gemini.er_tilgjengelig()}")
    
    if agent.er_tilgjengelig():
        print("\nGenererer test-kode...")
        kode = agent.generer_kode("Skriv en funksjon som beregner fibonacci-tall")
        print(kode[:500] + "..." if len(kode) > 500 else kode)
    else:
        print("Ingen AI tilgjengelig. Sjekk at Ollama kjører på localhost:11434")
