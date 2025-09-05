$exitcode = 0
Write-Host $($env:server)
$manual_build_list = $($env:manual_build_list)
$includecontent = "1"
if ($env:includecontent -eq "0")
{
    $includecontent = "0"
}

$temp = @()

## define the list of content.json files to be build
$content = @()
$build = @()
$gpservices =@()

if ($manual_build_list.Length -gt 0){
    Write-Output "Activating manual build from list"
    if ($manual_build_list -eq "*")
    {
        $temp = Get-ChildItem -Path .\ -Filter *.json -Name -Recurse
    }
    else
    {
        $temp = $manual_build_list -split ','
    }
}
else{
    ## get all the changed files
    $files = $(git diff-tree --name-only -r --no-commit-id HEAD)
    $temp = $files -split ' '
    $count = $temp.Length
    Write-Host "Total changed files $count files"
}   
For ($i=0; $i -lt $temp.Length; $i++)
{
    $name=$temp[$i]

    $dir=(Resolve-Path .\).Path
    $filename = ([system.io.fileinfo]$name).Name
    $path_no_file = $name.replace($filename,"")
    $fulldir = Join-Path $dir $path_no_file
    
    $cffile = Join-Path $fulldir "content.json"
    $gpfile = Join-Path $fulldir "gpservice.json"
    Write-Host $gpfile
    Test-Path $gpfile
    $aprxjsonfile = Join-Path $fulldir $filename
    
    If ($name -match '.aprx.json$')
    {
        # Huidige CI strategie rolt services uit naar MAPSO enterprise, de *.online.aprx.json is een specifieke configuratie voor ArcGIS online.
        # CI pipeline voor services verwacht de server entry MAPSO in de config. Deze key mist in de .online.aprx.json waardoor de CI pipeline faalt.
        # --> ERROR:root:Unexpected error while deploying the mapservice: 'MAPSO'
        If ($name -match '.online.aprx.json$')
        {
            Write-Host "Found ArcGIS Online configuration file, skipping $name in CI pipeline"
        }
        ElseIf(Test-Path $aprxjsonfile)
        {
            If (-Not $build.Contains($aprxjsonfile))
            {
                $build += $aprxjsonfile
                Write-Host "Added APRX.JSON $aprxjsonfile to build list"
            }
            Else
            {
                Write-Host "File $name already added to build list"
            }
        }
        Else 
        {
            Write-Host "File $aprxjsonfile does not exist"
        }

    }
    ElseIf (Test-Path $cffile)
    {
        If (-Not $content.Contains($cffile))
        {
            $content += $cffile
            Write-Host "Added $cffile to Content list"
        }
        Else
        {
            Write-Host "File $cffile already added to Content list"
        }
    }
    ElseIf (Test-Path $gpfile)
    {
        If (-Not $gpservices.Contains($gpfile))
        {
            $gpservices += $gpfile
            Write-Host "Added $gpfile to GPService list"
        }
        Else
        {
            Write-Host "File $gpfile already added to GPService list"
        }
    }        
    Else
    {
        ## construct the .aprx.json filename from the map or layer file name
        $mapfileparts = ($name -split '/', 0, "simplematch" )[-1] -split '.', 0, "simplematch"
        $match_pattern = ''
        $matched  = 0
        For ($j=0; $j -lt $mapfileparts.Length -and $matched -lt 1; $j++)
        {
            if ($mapfileparts[$j] -match 'lyrx' -or $mapfileparts[$j] -match 'mapx' -or $mapfileparts[$j] -match 'aprx') 
            {
                $matched = 1
            }
            else
            {
                if ($j -eq 0)
                {
                    $match_pattern = $mapfileparts[$j]
                }
                else
                {
                    $match_pattern = -join($match_pattern,'.',$mapfileparts[$j])
                }
            }
        }
        $match_pattern = -join($match_pattern,'.*aprx.json')
        Write-Host $match_pattern $name
        $mapfiles = Get-ChildItem (Resolve-Path .\) -Recurse -Include $match_pattern
        Write-Host $mapfiles
        For ($j=0; $j -lt $mapfiles.Length; $j++)
        {
            $mapfile =  $mapfiles[$j]
            If($mapfile) #empty strings will be ignored by this test
            {
                If(Test-Path $mapfile)
                {
                    If (-Not $build.Contains($mapfile))
                    {
                        $build += $mapfile
                        Write-Host "Added $mapfile to build list"
                    }
                    Else
                    {
                        Write-Host "File $mapfile already added to build list"
                    }
                }
            }
        }
    }
}

For ($i=0; $i -lt $build.Length; $i++)
{
    $rw = $($env:rewrite_connection)
    $restore_param = ""
    if ($rw -eq "1" -or $rw -eq $null){
        $restore_param = "-q true"
    }
    $buildthis = $build[$i]
    $arguments = "D:\GaiaBuilderServerTools\InstallMapservice_lite.py -f $buildthis -s $($env:server) -r false $restore_param -c true -d false -h true -i true -a true -z true -m true -t false"
    Write-Host $arguments
    ## -PassThru -Wait -NoNewWindow will show the output from the python process in the devops logging
    $process =  Start-Process -FilePath "D:\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" -ArgumentList $arguments  -PassThru -Wait -NoNewWindow
    $exitcode = $exitcode + $process.ExitCode
}

For ($i=0; $i -lt $gpservices.Length; $i++)
{
    $buildthis = $gpservices[$i]
    $arguments = "D:\GaiaBuilderServerTools\InstallGeoProcessor_lite.py -f $buildthis -s $($env:server)"
    Write-Host $arguments
    ## -PassThru -Wait -NoNewWindow will show the output from the python process in the devops logging
    $process =  Start-Process -FilePath "D:\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" -ArgumentList $arguments  -PassThru -Wait -NoNewWindow
    $exitcode = $exitcode + $process.ExitCode
}
if ($includecontent -eq "1"){
    For ($i=0; $i -lt $content.Length; $i++)
    {
        $buildthis = $content[$i]
        $arguments = "D:\GaiaBuilderServerTools\InstallContent_lite.py -f $buildthis -s $($env:server)"
        Write-Host $arguments
        ## -PassThru -Wait -NoNewWindow will show the output from the python process in the devops logging
        $process =  Start-Process -FilePath "D:\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" -ArgumentList $arguments  -PassThru -Wait -NoNewWindow
        $exitcode = $exitcode + $process.ExitCode
    }
}
exit $exitcode
