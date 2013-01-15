
$computer=$env:computername
$group='Administrators'
$userdomain='EMEA'
$username= read-host 'Enter the user name to add to the local administrators group'
  
      ([ADSI]"WinNT://$computer/$Group,group").psbase.Invoke("Add",([ADSI]"WinNT://$domain/$user").path)