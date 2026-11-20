---
title: "Give imported fighters their source fighter's hit-box kind set"
triage: ready-for-agent
assignee: claude
---

# 20 Give imported fighters their source fighter's hit-box kind set

Claimed and closed by Claude on 2026-11-20. /
Assumido e concluído pelo Claude em 20/11/2026.

[Parent specification](../spec.md) · [Found in ticket 16](16-imported-opponent-proxy.md) · [Slot anatomy](../slot-anatomy.md)

## What to build

The collision routine reads, at `$15D08` and `$169CA`, a 64-entry table of pointers at
`$6C62E` by the box owner's ID (`4 × (ID & $3F)`). Each pointer leads to a 16-byte bit
set of hit-box kinds that decides how that fighter's boxes are classified. Entries
above `$24` share one pointer, the set of fighter `$24`. So the imported `$30` uses a
set that differs from original Kyo's in 2 bits. The read with `$30` was observed in the
ticket 13 route (frames 5,400–6,100); no visible difference was found there, so the
moves that depend on those 2 bits are not known yet.

Give `$30` its source fighter's entry with a checked tool step, following the
"64-entry tables whose entries above `$24` share a default" row of the slot anatomy
(`wire_slot_lookups.py` already handles that kind).

## Acceptance criteria

- [x] A preparation step writes `$30`'s entry from its source fighter, with byte checks
  and tests on invented data; original entries are unchanged.
- [x] The private pair check of ticket 16 reports the `$15D1A` read with the same bytes
  as Kyo's in the ticket 13 window.
- [x] Original fighters facing originals are unchanged in a regression check, and the
  native build reports no new fallback.

## Português (Brasil)

# 20 Dar aos lutadores importados o conjunto de tipos de caixa do lutador de origem

_A rotina de colisão lê, em `$15D08` e `$169CA`, uma tabela de 64 ponteiros em `$6C62E`
pelo ID do dono da caixa. Cada ponteiro leva a um conjunto de 16 bytes de tipos de caixa
de golpe. As entradas acima de `$24` compartilham um ponteiro, o conjunto do lutador `$24`;
assim o `$30` importado usa um conjunto que difere do Kyo original em 2 bits. A leitura com
o `$30` foi observada no roteiro do ticket 13; nenhuma diferença visível apareceu, então
ainda não se sabe que golpes dependem desses 2 bits. Dar ao `$30` a entrada do lutador de
origem num passo de ferramenta verificado, como na linha "tabelas de 64 entradas com padrão
compartilhado acima de `$24`" da anatomia do slot._

### Critérios de aceitação

- [x] Um passo de preparo grava a entrada do `$30` a partir do lutador de origem, com
  conferência de bytes e testes com dados inventados; as entradas originais não mudam.
- [x] A conferência privada de pares do ticket 16 mostra a leitura em `$15D1A` com os mesmos
  bytes do Kyo na janela do ticket 13.
- [x] Originais contra originais ficam inalterados numa conferência de regressão e o build
  nativo não mostra novo fallback.

## Comments

### 2026-11-20 — Resolution: `$30` gets its source fighter's set

**Tool.** `tools/kof2003/import_slot/map_hitbox_kinds.py SOURCE DEST --sha256 HASH
--fighter-id 0x1e` (after `map_opponent_rows.py`). It copies the source fighter's pointer
in the table at `$6C62E` to entry `$30`. It is a data change of one entry (one byte differs
in the Rehearsal image): no code, no space in the fixed area (`$53340` onwards stays free)
and no native rebuild. It refuses the input unless every unused entry (`$25`–`$3F` except
`$30`) still holds fighter `$24`'s pointer, `$30` still holds that default, the source
fighter has its own set (so `$24` itself is refused, as in `wire_slot_lookups.py`) and every
original set lies in the fixed area below `$100000` and off the table; `--fighter-id` must
be an original ID. Four tests on invented data cover the result, unchanged entries, refused
tables and inputs (a set past the program, in the banked window or on the table, a source
without its own set) and refused paths. It is a separate step rather than a new row in
`wire_slot_lookups.py`, so the current candidate could be prepared from the ticket 16 image
without rebuilding the whole chain; the check is the same kind (shared default above `$24`).

**Pair check.** The ticket 16 ROM-read differential (interpreter, clone against the
reference, same five windows) was repeated on the new candidate. In the ticket 13 window
(frames 5,400–6,100) the read at `$15D1A` still uses a different address (entry `$30`
against entry `$1E`), now with the **same bytes** (it was the one DIFFERENT read before).
The other ID-indexed reads in all five windows are unchanged from ticket 16 and all read
the same bytes or banked frame data. **Open:** the second reader, `$169CA`, was not reached
in these windows, so it has no runtime check yet; it reads the same table entry, which now
holds Kyo's pointer.

**Regression and native build.** No rebuild: the native player compiles the program's
code, and this step changes one pointer in a data table that the code reads at run time
(slot anatomy, "Rebuilds"). The native player built for ticket 16 ran the four ticket 16 scripts on the new candidate: per-frame trace lines equal the ticket
16 candidate's in every script (6,101 or 9,001 frames), so no visible change, as expected
from ticket 16; native coverage is unchanged (same interpreted-instruction and
uncovered-entry counts as tickets 14 and 16, no new fallback). Original teams against the
unmodified control, with P1 and P2 scripts: GREEN at tolerance 0 in the ticket 16 loop,
which compares screenshots at frames 5,400, 6,000, 7,000, 8,000 and 9,000 (the fight; the
earlier frames are selection and intro).
Which moves depend on the 2 differing bits remains unknown; with the source fighter's set
they no longer matter for `$30`. Guile will need her own set when she gets her ID.

_PT-BR: **Ferramenta.** `map_hitbox_kinds.py` (depois do `map_opponent_rows.py`) copia
para a entrada `$30` da tabela em `$6C62E` o ponteiro do lutador de origem. É uma mudança
de dados numa entrada (um byte difere na imagem do Ensaio): sem código, sem espaço na área
fixa (`$53340` em diante continua livre) e sem recompilar o player nativo. Recusa a entrada
se alguma entrada sem uso não tiver o ponteiro do lutador `$24`, se o `$30` já tiver entrada
própria, se o lutador de origem não tiver conjunto próprio ou se algum conjunto original
ficar fora da área fixa (abaixo de `$100000`) ou sobre a tabela. Quatro
testes com dados inventados. É um passo separado, não uma linha nova do
`wire_slot_lookups.py`, para preparar o candidato a partir da imagem do ticket 16 sem refazer
a cadeia inteira. **Conferência de pares:** na janela do ticket 13 a leitura em `$15D1A`
agora traz os mesmos bytes do Kyo (antes era a única DIFERENTE); as demais leituras nas
cinco janelas não mudaram. **Em aberto:** o segundo leitor, `$169CA`, não foi alcançado
nessas janelas e ainda não tem conferência em execução; ele lê a mesma entrada, que agora
tem o ponteiro do Kyo. **Regressão e build nativo:** sem recompilar, porque só muda um
ponteiro numa tabela de dados lida em execução; com o player do ticket 16, os quatro roteiros dão linhas por quadro iguais às do candidato do
ticket 16 e a mesma cobertura nativa (nenhum fallback novo); originais contra o controle sem
modificação, roteiros de P1 e P2: VERDE com tolerância 0 nas capturas dos quadros 5.400 a
9.000 (a luta). Ainda não se sabe que golpes usam
os 2 bits; com o conjunto do lutador de origem isso deixa de importar para o `$30`. A Guile
vai precisar do próprio conjunto quando ganhar o ID dela._
