---
id: 12
title: "Choose how Guile's SVC portrait and HUD icon fit KOF 2003"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: [02, 05]
research:
---

## Question

The owner wants Guile's own SVC portrait and HUD icon. [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md) found that SVC has neither for Guile: it offers a 4-tile (32×32 px) grid icon, a full-body figure drawn with his fighter sprites, and an animated 80×96 px pre-fight dialogue face. KOF 2003 looks up by ID a portrait (two 7×8-tile layers), a name label, a team-slot icon, an order-select strip and a fix-layer HUD name, and blanks the label and portrait for `$22` ([How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md)). Which SVC art stands in for each KOF 2003 element, how is it fitted to KOF 2003's sizes, tile layout and palette slots (scaled, cropped, re-laid in tiles), what fills an element no SVC art fits, and which differences are accepted?

_PT-BR: O dono quer o retrato e o ícone de placar do próprio Guile no SVC. A pesquisa 05 viu que o SVC não tem nenhum dos dois para o Guile: tem um ícone de grade de 4 tiles (32×32 px), uma figura de corpo inteiro feita com os sprites de luta e um rosto animado de 80×96 px no diálogo antes da luta. O KOF 2003 busca por ID um retrato (duas camadas de 7×8 tiles), um nome, um ícone da vaga, uma faixa da ordem e o nome do placar na camada fixa, e esconde nome e retrato para `$22` (pesquisa 02). Qual arte do SVC faz o papel de cada elemento do KOF 2003, como se ajusta aos tamanhos, tiles e paletas (redimensionada, recortada, remontada), o que preenche um elemento que nenhuma arte do SVC cobre, e quais diferenças são aceitas?_

## Notes

- The two research notes disagree on KOF 2003's match HUD: [How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md) saw only fix-layer names (frame 5,400), while [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md) reported small face icons under each life bar in a KOF 2003 capture. Check which elements the HUD really has before choosing.
- The HUD name table at `$6EA9E` already holds "ADEL" for `$22`; a "GUILE" name needs new fix-layer tiles.
- Portrait palettes look like 28+2·ID (two samples) and order-strip palettes 20+2·ID (nine cases).
- The map's Destination names "Guile's SVC portrait and HUD icon", which SVC does not have as such; the resolution of this ticket may reword it, with the owner.

_PT-BR: as duas pesquisas divergem sobre o placar do KOF 2003: a 02 viu só nomes na camada fixa, a 05 relatou pequenos rostos sob as barras de vida numa captura; conferir antes de decidir. A tabela de nomes do placar já tem "ADEL" para `$22`; "GUILE" exige tiles novos na camada fixa. O Destino do mapa fala em "retrato e ícone de placar do Guile no SVC", que o SVC não tem como tal; a resolução deste ticket pode reescrevê-lo, com o dono._

## Resolution

Decided with the owner on 2026-11-16, looking at KOF 2003's selection and order screens next to SVC's captures (in `private/`; nothing from them is in the repository).

**The match HUD has no face icons.** In a KOF 2003 match capture the HUD shows life bars, timer, player name text and small "CHANGE OK" stock markers in the bottom corners; no faces under the bars. So there is no "HUD icon" to fill: the name in the match HUD is fix-layer text from the table at `$6EA9E`. The map's Destination, which named a "portrait and HUD icon", is reworded.

**Elements and their art.**
- **Large portrait** (two 7×8-tile layers, 56×64 px): a **crop of 56×64 px from Guile's SVC pre-fight dialogue face** (80×96, animated), one still frame, **not scaled**, so the pixels stay sharp. The edges and the animation are lost; if the frame uses more colours than a layer's 15 plus transparent, it is reduced.
- **Order-select strip** (2×7 tiles): cropped from the same portrait.
- **Team-slot icon** (the small square face shown at the bottom of the selection screen for each picked member): Guile's **4-tile 32×32 grid icon from SVC**. The exact size of KOF 2003's icon box was not measured and must be checked before implementation.
- **Name label** (7×1 tiles) and **match HUD name** (fix layer): **KOF 2003's own letters**, with new tiles only for a letter the font lacks.
- **Grid thumbnail**: none for now, as decided in [07](07-guile-in-selection.md).
- Nothing is left without art, so no placeholder is needed.

**Accepted differences.** The portrait is a still and cropped; colours may be reduced to fit KOF 2003's palette layout (portrait palettes `28+2·ID`, order strips `20+2·ID`); the name looks like KOF 2003's, not SVC's.

**Left open for implementation.** Which still frame of the dialogue face, the exact crop window, the palette reduction, and the size of the team-slot icon box.

**PT-BR**

Decidido com o dono em 16/11/2026, olhando as telas de seleção e de ordem do KOF 2003 ao lado das capturas do SVC (ficam em `private/`; nada delas está no repositório).

**O placar da luta não tem rostos.** Numa captura de luta do KOF 2003 o placar mostra barras de vida, relógio, texto com o nome do jogador e pequenos marcadores "CHANGE OK" nos cantos de baixo; nenhum rosto sob as barras. Então não há "ícone de placar" a preencher: o nome no placar é texto da camada fixa vindo da tabela em `$6EA9E`. O Destino do mapa, que falava em "retrato e ícone de placar", foi reescrito.

**Elementos e arte.**
- **Retrato grande** (duas camadas de 7×8 tiles, 56×64 px): um **recorte de 56×64 px do rosto de diálogo do Guile no SVC antes da luta** (80×96, animado), um quadro parado, **sem escalar**, para manter os pixels nítidos. Perdem-se as bordas e a animação; se o quadro usar mais cores que as 15 de uma camada mais transparente, elas são reduzidas.
- **Faixa da ordem** (2×7 tiles): recortada do mesmo retrato.
- **Ícone da vaga do time** (o rosto quadrado pequeno que aparece embaixo na tela de seleção para cada membro escolhido): o **ícone de grade de 4 tiles, 32×32, do Guile no SVC**. O tamanho exato da caixa do ícone no KOF 2003 não foi medido e deve ser conferido antes de implementar.
- **Nome** (7×1 tiles) e **nome no placar** (camada fixa): **letras do próprio KOF 2003**, com tiles novos só para uma letra que a fonte não tenha.
- **Miniatura da grade**: nenhuma por ora, como decidido no [07](07-guile-in-selection.md).
- Nada fica sem arte, então não é preciso um substituto.

**Diferenças aceitas.** O retrato é um quadro parado e recortado; as cores podem ser reduzidas para caber na paleta do KOF 2003 (paletas de retrato `28+2·ID`, faixas da ordem `20+2·ID`); o nome tem a cara do KOF 2003, não a do SVC.

**Em aberto para a implementação.** Qual quadro parado do rosto, a janela exata do recorte, a redução de paleta e o tamanho da caixa do ícone da vaga.
