# Create Windows service installer
$serviceName = "SecurityMonitorAgent"
$binaryPath = "$PSScriptRoot\agent\SecurityAgent.exe"

New-Service -Name $serviceName `
            -BinaryPathName $binaryPath `
            -DisplayName "Security Monitoring Agent" `
            -StartupType Automatic 