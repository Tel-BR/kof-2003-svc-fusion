---
label: wayfinder:map
title: "Map: KOF 2003 and SVC Chaos Versus fusion"
status: open
---

# Map: KOF 2003 and SVC Chaos Versus fusion

## Destination

Define the scope and acceptance criteria for a future local Versus mode. Every playable fighter and stage from both games is available under either ruleset. Both versions of each Shared Character can be selected in either mode. Before each fight, the players choose one Base Game whose original rules govern both sides. SVC uses 1v1 and KOF 2003 uses team play.

_PT-BR: definir o escopo e os critérios de aceitação de um futuro modo Versus local. Todos os lutadores jogáveis e cenários dos dois jogos ficam disponíveis sob qualquer um dos conjuntos de regras. As duas versões de cada personagem compartilhado podem ser selecionadas em qualquer modo. Antes de cada luta, os jogadores escolhem um jogo base cujas regras originais valem para os dois lados. O SVC usa 1x1 e o KOF 2003 usa equipes._

## Notes

- The owner confirmed the destination above. Local Versus is the first mode for the fusion. Use the [project glossary](../../../GLOSSARY.md).
- [Direction decision](../base-direction/tickets/11-direction-decision.md) chose KOF 2003 for the first import. Before expanding the roster, compare the measured work from that import with a small conversion in the reverse direction using a working SVC reference. In the future Versus mode, the Base Game is chosen for each fight.
- The current evidence covers a [native KOF 2003 test](../base-direction/tickets/09-run-kof2003-port.md) and an [interpreted SVC round with missing graphics](../base-direction/tickets/10-svc-native-cost.md). A proof that uses both rulesets depends on having a working implementation of each.
- Record the acceptance criteria here through the decision tickets. The implementation spec follows the map. Keep game data and experimental outputs under `private/`.

_PT-BR:_

- _O dono confirmou o destino acima. Versus local é o primeiro modo da fusão. Use o [glossário do projeto](../../../GLOSSARY.md)._
- _[Direction decision](../base-direction/tickets/11-direction-decision.md) definiu KOF 2003 para a primeira importação. Antes de ampliar o elenco, compare o trabalho medido nessa importação com um teste pequeno no sentido inverso, usando uma execução funcional do SVC como referência. No futuro Versus, o jogo base é escolhido para cada luta._
- _A evidência atual cobre um [teste nativo do KOF 2003](../base-direction/tickets/09-run-kof2003-port.md) e um [round interpretado do SVC com gráficos ausentes](../base-direction/tickets/10-svc-native-cost.md). Uma prova com os dois conjuntos de regras depende de ter uma implementação funcional de cada um._
- _Registre os critérios de aceitação pelos tickets de decisão. A especificação de implementação vem depois do mapa. Mantenha os dados dos jogos e as saídas de experimentos em `private/`._

## Decisions so far

<!-- Add one linked entry per resolved ticket. The confirmed destination is recorded above. -->

## Not yet specified

- Which adaptations can be shared across Imported Characters and which need to be defined per version or ruleset. The first cross-game fight will inform this.
- Which stage behaviors require adaptation in the other game. A test with a stage in each direction will inform this.

_PT-BR:_

- _Quais adaptações podem ser reaproveitadas entre personagens importados e quais precisam ser definidas por versão ou conjunto de regras. A primeira luta com conteúdo dos dois jogos vai ajudar a responder._
- _Quais comportamentos dos cenários exigem adaptação no outro jogo. Um teste com um cenário em cada sentido vai ajudar a responder._

## Out of scope

- Arcade progression and endings, online play, and implementation. / _Progressão e finais do Arcade, jogo online e implementação._
