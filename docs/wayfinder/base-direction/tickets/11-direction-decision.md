---
id: 11
title: "Direction decision"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: codex
blocked_by: [03, 04, 05, 08, 10]
research:
---

## Question

Given these results, which game is the Base Game? Is the measurement enough, or is the conversion prototype in both directions needed?

_PT-BR: com esses resultados, qual jogo é o jogo base? A medição basta, ou é preciso o protótipo nos dois sentidos?_

## Notes

Resolving this ticket reaches the map's destination; record the reasoning in an ADR (`docs/adr/`), since the choice is hard to reverse.

_PT-BR: resolver este ticket alcança o destino do mapa; registrar a justificativa numa ADR (`docs/adr/`), já que a escolha é difícil de reverter._

## Resolution

**English.** The owner approved KOF 2003 as the Base Game for the first milestone, with one SVC exclusive as the first Imported Character. The native KOF 2003 result is enough to choose the initial direction. Measure reusable and manual work during the first import, then use a small reverse conversion test on a working SVC reference to compare both directions before expanding the roster. [Decision record](../../../adr/0001-kof-2003-base-for-first-import.md)

**Português (Brasil).** O dono aprovou KOF 2003 como jogo base do primeiro marco, com um exclusivo do SVC como primeiro personagem importado. O resultado nativo do KOF 2003 basta para escolher a direção inicial. Medir o trabalho reaproveitável e o manual durante a primeira importação. Depois, usar um teste pequeno de conversão no sentido inverso, com uma execução funcional do SVC como referência, para comparar os dois sentidos antes de ampliar o elenco. [Registro da decisão](../../../adr/0001-kof-2003-base-for-first-import.md)
