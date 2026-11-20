---
id: 34
title: "Choose what Guile's Exceed super becomes in KOF 2003"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: []
research:
---

## Question

SVC Chaos gives Guile the Sonic Hurricane as an Exceed super. KOF 2003 has no Exceed: it uses whole stocks, with a limit of 3 to 5, and the Leader Super that only the team leader can use ([research](../../../specs/first-svc-character-import/research-guile-svc.md)). Guile's other supers fit one KOF 2003 stock each, so only this one has nowhere obvious to go. What does the Sonic Hurricane become in KOF 2003: a Leader Super, an ordinary one-stock super, or nothing in this import?

_PT-BR: o SVC Chaos dá ao Guile o Sonic Hurricane como golpe de Exceed. O KOF 2003 não tem Exceed: usa estoques inteiros, com limite de 3 a 5, e o Leader Super, que só o líder da equipe usa. Os outros supers do Guile cabem em um estoque cada, então só esse fica sem lugar óbvio. No que o Sonic Hurricane se transforma no KOF 2003: Leader Super, super comum de um estoque, ou nada nesta importação?_

## Notes

- The voice record of the Exceed is already identified: `0x04FB1C`, confirmed in the owner's MAME run ([33](33-confirm-voice-roles-in-mame.md)).
- Special moves and supers are out of scope for this map; it decides only what the Exceed becomes, so the moveset ticket of the spec inherits a decided target.
- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.

## Resolution

**Owner decision, 2026-11-20: the Sonic Hurricane becomes a Leader Super.**

Consequences. The move comes out only when Guile leads the team, which is the shape KOF 2003 already has for a fighter's strongest move, so no new system is invented and the Exceed gauge is not recreated. Guile without the leader position has the supers that fit one stock each and nothing else. The restriction is the price of keeping the move as the rare one it is in SVC.

Still open, to be measured when the moveset slice runs (spec ticket 05), not here: what a Leader Super costs in stocks in KOF 2003, and whether a fighter is marked as having one in data or in code. Whether every other SVC Exclusive Character's Exceed also becomes a Leader Super is not decided: this ticket decides Guile, and the second Exceed returns to the owner.

_PT-BR: **decisão do dono, 20/11/2026: o Sonic Hurricane vira Leader Super.**_

_Consequências: o golpe só sai quando o Guile for líder da equipe, que é a forma que o KOF 2003 já tem para o golpe mais forte de um lutador, então nenhum sistema novo é inventado e a barra de Exceed não é recriada. Fora da liderança, o Guile fica com os supers que cabem em um estoque cada e nada além. A restrição é o preço de manter o golpe tão raro quanto ele é no SVC._

_Em aberto, para medir quando a fatia do repertório rodar (ticket 05 do spec), não aqui: quanto custa um Leader Super em estoques no KOF 2003 e se um lutador é marcado como tendo um em dado ou em código. Se o Exceed de todo outro Personagem Exclusivo do SVC também vira Leader Super não está decidido: este ticket decide o Guile, e o segundo Exceed volta ao dono._
