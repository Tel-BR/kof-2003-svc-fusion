---
id: 18
title: "How KOF 2003's sprite-frame records number their tiles"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/18-sprite-frame-tiles:docs/wayfinder/guile-adelheid-slot/research/18-sprite-frame-tiles.md
---

## Question

[How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) decoded the sprite-frame directory (file `$200000`) only in part. The renderer reads, per column, a long start tile with bits 16–19 in the high word's low nibble and a row-mask word, and numbers tiles consecutively (`$0F971E`–`$0F9770`). Walking Adelheid's 335 animations with a 6-byte column layout gave tile numbers above `$7FFFF`, so the layout is not settled, and her complete tile range is open (1,592 tiles observed in `$68032`–`$6933C`). [How many fighter IDs KOF 2003's tables hold and how much free space its files have](03-slot-capacity.md) left open whether frame data can carry a tile number with bit 19 set.

What is the layout of a sprite-frame record (header words, columns, the extra layers from `+$72` and `+$80`, flips)? What are Adelheid's complete tile range and distinct tile count across all 335 animations? Can the frame data and the 68000 drawing path carry tile numbers of `$80000` and above? On the SVC side, what is the union of distinct body tiles Guile draws across the test runs of [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md), against the 756 observed and the block of about 9,100? Record addresses, sizes and counts only.

_PT-BR: a pesquisa 01 decodificou só em parte o diretório de quadros de sprite (arquivo `$200000`). Por coluna, o renderizador lê um tile inicial longo, com os bits 16–19 no nibble baixo da palavra alta, e uma palavra de máscara de linhas, e numera os tiles em sequência (`$0F971E`–`$0F9770`). Percorrer as 335 animações da Adelheid com colunas de 6 bytes deu tiles acima de `$7FFFF`, então o formato não está fechado, e a faixa completa de tiles dela segue aberta (1.592 tiles observados em `$68032`–`$6933C`). A pesquisa 03 deixou em aberto se os dados de quadro aceitam um tile com o bit 19 ligado. Qual é o formato de um registro de quadro (palavras de cabeçalho, colunas, as camadas extras de `+$72` e `+$80`, espelhamentos)? Qual é a faixa completa e a contagem de tiles distintos da Adelheid nas 335 animações? Os dados de quadro e o caminho de desenho do 68000 aceitam tiles a partir de `$80000`? No lado do SVC, qual é a união dos tiles distintos do corpo do Guile nas sessões de teste da pesquisa 05, comparada aos 756 observados e ao bloco de cerca de 9.100? Registrar só endereços, tamanhos e contagens._

## Resolution

**Record layout.** A sprite-frame record is a 4-byte header (palette offset, format, columns, rows) and a body in one of **eleven formats**, 0 to `$A`, picked by the second byte. The formats differ in how they store row masks (none, a word or a byte per column) and tiles (a run from one start tile, a word, a byte, or 3 bytes per tile). Research 01 knew only format 0 and read its start tile once per column; it comes once per frame. With all eleven decoded, the 19,034 records of the 37 fighters each end exactly where the next begins.

**Tiles at `$80000` and above: yes.** Every format has a full 4-bit field for tile bits 16–19 and none of the 44 drawing routines (`$0F971E`–`$0FA7ED`) masks it. No data uses bit 19 today; the highest tile in any directory is `$7E07D`. The native renderer masks the tile number to the next power of two of the tiles loaded, so with the 64 MiB set a tile `$80000 + n` would show tile `n`; once the set is larger, all 20 bits count and the tile cache grows from 128 to 256 MiB of RAM. This was read in the code on both sides and has not been tested by drawing such a tile.

**Adelheid.** Her 336 frames (0–335) use **7,211 tiles, one solid block `$68031`–`$69C5B`** (901 KiB). The 1,592 tiles observed earlier are all inside. Mukai's 10,481 tiles follow directly, then Maki's 7,756. The 37 fighters fill `$10000`–`$6E398` in ID order with no gap.

**Guile.** Combining the 63 recorded SVC sessions gives **2,145 distinct body tiles** inside his block (756 in one session before; the block is about 9,100). The sessions do not cover normals, specials or supers, so this is a floor for the slice. 2,145 fit in Adelheid's block; 9,100 would not. [How many tiles Guile's complete SVC frame data uses](21-guile-total-tiles.md) settles his total.

**PT-BR**

**Formato do registro.** Um registro de quadro tem 4 bytes de cabeçalho (deslocamento de paleta, formato, colunas, linhas) e um corpo em um de **onze formatos**, de 0 a `$A`, escolhido pelo segundo byte. Eles mudam a forma de guardar as máscaras de linha e os tiles. A pesquisa 01 só conhecia o formato 0 e lia o tile inicial uma vez por coluna; ele vem uma vez por quadro. Com os onze formatos, os 19.034 registros dos 37 lutadores terminam exatamente onde o próximo começa.

**Tiles a partir de `$80000`: sim.** Todos os formatos têm 4 bits inteiros para os bits 16–19 do tile, e nenhuma das 44 rotinas de desenho (`$0F971E`–`$0FA7ED`) corta esse campo. Hoje nenhum dado usa o bit 19; o tile mais alto é `$7E07D`. O renderizador nativo reduz o número do tile à próxima potência de dois dos tiles carregados: com os 64 MiB atuais, um tile `$80000 + n` mostraria o tile `n`; com um conjunto maior os 20 bits valem, e o cache de tiles passa de 128 para 256 MiB de RAM. Isso foi lido no código dos dois lados e ainda não foi testado desenhando um tile desses.

**Adelheid.** Os 336 quadros dela (0–335) usam **7.211 tiles, um bloco único de `$68031` a `$69C5B`** (901 KiB). Os 1.592 observados antes estão todos dentro. Os 10.481 tiles do Mukai vêm logo depois, e os 7.756 da Maki em seguida. Os 37 lutadores ocupam `$10000`–`$6E398` em ordem de ID, sem folga.

**Guile.** Juntando as 63 sessões gravadas do SVC aparecem **2.145 tiles distintos do corpo** dentro do bloco dele (eram 756 numa sessão; o bloco tem cerca de 9.100). As sessões não cobrem golpes normais, especiais nem supers, então é o mínimo desta fatia. 2.145 cabem no bloco da Adelheid; 9.100 não caberiam. O [ticket 21](21-guile-total-tiles.md) fecha o total dele.

Research / Pesquisa: `research/18-sprite-frame-tiles:docs/wayfinder/guile-adelheid-slot/research/18-sprite-frame-tiles.md` (commit `2eb507a`).
