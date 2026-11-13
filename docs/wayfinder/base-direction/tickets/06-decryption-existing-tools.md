---
id: 06
title: "Decryption with existing tools"
label: wayfinder:task
mode: AFK
status: closed
assignee: codex
blocked_by: [01, 02]
research:
---

## Question

Do the existing tools (the decrypt step of the KOF 2003 port, the approach of the Metal Slug 5 recomp) decrypt the owner's dumps of both games identically to MAME? Record the reproducible script and where the generated files are kept, outside the repository.

_PT-BR: as ferramentas existentes (o decrypt do port do KOF 2003, a abordagem do MS5 recomp) descriptografam meus dumps dos dois jogos de forma idêntica ao MAME? Registrar o script reproduzível e onde ficam os arquivos gerados, fora do repositório._

## Notes

Generated files go to `private/work/`. Third-party tools are run from outside the repository or from `private/`; their code is not copied in.

_PT-BR: arquivos gerados vão para `private/work/`. Ferramentas de terceiros rodam de fora do repositório ou de `private/`; o código delas não é copiado para cá._

## Resolution

**English.** The owner's `svc` and Export `kof2003` dumps produced **zero byte differences** against MAME 0.289 in the five cartridge regions tested for each game.

- **SVC Chaos, program (P).** The first comparison covered only the 8 MiB 68000 program. A local wrapper reused the Metal Slug 5 recomp's `probe_decryption.py` with the `svc` cartridge and its two P-ROMs. It learned a one-to-one map from synthetic inputs, predicted a fresh synthetic input with zero differences, then applied the map to the owner's dump and matched the whole region. The map uses MAME as a black-box reference during learning. [Metal Slug 5 recomp](https://github.com/AlmazProud/metal-slug-5-recomp)
- **SVC Chaos, graphics and audio (C, S, M1, V).** A private build of the KOF 2003 decryptor used SVC chip names, the SVC CMC50 graphics selector and PCM2 swap 3. The existing M1 logic handled the SVC dump. The program comparison used the synthetic map above. [MAME cartridge driver](https://raw.githubusercontent.com/mamedev/mame/master/src/devices/bus/neogeo/pvc.cpp)
- **KOF 2003.** The bundled Windows x64 `v0.1.0` decryptor matched all five regions after the 68000 word byte order was aligned, the eight sprite files were interleaved in pairs, the two sample files were concatenated, and MAME's 64 KiB Z80 mirror was checked and excluded from the M1 comparison. The SVC graphics and audio comparison used the same layouts. [KOF 2003 port v0.1.0](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0) · [MAME Lua memory regions](https://docs.mamedev.org/luascript/ref-mem.html#memory-region)

**Português (Brasil).** Os dumps `svc` e `kof2003` Export do dono tiveram **zero bytes divergentes** em relação ao MAME 0.289 nas cinco regiões de cartucho testadas de cada jogo.

- **SVC Chaos, programa (P).** A primeira comparação cobriu só os 8 MiB do programa 68000. Um script local reaproveitou o `probe_decryption.py` do Metal Slug 5 recomp com o cartucho `svc` e suas duas ROMs P. O script aprendeu um mapeamento biunívoco com entradas sintéticas, previu sem divergências a saída para uma entrada sintética nova e depois aplicou o mapeamento ao dump do dono. A região inteira bateu. O aprendizado usou o MAME como referência de caixa-preta. [Metal Slug 5 recomp](https://github.com/AlmazProud/metal-slug-5-recomp)
- **SVC Chaos, gráficos e áudio (C, S, M1, V).** Uma compilação privada do descriptografador do KOF 2003 usou os nomes dos chips do SVC, o seletor gráfico CMC50 do SVC e o modo 3 do PCM2. A rotina existente de M1 processou o dump do SVC. A comparação do programa usou o mapeamento sintético acima. [Driver do cartucho no MAME](https://raw.githubusercontent.com/mamedev/mame/master/src/devices/bus/neogeo/pvc.cpp)
- **KOF 2003.** O descriptografador do pacote Windows x64 `v0.1.0` bateu nas cinco regiões após alinhar a ordem de bytes nas palavras do 68000, intercalar os oito arquivos de sprites em pares, concatenar os dois arquivos de amostras e conferir o espelho de 64 KiB do Z80 no MAME antes de excluí-lo da comparação de M1. Os gráficos e o áudio do SVC foram comparados nos mesmos formatos. [Port do KOF 2003 v0.1.0](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0) · [Regiões de memória na API Lua do MAME](https://docs.mamedev.org/luascript/ref-mem.html#memory-region)

### Results / Resultados

The SHA-256 is for the MAME bytes used in the comparison. Each row had zero differences. / _O SHA-256 é dos bytes do MAME usados na comparação. Cada linha teve zero divergências._

| Set / Conjunto | Region / Região | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `svc` | P (MAME host order / ordem do host do MAME) | 8,388,608 | `7e2025976c1cdacb37cda878bd12d81dff2dd788115cb5e1a083137787b02dc7` |
| `svc` | C | 67,108,864 | `885b32972c296fdeabaf8e8e4cfbb327fd65228e9326251f6a107e59a5cfcb8c` |
| `svc` | S | 524,288 | `ffb54fecbfc05b416633a653b3763e7329941107692daaca0fd791bb0794e574` |
| `svc` | M1 | 524,288 | `0614ec869c369a1c92dc0dc0f8393612bffd17142c4d59f99991401633970578` |
| `svc` | V | 16,777,216 | `3183f5194896c5af63b7d3e26c25d4dc5fb54b1ab7dcf7b3016ccc97918f0114` |
| `kof2003` | P (68000 order / ordem do 68000) | 9,437,184 | `f6ad2e2d7496eb094b92108b85aca6c71cf6fb397c690e49a04048da27143215` |
| `kof2003` | C | 67,108,864 | `43c984c9332c9f641d3ab08731508c8c0d4efc28bf842d0cf4abbd8449f7a09e` |
| `kof2003` | S | 524,288 | `d6327c711ac102ef01abbadd2e03127384cf65ffc0a6213c121129da6839eebc` |
| `kof2003` | M1 | 524,288 | `13e6ed399292eff412d5c7ddb2285111afda8342efb06ba6d2d865775abfadc6` |
| `kof2003` | V | 16,777,216 | `44ee6c1f3c9f11d604df05cf54be7acde53cad556bf19ff9f46f5bb928a97fa2` |

### Reproduction / Reprodução

Run from the repository root in PowerShell with Python 3.11.9, NumPy 2.4.6, and MAME 0.289 for Windows x64. The script checks the input ZIP hashes from [Dump the cartridges](01-cartridge-dumps.md) and starts MAME with the `euro` BIOS. `svc-assets` also needs a C compiler (tested with the local `gcc` command, which reports Clang 22.1.8). The existing KOF port checkout is at `196b3f8ed2f25dfc34100c60835fee37ebcc69ad`. The private Metal Slug 5 checkout is at `2b3626d28420eae2ce2ac6210a34a1f5a65bc234`.

_Execute na raiz do repositório, no PowerShell, com Python 3.11.9, NumPy 2.4.6 e MAME 0.289 para Windows x64. O script confere os hashes dos ZIPs registrados em [Dump the cartridges](01-cartridge-dumps.md) e inicia o MAME com o BIOS `euro`. O comando `svc-assets` também requer um compilador C (teste com o comando local `gcc`, que reporta Clang 22.1.8). O checkout já existente do port do KOF está em `196b3f8ed2f25dfc34100c60835fee37ebcc69ad`. O checkout privado do Metal Slug 5 está em `2b3626d28420eae2ce2ac6210a34a1f5a65bc234`._

```powershell
python private/work/decryption-mame/compare.py svc-program
python private/work/decryption-mame/compare.py svc-assets
python private/work/decryption-mame/compare.py kof2003
```

The script and its Lua helper are in `private/work/decryption-mame/`. The ROM images, learned map, generated SVC decryptor and other outputs are in `private/work/decryption-mame/results/`. The SVC program from the learned map is `svc-learned-maincpu.bin` in MAME's little-endian host order. The comparisons apply to these dumps and static ROM regions. Native execution and runtime PVC banking are separate checks.

_O script e o auxiliar em Lua ficam em `private/work/decryption-mame/`. As imagens de ROM, o mapeamento aprendido, o descriptografador gerado para SVC e as demais saídas ficam em `private/work/decryption-mame/results/`. O programa do SVC obtido pelo mapeamento é `svc-learned-maincpu.bin`, na ordem little-endian do host do MAME. As comparações valem para estes dumps e as regiões estáticas de ROM. A execução nativa e a troca de bancos do PVC em execução são verificações à parte._
