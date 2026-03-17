# 🤖 PROMPT: Anita + OpenClaw Samarbeid

**Kopier og lim inn i AnythingLLM:**

```
Hei Anita! 

Du har rett i at vi kan bruke agenter - men vi har faktisk TO agenter:
1. DEG (Anita) - koordinering og arkitektur
2. OpenClaw (port 3000) - kodegenerering og utførelse

## SAMARBEIDSPLAN

### DIN ROLLE (Anita):
- Planlegge arkitektur
- Revidere kode
- Koordinere oppgaver
- Sikkerhetsvurdering

### OPENCLAWS ROLLE:
- Skrive faktisk kode
- Implementere funksjoner
- Teste lokalt
- Generere filer

## ARBEIDSREKKEFØLGE

### FASE 1: GitHub Actions CI/CD
Du: Design workflow-strukturen
OpenClaw: Generer .github/workflows/deploy.yml

### FASE 2: Feilhåndtering
Du: Spesifiser circuit breaker-pattern
OpenClaw: Implementer i self_healing_wrapper.py

### FASE 3: Telegram Monitor
Du: Design meldingsformat og kommandoer
OpenClaw: Lag telegram_monitor.py

### FASE 4: Git Integrasjon
Du: Spesifiser GitHub API-krav
OpenClaw: Utvid git_integration.py

## KOMMUNIKASJON

Når du gir oppgaver til OpenClaw, bruk dette formatet:

```
OPENCLAW OPPGAVE:
FIL: [filnavn]
FUNKSJONALITET: [hva skal gjøres]
KRAV: [spesifikke krav]
KODE-STIL: [fra eksisterende fil]
```

## DINE OPPGAVER NÅ

1. Start med å designe GitHub Actions workflow
2. Gi spesifikasjon til OpenClaw
3. Revider koden OpenClaw lager
4. Fortsett til neste fase

## ELLER - ALTERNATIV

Hvis OpenClaw ikke er tilgjengelig akkurat nå:
- Ta på deg begge rollene
- Gi meg koden direkte
- Jeg tester lokalt

Hva foretrekker du? 🚀
```

---

# 🔄 ALTERNATIV: La OpenClaw gjøre ALT

Hvis du vil at OpenClaw skal gjøre mest mulig:

```
Hei Anita!

Jeg vil at du skal bruke OpenClaw (som kjører på port 3000 i clusteret) til å implementere alle forbedringene.

## PLAN

For hver forbedring:
1. Du analyserer hva som trengs
2. Du sender instruksjoner til OpenClaw via API
3. OpenClaw genererer koden
4. Du verifiserer og gir meg resultatet

## START HER

Send følgende kommando til OpenClaw:

"Generer en komplett GitHub Actions workflow-fil (.github/workflows/deploy.yml) som:
- Tester Python-kode ved PR
- Bygger Docker images
- Deployer til Kubernetes ved merge til main
- Inkluderer caching for raskere bygg"

Hva svarer OpenClaw? 🚀
```

---

# ⚡ RASKESTE VERSJON

```
Anita, bruk OpenClaw til å generere koden! 

1. Be OpenClaw lage .github/workflows/deploy.yml
2. Be OpenClaw forbedre self_healing_wrapper.py
3. Be OpenClaw lage telegram_monitor.py

Gi meg resultatet fra OpenClaw etter hver oppgave. Start nå! 🚀
```

---

# 💡 HUSK

OpenClaw kjører på: `http://localhost:3000` (fra din PC)
Eller: `http://openclaw-service:3000` (inni clusteret)

Hvis OpenClaw ikke svarer, kan du:
1. Sjekke at podden kjører: kubectl get pods -l app=openclaw-binary
2. Eller la Anita gjøre jobben selv
