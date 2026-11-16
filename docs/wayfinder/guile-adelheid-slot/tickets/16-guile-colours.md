---
id: 16
title: "Choose Guile's four KOF 2003 colours"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: owner
blocked_by: []
research:
---

## Question

KOF 2003 gives every fighter four colour tables, picked by bits 6–7 of the team slot from buttons A, B, C and D. Each holds the index of 16 consecutive palettes (Adelheid: `$980`, `$990`, `$9A0`, `$9B0`, 64 palettes in all), loaded into hardware palettes `$10`–`$1F` for Player 1's first fighter. When the other team already has the same fighter in the same colour, bit 7 is flipped (A↔B, C↔D). Guile's SVC data on MVS has 2 distinct colour sets (A = C, B = D) of 8 palette slots each, `$10`–`$17`, four of them differing between the sets, plus two more blocks that repeat them except colour 0 and two entries. Sources: [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md), [How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md), [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md).

Which SVC set goes to each of KOF 2003's four buttons, where the other two colours come from (repeated, recoloured, or another source), and how Guile's 8 SVC slots fill KOF 2003's 16? The selection portrait and order-strip palettes follow the ID separately and belong to [Choose how Guile's SVC portrait and HUD icon fit KOF 2003](12-portrait-and-icon.md).

_PT-BR: o KOF 2003 dá a cada lutador quatro tabelas de cor, escolhidas pelos bits 6–7 da vaga a partir dos botões A, B, C e D. Cada uma guarda o índice de 16 paletas seguidas (Adelheid: `$980`, `$990`, `$9A0`, `$9B0`, 64 paletas no total), carregadas nas paletas de hardware `$10`–`$1F` do primeiro lutador do jogador 1. Se a outra equipe já tem o mesmo lutador na mesma cor, o bit 7 é invertido (A↔B, C↔D). No MVS, o Guile do SVC tem 2 conjuntos de cores distintos (A = C, B = D), de 8 slots cada, `$10`–`$17`, quatro deles diferentes entre os conjuntos, além de dois blocos que os repetem, exceto a cor 0 e duas entradas. Qual conjunto do SVC vai para cada botão do KOF 2003, de onde vêm as outras duas cores (repetidas, recoloridas ou outra fonte) e como os 8 slots do Guile preenchem os 16 do KOF 2003? As paletas do retrato e da faixa da ordem seguem o ID à parte e ficam com o ticket 12._

## Resolution

**Guile's colours C and D are clones of his SVC colours A and B, with subtle, safe palette changes so they do not look bad; this is the import rule for every SVC fighter.** The owner (2026-11-16) set it as a rule, not a Guile-only choice. Buttons A and B take the two SVC colour sets as they are, and C and D start from copies of them. What "subtle and safe" means in practice (how far colours may move, and which entries stay fixed, such as outlines and skin) and how Guile's 8 SVC palette slots fill KOF 2003's 16 are details for the plan, listed under Not yet specified on the map.

**PT-BR**

**As cores C e D do Guile são clones das cores A e B do SVC, com mudanças sutis e seguras de paleta para não ficarem feias; esta é a regra de importação de todo lutador do SVC.** O dono (16/11/2026) definiu como regra, não como escolha só do Guile. Os botões A e B recebem os dois conjuntos de cores do SVC como estão, e C e D partem de cópias deles. O que significa "sutil e seguro" na prática (quanto as cores podem variar e quais entradas ficam fixas, como contorno e pele) e como os 8 slots de paleta do Guile no SVC preenchem os 16 do KOF 2003 são detalhes do plano, listados em "Not yet specified" no mapa.
