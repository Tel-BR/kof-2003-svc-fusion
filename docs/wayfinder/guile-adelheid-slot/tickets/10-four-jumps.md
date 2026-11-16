---
id: 10
title: "Choose Guile's four KOF 2003 jumps"
label: wayfinder:prototype
mode: HITL
status: open
assignee:
blocked_by: [05]
research:
---

## Question

KOF 2003 has the hop, the jump, the super jump and the hyper hop, each with its own height and duration. Which of Guile's SVC jump animations serves each one, and how is it retimed? Show the candidates from MAME captures kept in `private/`.

_PT-BR: O KOF 2003 tem pulinho, pulo, super pulo e hiper pulinho, cada um com altura e duração próprias. Qual animação de pulo do Guile no SVC serve para cada um e como é reajustada no tempo? Mostrar as opções a partir de capturas do MAME guardadas em `private/`._

## Notes

- [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md): SVC Guile has one jump arc (height 90, 33 frames in the air) in neutral, forward and back versions; short taps give the same jump, and the Big Jump only lengthens forward travel. Every KOF 2003 jump will reuse these records at other timings and heights.
- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) measured all four KOF 2003 jumps as separate states (hop `$0E`/`$0F`, jump `$0B`–`$0D`, super jump `$14`/`$15`, hyper hop `$11`/`$13`), so the hyper hop exists even though SNK's system page does not list it. Their heights and durations were not measured.

_PT-BR: o Guile do SVC tem um único arco de pulo (altura 90, 33 quadros no ar), em três direções; toques curtos dão o mesmo pulo e o Big Jump só aumenta a distância. A pesquisa 01 mediu os quatro pulos do KOF 2003 como estados distintos, então o hiper pulinho existe, embora a página da SNK não o liste. Alturas e durações do KOF 2003 não foram medidas._
