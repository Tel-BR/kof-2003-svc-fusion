---
id: 12
title: "Choose how Guile's SVC portrait and HUD icon fit KOF 2003"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
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
