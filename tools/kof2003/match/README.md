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
| `probe.lua` | Logs animation pointer, position and health each frame. Defaults are SVC Chaos offsets. |
| `compare_captures.py` | Compares two capture sets by hash; reports equal or the first differing frame (graphics-set growth, ticket 01). |
| `repeat_reference.py` | Runs one build twice on `scripts/coin-start.txt` and `scripts/team-match.txt`, then compares the two capture sets. |
| `compare_builds.py` | Runs two builds (default A and B) once on both scripts, compares the captures by hash, checks B's `--verify` is not worse, and measures B's memory (graphics-set growth, ticket 02). |
| `memory_probe.py` | Measures a Windows process's peak and steady memory while it runs. |

Recording a session: start MAME with `-record <name>.inp -autoboot_script log_inputs.lua` and `INPUT_LOG` set. Do not use MAME's soft reset (F3) while recording. Close MAME and start again instead. Tests: `py -3 -m pytest match` from `tools/kof2003`.

### Reference build A (graphics-set growth, ticket 01)

Build A is the native player as built from the unchanged descriptor (64 MiB Graphics Set). Its copy lives in `private/work/graphics-growth/build-a/` (read-only); later builds go elsewhere. To rebuild it, run the native build in `private/work/mvs-native-build` with the descriptor unchanged and copy `KOF 2003.exe` and `SDL2.dll` into a new folder under `private/work/graphics-growth/`. To prove it repeats itself, from `tools/kof2003` on Windows:

```
py -3 -m match.repeat_reference
py -3 -m match.compare_captures RUN_A_DIR RUN_B_DIR
```

Runs and captures go under `private/work/graphics-growth/runs/`. Exit code 1 means a difference; the first differing frame is printed.

Build B (128 MiB) and its comparison with A: see `../growth/README.md` (ticket 02).

### Grown loader test (graphics-set growth, ticket 03)

`../loader/test_grown_loader.c` loads synthetic graphics file pairs at the 128 MiB size and at the 64 MiB size and checks pair interleaving, the tile at the fifth pair (tile number `$80000`), zero fill, and the 20-bit versus 19-bit tile mask. It uses no game data and compiles against the private toolkit (`private/work/samsho-runtime-source/neogeorecomp`, or `NEOGEORECOMP_SOURCE`). It needs a C compiler (clang or gcc) and writes about 80 MiB of temporary files under `private/`. From `tools/kof2003`:

```
py -3 -m loader.run_loader_test
```

Exit code 0 means every check passed.

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
| `probe.lua` | Registra ponteiro de animação, posição e vida a cada quadro. Os padrões são deslocamentos do SVC Chaos. |
| `compare_captures.py` | Compara dois conjuntos de capturas por hash; informa igual ou o primeiro quadro diferente (ampliação do Conjunto gráfico, ticket 01). |
| `repeat_reference.py` | Roda um build duas vezes com `scripts/coin-start.txt` e `scripts/team-match.txt` e compara os dois conjuntos de capturas. |
| `compare_builds.py` | Roda dois builds (por padrão A e B) uma vez nos dois roteiros, compara as capturas por hash, confere que o `--verify` do B não é pior e mede a memória do B (ampliação do Conjunto gráfico, ticket 02). |
| `memory_probe.py` | Mede o pico e o regime de memória de um processo do Windows enquanto ele roda. |

Para gravar uma sessão, abra o MAME com `-record <nome>.inp -autoboot_script log_inputs.lua` e `INPUT_LOG` definido. Não use o reset do MAME (F3) durante a gravação. Feche e abra o MAME de novo. Testes: `py -3 -m pytest match` a partir de `tools/kof2003`.

### Build de referência A (ampliação do Conjunto gráfico, ticket 01)

O build A é o player nativo compilado com o descritor sem mudança (Conjunto gráfico de 64 MiB). A cópia fica em `private/work/graphics-growth/build-a/` (somente leitura); os builds seguintes vão para outro lugar. Para recompilar, rode o build nativo em `private/work/mvs-native-build` com o descritor sem mudança e copie `KOF 2003.exe` e `SDL2.dll` para uma pasta nova em `private/work/graphics-growth/`. Para provar que ele se repete, a partir de `tools/kof2003`, no Windows:

```
py -3 -m match.repeat_reference
py -3 -m match.compare_captures PASTA_RODADA_A PASTA_RODADA_B
```

Rodadas e capturas ficam em `private/work/graphics-growth/runs/`. Código de saída 1 indica diferença; o primeiro quadro diferente é impresso.

Build B (128 MiB) e a comparação com o A: veja `../growth/README.md` (ticket 02).

### Teste do carregador ampliado (ampliação do Conjunto gráfico, ticket 03)

O `../loader/test_grown_loader.c` carrega pares sintéticos de arquivos gráficos com o tamanho de 128 MiB e com o de 64 MiB e confere a intercalação dos pares, o tile do quinto par (número de tile `$80000`), o preenchimento com zeros e a máscara de tile de 20 contra 19 bits. Não usa dados dos jogos e compila contra o kit privado (`private/work/samsho-runtime-source/neogeorecomp`, ou `NEOGEORECOMP_SOURCE`). Precisa de um compilador C (clang ou gcc) e grava cerca de 80 MiB de arquivos temporários em `private/`. A partir de `tools/kof2003`:

```
py -3 -m loader.run_loader_test
```

Código de saída 0 significa que todas as verificações passaram.
