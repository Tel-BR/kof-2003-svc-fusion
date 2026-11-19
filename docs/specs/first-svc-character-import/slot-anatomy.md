# What a new fighter ID touches in KOF 2003

_Reference for adding imported fighter slots (`$30`–`$3E`). Learned from the Kyo
Rehearsal in [ticket 14](issues/14-rehearsal-intro-and-command-normals.md). Addresses
are offsets in the validated decrypted program file; values beyond addresses,
sizes and counts stay in `private/`. A Portuguese version follows._

## 1. Identity

- A team-slot byte holds a 6-bit fighter ID and two colour bits. Player 1's team
  is at `$107D0C` with a second copy at `$107D12`; the copy is read when the
  fighter is created (frame window around 4,925 in the scripted route).
- A fighter object starts at `$101080` (objects `$300` apart) and holds the ID
  as a word at `+$1E`, with another copy at `+$19F`. The routine at `$28120`
  compares the object's ID with the team slot to decide whether it is the
  active fighter, so a test that changes one must change both.
- Some per-ID values are copied into the object at creation; others are looked
  up on every use. A slot can look right at rest and still fail in a move.

## 2. Kinds of ID-indexed data and what a new ID needs

| Kind | Where | What a new ID needs | Tool / status |
|---|---|---|---|
| 37-row tables (nine of 64-byte rows, six of 4 bytes, one of 80 bytes) | readers repointed by the tool | relocate to 64 rows, copy the source row | `relocate_action_tables.py` |
| Fighter-pair matrix | `$77B4A`, readers `$240E6`/`$24D06` | relocate, widen both axes | `relocate_action_tables.py` |
| Special-intro tables, 37 × 4 bytes | `$A5DB6` (read `$407EA`, `$40866`), `$A5E4A` (read `$409E8`, `$40C70`) | relocate to 64 rows | `wire_slot_lookups.py` |
| ID guards `≤$24`/`<$25` before relocated tables | `$166A8`, `$240F0`, `$24124`, `$27E06` | raise to `$3F`/`$40` | `wire_slot_lookups.py` |
| 64-entry tables whose entries above `$24` share a default | `$79672`, `$79772`, `$B8250` (pointers); `$79872`, `$798F2` (command lists); file `$62B9AC` (banked proximity directory) | own entry | `wire_slot_lookups.py` |
| Word-offset header with free room | `$B3204` (command → action) | own entry | `wire_slot_lookups.py` |
| Directories | master `$704A2`, move scripts `$7DC28`, four palette tables, banked `$200000` (frames) and `$380000` (step scripts) | own entry | tools; frames see §3 |
| Per-opponent rows, 42 bytes × 37 | under file `$62B9AC`: self ID → 8 modes → 6 tables; readers `$216AC`, `$21836` | proxy byte per imported ID (owner decision) | [ticket 16](issues/16-imported-opponent-proxy.md) |
| Fighter-pair byte table, 64 × 64 | `$6F312` (word row offsets, then rows) | row and column; zero for Kyo | not yet in tools |
| Identity lists | `$A5F1F` (FF-separated ID groups used by intro codes `$D0`+); 64-bit set `$25028` (tested via `$277E6`) | membership only if the import should belong | per character |
| Sound | 16 tables of 37 words at `$6CF1E` (via `$18EAA`), flags `$18D38`; guards `$18D08`, `$18E90` | relocation or own data | tickets 10–12 |
| Presentation: name, portraits, thumbnail, group/palette, in-fight name plate | selection per-ID readers add a constant to the ID and only handle IDs up to `$24`: name `$9042`, portrait `$9124`, thumbnail `$91FE`, group `$9338`; order screen portrait `$9E00` and group `$9F26`; the in-fight name plate is written by `$1F864`–`$1F8CE` from byte table `$6E9D0` (read at `$1F886`), then drawn by the fix-layer text engine (`$1ED44`, offsets `$6EA9E`) | a shared presentation map: 64-byte table at `$53100` (identity, `$30` = source fighter), routine `$53140`, trampolines from `$53150`, jumped to from the seven sites | `wire_slot_lookups.py` for the clone; Guile phase 4 adds its own art ([ticket 13](issues/13-rehearsal-selection-presentation.md)) |

**Found by scan, not yet exercised:** 64-entry tables with a shared default above
`$24` at `$0641E8`, `$06BDC0`, `$06D32A`, `$06D374` and `$06E9D0`. Each new slot
should check them before relying on the Rehearsal result.

**Guards left on purpose:** `$7A9C` (object `$2C` uses ID + `$176` as an
animation), `$19396` (team group as ID ÷ 3), the selection guards around
`$118FE` and the boss/Maki checks (`$9056`, `$D62C`).

## 3. Memory and space

- **Fixed area.** Relocated tables use `$44020`–`$52A20`; the palette and
  selection steps write up to `$52B51`; the intro tables use `$52C00`–`$52DFF`.
  `$52E00`–`$52E11` holds proxy code in the diagnostic candidate; `$52E12`–`$5FFFF`
  is free (filler, unread in the observed runs). The presentation map uses
  `$53100`–`$531FF`.
- **Frame bank.** The frame lookup (`$010AB8`–`$010B42`) always selects one bank;
  every original frame directory lives there. KOF 2003's NEO-PVC protection chip
  maps 8 KiB of RAM over `$2FE000`–`$2FFFFF` of that window: file data placed
  there reads back as chip RAM. Only about 12 KiB is free below it, less than one
  fighter. Imported frames go to a per-ID bank ([ticket 15](issues/15-imported-frame-bank.md)).
- **Bank switching.** Writes to `$2FFFF0`/`$2FFFF2` select the window; the current
  bank is kept at `$2FF000` (PVC RAM), and several routines convert pointers
  between banks (`$010A82`, `$02162E`).
- **Rebuilds.** The native player compiles the program's code at build time.
  Data changes take effect without rebuilding; code changes (guards, reader
  patches) need a rebuild or `--interp`.

## 4. How to check a new slot

1. Use the clone method: copy an original fighter into the new ID and compare
   with the original from an identical state.
2. Two swaps with the rehearsal monitor (`KOF_REHEARSAL_FORCE=0x1e:0x30@4874`
   after team order, before creation; `KOF_REHEARSAL_POKE` of the object ID, its
   copy and both team bytes while idle in the fight). Swapping during selection
   changes the CPU team order, so it is not a fair comparison.
3. Compare the per-frame trace (`KOF_REHEARSAL_TRACE`) and RAM (`KOF_REHEARSAL_DUMP`).
4. For the cause, an interpreter-only PC trace of both runs, filtered for the
   vertical-blank wait (`$586`–`$5AA`) and loops whose count depends on the ID
   value; the first remaining divergence names the branch. That instrumentation
   is private and temporary.
5. Test a code change with `--interp` first, then rebuild natively.
6. For presentation (ticket 13): run the same scripted selection (positions 1, 2,
   3 and the other player side) with the clone and with the reference ROM, which
   differs only in the selection cell, and compare the screenshots region by
   region (name, portrait, thumbnail, order screen, name plate under the life
   bars). To find a lookup that is not in this list, trace in the interpreter the
   ROM data reads of both runs and diff them: the reads made only by the clone's
   run at an out-of-range offset name the table.

## 5. Checklist for the next ID

- [ ] Run `relocate_action_tables.py`, then `wire_slot_lookups.py`, for the ID.
- [ ] Check the scan-only tables of §2.
- [ ] Place frames in the per-ID bank (ticket 15) and set the opponent proxy (ticket 16).
- [ ] Sound and identity lists as the character needs. Presentation: `wire_slot_lookups.py` maps the lookups; the character's own art and icon go in their tables (ticket 13 sites).
- [ ] Differential check against its source, then a regression check of originals.

---

## Português (Brasil)

# O que um novo ID de lutador afeta no KOF 2003

_Referência para acrescentar vagas de lutadores importados (`$30`–`$3E`).
Aprendido no Ensaio com o Kyo, no [ticket 14](issues/14-rehearsal-intro-and-command-normals.md).
Os endereços são posições no arquivo de programa decifrado validado; valores além
de endereços, tamanhos e contagens ficam em `private/`._

### 1. Identidade

- O byte da vaga na equipe guarda um ID de 6 bits e dois bits de cor. A equipe do
  jogador 1 fica em `$107D0C`, com segunda cópia em `$107D12`; a cópia é lida
  quando o lutador é criado (por volta do quadro 4.925 no roteiro).
- O objeto de lutador começa em `$101080` (objetos a cada `$300`) e guarda o ID
  como word em `+$1E`, com outra cópia em `+$19F`. A rotina `$28120` compara o ID
  do objeto com a vaga da equipe para saber se ele é o lutador ativo; um teste
  que troca um precisa trocar os dois.
- Alguns valores por ID são copiados no objeto na criação; outros são consultados
  a cada uso. Uma vaga pode parecer certa parada e falhar num golpe.

### 2. Tipos de dados indexados por ID

A tabela da seção 2 em inglês vale para as duas línguas (endereços, ferramentas
e situação). Resumo: tabelas de 37 linhas e a matriz de pares são movidas por
`relocate_action_tables.py`; as duas tabelas de intro, as quatro travas e as
entradas de tabelas de 64 com padrão comum são tratadas por
`wire_slot_lookups.py`; as linhas por adversário usam proxy (ticket 16); os
quadros vão para um banco por ID (ticket 15); som (tickets 10–12) e apresentação
(ticket 13: mapa compartilhado em `$53100`, pelo `wire_slot_lookups.py`; arte própria na fase 4 do Guile); listas de identidade são
decididas por personagem.

**Achadas por varredura, ainda não exercitadas:** tabelas de 64 entradas com
padrão comum acima de `$24` em `$0641E8`, `$06BDC0`, `$06D32A`, `$06D374` e
`$06E9D0`. Cada nova vaga deve conferi-las.

**Travas mantidas de propósito:** `$7A9C`, `$19396`, as travas da seleção perto
de `$118FE` e as checagens de chefes/Maki (`$9056`, `$D62C`).

### 3. Memória e espaço

- **Área fixa.** Tabelas movidas em `$44020`–`$52A20`; os passos de paletas e
  seleção escrevem até `$52B51`; as tabelas de intro usam `$52C00`–`$52DFF`.
  `$52E00`–`$52E11` guarda código de proxy no candidato de diagnóstico;
  `$52E12`–`$5FFFF` está livre. O mapa de apresentação usa `$53100`–`$531FF`.
- **Banco de quadros.** A busca de quadros (`$010AB8`–`$010B42`) sempre escolhe
  um único banco, onde estão todos os diretórios originais. O chip de proteção
  NEO-PVC mapeia 8 KiB de RAM sobre `$2FE000`–`$2FFFFF` dessa janela: dado do
  arquivo colocado ali é lido como RAM do chip. Só cerca de 12 KiB estão livres
  abaixo dela, menos que um lutador. Os quadros importados vão para um banco por
  ID ([ticket 15](issues/15-imported-frame-bank.md)).
- **Troca de banco.** Escritas em `$2FFFF0`/`$2FFFF2` escolhem a janela; o banco
  atual fica em `$2FF000` (RAM do PVC), e várias rotinas convertem ponteiros
  entre bancos (`$010A82`, `$02162E`).
- **Recompilação.** O player nativo compila o código do programa no build.
  Mudanças de dados valem sem recompilar; mudanças de código (travas, remendos de
  leitores) exigem recompilar ou usar `--interp`.

### 4. Como conferir uma nova vaga

1. Método do clone: copiar um lutador original para o novo ID e comparar com o
   original a partir de um estado idêntico.
2. Duas trocas pelo monitor do ensaio (`KOF_REHEARSAL_FORCE=0x1e:0x30@4874`
   depois da ordem da equipe, antes da criação; `KOF_REHEARSAL_POKE` do ID do
   objeto, da cópia e dos dois bytes da equipe com o lutador parado na luta).
   Trocar durante a seleção muda a ordem da equipe da CPU e não serve.
3. Comparar o trace por quadro (`KOF_REHEARSAL_TRACE`) e a RAM (`KOF_REHEARSAL_DUMP`).
4. Para achar a causa, trace de PC só no interpretador das duas execuções,
   filtrando a espera de vblank (`$586`–`$5AA`) e laços cujo número de voltas
   depende do valor do ID; a primeira divergência restante aponta o desvio. Essa
   instrumentação é privada e temporária.
5. Testar mudança de código primeiro com `--interp`, depois recompilar.
6. Para apresentação (ticket 13): rodar o mesmo roteiro de seleção (posições 1, 2,
   3 e o outro lado do jogador) com o clone e com a ROM de referência, que difere
   só na célula da seleção, e comparar as capturas por região (nome, retrato,
   miniatura, escolha de ordem, nome sob as barras de vida). Para achar uma
   busca fora desta lista, rastrear no interpretador as leituras de dados da ROM
   das duas execuções e comparar: as leituras só do clone, fora da faixa, apontam
   a tabela.

### 5. Checklist para o próximo ID

- [ ] Rodar `relocate_action_tables.py` e depois `wire_slot_lookups.py` para o ID.
- [ ] Conferir as tabelas só achadas por varredura (seção 2).
- [ ] Quadros no banco por ID (ticket 15) e proxy de adversário (ticket 16).
- [ ] Som e listas de identidade conforme o personagem. Apresentação: `wire_slot_lookups.py` mapeia as buscas; a arte e o ícone do personagem entram nas tabelas dos pontos do ticket 13.
- [ ] Conferência diferencial contra a origem e regressão dos originais.
