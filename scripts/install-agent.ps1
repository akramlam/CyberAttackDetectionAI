# Enhanced installer with security measures
$serviceName = "SecurityMonitorAgent"
$binaryPath = "$PSScriptRoot\agent\SecurityAgent.exe"

# Create service with restricted permissions
New-Service -Name $serviceName `
            -BinaryPathName $binaryPath `
            -DisplayName "Security Monitoring Agent" `
            -StartupType Automatic `
            -Description "Secure monitoring and command execution agent"

# Set up restricted service account
$serviceAccount = "NT SERVICE\$serviceName"
$acl = Get-Acl $binaryPath
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $serviceAccount,
    "ReadAndExecute",
    "Allow"
)
$acl.AddAccessRule($accessRule)
Set-Acl $binaryPath $acl

# Configure service security
$sddt = New-Object System.Management.ManagementClass Win32_SecurityDescriptorHelper
$sddl = "D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)"
$sddt.Win32SetSecurityDescriptor($serviceName, $sddl) 