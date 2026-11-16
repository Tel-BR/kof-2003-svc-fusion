---
id: 02
title: "How KOF 2003's selection screen maps cells and codes to fighter IDs"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/02-selection-screen:docs/wayfinder/guile-adelheid-slot/research/02-selection-screen.md
---

## Question

How does the MVS selection screen turn a cursor cell, and any built-in unlock code, into a fighter ID? Can Adelheid or Mukai be reached through any official path (codes, cheats, the AES side)? Where do the selection portrait, the HUD icon and the fighter name come from (tables, tile ranges, palette, size in tiles), and how are they looked up from the ID?

_PT-BR: Como a tela de seleção do MVS transforma uma célula do cursor, e qualquer código de liberação do próprio jogo, num ID de lutador? A Adelheid ou o Mukai podem ser alcançados por algum caminho oficial (códigos, cheats, lado AES)? De onde vêm o retrato da seleção, o ícone do placar e o nome do lutador (tabelas, faixas de tiles, paleta, tamanho em tiles), e como são buscados a partir do ID?_

## Resolution

**Cell → ID.** A 39-cell table at `$9856` (6 bytes per cell: X, Y, ID; `$FFFF` is random) maps cell `row × 3 + column` to the ID, and buttons A/B/C/D set the two colour bits. The visible grid has 11 rows (33 cells). Rows 11–12 hold Kusanagi, Adelheid, Mukai, Chizuru, Maki and a second random cell; the cursor reaches them only when the BIOS developer-mode word `$10FE80` is non-zero. Picking `$22` or `$23` ends team selection after one member (`$96FE`–`$972E`), and so does Chizuru followed by Maki.

**Official paths.** None reaches Adelheid or Mukai. The game has only two codes, which give Kusanagi (`$21`) and Chizuru (`$20`). Selection never reads the AES/MVS flag (inference; no AES BIOS was available to test). No published cheat was found. Developer mode reaches both in MAME.

**Art and names.** All selection art is animation group `$2C`, looked up by ID plus an offset: name label ID+`$1B` (7×1 tiles), portrait ID+`$49` (two 7×8-tile layers; palettes 28+2·ID, inferred from two samples), team-slot icon ID+`$6E`, order-select strip ID+`$100` (2×7 tiles; palettes 20+2·ID, confirmed in 9 cases). The code blanks the label, portrait and per-team object for `$22`–`$24`; their label, portrait and icon entries are generic placeholders, while their order strips have their own art. The grid thumbnails are one static image with one palette per cell and no hidden rows. The match HUD name is fix-layer text from a per-ID table at `$6EA9E`, which already holds "ADEL" for `$22`.

**PT-BR**

**Célula → ID.** Uma tabela de 39 células em `$9856` (6 bytes por célula: X, Y, ID; `$FFFF` é aleatório) associa a célula `linha × 3 + coluna` ao ID, e os botões A/B/C/D definem os dois bits de cor. A grade visível tem 11 linhas (33 células). As linhas 11–12 têm Kusanagi, Adelheid, Mukai, Chizuru, Maki e um segundo aleatório; o cursor só chega a elas quando a palavra de modo desenvolvedor da BIOS, `$10FE80`, é diferente de zero. Escolher `$22` ou `$23` fecha a equipe com um só membro (`$96FE`–`$972E`), e o mesmo vale para Chizuru seguida de Maki.

**Caminhos oficiais.** Nenhum leva à Adelheid ou ao Mukai. O jogo só tem dois códigos, que dão Kusanagi (`$21`) e Chizuru (`$20`). A seleção não consulta o modo AES/MVS (inferência; não havia BIOS AES para testar). Nenhum cheat publicado foi encontrado. O modo desenvolvedor libera os dois no MAME.

**Arte e nomes.** Toda a arte da seleção é o grupo de animações `$2C`, buscado por ID mais um deslocamento: nome ID+`$1B` (7×1 tiles), retrato ID+`$49` (duas camadas de 7×8 tiles; paletas 28+2·ID, inferido de duas amostras), ícone da vaga ID+`$6E`, faixa da ordem ID+`$100` (2×7 tiles; paletas 20+2·ID, confirmado em 9 casos). O código esconde nome, retrato e o objeto por equipe para `$22`–`$24`; as entradas de nome, retrato e ícone deles são marcadores genéricos, mas as faixas da ordem têm arte própria. As miniaturas da grade são uma imagem fixa, com uma paleta por célula e sem as linhas ocultas. O nome no placar da luta é texto da camada fixa, de uma tabela por ID em `$6EA9E`, que já tem "ADEL" para `$22`.

Research / Pesquisa: `research/02-selection-screen:docs/wayfinder/guile-adelheid-slot/research/02-selection-screen.md` (commit `62dbb19`).
