---
id: 11
title: "Choose Guile's Guard Cancel attack"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: owner
blocked_by: [05]
research:
---

## Question

KOF 2003's Guard Cancel attack is the CD blowback performed while blocking. Guile's evasive and Guard Cancel rolls are decided in [Decide whether ADR 0002 holds for Guile, whose SVC break-fall is not a roll](17-adr-0002-for-guile.md). Which SVC animation becomes his Guard Cancel blowback (his SVC Guard Cancel attack, a heavy normal, or another), knowing the same animation will likely serve the plain CD blowback later?

_PT-BR: O golpe de Guard Cancel do KOF 2003 é o CD feito durante a defesa. As esquivas e a esquiva de Guard Cancel do Guile são decididas no [ticket 17](17-adr-0002-for-guile.md). Qual animação do SVC vira o CD de Guard Cancel do Guile (o golpe de Guard Cancel dele no SVC, um normal forte ou outra), sabendo que a mesma animação deve servir depois para o CD comum?_

## Notes

- [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md): Guile's SVC Guard Cancel attack (C+D in blockstun) has 15 poses over 42 frames, does no damage and pushes the opponent back 176 px.
- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): KOF 2003's Guard Cancel CD is state `$47`, action `$83`, common code; the plain CD blowback after blockstun took state `$39`.

_PT-BR: o golpe de Guard Cancel do Guile no SVC tem 15 poses em 42 quadros, não causa dano e empurra 176 px. No KOF 2003 o Guard Cancel CD é o estado `$47`, ação `$83`, código comum; o CD comum depois da defesa usou o estado `$39`._

## Resolution

**Guile's Guard Cancel blowback uses his own SVC Guard Cancel attack (C+D), and this is the import rule for SVC fighters.** The owner (2026-11-16) chose it for the same function in both games: the SVC attack is 15 poses over 42 frames, deals no damage and pushes the opponent far ([Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md)). KOF 2003 sets damage, cost and knock-back. The same animation will serve the plain CD blowback later.

**PT-BR**

**O CD de Guard Cancel do Guile usa o golpe de Guard Cancel dele no SVC (C+D), e esta é a regra de importação dos lutadores do SVC.** O dono (16/11/2026) escolheu por ser a mesma função nos dois jogos: o golpe do SVC tem 15 poses em 42 quadros, não causa dano e empurra o adversário para longe (pesquisa 05). O KOF 2003 define dano, custo e empurrão. A mesma animação servirá depois para o CD comum.
