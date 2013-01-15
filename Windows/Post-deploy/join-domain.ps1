
$computerName = Read-Host 'Enter the computer name for adding to the domain'
(Get-WmiObject win32_computersystem).rename("newname")

add-computer -Credential $(Get-Credential) -DomainName EMEA.CORP.YR.COM

Restart-Computer