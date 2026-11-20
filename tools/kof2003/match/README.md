# Match tools

Scripted, silent runs of the native KOF 2003 player and of MAME's Neo Geo games. Captures, logs, recordings and RAM dumps contain game data. `mame_run.py` and `run.py` write them under `private/`. Keep any path you pass yourself, such as `INPUT_LOG` or `DUMP_OUT`, under `private/` too.

| File | Purpose |
|---|---|
| `input_script.py` | Reads the native player's input script format. |
| `verify_report.py` | Reads the native player's `--verify` summary. |
| `run.py` | Plays one script on the native player and on MAME, with captures (ticket 02). |
| `replay.lua` | Applies a transition list in MAME and saves captures. |
| `session.py` | Reads an owner-recorded input log and continues it with a test script. |
| `mame_run.py` | Runs a scripted test in MAME, optionally continuing a recorded session, or plays back an `.inp` recording with captures. Offsets were measured for SVC Chaos. |
| `log_inputs.lua` | Records the owner's inputs while playing in MAME. |
| `playback_shots.lua` | Saves captures while MAME plays back an `.inp` recording. |
| `probe.lua` | Logs animation pointer, position and health each frame. Defaults are SVC Chaos offsets; `PROBE_ADDRESSES` logs any addresses in the native probe's format. |
| `compare_captures.py` | Compares two capture sets by hash; reports equal or the first differing frame (graphics-set growth, ticket 01). |
| `repeat_reference.py` | Runs one build twice on `scripts/coin-start.txt` and `scripts/team-match.txt`, then compares the two capture sets. |
| `compare_builds.py` | Runs two builds (default A and B) once on both scripts, compares the captures by hash, checks B's `--verify` is not worse, and measures B's memory (graphics-set growth, ticket 02). |
| `memory_probe.py` | Measures a Windows process's peak and steady memory while it runs. |
| `native_probe.c` | Optional per-frame memory probe compiled into the native player (ticket 08). |
| `probe_hook.py` | Adds the probe's call to a private copy of the runtime's frame loop. |
| `probe_log.py` | Reads the probe address list and logs shared by both runtimes, and compares two logs. |
| `probe_run.py` | Probes one script on the native player and on MAME and compares the logs. |
| `svc_id_static.py` | Static reader inventory for SVC Chaos fighter IDs (wayfinder 28): sweeps the decrypted program and follows each ID read to the tables it indexes. Needs `pip install capstone`; reports go under `private/`. `svc_id_readers.lua` dumps the fighter objects in MAME (its read taps do not work). |

Recording a session: start MAME with `-record <name>.inp -autoboot_script log_inputs.lua` and `INPUT_LOG` set. Do not use MAME's soft reset (F3) while recording. Close MAME and start again instead. Tests: `py -3 -m pytest match` from `tools/kof2003`.

### Reference build A (graphics-set growth, ticket 01)

Build A is the native player as built from the unchanged descriptor (64 MiB Graphics Set). Its copy lives in `private/work/graphics-growth/build-a/` (read-only); later builds go elsewhere. To rebuild it, run the native build in `private/work/mvs-native-build` with the descriptor unchanged and copy `KOF 2003.exe` and `SDL2.dll` into a new folder under `private/work/graphics-growth/`. To prove it repeats itself, from `tools/kof2003` on Windows:

```
py -3 -m match.repeat_reference
py -3 -m match.compare_captures RUN_A_DIR RUN_B_DIR
```

Runs and captures go under `private/work/graphics-growth/runs/`. Exit code 1 means a difference; the first differing frame is printed.

Build B (128 MiB) and its comparison with A: see `../growth/README.md` (ticket 02). Build C, which draws one synthetic tile from the Added Space: the same file (ticket 04).

### Grown loader test (graphics-set growth, ticket 03)

`../loader/test_grown_loader.c` loads synthetic graphics file pairs at the 128 MiB size and at the 64 MiB size and checks pair interleaving, the tile at the fifth pair (tile number `$80000`), zero fill, and the 20-bit versus 19-bit tile mask. It uses no game data and compiles against the private toolkit (`private/work/samsho-runtime-source/neogeorecomp`, or `NEOGEORECOMP_SOURCE`). It needs a C compiler (clang or gcc) and writes about 80 MiB of temporary files under `private/`. From `tools/kof2003`:

```
py -3 -m loader.run_loader_test
```

Exit code 0 means every check passed.

### Native memory probe (first SVC import, ticket 08)

The native player can log chosen memory every frame, in the same format as `probe.lua` in MAME. It takes an address list such as `0x1010e0:4,0x2fe91d:1` (hex 68000 address, then 1, 2 or 4 bytes; up to 16 entries) and writes one line per frame, `<frame>\t<hex>\t<hex>...`. Reads have no side effects and reach work RAM and NEO-PVC RAM. The probe is off twice over: the CMake option `KOF2003_NATIVE_PROBE` is off by default, and a player built with it logs nothing unless `KOF_NATIVE_PROBE` is set. Only a private copy of the runtime is changed.

Build it once, from the repository root in PowerShell 7.4+, after the [Windows build guide](../../../docs/specs/first-svc-character-import/native-mvs-windows.md) has produced the control build in `private/work/mvs-native-build`:

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$root = (Get-Location).Path
$probe = Join-Path $root 'private/work/native-probe'
New-Item -ItemType Directory -Path $probe | Out-Null
Copy-Item -LiteralPath "$root/private/work/samsho-runtime-source/neogeorecomp" -Destination "$probe/runtime" -Recurse
$source = "$probe/runtime/src/neogeo.c"
$hash = (Get-FileHash -Algorithm SHA256 $source).Hash
py -3 tools/kof2003/match/probe_hook.py $source "$probe/runtime/src/neogeo-probe.c" --sha256 $hash
Move-Item -LiteralPath "$probe/runtime/src/neogeo-probe.c" -Destination $source -Force
Copy-Item -LiteralPath "$root/private/work/mvs-native-build/entries.txt" -Destination "$probe/entries.txt"
$roms = (Get-Content "$root/private/work/mvs-native-build/CMakeCache.txt" | Where-Object { $_ -like 'KOF2003_ROMS:PATH=*' }) -replace '^KOF2003_ROMS:PATH=', ''
$sdl = "$root/private/work/SDL2-2.32.10/x86_64-w64-mingw32/lib/cmake/SDL2"
cmake -S tools/kof2003 -B "$probe/build" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ "-DKOF2003_SOURCE=$root/private/work/kof2003-port" "-DNEOGEORECOMP_SOURCE=$probe/runtime" "-DKOF2003_ROMS=$roms" "-DKOF2003_ENTRIES=$probe/entries.txt" "-DSDL2_DIR=$sdl" -DKOF2003_NATIVE_PROBE=ON
cmake --build "$probe/build" --target kof2003_player --parallel 1
```

Check that the probe build still passes the native MVS control with the option off (no `KOF_NATIVE_PROBE` in the environment): zero state mismatches and zero interpreted instructions in the summary.

```powershell
Remove-Item Env:KOF_NATIVE_PROBE* -ErrorAction SilentlyContinue
& "$probe/build/KOF 2003.exe" --headless --verify --rom-path $roms --bios sp-s2.sp1 --frames 6000 --input "$root/private/work/kof2003-port/tests/play.txt" *> "$probe/verify-off.log"
Get-Content "$probe/verify-off.log" | Select-String '^\[verify\] \d+ blocks checked','^\[exec\] native blocks'
```

Probe a script in both runtimes and compare, from `tools/kof2003`:

```
py -3 -m match.probe_run match/scripts/team-match.txt --frames 36100 --first 290 --last 5599
py -3 -m match.probe_log NATIVE_LOG MAME_LOG --columns 7 --first 290 --last 5599
```

The default addresses (`TEAM_MATCH_ADDRESSES` in `probe_run.py`) are P1's pose pointer (`$101080 + $60`) and the health of P1's and P2's three team members in NEO-PVC RAM (`$2FE91D`, `$2FEA1D`, `$2FEB1D`, `$2FED1D`, `$2FEE1D`, `$2FEF1D`); pass `--probe` for others. To log without MAME, set `KOF_NATIVE_PROBE`, `KOF_NATIVE_PROBE_LOG` (a path under `private/`) and optionally `KOF_NATIVE_PROBE_FIRST`, then run the player. Both logs use the native player's frame numbers: MAME's probe is labelled with `REPLAY_OFFSET` 2, and no extra shift is needed. Frames before 290 differ while the BIOS tests memory at power-on, and the team match diverges from its first in-fight input at frame 5,600 for the reason recorded in [ticket 07](../../../docs/specs/first-svc-character-import/issues/07-explain-in-fight-input-divergence.md).

## Ferramentas de luta

Execuções por roteiro e sem som do executável nativo do KOF 2003 e dos jogos Neo Geo no MAME. Capturas, logs, gravações e dumps de RAM contêm dados dos jogos. O `mame_run.py` e o `run.py` os gravam em `private/`. Mantenha também em `private/` qualquer caminho que você mesmo indicar, como `INPUT_LOG` ou `DUMP_OUT`.

| Arquivo | Função |
|---|---|
| `input_script.py` | Lê o formato de roteiro de entradas do executável nativo. |
| `verify_report.py` | Lê o resumo do `--verify` do executável nativo. |
| `run.py` | Executa um roteiro no nativo e no MAME, com capturas (ticket 02). |
| `replay.lua` | Aplica uma lista de mudanças de entrada no MAME e salva capturas. |
| `session.py` | Lê um log de entradas gravado pelo dono e o continua com um roteiro de teste. |
| `mame_run.py` | Executa um teste por roteiro no MAME, opcionalmente continuando uma sessão gravada, ou repete uma gravação `.inp` com capturas. Os deslocamentos foram medidos para o SVC Chaos. |
| `log_inputs.lua` | Registra as entradas do dono enquanto ele joga no MAME. |
| `playback_shots.lua` | Salva capturas enquanto o MAME repete uma gravação `.inp`. |
| `probe.lua` | Registra ponteiro de animação, posição e vida a cada quadro. Os padrões são deslocamentos do SVC Chaos; `PROBE_ADDRESSES` registra quaisquer endereços no formato da sonda nativa. |
| `compare_captures.py` | Compara dois conjuntos de capturas por hash; informa igual ou o primeiro quadro diferente (ampliação do Conjunto gráfico, ticket 01). |
| `repeat_reference.py` | Roda um build duas vezes com `scripts/coin-start.txt` e `scripts/team-match.txt` e compara os dois conjuntos de capturas. |
| `compare_builds.py` | Roda dois builds (por padrão A e B) uma vez nos dois roteiros, compara as capturas por hash, confere que o `--verify` do B não é pior e mede a memória do B (ampliação do Conjunto gráfico, ticket 02). |
| `memory_probe.py` | Mede o pico e o regime de memória de um processo do Windows enquanto ele roda. |
| `native_probe.c` | Sonda de memória opcional, quadro a quadro, compilada no executável nativo (ticket 08). |
| `probe_hook.py` | Acrescenta a chamada da sonda a uma cópia privada do laço de quadros do runtime. |
| `probe_log.py` | Lê a lista de endereços e os logs da sonda, comuns aos dois runtimes, e compara dois logs. |
| `probe_run.py` | Sonda um roteiro no nativo e no MAME e compara os logs. |

Para gravar uma sessão, abra o MAME com `-record <nome>.inp -autoboot_script log_inputs.lua` e `INPUT_LOG` definido. Não use o reset do MAME (F3) durante a gravação. Feche e abra o MAME de novo. Testes: `py -3 -m pytest match` a partir de `tools/kof2003`.

### Build de referência A (ampliação do Conjunto gráfico, ticket 01)

O build A é o player nativo compilado com o descritor sem mudança (Conjunto gráfico de 64 MiB). A cópia fica em `private/work/graphics-growth/build-a/` (somente leitura); os builds seguintes vão para outro lugar. Para recompilar, rode o build nativo em `private/work/mvs-native-build` com o descritor sem mudança e copie `KOF 2003.exe` e `SDL2.dll` para uma pasta nova em `private/work/graphics-growth/`. Para provar que ele se repete, a partir de `tools/kof2003`, no Windows:

```
py -3 -m match.repeat_reference
py -3 -m match.compare_captures PASTA_RODADA_A PASTA_RODADA_B
```

Rodadas e capturas ficam em `private/work/graphics-growth/runs/`. Código de saída 1 indica diferença; o primeiro quadro diferente é impresso.

Build B (128 MiB) e a comparação com o A: veja `../growth/README.md` (ticket 02). O build C, que desenha um tile sintético do Espaço acrescentado: o mesmo arquivo (ticket 04).

### Teste do carregador ampliado (ampliação do Conjunto gráfico, ticket 03)

O `../loader/test_grown_loader.c` carrega pares sintéticos de arquivos gráficos com o tamanho de 128 MiB e com o de 64 MiB e confere a intercalação dos pares, o tile do quinto par (número de tile `$80000`), o preenchimento com zeros e a máscara de tile de 20 contra 19 bits. Não usa dados dos jogos e compila contra o kit privado (`private/work/samsho-runtime-source/neogeorecomp`, ou `NEOGEORECOMP_SOURCE`). Precisa de um compilador C (clang ou gcc) e grava cerca de 80 MiB de arquivos temporários em `private/`. A partir de `tools/kof2003`:

```
py -3 -m loader.run_loader_test
```

Código de saída 0 significa que todas as verificações passaram.

### Sonda de memória nativa (primeira importação do SVC, ticket 08)

O executável nativo pode registrar a cada quadro a memória escolhida, no mesmo formato do `probe.lua` no MAME. Ele recebe uma lista de endereços como `0x1010e0:4,0x2fe91d:1` (endereço 68000 em hexadecimal, depois 1, 2 ou 4 bytes; até 16 entradas) e grava uma linha por quadro, `<quadro>\t<hex>\t<hex>...`. As leituras não têm efeitos colaterais e alcançam a RAM de trabalho e a RAM do NEO-PVC. A sonda fica desligada por dois motivos: a opção CMake `KOF2003_NATIVE_PROBE` vem desligada, e um executável compilado com ela não registra nada sem `KOF_NATIVE_PROBE` definida. Só uma cópia privada do runtime é alterada.

Para compilar, rode os comandos da versão em inglês acima a partir da raiz do repositório, no PowerShell 7.4+, depois que o [guia de build no Windows](../../../docs/specs/first-svc-character-import/native-mvs-windows.md) tiver gerado o build de controle em `private/work/mvs-native-build`. Em seguida confira que o build com a sonda ainda passa no controle MVS nativo com a opção desligada (sem `KOF_NATIVE_PROBE` no ambiente): zero divergências de estado e zero instruções interpretadas no resumo.

Para sondar um roteiro nos dois runtimes e comparar, a partir de `tools/kof2003`, use os comandos `match.probe_run` e `match.probe_log` acima. Os endereços padrão (`TEAM_MATCH_ADDRESSES` em `probe_run.py`) são o ponteiro de pose do P1 (`$101080 + $60`) e a vida dos três membros das equipes do P1 e do P2 na RAM do NEO-PVC (`$2FE91D`, `$2FEA1D`, `$2FEB1D`, `$2FED1D`, `$2FEE1D`, `$2FEF1D`); use `--probe` para outros. Para registrar sem o MAME, defina `KOF_NATIVE_PROBE`, `KOF_NATIVE_PROBE_LOG` (um caminho dentro de `private/`) e, se quiser, `KOF_NATIVE_PROBE_FIRST`, e rode o executável. Os dois logs usam os números de quadro do executável nativo: a sonda do MAME é rotulada com `REPLAY_OFFSET` 2 e não é preciso deslocamento extra. Os quadros antes do 290 diferem enquanto a BIOS testa a memória ao ligar, e a luta em equipe diverge a partir do primeiro comando durante a luta, no quadro 5.600, pelo motivo registrado no [ticket 07](../../../docs/specs/first-svc-character-import/issues/07-explain-in-fight-input-divergence.md).
