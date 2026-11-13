---
id: 10
title: "Cost of making SVC native"
label: wayfinder:task
mode: AFK
status: closed
assignee: codex
blocked_by: [06, 09]
research:
---

## Question

On the foundation where KOF 2003 already runs, what is missing for SVC Chaos to run natively (protection, jump tables, hardware differences)? How much does it cost to have both games in the same runtime?

_PT-BR: na fundação em que o KOF 2003 já roda, o que falta para o SVC rodar nativo (proteção, tabelas de salto, diferenças de hardware)? Quanto custa ter os dois no mesmo runtime?_

## Resolution

### English

**Measured.** The Windows x64 KOF 2003 `v0.1.0` executable, built on neogeorecomp v0.2.0 with the port's board changes, ran the SVC cartridge through the start of its first 1v1 round in interpreter mode. The test reused the five validated SVC regions and the Europe MVS v2 BIOS. The KOF 2003 control passed the same one-frame loader test with its own ROMs. [KOF 2003 runtime control](09-run-kof2003-port.md) · [Validated cartridge regions](06-decryption-existing-tools.md) · [Port release](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0)

- **First blocker.** The executable exited with code 1 before boot because its KOF 2003 cartridge descriptor requires a 9 MiB program file. SVC has 8 MiB. The probe converted the validated program to 68000 byte order, provided the SVC assets under the filenames expected by the executable and appended 1 MiB of zeros for the loader test. The same executable then exited successfully with the one-frame limit. A real SVC descriptor should declare 8 MiB and enforce its own bank bounds.
- **Furthest verified point.** A 2,500-frame run with scripted coin, start and A inputs reached the title (frame 500), character select (1,500), pre-fight dialogue (2,200) and an active round with the timer at 57 (2,499). The HUD and a few sprites rendered, while the stage and most fighter graphics were absent. MAME 0.289 showed the stage and both fighters at the same round timer. The two runs selected different opponents, so this is a visual comparison of the same phase with no frame-exact or CPU-state comparison. The cause of the rendering gap is open.
- **PVC reference.** MAME first wrote to the bank-selector range at reference frame 280 (PC `0x0094B8`, write to `0x2FFFF8`), then to general PVC RAM at frame 281 and a color register at frame 290. Across 2,500 frames the MAME tap counted 132,387 writes in the bank-selector range, 99,640 other PVC RAM writes and 27,186 color-register writes. Counts describe bus writes, including repeated selections. The port run did not capture PVC state or effective bank offsets.
- **Native execution.** The executable reported zero native blocks for SVC. The 18,439 entries reported on startup belong to KOF 2003 and were disabled by `--interp`. Its public source snapshot omits the build files and the modified runtime linked into the release. Native state divergences and native coverage for SVC remain unmeasured. [Source snapshot notes](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/196b3f8ed2f25dfc34100c60835fee37ebcc69ad/SOURCE-NOTES.md)

**Remaining work and cost estimate.** The evidence supports reusing the board model for early execution. A second native game requires its own cartridge configuration, dispatch table and verification. The effort to reach a correctly rendered native fight remains unmeasured.

| Area | Remaining work and estimated scope |
| --- | --- |
| Cartridge and build | Declare the 8 MiB program and SVC ROM layout. Recover or reproduce the KOF port's runtime changes in a build that can run both descriptors. The descriptor change is small. Build recovery is an independent dependency with unknown effort. |
| PVC protection and banking | Both cartridges use the same MAME PVC handler. Compare the first bank write and subsequent readback against MAME, including byte and word masks, register side effects, the effective ROM offset and out-of-range handling. Check color pack/unpack and banked reads through the first round. Shared handling looks reusable. The extent of any fixes depends on the first state mismatch. [MAME cartridge mapping](https://github.com/mamedev/mame/blob/master/src/mame/snk/neogeo.cpp) · [MAME PVC model](https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/prot_pvc.cpp) |
| Jump tables and native dispatch | Generate SVC-specific code and entry points from the vectors, direct targets and jump tables. Profile boot, selection and a 1v1 round with the interpreter to find missed indirect targets. Check banked targets using the effective ROM offset along with the 68000 address. Then compare native and interpreted execution on that same input segment using `--verify` for registers, flags and bus writes, tracking cycle differences and fallback coverage separately. Target count and profiling effort are unknown. [neogeorecomp](https://github.com/sp00nznet/neogeorecomp) |
| Board behavior | MAME uses the same PVC family and fixed-layer bank type for these cartridges. Their program sizes and decryption parameters differ, and the validated assets already cover the latter. Compare matched stage and fighters with synchronized inputs and initial state. Trace VRAM writes, sprite tile indices, palette, and fixed-layer bank selection at the first visual divergence. Also check Z80/YM2610 sound and interrupt timing. The round shows an unresolved rendering gap, so the scope of board fixes remains open. [MAME cartridge variants](https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/pvc.cpp) · [MAME fixed-layer bank types](https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/pvc.h) |

### Português (Brasil)

**Medido.** O executável Windows x64 do KOF 2003 `v0.1.0`, baseado no neogeorecomp v0.2.0 com as adaptações de placa do port, executou o cartucho do SVC em modo interpretado até o início da primeira luta 1x1. O teste reaproveitou as cinco regiões validadas do SVC e a BIOS Europe MVS v2. O KOF 2003 passou no mesmo teste de carregamento de um quadro com suas próprias ROMs. [Controle com o runtime do KOF 2003](09-run-kof2003-port.md) · [Regiões validadas dos cartuchos](06-decryption-existing-tools.md) · [Versão do port](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0)

- **Primeiro bloqueio.** O executável encerrou com código 1 antes da inicialização porque a descrição do cartucho do KOF 2003 exige um arquivo de programa de 9 MiB. O do SVC tem 8 MiB. O teste converteu o programa validado para a ordem de bytes do 68000, apresentou os arquivos do SVC com os nomes esperados pelo executável e acrescentou 1 MiB de zeros para testar o carregador. O mesmo executável então encerrou com sucesso no limite de um quadro. A descrição própria do SVC deve declarar 8 MiB e respeitar os limites de bancos desse cartucho.
- **Ponto mais avançado verificado.** Uma execução de 2.500 quadros com moeda, Start e A por script chegou ao título (quadro 500), à seleção (1.500), ao diálogo pré-luta (2.200) e a um round em andamento com 57 no cronômetro (2.499). O HUD e alguns sprites apareceram, mas faltaram o cenário e a maior parte dos gráficos dos lutadores. O MAME 0.289 mostrou o cenário e os dois lutadores com o mesmo tempo de round. As duas execuções selecionaram adversários diferentes, então a comparação foi visual e na mesma fase. A comparação quadro a quadro e de estado da CPU segue pendente, assim como a causa da falha gráfica.
- **Referência do PVC.** A primeira escrita no intervalo do seletor de bancos no MAME ocorreu no quadro de referência 280 (PC `0x0094B8`, escrita em `0x2FFFF8`). A primeira escrita na RAM geral do PVC ocorreu no quadro 281 e a primeira em um registrador de cor no 290. Em 2.500 quadros, o monitor do MAME contou 132.387 escritas no intervalo do seletor, 99.640 outras escritas na RAM do PVC e 27.186 escritas nos registradores de cor. As contagens são de escritas no barramento e incluem seleções repetidas. A execução no port não capturou o estado do PVC nem os offsets efetivos dos bancos.
- **Execução nativa.** O executável registrou zero blocos nativos para o SVC. As 18.439 entradas anunciadas no início pertencem ao KOF 2003 e foram desativadas com `--interp`. O código-fonte público do port omite os arquivos de build e o runtime modificado vinculado à versão distribuída. As divergências de estado e a cobertura da execução nativa do SVC seguem sem medição. [Notas da versão pública do código](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/196b3f8ed2f25dfc34100c60835fee37ebcc69ad/SOURCE-NOTES.md)

**Trabalho restante e estimativa de custo.** A execução inicial indica que dá para reaproveitar o modelo de placa. Um segundo jogo nativo exige configuração de cartucho, tabela de despacho e verificação próprias. O esforço até uma luta nativa com renderização correta segue sem medição.

| Área | Trabalho restante e estimativa de escopo |
| --- | --- |
| Cartucho e build | Declarar o programa de 8 MiB e o layout das ROMs do SVC. Recuperar ou reproduzir as adaptações de runtime do port do KOF num build que aceite as duas descrições. A mudança de descrição é pequena. Recuperar o build é uma dependência à parte, com esforço em aberto. |
| Proteção e troca de bancos PVC | Os dois cartuchos usam o mesmo tratamento de PVC no MAME. Comparar com o MAME a primeira escrita de banco e a leitura posterior, incluindo máscaras de byte e palavra, efeitos nos registradores, offset efetivo na ROM e tratamento de valores fora dos limites. Conferir o empacotamento de cores e as leituras dos bancos até o primeiro round. O tratamento compartilhado parece reaproveitável. O tamanho de eventuais correções depende da primeira diferença de estado encontrada. [Mapa de cartucho no MAME](https://github.com/mamedev/mame/blob/master/src/mame/snk/neogeo.cpp) · [Modelo do PVC no MAME](https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/prot_pvc.cpp) |
| Tabelas de salto e despacho nativo | Gerar código e entradas do SVC a partir dos vetores, destinos diretos e tabelas de salto. Usar o interpretador para levantar destinos indiretos que faltarem durante a inicialização, a seleção e uma luta 1x1. Conferir os destinos em bancos com o offset efetivo na ROM junto do endereço do 68000. No mesmo trecho e com as mesmas entradas, usar `--verify` para comparar registradores, flags e escritas no barramento entre nativo e interpretado. Contabilizar à parte diferenças de ciclos e trechos que voltam ao interpretador. O número de destinos e o esforço de perfilamento estão em aberto. [neogeorecomp](https://github.com/sp00nznet/neogeorecomp) |
| Comportamento da placa | O MAME usa a mesma família PVC e o mesmo tipo de banco da camada fixa nos dois cartuchos. O tamanho do programa e os parâmetros de descriptografia diferem, e as regiões validadas já cobrem a descriptografia. Comparar a mesma fase da luta com os mesmos lutadores, cenário, entradas e estado inicial. Rastrear escritas na VRAM, índices de tiles dos sprites, paleta e banco da camada fixa na primeira divergência visual. Conferir também som Z80/YM2610 e temporização das interrupções. A falha gráfica observada deixa em aberto o escopo das correções de placa. [Variantes dos cartuchos no MAME](https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/pvc.cpp) · [Bancos da camada fixa no MAME](https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/pvc.h) |

### Reproduction / Reprodução

Run from the repository root with Python 3.11, NumPy, the prepared Windows KOF 2003 `v0.1.0` release and local MAME 0.289. Scripts, staged assets, logs, traces and captures are under `private/work/svc-native-cost/`. The last two commands run headless, muted and below normal priority. The exact round participants may differ across runtimes. / _Execute na raiz do repositório com Python 3.11, NumPy, o port Windows do KOF 2003 `v0.1.0` já preparado e o MAME 0.289 local. Scripts, arquivos preparados, logs, traces e capturas ficam em `private/work/svc-native-cost/`. Os dois últimos comandos rodam sem janela, sem áudio e com prioridade abaixo da normal. Os participantes da luta podem variar entre os runtimes._

```powershell
python private/work/svc-native-cost/probe.py kof 1
python private/work/svc-native-cost/probe.py svc 1
python private/work/svc-native-cost/probe.py svc-padded 1
python private/work/svc-native-cost/probe.py svc-padded 2500 500 800 1200 1500 1900 2200 2499 --input private/work/svc-native-cost/svc-input.txt
python private/work/svc-native-cost/reference.py 2500 500 800 1200 1500 1900 2200 2499
```

The base game choice belongs to [Direction decision](11-direction-decision.md). / _A escolha do jogo base fica em [Direction decision](11-direction-decision.md)._
