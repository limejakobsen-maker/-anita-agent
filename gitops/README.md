# GitOps for Anita Agent

Denne mappen inneholder GitOps-konfigurasjon for Anita Agent deployment.

## Struktur

```
gitops/
├── base/                    # Basiskonfigurasjon (miljø-uavhengig)
├── overlays/
│   ├── testing/            # Testing-miljø
│   └── production/         # Produksjonsmiljø
└── README.md
```

## GitOps-verktøy

Vi støtter to GitOps-verktøy:

### 1. Flux CD (anbefalt)
- Automated sync
- Image automation
- Policy-based deployment

### 2. ArgoCD
- Deklarativ oppsett
- UI for visuell oversikt
- App of Apps pattern

## Kom i gang

### Flux CD

```bash
# Install Flux
flux install

# Bootstrap repository
flux bootstrap github \
  --owner=YOUR_GITHUB_USER \
  --repository=anita-agent \
  --path=gitops/clusters/production \
  --personal
```

### ArgoCD

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Apply Application manifests
kubectl apply -f gitops/argocd/applications/
```

## Miljøer

| Miljø | Namespace | Branch | Auto-sync |
|-------|-----------|--------|-----------|
| Testing | testing-anita-agent | develop | Ja |
| Production | anita-agent | main | Ja (med approval) |

## Image Tagging

- **Testing**: `develop-<sha>`
- **Production**: `v<version>` eller `<sha>`

## Troubleshooting

Se `troubleshooting.md` for vanlige problemer og løsninger.
