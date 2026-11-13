# KOF 2003 native MVS on Windows

Use Windows x64, PowerShell 7.4 or newer, Git, CMake 3.21 or newer, Ninja, and Clang targeting `x86_64-w64-windows-gnu`. Run the commands from the project root in the same shell. Reuse the pinned checkouts if they already exist. Keep the external checkouts, ROMs, generated C, profile data, logs and captures in `private/`. Use the `kof2003` parent cartridge and the Europe MVS v2 BIOS, `sp-s2.sp1`. [Validated input hashes](../../wayfinder/base-direction/tickets/01-cartridge-dumps.md)

## Prepare and replay the published control

Download the Windows x64 zip from the [KOF 2003 v0.1.0 release](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0) into `private/work/`. Its SHA-256 is `d08cd8459306e9b8e7665da3f95e04c374f8954d848010c6b021a7b8c86d4b47`. Extract it into a fresh directory because the supplied preparation script replaces its own `roms-src` folder.

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$work = (New-Item -ItemType Directory -Force private/work).FullName
$gameZip = (Resolve-Path private/dumps/kof2003/kof2003.zip).Path
$biosZip = (Resolve-Path private/bios/neogeo.zip).Path
$port = Join-Path $work 'kof2003-port'
git clone https://github.com/omegakatana92/The-King-of-Fighters-2003.git $port
git -C $port checkout --detach 196b3f8ed2f25dfc34100c60835fee37ebcc69ad

$control = Join-Path $work 'mvs-release'
Expand-Archive (Join-Path $work 'KOF.2003-Windows-x64-v0.1.0.zip') $control
$release = Join-Path $control 'KOF 2003-Windows-x64'
$roms = Join-Path $release 'roms'
$play = Join-Path $port 'tests/play.txt'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $release 'Prepare-ROMs.ps1') -KofZip $gameZip -NeoGeoZip $biosZip

& (Join-Path $release 'KOF 2003.exe') --headless --verify --rom-path $roms --bios sp-s2.sp1 --frames 6000 --input $play *> (Join-Path $control 'verify.log')
Get-Content (Join-Path $control 'verify.log') | Select-String '^\[verify\] \d+ blocks checked','^\[exec\] native blocks'
```

Require a successful exit, zero state mismatches and zero interpreted instructions. Record native coverage and cycle differences from the summary. Exact block counts varied slightly in the two local runs. [Ticket 01 measurements](issues/01-reproduce-native-mvs.md)

## Configure and build the modifiable player

The public KOF 2003 snapshot supplies the cartridge descriptor, player entry point, generator entry point and test inputs. Its author omitted the build files and the adapted toolkit. The same author's Samurai Shodown repository supplies a toolkit with the NEO-PVC and fixed-layer banking required by the KOF 2003 descriptor. Use the pinned toolkit with this repository's CMake configuration. [KOF 2003 source notes](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/v0.1.0/SOURCE-NOTES.md) · [Adapted toolkit](https://github.com/omegakatana92/Samurai-Shodown-Recomp/tree/c745e97211a81eefdfb436a1cabd8570d3eae90d/neogeorecomp) · [Local CMake configuration](../../../tools/kof2003/CMakeLists.txt)

Put `SDL2-devel-2.32.10-mingw.tar.gz` from the [SDL2 2.32.10 release](https://github.com/libsdl-org/SDL/releases/tag/release-2.32.10) in `private/work/`. Its SHA-256 is `83a5d74012311edc3c0d40ea6faecbe57ad692aa033fa5dc273cc937e3938ff2`.

```powershell
$runtime = Join-Path $work 'samsho-runtime-source'
git clone --no-checkout https://github.com/omegakatana92/Samurai-Shodown-Recomp.git $runtime
git -C $runtime checkout --detach c745e97211a81eefdfb436a1cabd8570d3eae90d
tar -xf (Join-Path $work 'SDL2-devel-2.32.10-mingw.tar.gz') -C $work
$sdl = Join-Path $work 'SDL2-2.32.10/x86_64-w64-mingw32/lib/cmake/SDL2'
$build = Join-Path $work 'mvs-native-build'
cmake -S tools/kof2003 -B $build -G Ninja -DCMAKE_BUILD_TYPE=Release `
    -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ `
    "-DKOF2003_SOURCE=$port" "-DNEOGEORECOMP_SOURCE=$runtime/neogeorecomp" `
    "-DKOF2003_ROMS=$roms" "-DSDL2_DIR=$sdl"
```

Consult the project owner before starting the compilation on their machine. Once approved, compile with one job. Profile the reference input with the resulting player and rebuild to include entry points discovered at runtime.

```powershell
cmake --build $build --target kof2003_player --parallel 1
$player = Join-Path $build 'KOF 2003.exe'
$entries = Join-Path $build 'entries.txt'
& $player --headless --rom-path $roms --bios sp-s2.sp1 --frames 6000 --input $play --dump-misses $entries
cmake --build $build --target kof2003_player --parallel 1
& $player --headless --verify --rom-path $roms --bios sp-s2.sp1 --frames 6000 --input $play *> (Join-Path $build 'verify.log')
Get-Content (Join-Path $build 'verify.log') | Select-String '^\[verify\] \d+ blocks checked','^\[exec\] native blocks'
```

Apply the same verification criteria to the rebuilt player. Read the summary for zero state mismatches and zero interpreted instructions, since the player's exit code alone does not verify either metric. Record cycle differences separately.

The release replay and ROM preparation passed locally. The local build configuration generated a Ninja build with Clang 22.1.8 and CMake 3.31.12. Compilation and replay from the resulting executable are pending.

# KOF 2003 nativo em MVS no Windows

Use Windows x64, PowerShell 7.4 ou superior, Git, CMake 3.21 ou superior, Ninja e Clang com alvo `x86_64-w64-windows-gnu`. Execute os blocos acima a partir da raiz do projeto no mesmo terminal. Reaproveite os clones fixados nas revisões indicadas se já existirem. Mantenha os clones externos, ROMs, C gerado, dados de perfil, logs e capturas em `private/`. Use o conjunto pai `kof2003` e a BIOS Europe MVS v2, `sp-s2.sp1`. [Hashes das entradas validadas](../../wayfinder/base-direction/tickets/01-cartridge-dumps.md)

1. Baixe o pacote Windows x64 da versão `v0.1.0` para `private/work/` e confira o SHA-256 acima. O primeiro bloco prepara os dumps em uma extração nova e roda o roteiro original de 6.000 quadros. Confira o código de saída e o resumo de `--verify`. O controle deve ter zero divergências de estado e zero instruções executadas pelo interpretador. Registre a cobertura e as diferenças de ciclos. [Versão publicada](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0) · [Medições do ticket 01](issues/01-reproduce-native-mvs.md)
2. Baixe o SDK SDL2 para `private/work/`, confira o SHA-256 acima e rode o segundo bloco. O autor publicou a descrição do cartucho e os pontos de entrada do executável e do gerador no repositório do KOF 2003. O bloco obtém de outro port do mesmo autor uma versão do runtime com suporte a NEO-PVC e à seleção de bancos da camada fixa. [SDL2 2.32.10](https://github.com/libsdl-org/SDL/releases/tag/release-2.32.10) · [Runtime adaptado](https://github.com/omegakatana92/Samurai-Shodown-Recomp/tree/c745e97211a81eefdfb436a1cabd8570d3eae90d/neogeorecomp) · [Configuração CMake](../../../tools/kof2003/CMakeLists.txt)
3. Consulte o dono antes de iniciar a compilação na máquina dele. Com a aprovação, rode o terceiro bloco com um processo por vez. Ele compila o executável, usa o roteiro original para encontrar pontos de entrada descobertos durante a execução, recompila e roda o mesmo controle MVS. Confirme zero divergências de estado e zero instruções interpretadas no resumo. Registre as diferenças de ciclos à parte.

A preparação dos dumps e o controle com o executável publicado passaram. A configuração local gerou um build Ninja com Clang 22.1.8 e CMake 3.31.12. A compilação e o teste com o executável resultante estão pendentes.
