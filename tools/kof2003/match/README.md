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

Recording a session: start MAME with `-record <name>.inp -autoboot_script log_inputs.lua` and `INPUT_LOG` set. Do not use MAME's soft reset (F3) while recording. Close MAME and start again instead. Tests: `py -3 -m pytest match` from `tools/kof2003`.

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

Para gravar uma sessão, abra o MAME com `-record <nome>.inp -autoboot_script log_inputs.lua` e `INPUT_LOG` definido. Não use o reset do MAME (F3) durante a gravação. Feche e abra o MAME de novo. Testes: `py -3 -m pytest match` a partir de `tools/kof2003`.
