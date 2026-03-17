# 🚀 PROMPT: Be Anita implementere forbedringer med sine agenter

**Kopier teksten under og lim inn i AnythingLLM:**

---

```
Hei Anita! 

Takk for analysen! Nå vil jeg at du skal IMPLEMENTERE forbedringene ved å bruke dine egne agenter.

## OPPGAVE
Bruk dine AI-agenter til å implementere følgende forbedringer i systemet mitt:

### 1. 🔴 KRITISK: Robust feilhåndtering
- AGENT: "SecurityAgent"
- OPPGAVE: Forbedre self_healing_wrapper.py med:
  * Circuit breaker pattern
  * Exponential backoff for retries
  * Bedre logging med strukturert JSON
  * Fallback-kjeder (hvis Ollama feiler → prøv Kimi → prøv Gemini)

### 2. 🟠 HØY: GitHub Actions CI/CD
- AGENT: "DevOpsAgent"  
- OPPGAVE: Lag komplett GitHub Actions workflow:
  * .github/workflows/deploy.yml
  * Automatisk testing på PR
  * Bygg og push Docker images til GitHub Container Registry
  * Deploy til Kubernetes ved merge til main
  * Integrer med eksisterende git_integration.py

### 3. 🟡 MEDIUM: ComfyUI optimalisering
- AGENT: "IntegrationAgent"
- OPPGAVE: Forbedre comfyui_integration.py:
  * Legg til caching av prompts
  * Queue-system for bildegenerering
  * Progress-tracking via WebSocket
  * Bedre feilhåndtering hvis ComfyUI er nede

### 4. 🟢 MEDIUM: Smart Git forbedring  
- AGENT: "GitAgent"
- OPPGAVE: Utvid git_integration.py:
  * Automatisk PR-oppretting ved fase-fullføring
  * Integrasjon med conventional commits
  * Auto-generering av release notes
  * Støtte for GitHub API (ikke bare lokalt git)

### 5. 🔵 LAV: Kubernetes optimalisering
- AGENT: "K8sAgent"
- OPPGAVE: Forbedre Kubernetes-manifester:
  * Legg til HPA (Horizontal Pod Autoscaler)
  * Resource limits/requests på alle pods
  * NetworkPolicies for sikkerhet
  * PodDisruptionBudgets

### 6. 🟣 BONUS: Telegram-overvåking
- AGENT: "MonitoringAgent"
- OPPGAVE: Lag telegram_monitor.py:
  * Webhook som mottar alerts fra Kubernetes
  * Formater og send til Telegram Bot
  * Dashboard-kommando (!status viser alle tjenester)
  * Alert ved pod crashes/restarts

## LEVERANSEFORMAT

For hver agent, gi meg:

```
AGENT: [Navn]
STATUS: [Klar til jobbe / Vent på avhengighet]
FIL: [Fil som skal lages/endres]
KODE:
```python
[Full kode her]
```
BESKRIVELSE: [Hva ble gjort]
TESTING: [Hvordan teste]
```

## ARBEIDSREKKEFØLGE

1. Start med SecurityAgent (feilhåndtering) - dette er fundamentet
2. Deretter DevOpsAgent (CI/CD) - dette muliggjør automatisk deploy
3. Så GitAgent - integrerer med CI/CD
4. Deretter IntegrationAgent og K8sAgent (kan jobbe parallelt)
5. Til slutt MonitoringAgent - avhenger av at alt annet fungerer

## SPESIFIKKE KRAV

1. All kode skal være på NORSK (kommentarer, variabelnavn, docstrings)
2. Bruk type hints i Python
3. Inkluder docstrings for alle funksjoner
4. Følg eksisterende kodestil fra filene jeg delte
5. Sikre bakoverkompatibilitet der det er mulig

## EKSTRA OPPGAVE

Hvis du finner flere gratis forbedringer mens agenter jobber:
- Noter dem ned
- Prioriter dem
- La "ImprovementAgent" implementere dem

---

**SPØRSMÅL TIL DEG:**

1. Skal jeg starte med én agent om gangen, eller kan flere jobbe parallelt?
2. Vil du ha koden som ferdige filer jeg kan kopiere, eller som git patcher?
3. Skal agenter også lage tester for koden de produserer?

La oss starte! 🚀
```

---

## 💡 ALTERNATIV - Kortere versjon

Hvis Anita blir overveldet, bruk denne korte versjonen:

```
Anita, bruk dine agenter til å implementere disse forbedringene:

PRIORITET 1 (Gjør nå):
1. Lag GitHub Actions workflow (.github/workflows/deploy.yml)
2. Forbedre self_healing_wrapper.py med circuit breaker
3. Lag telegram_monitor.py for varsling

For hver oppgave:
- Navngi agenten
- Gi meg full kode
- Forklar hva som ble gjort

Start med prioritet 1. Klar? 🚀
```

---

## 📋 TIPS FOR DEG

Når Anita svarer:
1. Kopier koden hun gir deg
2. Lagre til riktig fil
3. Test at det fungerer
4. Gi Anita tilbakemelding
5. Fortsett til neste agent

Hvis Anita spør om noe du ikke vet, spør meg! 
