# Den Digitale Riggen - Enkel Kontrollpanel
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Den Digitale Riggen - Kontrollpanel"
$form.Size = New-Object System.Drawing.Size(900, 650)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 50)

$title = New-Object System.Windows.Forms.Label
$title.Text = "DEN DIGITALE RIGGEN"
$title.Font = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$title.ForeColor = [System.Drawing.Color]::FromArgb(233, 69, 96)
$title.Location = New-Object System.Drawing.Point(250, 20)
$title.AutoSize = $true
$form.Controls.Add($title)

function Test-PortFunc {
    param($ip, $port)
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.Connect($ip, $port)
        $tcp.Close()
        return $true
    } catch { return $false }
}

function Test-HostFunc {
    param($ip)
    return Test-Connection $ip -Count 1 -Quiet -ErrorAction SilentlyContinue
}

$status = New-Object System.Windows.Forms.TextBox
$status.Multiline = $true
$status.ScrollBars = "Vertical"
$status.Size = New-Object System.Drawing.Size(850, 220)
$status.Location = New-Object System.Drawing.Point(20, 380)
$status.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 35)
$status.ForeColor = [System.Drawing.Color]::LightGreen
$status.Font = New-Object System.Drawing.Font("Consolas", 10)
$status.ReadOnly = $true
$form.Controls.Add($status)

function Log($msg) {
    $status.AppendText("$msg`r`n")
}

$acer = New-Object System.Windows.Forms.GroupBox
$acer.Text = "ACER (Lokal)"
$acer.Size = New-Object System.Drawing.Size(400, 200)
$acer.Location = New-Object System.Drawing.Point(20, 70)
$acer.ForeColor = [System.Drawing.Color]::White
$acer.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$form.Controls.Add($acer)

$btn1 = New-Object System.Windows.Forms.Button
$btn1.Text = "Apne Sandkasse"
$btn1.Size = New-Object System.Drawing.Size(350, 40)
$btn1.Location = New-Object System.Drawing.Point(20, 30)
$btn1.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 100)
$btn1.ForeColor = [System.Drawing.Color]::White
$btn1.Add_Click({
    Start-Process "explorer.exe" "C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI"
    Log("[OK] Apnet Sandkasse")
})
$acer.Controls.Add($btn1)

$btn2 = New-Object System.Windows.Forms.Button
$btn2.Text = "System Monitor"
$btn2.Size = New-Object System.Drawing.Size(350, 40)
$btn2.Location = New-Object System.Drawing.Point(20, 80)
$btn2.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 100)
$btn2.ForeColor = [System.Drawing.Color]::White
$btn2.Add_Click({
    $p = "C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI\Rigg_Monitor.ps1"
    Start-Process powershell.exe -ArgumentList "-NoExit -ExecutionPolicy Bypass -File `"$p`""
    Log("[OK] Startet Monitor")
})
$acer.Controls.Add($btn2)

$btn3 = New-Object System.Windows.Forms.Button
$btn3.Text = "Apne Z: Disk"
$btn3.Size = New-Object System.Drawing.Size(350, 40)
$btn3.Location = New-Object System.Drawing.Point(20, 130)
$btn3.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 100)
$btn3.ForeColor = [System.Drawing.Color]::White
$btn3.Add_Click({
    if (Test-Path "Z:\") {
        Start-Process "explorer.exe" "Z:"
        Log("[OK] Apnet Z:")
    } else {
        net use Z: "\\192.168.1.200\Bygg_Arkiv" /persistent:yes 2>&1 | Out-Null
        if (Test-Path "Z:\") {
            Start-Process "explorer.exe" "Z:"
            Log("[OK] Z: tilkoblet")
        } else {
            Log("[FEIL] Z: feil")
        }
    }
})
$acer.Controls.Add($btn3)

$tr = New-Object System.Windows.Forms.GroupBox
$tr.Text = "THREADRIPPER (192.168.1.200)"
$tr.Size = New-Object System.Drawing.Size(400, 200)
$tr.Location = New-Object System.Drawing.Point(450, 70)
$tr.ForeColor = [System.Drawing.Color]::White
$tr.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$form.Controls.Add($tr)

$btn4 = New-Object System.Windows.Forms.Button
$btn4.Text = "Remote Desktop (RDP)"
$btn4.Size = New-Object System.Drawing.Size(350, 40)
$btn4.Location = New-Object System.Drawing.Point(20, 30)
$btn4.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 100)
$btn4.ForeColor = [System.Drawing.Color]::White
$btn4.Add_Click({
    if (Test-PortFunc "192.168.1.200" 3389) {
        Start-Process "mstsc.exe" "/v:192.168.1.200"
        Log("[OK] RDP startet")
    } else {
        Log("[FEIL] RDP stengt")
        [System.Windows.Forms.MessageBox]::Show("RDP ikke aktivert. Kjor Aktiver_RDP_Threadripper.ps1 pa Threadripper.")
    }
})
$tr.Controls.Add($btn4)

$btn5 = New-Object System.Windows.Forms.Button
$btn5.Text = "AnythingLLM Web"
$btn5.Size = New-Object System.Drawing.Size(350, 40)
$btn5.Location = New-Object System.Drawing.Point(20, 80)
$btn5.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 100)
$btn5.ForeColor = [System.Drawing.Color]::White
$btn5.Add_Click({
    if (Test-PortFunc "192.168.1.200" 3001) {
        Start-Process "http://192.168.1.200:3001"
        Log("[OK] AnythingLLM apnet")
    } else {
        Log("[FEIL] AnythingLLM stoppet")
    }
})
$tr.Controls.Add($btn5)

$btn6 = New-Object System.Windows.Forms.Button
$btn6.Text = "Aktiver RDP (bruk pa Threadripper)"
$btn6.Size = New-Object System.Drawing.Size(350, 40)
$btn6.Location = New-Object System.Drawing.Point(20, 130)
$btn6.BackColor = [System.Drawing.Color]::FromArgb(100, 60, 0)
$btn6.ForeColor = [System.Drawing.Color]::White
$btn6.Add_Click({
    [System.Windows.Forms.MessageBox]::Show("Kopier Aktiver_RDP_Threadripper.ps1 til Threadripper og kjor som Administrator.")
})
$tr.Controls.Add($btn6)

$len = New-Object System.Windows.Forms.GroupBox
$len.Text = "LENOVO SANDKASSE (100.108.91.44)"
$len.Size = New-Object System.Drawing.Size(830, 80)
$len.Location = New-Object System.Drawing.Point(20, 290)
$len.ForeColor = [System.Drawing.Color]::White
$len.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$form.Controls.Add($len)

$btn7 = New-Object System.Windows.Forms.Button
$btn7.Text = "SSH Terminal"
$btn7.Size = New-Object System.Drawing.Size(200, 40)
$btn7.Location = New-Object System.Drawing.Point(20, 30)
$btn7.BackColor = [System.Drawing.Color]::FromArgb(0, 100, 80)
$btn7.ForeColor = [System.Drawing.Color]::White
$btn7.Add_Click({
    Start-Process powershell.exe -ArgumentList "-NoExit -Command ssh emil@100.108.91.44"
    Log("[OK] SSH til Lenovo")
})
$len.Controls.Add($btn7)

$btn8 = New-Object System.Windows.Forms.Button
$btn8.Text = "Setup SSH-nokkel"
$btn8.Size = New-Object System.Drawing.Size(200, 40)
$btn8.Location = New-Object System.Drawing.Point(240, 30)
$btn8.BackColor = [System.Drawing.Color]::FromArgb(100, 80, 0)
$btn8.ForeColor = [System.Drawing.Color]::White
$btn8.Add_Click({
    $p = "C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI\Setup_SSH_Lenovo.ps1"
    Start-Process powershell.exe -ArgumentList "-NoExit -ExecutionPolicy Bypass -File `"$p`""
})
$len.Controls.Add($btn8)

$btn9 = New-Object System.Windows.Forms.Button
$btn9.Text = "Sjekk Status"
$btn9.Size = New-Object System.Drawing.Size(150, 40)
$btn9.Location = New-Object System.Drawing.Point(600, 30)
$btn9.BackColor = [System.Drawing.Color]::FromArgb(80, 80, 120)
$btn9.ForeColor = [System.Drawing.Color]::White
$btn9.Add_Click({
    $status.Clear()
    Log("Sjekker status...")
    Log("")
    
    Log("THREADRIPPER:")
    if (Test-HostFunc "192.168.1.200") {
        Log("  Nettverk: OK")
        if (Test-PortFunc "192.168.1.200" 3389) { Log("  RDP: OK") } else { Log("  RDP: STENGT") }
        if (Test-PortFunc "192.168.1.200" 3001) { Log("  AnythingLLM: OK") } else { Log("  AnythingLLM: STOPPET") }
        if (Test-PortFunc "192.168.1.200" 445) { Log("  SMB: OK") } else { Log("  SMB: STENGT") }
    } else {
        Log("  Nettverk: OFFLINE")
    }
    
    Log("")
    Log("LENOVO:")
    if (Test-HostFunc "100.108.91.44") {
        Log("  Tailscale: OK")
        if (Test-PortFunc "100.108.91.44" 22) { Log("  SSH: OK") } else { Log("  SSH: STENGT") }
    } else {
        Log("  Tailscale: OFFLINE")
    }
    
    Log("")
    Log("Ferdig!")
})
$len.Controls.Add($btn9)

Log("Kontrollpanel startet")
Log("Klikk 'Sjekk Status' for a se tilstand")
$form.ShowDialog()
