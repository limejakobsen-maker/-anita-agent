#!/usr/bin/env pwsh
# Install shadcn/ui components script

Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║       INSTALLERER SHADCN/UI KOMPONENTER                      ║
║       for Anita Agent Dashboard                              ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Sjekk om shadcn er installert
if (-not (Get-Command shadcn -ErrorAction SilentlyContinue)) {
    Write-Host "Installerer shadcn..." -ForegroundColor Yellow
    npx shadcn@latest init
}

# Liste over komponenter å installere
$components = @(
    # Layout
    "accordion"
    "card"
    "collapsible"
    "resizable"
    "scroll-area"
    "separator"
    "sidebar"
    "skeleton"
    "tabs"
    
    # Forms
    "button"
    "checkbox"
    "form"
    "input"
    "label"
    "radio-group"
    "select"
    "slider"
    "switch"
    "textarea"
    
    # Feedback
    "alert"
    "alert-dialog"
    "dialog"
    "dropdown-menu"
    "popover"
    "progress"
    "sonner"
    "toast"
    "tooltip"
    
    # Data Display
    "avatar"
    "badge"
    "calendar"
    "carousel"
    "command"
    "context-menu"
    "hover-card"
    "menubar"
    "navigation-menu"
    "pagination"
    "table"
    "toggle"
    "toggle-group"
)

Write-Host "`nInstallerer $($components.Count) komponenter..." -ForegroundColor Green

foreach ($component in $components) {
    Write-Host "  📦 Installerer $component..." -ForegroundColor Gray
    npx shadcn add $component -y
}

Write-Host "`n✅ Alle komponenter installert!" -ForegroundColor Green
Write-Host "`nNeste steg:" -ForegroundColor Cyan
Write-Host "  1. Kopier app/ mappen fra eksempelet" -ForegroundColor White
Write-Host "  2. Kjør: npm run dev" -ForegroundColor White
Write-Host "  3. Åpne: http://localhost:3000" -ForegroundColor White
