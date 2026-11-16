---
id: 14
title: "Review ticket 04's five phases with every decision in place"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
blocked_by: [06, 07, 08, 09, 10, 11, 12, 13, 15, 16, 17, 19, 22, 23, 24]
research:
---

## Question

With every decision on this map in place, are ticket 04's five phases still the right cut? Confirm, resize, merge or split them so each phase fits one session and carries no open decision; place the new actions, the portrait and icon, the sounds and the slot strategy; and record how the effort log separates reusable from Guile-specific work. Update ticket 04 and the spec where the scope grew.

_PT-BR: Com todas as decisões do mapa tomadas, as cinco fases do ticket 04 continuam sendo o recorte certo? Confirmar, redimensionar, juntar ou dividir para que cada fase caiba numa sessão sem decisão pendente; encaixar as ações novas, retrato e ícone, sons e a estratégia de vagas; e registrar como o registro de esforço separa o reaproveitável do específico do Guile. Atualizar o ticket 04 e o spec onde o escopo cresceu._

## Notes

- [How the native port's generator handles changed or added 68000 code and data](04-port-generator.md) for the verification phase: today's `play.txt` reaches neither Guile nor Adelheid, so the profile and verify scripts for the slice are still to be chosen; `entries.txt` is merged and never pruned; the exit code is always 0; `--verify` checks only the native blocks a session runs.

_PT-BR: para a fase de verificação, o `play.txt` atual não chega ao Guile nem à Adelheid, então os roteiros de perfil e verify da fatia ainda precisam ser escolhidos; o `entries.txt` só acumula; o código de saída é sempre 0; o `--verify` só confere os blocos nativos que a sessão executa._

**Owner update (2026-11-16).** Guile gets a new ID instead of Adelheid's slot, and the graphics set grows to 128 MiB inside his slice ([Choose where Guile's tiles go in the graphics files](19-guile-tile-placement.md)). The review rewrites the spec and ticket 04, which still say Adelheid's slot, and places the growth of the graphics set and the first native drawing of a tile at `$80000` or above in the phases.

_PT-BR: **Atualização do dono (16/11/2026).** O Guile recebe um ID novo em vez da vaga da Adelheid, e os gráficos crescem para 128 MiB dentro da fatia dele. A revisão reescreve o spec e o ticket 04, que ainda dizem vaga da Adelheid, e encaixa nas fases o crescimento dos gráficos e o primeiro desenho nativo de um tile a partir de `$80000`._

The owner also agreed (2026-11-16) that the growth of the graphics set is tested on its own, before Guile is built on it; the review makes that test a phase ahead of Guile's.

_PT-BR: o dono também concordou (16/11/2026) que a ampliação dos gráficos é testada sozinha, antes de o Guile ser montado em cima dela; a revisão faz desse teste uma fase anterior às do Guile._

The rehearsal before Guile, chosen by the owner (2026-11-16): clone a complex regular fighter (the owner named Kyo or Kusanagi as examples; not Adelheid, whose jump, speed and small move set are atypical) into a new ID with its tiles in the added graphics space. It exercises the graphics growth, the relocated ID tables and a new ID with data known to work, and the clone can be checked against the original fighter with the same scripted inputs. The review makes it a phase ahead of Guile's, and takes the first target as 4 imported fighters.

_PT-BR: o ensaio antes do Guile, escolhido pelo dono (16/11/2026): clonar um lutador regular e complexo (o dono citou Kyo ou Kusanagi como exemplos; não a Adelheid, de pulo, velocidade e conjunto de golpes atípicos) num ID novo com os tiles no espaço gráfico acrescentado. Ele exercita a ampliação dos gráficos, as tabelas de ID movidas e um ID novo com dados que sabemos que funcionam, e o clone pode ser conferido contra o lutador original com as mesmas entradas por script. A revisão faz dele uma fase anterior às do Guile e toma como primeira meta 4 lutadores importados._

The owner's idea (2026-11-16): the boss rule may let Guile be tested alone, without a team, and may suit overpowered SVC fighters. After [How KOF 2003's boss selection rule works and whether a new ID can use it](22-boss-selection-rule.md), the review asks the owner whether the first imported match may be a solo match instead of a team match, which changes ticket 04's acceptance criteria and the spec.

_PT-BR: a ideia do dono (16/11/2026): a regra de chefe pode permitir testar o Guile sozinho, sem time, e pode servir a lutadores overpower do SVC. Depois da pesquisa 22, a revisão pergunta ao dono se a primeira luta com o importado pode ser solo em vez de em equipe, o que muda os critérios de aceitação do ticket 04 e o spec._
