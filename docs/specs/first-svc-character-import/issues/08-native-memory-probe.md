---
title: "Probe fighter memory in the native player"
triage: ready-for-agent
assignee: claude
---

# 08 Probe fighter memory in the native player

[Parent specification](../spec.md)

## What to build

Give the native KOF 2003 player a headless option that logs selected work-RAM addresses every frame, so the import can be measured in the native build the same way `tools/kof2003/match/probe.lua` measures MAME. Change only the local runtime copy under `private/`. The owner authorized the rebuild on 2026-11-15.

## Blocked by

None.

## Acceptance criteria

- [x] A scripted native run writes one line per frame with the requested addresses, and the option is off by default.
- [x] For the scripted Iori team match, the native log of P1's pose pointer (`$101080 + 0x60`) and both fighters' health matches the MAME probe for the same frames. (Frames 290–5,599, up to the first in-fight input; P2 took no damage there. See the resolution.)
- [x] The native MVS control run still passes `--verify` with the option off.
- [x] Commands to build and run it are recorded under `tools/kof2003/`.

## Comments

### 2026-11-20 — Resolution: the native player logs memory each frame and matches MAME

**Tools.** `tools/kof2003/match/native_probe.c` is the probe; `probe_hook.py` adds its call after each frame to a private copy of the runtime's `neogeo.c` (source SHA-256 `1dccd6a0…6893`, hooked `d5aa298c…68c1`); the CMake option `KOF2003_NATIVE_PROBE` (off by default) compiles it in. At run time it logs only when `KOF_NATIVE_PROBE` holds an address list such as `0x1010e0:4,0x2fe91d:1`, writing `<frame>\t<hex>...` to `KOF_NATIVE_PROBE_LOG`. It reads through the runtime's side-effect-free word peek, so it reaches work RAM and NEO-PVC RAM and cannot change the run. `probe.lua` gained the same address-list mode (`PROBE_ADDRESSES`) and now labels frames with `REPLAY_OFFSET` like `replay.lua` (SVC runs through `mame_run.py` keep offset 1). `probe_log.py` parses lists and logs and compares two logs; `probe_run.py` runs one script on both runtimes and compares. Tests: the C probe compiled against a fake bus, the hook, the log format and comparison, the orchestration with fake runtimes, and the Lua mode against a fake MAME (with `lupa`). Build and run commands are in `tools/kof2003/match/README.md`. The build lives in `private/work/native-probe/`.

**Health is not in work RAM.** KOF 2003 keeps each team member's health in NEO-PVC RAM: P1 at `$2FE91D`, `$2FEA1D`, `$2FEB1D`, P2 at `$2FED1D`, `$2FEE1D`, `$2FEF1D` ([peon2's KOF 2003 module](https://github.com/peon2/fbneo-training-mode/blob/bf3541e1d4f586f76f401617af4fa842447591de/games/kof2003/kof2003.lua)). The probe therefore takes any bus address, not only work RAM. The runs confirm P1's: the value is set to full when the fight starts and drops at each hit Iori takes.

**Comparison.** `team-match.txt`, 36,100 frames, pose pointer (`$101080 + $60`) and the six health bytes. Both logs carry the native frame numbers and need no shift (shifts −3 to +3 were tried; only 0 matches). All seven columns are identical on the 5,310 frames from 290 to 5,599. That window covers the fight start at frame 4,926 and four hits on Iori (frames 5,267, 5,335, 5,361 and 5,460). Frames before 290 differ while the BIOS tests memory at power-on. From frame 5,600, the first in-fight input, the runs diverge, as recorded in [ticket 07](07-explain-in-fight-input-divergence.md). In both runtimes Iori's team then loses all three members and Whip's team is never hit, so P2's health column matched only at its full value: this script never exercises it with damage. The full two-runtime run takes about 2.5 minutes. The README commands, run as written in PowerShell 7, gave the same result with the final build (`equal on 5310 frames`, saved in the run's `summary.txt` under `private/work/native-probe/runs/`).

**P2's health and the one-frame lead.** `match/scripts/iori-hits-whip.txt` adds one C press at frame 5,300. Iori hits Whip in both runtimes and P2's first health byte drops (native at frame 5,306, MAME at 5,307, by a slightly different amount), which confirms `$2FED1D` as P2's health. The logs differ from frame 5,301: the native player starts the move one frame before MAME's replay. With a press at frame 5,410, Iori's whole move runs one frame ahead in the native log (native frame N equals MAME frame N + 1) and both rejoin when Whip hits him at frame 5,459. A press at frame 5,480, while Iori is being hit, changes nothing, and the logs stay identical to frame 5,999. In-fight input therefore reaches the game one frame earlier in the native player than in `replay.lua`. This is new evidence for [ticket 07](07-explain-in-fight-input-divergence.md), which the owner closed; it is not pursued here.

**Control.** The probe build with the option off replays the native MVS control (6,000 frames, `tests/play.txt`) under `--verify` with 3,583,428 blocks checked, 0 state mismatches, 2,669 cycle-count differences (the same as the control build), 0 interpreted instructions and 0 uncovered entry points. With the probe on, the same run also has 0 mismatches and 0 interpreted instructions and writes 6,000 lines.

_PT-BR: **Ferramentas.** `tools/kof2003/match/native_probe.c` é a sonda; `probe_hook.py` acrescenta a chamada dela, depois de cada quadro, a uma cópia privada do `neogeo.c` do runtime (SHA-256 da origem `1dccd6a0…6893`, com o gancho `d5aa298c…68c1`); a opção CMake `KOF2003_NATIVE_PROBE` (desligada por padrão) a compila. Na execução, ela só registra quando `KOF_NATIVE_PROBE` traz uma lista de endereços como `0x1010e0:4,0x2fe91d:1`, gravando `<quadro>\t<hex>...` em `KOF_NATIVE_PROBE_LOG`. A leitura usa a consulta de palavras do runtime, sem efeitos colaterais, então alcança a RAM de trabalho e a RAM do NEO-PVC e não pode alterar a execução. O `probe.lua` ganhou o mesmo modo de lista (`PROBE_ADDRESSES`) e agora rotula os quadros com `REPLAY_OFFSET`, como o `replay.lua` (as execuções do SVC pelo `mame_run.py` continuam com deslocamento 1). O `probe_log.py` lê listas e logs e compara dois logs; o `probe_run.py` roda um roteiro nos dois runtimes e compara. Testes: a sonda em C compilada contra um barramento falso, o gancho, o formato e a comparação dos logs, a orquestração com runtimes falsos e o modo Lua contra um MAME falso (com `lupa`). Os comandos de build e execução estão em `tools/kof2003/match/README.md`. O build fica em `private/work/native-probe/`._

_**A vida não fica na RAM de trabalho.** O KOF 2003 guarda a vida de cada membro da equipe na RAM do NEO-PVC: P1 em `$2FE91D`, `$2FEA1D`, `$2FEB1D`, P2 em `$2FED1D`, `$2FEE1D`, `$2FEF1D` (módulo do KOF 2003 do peon2, link acima). Por isso a sonda aceita qualquer endereço do barramento, não só a RAM de trabalho. As execuções confirmam os do P1: o valor fica cheio quando a luta começa e cai a cada golpe que o Iori recebe._

_**Comparação.** `team-match.txt`, 36.100 quadros, ponteiro de pose (`$101080 + $60`) e os seis bytes de vida. Os dois logs usam os números de quadro do nativo e não precisam de deslocamento (foram testados de −3 a +3; só o 0 coincide). As sete colunas são idênticas nos 5.310 quadros de 290 a 5.599. Essa janela inclui o início da luta no quadro 4.926 e quatro golpes no Iori (quadros 5.267, 5.335, 5.361 e 5.460). Antes do quadro 290 há diferenças enquanto a BIOS testa a memória ao ligar. A partir do quadro 5.600, o primeiro comando durante a luta, as execuções divergem, como registrado no [ticket 07](07-explain-in-fight-input-divergence.md). Nos dois runtimes a equipe do Iori perde os três membros e a da Whip nunca é atingida, então a coluna de vida do P2 só coincidiu no valor cheio: este roteiro nunca a exercita com dano. A execução completa nos dois runtimes leva cerca de 2,5 minutos._

_Os comandos do README, executados como estão no PowerShell 7, deram o mesmo resultado com o build final (`equal on 5310 frames`, gravado no `summary.txt` da execução em `private/work/native-probe/runs/`)._

_**A vida do P2 e o quadro de vantagem.** O `match/scripts/iori-hits-whip.txt` acrescenta um C no quadro 5.300. O Iori acerta a Whip nos dois runtimes e o primeiro byte de vida do P2 cai (no nativo no quadro 5.306, no MAME no 5.307, com valores um pouco diferentes), o que confirma `$2FED1D` como a vida do P2. Os logs diferem a partir do quadro 5.301: o nativo começa o golpe um quadro antes da repetição do MAME. Com o botão no quadro 5.410, o golpe inteiro do Iori corre um quadro adiantado no log nativo (o quadro N do nativo é igual ao N + 1 do MAME) e os dois voltam a coincidir quando a Whip o acerta no quadro 5.459. Com o botão no quadro 5.480, enquanto o Iori apanha, nada muda e os logs ficam idênticos até o quadro 5.999. O comando durante a luta chega ao jogo, portanto, um quadro antes no nativo do que no `replay.lua`. É uma evidência nova para o [ticket 07](07-explain-in-fight-input-divergence.md), que o dono fechou; não foi investigada aqui._

_**Controle.** O build com a sonda e a opção desligada repete o controle MVS nativo (6.000 quadros, `tests/play.txt`) com `--verify`: 3.583.428 blocos verificados, 0 divergências de estado, 2.669 diferenças de ciclos (as mesmas do build de controle), 0 instruções interpretadas e 0 pontos de entrada sem cobertura. Com a sonda ligada, a mesma execução também tem 0 divergências e 0 instruções interpretadas e grava 6.000 linhas._
