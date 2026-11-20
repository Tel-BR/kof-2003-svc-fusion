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

## Progress, 2026-11-20

Started on the owner's instruction. Two results, one of them the question's first missing piece.

**The fighter object's ID field is found, and Guile's SVC ID with it.** An SVC fighter object starts at `$10A100` (the second at `$10A380`) and holds the fighter ID as a byte at **`+$71`**, with copies at **`+$77`** and **`+$1D6`**; the same three offsets also appear doubled at `+$181` (the ID times two, i.e. a word offset into a table). Guile is ID **`$13`**. Method: `tools/kof2003/match/svc_id_readers.lua` dumps `$300` bytes of both objects at chosen frames while a recorded session plays back; two recorded sessions were compared (`session-150700`, `session-152733`), both with Guile as player 1 and a different opponent each. Of the 26 object bytes that are constant through a match and differ between the two fighters, only these three carry the same value for Guile in both sessions while following the opponent in player 2. This is the SVC counterpart of KOF 2003's word at `+$1E` with its copy at `+$19F` ([slot anatomy](../../../specs/first-svc-character-import/slot-anatomy.md) §1).

**The instrument the ticket assumed does not work, and that is worth knowing before the next attempt.** MAME memory taps on work RAM see nothing: over a whole recorded match the only reads of those three offsets were the BIOS memory test at boot, from BIOS code. Debugger watchpoints (`-debug -debugger none`) are accepted but their `printf` output has nowhere to go with no debugger console. So "put a read watchpoint on the ID and collect the readers" cannot be done as written. The routes left, in the order they look cheapest: disassemble the decrypted SVC program (`private/work/decryption-mame/results/svc-learned-maincpu.bin`, verified against MAME's own export) through the debugger's `dasm` into files under `private/`, and search statically for the `(d16,An)` displacements `$0071`, `$0077` and `$01D6`, the way the KOF 2003 research read code; or build an SVC native player from `svc-port`, which gives commented C like KOF 2003's, at the cost of a port.

Nothing else of the question is answered yet: the readers, the tables, their sizes and counts, and the mapping to the slot-anatomy kinds are all still open.

_PT-BR: **o campo de ID do objeto de lutador foi achado, e com ele o ID do Guile no SVC.** O objeto começa em `$10A100` (o segundo em `$10A380`) e guarda o ID como byte em **`+$71`**, com cópias em **`+$77`** e **`+$1D6`**; os mesmos três aparecem dobrados em `+$181` (o ID vezes dois, deslocamento de palavra numa tabela). O Guile é o ID **`$13`**. Método: o `svc_id_readers.lua` despeja `$300` bytes dos dois objetos em quadros escolhidos enquanto uma sessão gravada é repetida; duas sessões foram comparadas, as duas com o Guile no jogador 1 e um adversário diferente em cada. Dos 26 bytes do objeto que ficam constantes durante a luta e diferem entre os dois lutadores, só esses três carregam o mesmo valor para o Guile nas duas sessões enquanto acompanham o adversário no jogador 2. É o equivalente, no SVC, à palavra em `+$1E` com cópia em `+$19F` do KOF 2003._

_**O instrumento que o ticket supunha não funciona, e isso vale saber antes da próxima tentativa.** Os taps de memória do MAME não veem leitura de RAM: numa luta gravada inteira, as únicas leituras desses três deslocamentos foram o teste de memória da BIOS no boot. Watchpoints do depurador são aceitos, mas o `printf` deles não tem para onde ir sem console. Então "pôr watchpoint de leitura no ID e reunir os leitores" não dá para fazer como está escrito. As rotas que sobram, da mais barata para a mais cara: desmontar o programa decifrado do SVC pelo `dasm` do depurador para arquivos em `private/` e procurar estaticamente os deslocamentos `$0071`, `$0077` e `$01D6`, como a pesquisa do KOF 2003 leu código; ou construir um player nativo do SVC a partir do `svc-port`, que dá C comentado como o do KOF 2003, ao custo de um porte._

_Nada mais da pergunta está respondido: os leitores, as tabelas, tamanhos e contagens e o mapeamento aos tipos da anatomia da vaga seguem em aberto._
