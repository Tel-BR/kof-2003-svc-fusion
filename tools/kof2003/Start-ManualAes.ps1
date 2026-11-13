param(
    [string]$Mame = (Join-Path $env:USERPROFILE 'MAME/mame.exe')
)

$ErrorActionPreference = 'Stop'
$mameExe = Get-Item -LiteralPath $Mame
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$profile = Join-Path $root 'private/work/manual-kof2003'
$cfg = (New-Item -ItemType Directory -Force -Path (Join-Path $profile 'cfg')).FullName
$nvram = (New-Item -ItemType Directory -Force -Path (Join-Path $profile 'nvram')).FullName
$romPath = "$root/private/dumps/kof2003;$root/private/bios"

Start-Process -FilePath $mameExe.FullName -WorkingDirectory $mameExe.DirectoryName -ArgumentList @(
    'kof2003', '-bios', 'unibios40', '-noreadconfig', '-skip_gameinfo',
    '-rompath', ('"{0}"' -f $romPath),
    '-ctrlrpath', ('"{0}"' -f $PSScriptRoot), '-ctrlr', 'manual-p1',
    '-cfg_directory', ('"{0}"' -f $cfg), '-nvram_directory', ('"{0}"' -f $nvram),
    '-window', '-maximize', '-video', 'gdi'
)
