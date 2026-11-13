---
id: 07
title: "Shared art"
label: wayfinder:task
mode: AFK
status: closed
assignee: codex
blocked_by: [06]
research:
---

## Question

How much of the C-ROM art is identical between the two games (hashes of 16×16 tiles), which fighters do the shared tiles belong to, and where are each game's anchors?

_PT-BR: quanto da arte das C-ROMs é idêntica entre os dois jogos (hash de tiles 16x16), a quais personagens pertencem os tiles em comum, e onde ficam as âncoras de cada jogo?_

## Notes

Only counts, hashes and addresses go in the resolution; no tile images.

_PT-BR: só contagens, hashes e endereços entram na resolução; nenhuma imagem de tile._

## Resolution

### C-ROM comparison / Comparação das C-ROMs

**English.** The full C regions share **59,291 distinct nonzero tile hashes**, including **47,213** that occur at exactly one address in each game. They cover **18.68%** of the nonzero tile slots in KOF 2003 and **14.83%** in SVC Chaos. Each slot is one aligned 16×16 tile at 4 bits per pixel, stored in 128 bytes. The comparison excludes all-zero tiles, hashes the original tile bytes with SHA-256, and checks each matching occurrence byte for byte. The counts cover the full sprite region, including non-fighter art. Palette selection, mirroring and visual similarity are outside the exact-byte comparison. [MAME 0.289 Neo Geo sprite decoder](https://github.com/mamedev/mame/blob/mame0289/src/mame/snk/neogeo_spr.cpp#L610-L655)

**Português (Brasil).** As regiões C completas têm **59.291 hashes distintos de tiles não zerados em comum**, dos quais **47.213** aparecem em um único endereço em cada jogo. Eles cobrem **18,68%** das posições de tiles não zerados no KOF 2003 e **14,83%** no SVC Chaos. Cada posição é um tile 16×16 alinhado, com 4 bits por pixel e 128 bytes. A comparação exclui os tiles inteiramente zerados, calcula o SHA-256 sobre os bytes originais de cada tile e confere byte a byte cada ocorrência correspondente. As contagens cobrem a região inteira de sprites, inclusive arte que não pertence a lutadores. Seleção de paleta, espelhamento e semelhança visual ficam fora da comparação exata de bytes. [Decodificador de sprites Neo Geo do MAME 0.289](https://github.com/mamedev/mame/blob/mame0289/src/mame/snk/neogeo_spr.cpp#L610-L655)

| Set / Conjunto | Tile slots / Posições de tiles | All-zero slots / Posições zeradas | Distinct nonzero hashes / Hashes distintos não zerados | Nonzero slots with a match / Posições não zeradas com correspondência |
| --- | ---: | ---: | ---: | ---: |
| `kof2003` Export | 524,288 | 2,399 | 459,869 | 97,500 |
| `svc` | 524,288 | 1,916 | 482,988 | 77,442 |

| Validated input under `private/work/decryption-mame/results/` / Entrada validada nessa pasta | Bytes | SHA-256 |
| --- | ---: | --- |
| `kof2003-mame/sprites.bin` | 67,108,864 | `43c984c9332c9f641d3ab08731508c8c0d4efc28bf842d0cf4abbd8449f7a09e` |
| `svc-assets-mame/sprites.bin` | 67,108,864 | `885b32972c296fdeabaf8e8e4cfbb327fd65228e9326251f6a107e59a5cfcb8c` |

### Fighter attribution and anchors / Atribuição a lutadores e âncoras

**English.** MAME 0.289 with the `euro` BIOS provided the tile IDs from the linked Neo Geo sprite columns of the selected player-one fighter during the first round. Four frame samples per game cover the intro and idle poses, with extra idle samples for Kyo and Kim. Exact tiles were observed on the same fighter in both games for Iori, Terry, Ryo, Kim and Mai. For Kyo, some sampled hashes occur in the other game's full C region, but none was observed on Kyo in both samples. The counts cover the sampled poses of the six Shared Characters and leave the full move and sprite inventory open. [MAME 0.289 sprite column and tile addressing](https://github.com/mamedev/mame/blob/mame0289/src/mame/snk/neogeo_spr.cpp#L292-L359)

**Português (Brasil).** No MAME 0.289 com o BIOS `euro`, os IDs dos tiles vieram das colunas encadeadas de sprites Neo Geo do lutador selecionado pelo jogador 1 durante o primeiro round. Quatro quadros por jogo cobrem poses de entrada e de espera, com quadros adicionais de espera para Kyo e Kim. Foram observados tiles idênticos no mesmo lutador nos dois jogos para Iori, Terry, Ryo, Kim e Mai. Para Kyo, alguns hashes amostrados aparecem na região C completa do outro jogo, mas nenhum foi observado no Kyo das duas amostras. As contagens se limitam às amostras dos seis personagens compartilhados e deixam em aberto o inventário completo de golpes e sprites. [Endereçamento de colunas e tiles no MAME 0.289](https://github.com/mamedev/mame/blob/mame0289/src/mame/snk/neogeo_spr.cpp#L292-L359)

| Fighter / Lutador | KOF 2003 sampled distinct hashes / Hashes distintos amostrados | SVC sampled distinct hashes / Hashes distintos amostrados | KOF sample in all of SVC / Amostra KOF no SVC inteiro | SVC sample in all of KOF / Amostra SVC no KOF inteiro | Same-fighter overlap / Em comum no mesmo lutador |
| --- | ---: | ---: | ---: | ---: | ---: |
| Kyo Kusanagi | 233 | 253 | 10 | 211 | 0 |
| Iori Yagami | 107 | 95 | 107 | 95 | 28 |
| Terry Bogard | 90 | 70 | 20 | 16 | 7 |
| Ryo Sakazaki | 48 | 78 | 48 | 78 | 25 |
| Kim Kaphwan | 297 | 132 | 297 | 132 | 60 |
| Mai Shiranui | 89 | 94 | 89 | 94 | 31 |

Addresses are hexadecimal **tile ID / byte offset** in the decrypted C region (`offset = tile ID × 0x80`). Each paired anchor appears exactly once per game. Kyo has one independently observed anchor per game. / _Os endereços são **ID do tile / deslocamento em bytes** em hexadecimal na região C descriptografada (`deslocamento = ID × 0x80`). Cada âncora pareada aparece uma única vez por jogo. Kyo tem uma âncora observada separadamente em cada jogo._

| Anchor / Âncora | KOF 2003 | SVC Chaos | Tile SHA-256 / SHA-256 do tile |
| --- | --- | --- | --- |
| C region example / Exemplo da região C | `0x00002 / 0x0000100` | `0x00002 / 0x0000100` | `52752faed2890a6f5ab408a118ed86113aecc3ead6ca14527a627bcfd45bb92c` |
| Iori | `0x60b16 / 0x3058b00` | `0x0d405 / 0x06a0280` | `cdf105c64a453baf80187c24762ff4fb6ea16e19845f5518604bd7c290d43475` |
| Terry | `0x1917e / 0x0c8bf00` | `0x1dfbe / 0x0efdf00` | `13ec732b655892edd6181574d8bd73dbfb003cdcf4a2fb9f64eb19e266ab1387` |
| Ryo | `0x23a59 / 0x11d2c80` | `0x1bee0 / 0x0df7000` | `b0132d4443249b94490a03717fd498db17af2c87328a13f1d9011f20a6829f41` |
| Kim | `0x2a18f / 0x150c780` | `0x24fc0 / 0x127e000` | `312d9ebd66bc0b607fccdde709ac09067ddbd67bb44e996ae1712392cb70942d` |
| Mai | `0x4142c / 0x20a1600` | `0x20803 / 0x1040180` | `fc39cf99ca23f78a94fa5102bf1b9e3db5a4237892d1885078b5b4b43b7a3f13` |
| Kyo (KOF 2003) | `0x5de00 / 0x2ef0000` | — | `3c1d993375de6874b9804597a3f993ebf7cc0efa04c0373ac249731f7189e487` |
| Kyo (SVC Chaos) | — | `0x19a51 / 0x0cd2880` | `d8d26fa72416b0fa862f7cd320bf671317207cd312cc2ff47901690056bfece9` |

### Reproduction / Reprodução

**English.** Run from the repository root with Python 3.11.9. The first command verifies and compares the two existing C regions from [Decryption with existing tools](06-decryption-existing-tools.md). The next two reproduce the fighter counts using MAME 0.289 at `~/MAME/mame.exe` and the existing private cart and BIOS ZIPs. The local Lua helper and the captured tile addresses stay under `private/work/decryption-mame/`.

**Português (Brasil).** Execute na raiz do repositório com Python 3.11.9. O primeiro comando verifica e compara as duas regiões C já obtidas em [Decryption with existing tools](06-decryption-existing-tools.md). Os dois seguintes reproduzem as contagens dos lutadores com o MAME 0.289 em `~/MAME/mame.exe` e os ZIPs privados já existentes dos cartuchos e do BIOS. O auxiliar Lua local e os endereços de tiles capturados ficam em `private/work/decryption-mame/`.

```powershell
python private/work/decryption-mame/shared_art.py
python private/work/decryption-mame/run_shared_art.py
python private/work/decryption-mame/shared_art.py --fighters
```

## Owner follow-up / Complemento do dono do repositório

**English.** Use separate sprite anchors for SVC Chaos Kyo and KOF 2003 Kyo when correlating their animations. The owner observed that SVC Kyo visually combines traits of Kyo and Kusanagi from KOF 2003.

**Português (Brasil).** Use âncoras de sprite próprias para o Kyo do SVC Chaos e para o Kyo do KOF 2003 ao correlacionar as animações. O dono do repositório observou que o Kyo do SVC parece combinar traços visuais de Kyo e Kusanagi do KOF 2003.

**English.** The owner observed substantial differences between the two versions of Terry. The seven exact matches identify individual tiles in the sampled poses. Animation and moveset correspondence remain open.

**Português (Brasil).** O dono do repositório observou diferenças marcantes entre as duas versões do Terry. As sete correspondências exatas identificam tiles individuais nas poses amostradas. A correspondência de animações e golpes segue em aberto.
