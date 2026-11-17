---
id: 10
title: "Choose Guile's four KOF 2003 jumps"
label: wayfinder:prototype
mode: HITL
status: closed
assignee: tel
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

## Resolution

Decided with the owner on 2026-11-16, looking at frame strips of the SVC jump captured in MAME (`private/work/svc-guile/tests/run-jump-neutral` and `run-jump-forward`; nothing from them is in the repository). The strips confirm ticket 05: one arc that rises, holds a tucked pose near the top, falls and lands, the same poses in the neutral and forward versions.

**Rule.** One SVC arc serves all four KOF 2003 jumps (hop, jump, super jump, hyper hop), **retimed in height and duration**: the normal jump uses the arc as it is, the super jump is the same arc higher and longer, and the hop and hyper hop the same arc lower and shorter. The poses are the same in all four.

**Condition (owner).** The retiming must follow **when KOF 2003 changes sprites** during each of its four jumps, so the imported jump reads like a native one: the instants at which the pose changes are placed in proportion to KOF 2003's own pose changes in that jump, not simply stretched.

**Scope (owner).** This rule, like the run and backstep of [ticket 09](09-run-and-backstep.md), holds for every SVC fighter imported, not only Guile.

**Left open.** KOF 2003's own heights, durations and pose-change instants for the four jumps (states `$0E`/`$0F`, `$0B`-`$0D`, `$14`/`$15`, `$11`/`$13`) were not measured. That measurement is the same one the run and backstep need, and belongs to the implementation tickets; the existing probe tools carry SVC offsets and need the KOF 2003 ones first.

**PT-BR**

Decidido com o dono em 16/11/2026, olhando tiras de quadros do pulo do SVC capturadas no MAME (`private/work/svc-guile/tests/run-jump-neutral` e `run-jump-forward`; nada delas está no repositório). As tiras confirmam o ticket 05: um arco que sobe, mantém uma pose encolhida perto do topo, desce e pousa, com as mesmas poses nas versões neutra e para frente.

**Regra.** Um arco do SVC serve aos quatro pulos do KOF 2003 (pulinho, pulo, super pulo e hiper pulinho), **reajustado em altura e duração**: o pulo normal usa o arco como está, o super pulo é o mesmo arco mais alto e mais longo, e o pulinho e o hiper pulinho o mesmo arco mais baixo e mais curto. As poses são as mesmas nos quatro.

**Condição (dono).** O reajuste deve seguir **quando o KOF 2003 troca de sprite** em cada um dos quatro pulos, para o pulo importado parecer nativo: os instantes de troca de pose são postos em proporção às trocas do próprio KOF 2003 naquele pulo, e não só esticados.

**Alcance (dono).** Esta regra, como a corrida e o passo para trás do [ticket 09](09-run-and-backstep.md), vale para todo lutador do SVC importado, não só o Guile.

**Em aberto.** Alturas, durações e instantes de troca de pose do próprio KOF 2003 para os quatro pulos (estados `$0E`/`$0F`, `$0B`-`$0D`, `$14`/`$15`, `$11`/`$13`) não foram medidos. Essa medição é a mesma de que a corrida e o passo para trás precisam, e pertence aos tickets de implementação; as ferramentas de sonda atuais têm os deslocamentos do SVC e precisam primeiro dos do KOF 2003.
