---
id: 35
title: "Choose which charge rule Guile uses in KOF 2003"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: []
research:
---

## Question

Guile's moves are charge moves, and KOF 2003 already has a charge fighter in Ash. Which charge rule does Guile follow once imported: KOF 2003's usual one (hold back or down, as Ash does), or the one his SVC version uses?

_PT-BR: os golpes do Guile são de carga, e o KOF 2003 já tem um lutador de carga no Ash. Qual regra de carga o Guile segue depois de importado: a usual do KOF 2003 (segurar trás ou baixo, como o Ash), ou a da versão dele no SVC?_

## Notes

- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.

## Resolution

**Owner decision and correction, 2026-11-20.** Guile's special moves follow the same charge rule as Ash, which is KOF 2003's usual one, so nothing has to be adapted to make the specials feel like the rest of the roster.

The owner also corrected the premise this question carried. An earlier note said SVC's charge rule works from a neutral position and so differs from SNK's usual command ([research](../../../specs/first-svc-character-import/research-guile-svc.md)). The owner tested it: **Guile does not charge from neutral.** In his specials he plays like Ash. What is distinctive is his **charge supers**, and that difference is not yet written down anywhere in this repository.

**When the charge supers become due (owner, 2026-11-20).** Not in this slice: the seven phases of [ticket 04](../../../specs/first-svc-character-import/issues/04-complete-first-imported-match.md) carry no special moves and no supers, so nothing before the moveset slice ([ticket 05](../../../specs/first-svc-character-import/issues/05-validate-imported-moveset.md)) depends on how Guile's charge supers behave. The description stays pending until that slice opens, and it is an input to it, not a blocker now.

Consequences: the specials inherit Ash's rule with no adaptation and no new code. The charge supers are the only part still to be described, which belongs to the moveset slice (spec ticket 05); until the owner describes them, or a MAME reading measures them, no ticket may assume they behave like Ash's. The wrong sentence in the research note is corrected rather than left to mislead a later reader.

_PT-BR: **decisão e correção do dono, 20/11/2026.** Os especiais do Guile seguem a mesma regra de carga do Ash, que é a usual do KOF 2003, então nada precisa ser adaptado para os especiais parecerem com os do resto do elenco._

_O dono também corrigiu a premissa que esta pergunta carregava. Uma nota anterior dizia que a regra de carga do SVC funciona a partir da posição neutra e por isso diferia do comando usual da SNK. O dono testou: **o Guile não carrega em posição neutra.** Nos especiais ele joga como o Ash. O que é bem exclusivo são os **supers de carga** dele, e essa diferença ainda não está escrita em lugar nenhum deste repositório._

_**Quando os supers de carga entram (dono, 20/11/2026).** Não nesta fatia: as sete fases do ticket 04 não têm especiais nem supers, então nada antes da fatia do repertório (ticket 05) depende de como os supers de carga do Guile se comportam. A descrição fica pendente até aquela fatia abrir, e é entrada dela, não bloqueio de agora._

_Consequências: os especiais herdam a regra do Ash sem adaptação e sem código novo. Os supers de carga são a única parte a descrever, e isso pertence à fatia do repertório (ticket 05 do spec); até o dono descrevê-los, ou uma leitura no MAME medi-los, nenhum ticket pode supor que eles se comportam como os do Ash. A frase errada da nota de pesquisa é corrigida em vez de ficar enganando quem ler depois._
