# CI/CD Guide for Anita Agent

Denne guiden forklarer hvordan CI/CD-pipelinen er satt opp og hvordan du bruker den.

## 📋 Oversikt

```
┌─────────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CODE PUSH    →  2. TESTS    →  3. BUILD    →  4. DEPLOY     │
│       │                  │               │              │       │
│       ▼                  ▼               ▼              ▼       │
│  ┌────────┐       ┌──────────┐    ┌──────────┐   ┌──────────┐  │
│  │ Lint   │       │ Unit     │    │ Docker   │   │ K3d      │  │
│  │ Format │       │ Integr.  │    │ Push     │   │ Testing  │  │
│  │ Security│       │ Coverage │    │          │   │ GitOps   │  │
│  └────────┘       └──────────┘    └──────────┘   └──────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Kom i gang

### 1. GitHub Secrets (Påkrevd)

Gå til **Settings → Secrets and variables → Actions** og legg til:

| Secret | Beskrivelse |
|--------|-------------|
| `GITHUB_TOKEN` | Autogenerert (trenger packages:write) |
| `ARGOCD_API_URL` | URL til ArgoCD server (valgfritt) |
| `ARGOCD_TOKEN` | ArgoCD API token (valgfritt) |

### 2. Aktiver GitHub Container Registry

1. Gå til **Settings → Packages**
2. Sikre at "Inherit access from source repository" er på

### 3. Konfigurer GitOps (Velg ett)

#### Alternativ A: Flux CD

```bash
# Install Flux CLI
brew install fluxcd/tap/flux  # macOS
# eller
curl -s https://fluxcd.io/install.sh | sudo bash  # Linux

# Bootstrap (kjør på cluster)
flux bootstrap github \
  --owner=din-bruker \
  --repository=PROSJEKTMAPPE-AI \
  --branch=main \
  --path=gitops/flux \
  --personal
```

#### Alternativ B: ArgoCD

```bash
# Installer ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Appliser Applications
kubectl apply -f gitops/argocd/
```

## 🔧 Pipeline Stages

### Stage 1: Code Quality

```yaml
Jobs: code-quality
Tools:
  - Black (formatting)
  - isort (import sorting)
  - Flake8 (linting)
  - Bandit (security)
  - Pylint (code analysis)
```

**Hvis denne feiler:** Fiks kodekvalitet før merge.

### Stage 2: Testing

```yaml
Jobs: test
Types:
  - Unit tests (isolated, rask)
  - Integration tests (med dependencies)
Coverage: Minst 80%
```

**Kjøre lokalt:**
```bash
# Alle tester
pytest

# Kun unit tester
pytest -m unit

# Med coverage
pytest --cov=. --cov-report=html
```

### Stage 3: Build

```yaml
Jobs: build
Output: ghcr.io/emil/anita-agent:<tag>
Tags:
  - main: latest, sha-xxxx
  - develop: develop, develop-sha-xxxx
```

### Stage 4: Deploy

| Miljø | Trigger | Namespace | GitOps |
|-------|---------|-----------|--------|
| Testing | Push til develop | testing-anita-agent | Auto-sync |
| Production | Push til main | anita-agent | Manuell approval |

## 📊 Testing Strategy

### Testkategorier

```
tests/
├── unit/              # Raske, isolerte tester
│   ├── test_error_handler.py
│   └── test_self_healing_wrapper.py
├── integration/       # Tester med eksterne deps
│   └── test_protocol_server.py
└── fixtures/          # Test data
```

### Markers

Bruk markers for å kategorisere tester:

```python
@pytest.mark.unit              # Unit test
@pytest.mark.integration       # Integration test
@pytest.mark.slow              # Trenger >1s
@pytest.mark.security          # Sikkerhetstest
```

### Kjøre spesifikke tester

```bash
# Kun unit tester
pytest -m unit

# Unngå treige tester
pytest -m "not slow"

# Kun sikkerhetstester
pytest -m security
```

## 🐳 Docker

### Bygge lokalt

```bash
# Bygg for testing
docker build --target testing -t anita-agent:test .

# Bygg for produksjon
docker build --target production -t anita-agent:latest .
```

### Kjøre lokalt

```bash
docker run -p 8080:8080 -p 8765:8765 anita-agent:latest
```

## ☸️ Kubernetes / K3d

### Sette opp lokal cluster

```bash
# Install K3d
brew install k3d  # macOS
# eller
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Lag cluster
k3d cluster create anita-agent \
  --agents 2 \
  --port "8080:80@loadbalancer" \
  --port "8765:8765@loadbalancer"

# Deploy
kubectl apply -k gitops/overlays/testing
```

### Verifisere deployment

```bash
# Sjekk pods
kubectl get pods -n testing-anita-agent

# Sjekk logs
kubectl logs -n testing-anita-agent -l app=anita-agent

# Port-forward for testing
kubectl port-forward -n testing-anita-agent svc/anita-agent 8080:8080
```

## 🔄 GitOps Workflows

### Flux CD Image Automation

Flux vil automatisk:
1. Sjekke for nye images
2. Oppdatere kustomization.yaml
3. Commite endringer
4. Synce til cluster

### ArgoCD Sync

ArgoCD vil:
1. Sjekke repository hvert 3. minutt
2. Detektere endringer
3. Synce automatisk (hvis enabled)

## 📈 Monitorering

### GitHub Actions

- Gå til **Actions** fanen i repo
- Se status for hver workflow
- Klikk inn for detaljer

### Kubernetes

```bash
# Sjekk deployment status
kubectl get deployments -n anita-agent

# Sjekk events
kubectl get events -n anita-agent --sort-by='.lastTimestamp'

# Sjekk resources
kubectl top pods -n anita-agent
```

## 🛠️ Troubleshooting

### Pipeline feiler på tester

```bash
# Kjør lokalt for debugging
pytest -xvs  # Verbose output

# Sjekk hvilken test som feiler
pytest --tb=long
```

### Docker build feiler

```bash
# Sjekk Dockerfile syntaks
docker build --no-cache -t test .

# Sjekk layers
docker history anita-agent:latest
```

### Kubernetes deployment feiler

```bash
# Sjekk beskrivelse
kubectl describe deployment anita-agent -n testing-anita-agent

# Sjekk pod events
kubectl describe pod <pod-name> -n testing-anita-agent

# Sjekk logs
kubectl logs <pod-name> -n testing-anita-agent --previous
```

### GitOps sync feiler

**Flux:**
```bash
flux get kustomizations
flux logs
```

**ArgoCD:**
```bash
argocd app list
argocd app logs anita-agent-testing
```

## 📝 Best Practices

1. **Alltid skriv tester** for ny funksjonalitet
2. **Hold coverage >80%** for å sikre kvalitet
3. **Bruke feature branches** for utvikling
4. **Code review** før merge til main
5. **Monitorer** produksjon etter deploy

## 🔗 Nyttige Lenker

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [pytest Docs](https://docs.pytest.org/)
- [Flux CD Docs](https://fluxcd.io/docs/)
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)
- [K3d Docs](https://k3d.io/)

---

**Sist oppdatert:** 2026-03-17
