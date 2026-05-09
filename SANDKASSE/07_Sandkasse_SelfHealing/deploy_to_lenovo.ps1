# Deploy Self-Healing System til Lenovo Sandkasse
# Dette scriptet kopierer fra PROSJEKTMAPPE AI til Lenovo

param(
    [string]$LenovoIP = "100.108.91.44",
    [string]$Username = "emil"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEPLOY TIL LENOVO SANDKASSE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$sourcePath = "C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI\07_Sandkasse_SelfHealing"

if (-not (Test-Path $sourcePath)) {
    Write-Host "FEIL: Kilde-mappe ikke funnet: $sourcePath" -ForegroundColor Red
    exit 1
}

Write-Host "`nKilde: $sourcePath" -ForegroundColor Gray
Write-Host "Mål: $Username@$LenovoIP`:~" -ForegroundColor Gray

Write-Host "`nMetode 1: File Explorer (anbefalt)" -ForegroundColor Yellow
Write-Host "  1. Åpne: \\$LenovoIP\emil" -ForegroundColor White
Write-Host "  2. Kopier mappen '07_Sandkasse_SelfHealing'" -ForegroundColor White
Write-Host "  3. Lim inn på Lenovo som 'self_healing_system'" -ForegroundColor White

Write-Host "`nMetode 2: USB" -ForegroundColor Yellow
Write-Host "  1. Kopier $sourcePath til USB" -ForegroundColor White
Write-Host "  2. Flytt til Lenovo" -ForegroundColor White
Write-Host "  3. Plasser i /home/emil/self_healing_system/" -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  FILER KLAR FOR DEPLOY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Get-ChildItem $sourcePath -File | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor Gray
}
