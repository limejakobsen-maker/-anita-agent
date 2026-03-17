<#
.SYNOPSIS
    Testskript for AI-studio – sjekker alle tjenester på vert og i Kubernetes
.NOTES
    Kjør som administrator (kreves for noen nettverkstester)
#>

# --- Funksjon for farget utskrift ---
function Write-Color($text, $color) {
    $original = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $color
    Write-Output $text
    $host.UI.RawUI.ForegroundColor = $original
}

Write-Host "`n╔══════════════════════════════════════════════════════════╗"
Write-Host "║       SYSTEMTEST – AI-STUDIO (Threadripper)            ║"
Write-Host "╚══════════════════════════════════════════════════════════╝`n"

$global:feil = 0
$global:advarsel = 0

# --- Hjelpefunksjon for å teste HTTP-endepunkt ---
function Test-Http {
    param($navn, $url, $forventetStatus = 200)
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq $forventetStatus) {
            Write-Color "  ✅ $navn : OK" "Green"
            return $true
        } else {
            Write-Color "  ❌ $navn : Feil statuskode $($response.StatusCode)" "Red"
            $global:feil++
            return $false
        }
    } catch {
        Write-Color "  ❌ $navn : Ingen kontakt ($($_.Exception.Message))" "Red"
        $global:feil++
        return $false
    }
}

# --- Test 1: Tjenester på vertsmaskin (Threadripper) ---
Write-Host "`n📡 TJENESTER PÅ VERT (100.103.79.103):"
Test-Http "Anita AI" "http://100.103.79.103:3001/api/health"
Test-Http "AI Agent Office" "http://100.103.79.103:3002"
Test-Http "Ollama API" "http://100.103.79.103:11434/api/tags"
Test-Http "Brekkestranda nettside" "http://100.103.79.103:8080"

# --- Test 2: Kubernetes-cluster ---
Write-Host "`n☸️  KUBERNETES:"
try {
    $nodes = kubectl get nodes -o name
    if ($nodes) {
        Write-Color "  ✅ K8s cluster – nås" "Green"
    } else {
        Write-Color "  ❌ K8s cluster – ingen noder funnet" "Red"
        $global:feil++
    }
} catch {
    Write-Color "  ❌ K8s cluster – ikke tilgjengelig (kubectl feil)" "Red"
    $global:feil++
}

# --- Test 3: Pods i Kubernetes ---
Write-Host "`n🫙  PODS:"
$pods = kubectl get pods -l app=pettersmart -o json | ConvertFrom-Json
if ($pods.items.Count -gt 0) {
    $pod = $pods.items[0]
    if ($pod.status.phase -eq "Running" -and $pod.status.containerStatuses.Count -eq 2 -and $pod.status.containerStatuses[0].ready -and $pod.status.containerStatuses[1].ready) {
        Write-Color "  ✅ Petter Smart – kjører (2/2 ready)" "Green"
    } else {
        Write-Color "  ⚠️ Petter Smart – status: $($pod.status.phase)" "Yellow"
        $global:advarsel++
    }
} else {
    Write-Color "  ❌ Petter Smart – ingen pod funnet" "Red"
    $global:feil++
}

$pods = kubectl get pods -l app=protokoll -o json | ConvertFrom-Json
if ($pods.items.Count -gt 0) {
    $pod = $pods.items[0]
    if ($pod.status.phase -eq "Running" -and $pod.status.containerStatuses.Count -eq 2 -and $pod.status.containerStatuses[0].ready -and $pod.status.containerStatuses[1].ready) {
        Write-Color "  ✅ Protokoll-server – kjører (2/2 ready)" "Green"
    } else {
        Write-Color "  ⚠️ Protokoll-server – status: $($pod.status.phase)" "Yellow"
        $global:advarsel++
    }
} else {
    Write-Color "  ❌ Protokoll-server – ingen pod funnet" "Red"
    $global:feil++
}

# --- Test 4: Tjenester i Kubernetes ---
Write-Host "`n🔗 INTERNE TJENESTER:"
# Sjekk om protokoll-servicen finnes
$svc = kubectl get svc protokoll -o json | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($svc) {
    Write-Color "  ✅ Service 'protokoll' finnes" "Green"
} else {
    Write-Color "  ❌ Service 'protokoll' mangler" "Red"
    $global:feil++
}

# Test at Petter Smart kan nå protokoll-server internt
try {
    $result = kubectl exec -it deploy/pettersmart -c pettersmart -- python -c "import requests; print(requests.get('http://protokoll:8765/status').text)" 2>$null
    if ($result -match '"status": "idle"') {
        Write-Color "  ✅ Petter Smart -> protokoll : OK" "Green"
    } else {
        Write-Color "  ❌ Petter Smart -> protokoll : feil svar" "Red"
        $global:feil++
    }
} catch {
    Write-Color "  ❌ Petter Smart -> protokoll : kunne ikke koble til" "Red"
    $global:feil++
}

# --- Test 5: Consul ---
Write-Host "`n🔄 CONSUL:"
# Prøv å port-forwarde og sjekk Consul UI
$job = Start-Job -ScriptBlock { kubectl port-forward -n consul svc/consul-ui 8501:8500 }
Start-Sleep -Seconds 3
try {
    $consulStatus = Invoke-WebRequest -Uri "http://localhost:8501/v1/status/leader" -TimeoutSec 5 -UseBasicParsing
    if ($consulStatus.Content -match '"') {
        Write-Color "  ✅ Consul leader – OK" "Green"
    } else {
        Write-Color "  ⚠️ Consul – ingen leader" "Yellow"
        $global:advarsel++
    }
} catch {
    Write-Color "  ❌ Consul UI – ikke tilgjengelig" "Red"
    $global:feil++
}
Stop-Job $job
Remove-Job $job

# --- Test 6: Ollama-modeller (via vert) ---
Write-Host "`n📦 OLLAMA-MODELLER:"
try {
    $models = Invoke-RestMethod -Uri "http://100.103.79.103:11434/api/tags" -TimeoutSec 5
    $antall = $models.models.Count
    Write-Color "  ✅ $antall modeller tilgjengelig" "Green"
    if ($antall -lt 10) {
        Write-Color "  ⚠️ Forventet minst 10 modeller (fant $antall)" "Yellow"
        $global:advarsel++
    }
    # Sjekk om deepseek-coder-v2:16b finnes
    $harCoder = $models.models.name -contains "deepseek-coder-v2:16b"
    if (-not $harCoder) {
        Write-Color "  ⚠️ deepseek-coder-v2:16b mangler" "Yellow"
        $global:advarsel++
    }
} catch {
    Write-Color "  ❌ Kunne ikke hente modelliste" "Red"
    $global:feil++
}

# --- Oppsummering ---
Write-Host "`n══════════════════════════════════════════════════════════"
if ($global:feil -eq 0 -and $global:advarsel -eq 0) {
    Write-Color "  ALT FUNGERER PERFEKT! (0 feil, 0 advarsler)" "Green"
} elseif ($global:feil -eq 0) {
    Write-Color "  SYSTEMET FUNGERER, men $global:advarsel advarsel(er)" "Yellow"
} else {
    Write-Color "  SYSTEMET HAR $global:feil FEIL – må fikses" "Red"
}
Write-Host "══════════════════════════════════════════════════════════`n"