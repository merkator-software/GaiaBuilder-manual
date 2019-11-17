#Script taken from https://lostechies.com/keithdahlby/2011/08/13/allowing-a-windows-service-to-interact-with-desktop-without-localsystem/
$svcName = Get-Service -DisplayName *Jenkins* | select -Exp Name
$svcKey = Get-Item HKLM:\SYSTEM\CurrentControlSet\Services\$svcName

# Set 9th bit, from http://www.codeproject.com/KB/install/cswindowsservicedesktop.aspx
$newType = $svcKey.GetValue('Type') -bor 0x100
Set-ItemProperty $svcKey.PSPath -Name Type -Value $newType