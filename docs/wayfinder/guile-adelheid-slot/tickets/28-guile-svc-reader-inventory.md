---
id: 28
title: "Inventory everything SVC reads by Guile's fighter ID"
label: wayfinder:research
mode: AFK
status: open
assignee: claude-research
blocked_by: []
research:
---

## Question

Which data does SVC Chaos look up by Guile's fighter ID, and where? The Kyo
Rehearsal in KOF 2003 exposed five classes of ID-indexed data that the earlier
research had missed ([slot anatomy](../../../specs/first-svc-character-import/slot-anatomy.md)).
Export needs the same completeness on the SVC side. Without modifying SVC, use
MAME as the reading instrument: read watchpoints on the fighter object's ID and
on the team slot during creation, an intro and a scripted set of moves (walk,
normals, command normals, a throw given and received, specials, supers, Guard
Cancels); collect every reader routine; derive the tables from them; and map
each one to its KOF 2003 counterpart using the slot-anatomy kinds (ID tables,
command lists, command-to-action, per-opponent rows, frames, sound,
presentation, identity lists). Record addresses, sizes and counts only.

_PT-BR: quais dados o SVC Chaos busca pelo ID de lutador do Guile, e onde? O
Ensaio com o Kyo no KOF 2003 expôs cinco classes de dados indexados por ID que a
pesquisa anterior tinha deixado passar ([anatomia da vaga](../../../specs/first-svc-character-import/slot-anatomy.md)).
A exportação precisa da mesma completude do lado do SVC. Sem modificar o SVC,
usar o MAME como instrumento de leitura: watchpoints de leitura no ID do objeto
de lutador e na vaga da equipe durante a criação, uma intro e um conjunto de
golpes por roteiro (andar, normais, normais de comando, arremesso aplicado e
recebido, especiais, supers, Guard Cancels); reunir toda rotina leitora; achar as
tabelas a partir delas; e associar cada uma à equivalente no KOF 2003 pelos tipos
da anatomia da vaga (tabelas por ID, listas de comandos, comando → ação, linhas
por adversário, quadros, som, apresentação, listas de identidade). Registrar só
endereços, tamanhos e contagens._
