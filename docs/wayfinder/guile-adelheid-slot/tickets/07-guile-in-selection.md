---
id: 07
title: "Choose how Guile is reached in the selection screen"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
blocked_by: [02, 06, 22]
research:
---

## Question

Guile now gets a new fighter ID, not Adelheid's `$22` (see [Choose how fighter slots are found for the SVC Exclusive Characters](06-slot-strategy.md)). [How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md) found a 39-cell table of 6 bytes (X, Y, ID) with the grid drawn as one fixed image and no hidden rows, and a hide rule for the label and portrait that applies only to `$22`-`$24`. How does a player reach Guile through the game's own selection flow while every original fighter stays available: a new cell in the table and the grid image, a code, or another route the research exposes? The answer must also work for the next SVC fighters.

_PT-BR: O Guile agora recebe um ID novo, não o `$22` da Adelheid (ticket 06). A pesquisa 02 achou uma tabela de 39 células de 6 bytes (X, Y, ID), com a grade desenhada como uma imagem fixa sem linhas ocultas, e uma regra que esconde nome e retrato só para `$22`-`$24`. Como o jogador chega ao Guile pelo fluxo de seleção do próprio jogo, mantendo todos os lutadores originais: uma célula nova na tabela e na imagem da grade, um código ou outro caminho que a pesquisa revelar? A resposta também precisa servir para os próximos lutadores do SVC._

**Owner update (2026-11-16).** For now the owner wants 4 imported fighters. The final layout is left for later: imported fighters may form teams, and the selection screen may be recreated for widescreen. Those are recorded as possibilities, not decided. So this ticket decides only the cheapest, reversible way to reach the first 4 fighters, and must not close the door on those later options.

_PT-BR: **Atualização do dono (16/11/2026).** Por enquanto o dono quer 4 lutadores importados. O desenho final fica para depois: os importados podem formar times e a tela de seleção pode ser recriada para widescreen. Isso fica registrado como possibilidade, não decidido. Este ticket decide só o jeito mais barato e reversível de chegar aos 4 primeiros, sem fechar as portas dessas opções futuras._
