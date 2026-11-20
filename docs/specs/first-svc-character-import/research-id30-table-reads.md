# Which scan-only tables and which `$169CA` read the imported ID `$30` reads

_Research note for [slot anatomy](slot-anatomy.md) §2 ("Found by scan, not yet
exercised") and the open point of [ticket 20](issues/20-imported-hitbox-kind-set.md).
Researched on 2026-11-20 against the current Rehearsal candidate. Addresses are
offsets in the decrypted program file (equal to 68000 addresses below `$100000`).
Per the repository's hard rule, game bytes and disassembly listings stay in
`private/`; this note gives addresses, offsets, counts and the logic in words.
A Portuguese version follows._

"Ticket 20" here is [issues/20-imported-hitbox-kind-set.md](issues/20-imported-hitbox-kind-set.md),
the only ticket that mentions `$169CA`. The wayfinder ticket
`docs/wayfinder/guile-adelheid-slot/tickets/20-frame-and-collision-format.md`
has the same number and is not about this reader.

## Short answer

| Table / reader | Read for `$30`? | Offset actually read for `$30` | Evidence |
|---|---|---|---|
| `$0641E8` (64 words) | **No reader found**: not read in any static or traced path | none (entry `$30` would be offset `$60`, value zero, the shared value of `$25`–`$3F`) | static and runtime (negative, including a 39,300-frame run on both ROMs) |
| `$06BDC0` (64 word offsets to rival lists) | **Yes, through the presentation map**, when `$30` is the winner on the victory screen | `$3C` (entry `$1E`, Kyo's list), not `$60` | static and runtime |
| `$06D32A` (sound table 14 of 16) | **No**: the only reader skips IDs above `$24` | none | static and runtime: guard seen skipping `$30`; table read for IDs up to `$1F` only |
| `$06D374` (sound table 15 of 16) | **No**: same reader and guard | none | static; never selected at runtime |
| `$06E9D0` (name-plate byte table, 2 bytes per ID) | **Yes, through the presentation map** | `$3C` or `$3D` (Kyo's pair), not `$60`/`$61` | static; result checked by screenshots in ticket 13 |
| `$169CA` (second reader of `$6C62E`) | **If reached, yes**, with no remap: entry `$30` (`$06C6EE`), which now holds Kyo's set pointer `$06C90E` | `$C0` | static; at runtime `$169A2` is entered but its range check was never passed, on either ROM |

Only `$169CA` still uses the raw `$30`; the two tables that are read for `$30`
are read at Kyo's entry because their readers go through the presentation map
at `$53100`. Nothing in the list reads an out-of-range entry for `$30` in the
current candidate.

## Sources and method

- **Program image.** `private/work/first-import/diag-t17/roms-t20/271-pd.bin`,
  the ROM set opened by `Jogar-Ensaio.cmd` (through
  `private/work/first-import/diag-t17/Jogar-Ensaio-t20.ps1`). It differs from the
  ticket 16 image `roms-t16/271-pd.bin` in exactly one byte, at `$6C6F1` (inside
  entry `$30` of `$6C62E`): a Python byte comparison of the two files.
- **Code.** The per-instruction comments of the recompiled C of the ticket 16
  native build, `private/work/first-import/diag-t17/build-t16/generated/recomp_*.c`
  (81,866 decoded instructions, 18,404 entry points). Ticket 20 changed data only,
  so this code is the candidate's code. Indexed with a throwaway script outside
  the repository; no file in the repository was changed.
- **Reference search.** Every big-endian long in the 9 MiB program file equal to
  each table address, and every operand in the decoded instructions between
  `$63000`–`$64400`, `$6BD00`–`$6BE00`, `$6D200`–`$6D400` and `$6E900`–`$6EA00`.
- **Runtime.** No new run: the ROM-read tracer of ticket 17 (`[DEBUG-t17b]` in
  `private/work/first-import/diag-t17/runtime-trace/src/exec.c:440-455`) is a
  Windows build (`build-trace\KOF 2003.exe`) and the shell available for this
  research is a Linux VM without Wine. Instead, all 34 existing logs with tracer
  lines under `private/work/first-import/` were scanned for reads inside each
  table (16 `trace14-*` clone/reference pairs from tickets 14, 16 and 20, fight
  windows between frames 5,400 and 6,100, plus the Orochinagi runs; and four
  `wide-trc-*` victory-screen runs of ticket 17). The tracer prints each distinct
  (program counter, address, size) once per window, with D0–D7.
- **How `$30` gets there.** The clone's selection cell holds `$30` (the reference
  ROM differs only there, `$30` against `$1E` at `0x52B0F`:
  [ticket 13](issues/13-rehearsal-selection-presentation.md) lines 114-115), so the
  team bytes and the fighter object (word `+$1E`, byte `+$1F`) hold the raw `$30`
  ([slot anatomy](slot-anatomy.md) §1). No general remap exists; IDs are mapped
  only at patched sites: the presentation map `$53100` (identity for `$00`–`$24`
  and for `$25`–`$3F` except `$30`, which holds `$1E`: checked in `roms-t20`) via
  `$53140` and its callers `$53150`–`$5318C`, `$53200`, `$53240`, `$53280`, and the
  opponent proxy at `$532C0`/`$53300`.

## Per table

### `$0641E8`: no reader found

- **Code sites.** None. The long `$000641E8` occurs three times in the program
  file, at `$1648`, `$10952` and `$1CC78`; all three straddle two instructions
  in decoded code (a word store followed by a `lea` with displacement at
  `$1646`/`$164A`; a branch followed by a `lea` at `$10950`/`$10954` and at
  `$1CC76`/`$1CC7A`), so they are encoding coincidences, not pointers. No decoded
  instruction has an operand in `$63000`–`$64400`, and the only decoded code
  between `$5C1E8` and `$6C1E7` (reach of a PC-relative reference) is at
  `$60890`–`$60908`, which uses no PC-relative operand.
- **Runtime.** No read inside `$0641E8`–`$064267` in any of the 34 logs,
  clone or reference.
- **Data.** As 64 words, entries `$00`–`$24` rise from zero to `$1250` (an offset
  directory shape) and entries `$25`–`$3F`, including `$30`, are all zero. If some
  undiscovered path read it for `$30` it would get offset zero, that is the table
  itself: garbage, not a default record.
- **Classification.** Not read for `$30` as far as the decoded code and the traced
  windows show. Code reached only through computed jumps that the recompiler did
  not discover cannot be excluded statically.

### `$06BDC0`: read for `$30`, at Kyo's entry

- **Code site.** Routine `$E8F2`, its only caller `$E43A` (victory screen). The
  routine masks the winner's byte from the screen object (`+$144`) to six bits,
  doubles it, adds the word found at `$6BDC0` + that offset to `$6BDC0` (read at
  `$E906`), then walks the list comparing each rival byte with the other fighter's
  byte (`+$148`, masked to six bits). The win quote read at `$E44A` uses the same
  `+$144` ID times 16.
- **Remap before the read.** `+$144`–`+$146` are filled at `$E202` by a call to
  `$53200` (ticket 17, `tools/kof2003/import_slot/map_victory_screen.py` lines
  28-32), which keeps the colour bits and maps the ID through `$53100`. For `$30`
  the routine therefore reads offset `$3C` (address `$06BDFC`), entry `$1E`, whose
  list starts at `$06BFC6`. The raw entry `$30` (`$06BE20`) holds the shared default
  of `$25`–`$3F` (list at `$06C030`; entry `$24` is a different list).
- **Runtime.** `wide-trc-v/run.log` (ROM set `roms-v`, clone leading, `POS=1`,
  window 8,100–8,360, `private/work/first-import/diag-t17/trace2.ps1` line 14):
  pc `$E906` reads `$06BDFC` with D0 = `$003C`. The pre-fix clone run
  `wide-trc-clone/run.log` read `$06BE20` with D0 = `$0060`. `roms-v` and
  `roms-t20` are byte-equal at `$E202`–`$E207`, `$E432`–`$E449`, `$E8F2`–`$E929`,
  the map and the `$53200` routine.
- **Classification.** Read for `$30`, entry `$1E`: valid. Side note: the other
  fighter's byte at `+$148` is copied raw at `$E0A2` and not mapped, so when the
  loser is `$30` no rival list can match it and the routine takes the default
  branch (`$E91C`). That is a pair rule (Kyo's rivals do not recognise the clone
  as a loser), not an out-of-range read.

### `$06D32A` and `$06D374`: not read for `$30`

- **What they are.** Entries 14 and 15 of the 16-long pointer table at `$18EAA`,
  whose targets run from `$6CF1E` in steps of `$4A` (37 words): the per-fighter
  sound tables of slot anatomy §2, "Sound" row (line 37). They are 37-entry tables
  laid end to end, not 64-entry tables. Read as 64 words, `$06D32A`'s entries
  `$25`–`$3F` are the first 27 words of table 15 (27 distinct values); `$06D374`'s
  are words after the block (all equal), which explains the scan's "shared default".
- **Code site.** Routine `$18E6E` (callers `$18B2C`, `$18B74`, `$18BBC`, `$18C04`):
  table number = D0 & 15 (numbers 0 and 1 first play sound `$3014`); the routine
  loads the table pointer from `$18EAA` + 4 × number, reads the fighter's ID word
  at `+$1E`, and **skips the lookup when it is above `$24`** (unsigned compare at
  `$18E94`, branch at `$18E98`); otherwise it reads the word at ID × 2 (`$18E9E`) and
  plays it. The word is not masked, so `$0030` skips. No map is applied here.
- **Runtime.** No read inside either table in the 34 logs (no line at pc `$18E9E`,
  even in reference runs, so these calls did not occur in the traced windows).
- **Classification.** Not read for `$30` (guard at `$18E94`). The practical effect
  is that the clone makes no sound for those two call types, never a wrong sound.
  This is the sound area of tickets 10–12, not a missing table entry.

### `$06E9D0`: read for `$30`, at Kyo's entry

- **Code site.** The in-fight name-plate writer `$1F864`–`$1F8CE`. At `$1F886` the
  original six-bit-mask-and-double was replaced by a call to `$53180` (ticket 13,
  `tools/kof2003/import_slot/wire_slot_lookups.py` lines 50-64), which masks the
  team byte to six bits, maps it through `$53100` and doubles it. The writer adds
  one when the byte at A5 − `$7A5` is non-zero, then reads the byte at `$6E9D0` +
  index (`$1F89C`). It is the only decoded reference to `$6E9D0`.
- **For `$30`.** Index `$3C` or `$3D` (Kyo's pair) instead of `$60`/`$61`. The table
  is 128 bytes (to `$6EA50`), two per ID; every ID `$25`–`$3F` shares one pair (the
  blank name of [ticket 13](issues/13-rehearsal-selection-presentation.md) lines
  98-99), which differs from Kyo's.
- **Runtime.** No tracer window covers the writer (no line at pc `$1F89C` in the 34
  logs). Ticket 13 compared the name plate of the clone and the reference by
  screenshots: equal at team positions 1, 2 and 3 (lines 119-121).
- **Classification.** Read for `$30`, entry `$1E`: valid. Slot anatomy already lists
  this site in the "Presentation" row (line 38).

### `$169CA`: reads entry `$30` if reached; never reached so far

- **Code site.** Routine `$169A2`, called at `$16844` and `$168B4` from `$167C8`,
  which the collision routine calls unconditionally at its end (`$15D7C`). The two
  calls pass each player's current object (the longs at A5 − `$2E4` and A5 − `$2C4`)
  as A4. The routine takes the low seven bits of A4's byte `+$C4` and returns at once
  unless they are `$60`–`$7F`. Otherwise it finds the object whose offset is the word
  at A4 `+$C8` (relative to A5 − `$8000`), reads that object's ID byte `+$1F`, masks
  it to six bits, multiplies by 4, loads the long at `$6C62E` + that (`$169DC`) and
  tests bit (kind − 96) of word 3 of the 16-byte set through `$15D96`.
- **For `$30`.** No remap: if the object at `+$C8` has ID `$30`, the read is offset
  `$C0`, address `$06C6EE`. In `roms-t20` that entry holds `$06C90E`, the same set
  pointer as entry `$1E` (Kyo); in `roms-t16` it held `$06C96E`, the default shared
  with fighter `$24`. So the value is valid now.
- **Runtime.** No line at pc `$169DC` in any of the 34 logs, clone or reference,
  including the Orochinagi runs; ticket 20 already recorded that the reader was not
  reached (issue 20, lines 82-83). The sibling reader `$15D08` uses the same index
  logic and was observed in all five ticket 20 clone traces: pc `$15D1A` reads
  `$06C6EE` (D0 = `$00C0`), and the set reads at `$15DA6` land in `$06C90E`'s set
  (offset `$1E0` from `$6C72E`), where the ticket 16 clone read the `$24` set
  (offset `$240`).
- **Classification.** Read for `$30` when reached, entry `$30` = Kyo's set
  (static only); the reach condition was never met in the traced windows.

## Follow-up run (2026-11-20)

The tracer of ticket 17 was then run natively on Windows (Desktop shell), so the
"no new run" limit above no longer applies to these points.

- **Run.** `build-trace\KOF 2003.exe --interp` with `KOF_T17R=0-39300`, clone ROM set
  `roms-t20` and reference `roms-ref` with the same input script (private helper and
  logs in `private/work/first-import/diag-id30/`). Script: the ticket 16 versus route
  (`t16-attack.txt` up to frame 5,400; P1 team led by `$30`, P2 team led by Kyo), then a P1
  sweep of 16 motions (quarter and half circles, dragon punches, double motions, plain
  directions) × 7 buttons (A, B, C, D, A+B, C+D, B+C), facing both ways, twice, plus jump
  attacks. In the clone run P1 beat the idle P2 team (frame 9,502), fought a CPU team
  until frame 17,864, then the run went through game over, a second selection and a
  second match. Both runs ended normally after 487 s.
- **`$169CA`.** Routine `$169A2` was entered in both runs (pc `$169A8` reads A4 `+$C4`
  for 19 object addresses in the clone run, 13 in the reference), but no line at
  `$169BE`, `$169CA` or `$169DC` exists in either log: the low seven bits of `+$C4` were
  never `$60`–`$7F`. Not even original Kyo on the reference ROM reaches the read with
  this sweep.
- **What `+$C4` and `+$C8` hold.** The hit routine writes them on the object that was
  hit: `+$C4` gets the kind word of the colliding box entry (`$16292` and `$162FE`) and
  `+$C8` the offset of the hitter; when the hitter is an effect (bit 4 of its `+$1C`
  set), `+$C8` gets its owner fighter instead (`+$13E`, `$1626E`–`$1629C`). So
  `$169CA` reads the ID of the fighter that hit the player, and sees `$30` only when the
  clone hits an opponent and the recorded box kind is in `$60`–`$7F`, a kind none of the
  sweep's moves (Kyo's or the CPU teams') produced. When it happens, the read is entry
  `$30`, Kyo's set.
- **`$0641E8`.** No read of `$0641E8`–`$064267` in either 39,300-frame log (attract
  mode, two selections, versus and CPU fights, victory and game-over screens). Code
  reached only through screens outside this route (endings, story demos) is still not
  excluded.
- **Sound guard.** The existing ticket 20 logs already show it: in `trace14-t20a1` the
  clone's reader reads the ID word `$10109E` at `$18E90` and continues at `$18EA6` with
  D0 = `$0030`, with no read at `$18E9E`; the reference reads `$06CFA4` there with
  D0 = `$003C`. The guard does not depend on which of the 16 tables the caller picks.
  In the sweep the reader picked tables 0–4, 6 and 10–14 (pointer reads at `$18E8C`);
  table 14 (`$06D32A`) was read at offsets up to `$3E` (IDs up to `$1F`) and table 15
  never.
- **Other readers in the same run.** `$06BDC0` at `$E906`: clone offsets `$32`, `$36`,
  `$3C`, `$3E`; `$06E9D0` at `$1F89C`: offsets up to `$3F`; `$6C62E` at `$15D1A`: offset
  `$C0` (entry `$30`) among others. No read at offset `$60` (or `$60`/`$61`) in either
  table: the clone keeps reading Kyo's entries there.

## Open questions

1. Which box kind (low seven bits `$60`–`$7F`) triggers `$169A2`, and on which
   fighter's move. It does not change the answer for `$30` (the read lands on Kyo's
   set), so it matters only to a future slot whose source fighter has a different set.
2. Whether `$0641E8` is read on screens outside this route (endings, story demos).
3. The victory-screen rival lists see a losing `$30` as no rival (raw byte at
   `+$148`). If Kyo's specific win quotes against certain losers should also apply
   to the clone as loser, `$E0A2` or `$E8F2` needs the map too: an owner decision.

---

## Português (Brasil)

# Quais tabelas achadas por varredura e qual leitura em `$169CA` o ID importado `$30` lê

_Nota de pesquisa para a seção 2 da [anatomia da vaga](slot-anatomy.md) ("Achadas por
varredura, ainda não exercitadas") e o ponto em aberto do
[ticket 20](issues/20-imported-hitbox-kind-set.md). Pesquisada em 20/11/2026 sobre o
candidato atual do Ensaio. Endereços são posições no arquivo de programa decifrado.
Bytes e listagens de disassembly ficam em `private/`._

"Ticket 20" aqui é [issues/20-imported-hitbox-kind-set.md](issues/20-imported-hitbox-kind-set.md),
o único que cita `$169CA`; o ticket 20 do mapa `guile-adelheid-slot` tem o mesmo número
e trata de outro assunto.

### Resposta curta

| Tabela / leitor | O `$30` lê? | Posição lida para o `$30` | Evidência |
|---|---|---|---|
| `$0641E8` (64 words) | **Nenhum leitor achado** | nenhuma (a entrada `$30` seria `$60`, valor zero, igual a `$25`–`$3F`) | estática e execução (negativa, inclusive numa execução de 39.300 quadros nas duas ROMs) |
| `$06BDC0` (listas de rivais) | **Sim, pelo mapa de apresentação**, quando o `$30` vence | `$3C` (entrada `$1E`, lista do Kyo), não `$60` | estática e execução |
| `$06D32A` (tabela de som 14 de 16) | **Não**: o único leitor pula IDs acima de `$24` | nenhuma | estática e execução: trava vista pulando o `$30`; tabela lida só para IDs até `$1F` |
| `$06D374` (tabela de som 15 de 16) | **Não**: mesmo leitor e trava | nenhuma | estática; nunca escolhida em execução |
| `$06E9D0` (nome sob as barras de vida) | **Sim, pelo mapa de apresentação** | `$3C`/`$3D` (par do Kyo), não `$60`/`$61` | estática; resultado conferido por capturas no ticket 13 |
| `$169CA` (segundo leitor de `$6C62E`) | **Se alcançado, sim**, sem mapa: entrada `$30` (`$06C6EE`), que hoje aponta para o conjunto do Kyo (`$06C90E`) | `$C0` | estática; em execução o `$169A2` é chamado, mas a checagem de faixa nunca passou, em nenhuma das duas ROMs |

Só o `$169CA` ainda usa o `$30` cru; as duas tabelas lidas para o `$30` são lidas na
entrada do Kyo porque os leitores passam pelo mapa em `$53100`. No candidato atual
nenhuma tabela da lista é lida fora da faixa para o `$30`.

### Pontos principais

- **Fontes.** Imagem `private/work/first-import/diag-t17/roms-t20/271-pd.bin` (a do
  atalho do Ensaio; difere da do ticket 16 só no byte `$6C6F1`), código pelos
  comentários do C recompilado do build do ticket 16 e as 34 listagens existentes do
  rastreador de leituras da ROM. Não houve execução nova: o rastreador é um executável
  Windows e o shell desta pesquisa é uma VM Linux sem Wine.
- **`$0641E8`.** As três ocorrências do endereço no programa caem no meio de duas
  instruções (coincidências de codificação); nenhuma instrução decodificada o usa e
  nenhuma listagem o lê. Se algo o lesse para o `$30`, pegaria deslocamento zero, isto
  é, lixo. Não dá para excluir código só alcançado por saltos calculados.
- **`$06BDC0`.** Lido em `$E906` pela rotina `$E8F2` com o ID do vencedor que o
  `$53200` (ticket 17) já mapeou; rastreio `wide-trc-v`: deslocamento `$3C`. O byte do
  perdedor (`+$148`) não é mapeado: um `$30` perdedor não é reconhecido como rival e
  a rotina usa o ramo padrão; isso é regra de par, não leitura fora da faixa.
- **`$06D32A` e `$06D374`.** São as tabelas 14 e 15 das 16 tabelas de som de 37 words
  (ponteiros em `$18EAA`, passo `$4A`), não tabelas de 64. O leitor `$18E6E` pula a
  busca quando o word de ID em `+$1E` passa de `$24` (`$18E94`); para o clone o efeito
  é silêncio nessas chamadas, nunca som errado (área dos tickets 10–12).
- **`$06E9D0`.** O escritor do nome (`$1F864`–`$1F8CE`) chama `$53180` em `$1F886`
  (ticket 13), que mapeia e dobra o ID; o `$30` lê o par do Kyo.
- **`$169CA`.** Só segue se os 7 bits baixos do byte `+$C4` do objeto do jogador
  estiverem em `$60`–`$7F`; aí lê o ID (`+$1F`) do objeto apontado por `+$C8`, sem
  mapa. Para o `$30` leria a entrada `$30`, que desde o ticket 20 tem o ponteiro do
  conjunto do Kyo: valor válido. Nenhuma listagem mostra leitura em `$169DC`; o leitor
  irmão `$15D08` foi visto lendo a entrada `$30` e o conjunto do Kyo nas cinco
  listagens do ticket 20.

### Execução complementar (20/11/2026)

Depois, o rastreador do ticket 17 rodou nativo no Windows; o limite "não houve execução
nova" acima não vale mais para estes pontos.

- **Execução.** `build-trace\KOF 2003.exe --interp` com `KOF_T17R=0-39300`, clone
  `roms-t20` e referência `roms-ref` com o mesmo roteiro (ajudante e logs em
  `private/work/first-import/diag-id30/`): a rota versus do ticket 16 até o quadro 5.400
  (P1 liderado pelo `$30`, P2 liderado pelo Kyo) e depois uma varredura do P1 com 16 movimentos
  × 7 botões (A, B, C, D, A+B, C+D, B+C), virado para os dois lados, duas vezes, mais
  ataques no pulo. No clone, o P1 venceu a equipe parada do P2 (quadro 9.502), lutou
  contra uma equipe da CPU até o quadro 17.864 e a execução seguiu por fim de jogo,
  nova seleção e segunda partida. As duas execuções terminaram normalmente em 487 s.
- **`$169CA`.** A rotina `$169A2` foi chamada nas duas execuções (o pc `$169A8` lê o
  `+$C4` de 19 objetos no clone e 13 na referência), mas nenhum log tem linha em
  `$169BE`, `$169CA` ou `$169DC`: os 7 bits baixos de `+$C4` nunca ficaram em
  `$60`–`$7F`. Nem o Kyo original, na ROM de referência, chega à leitura com essa
  varredura.
- **O que `+$C4` e `+$C8` guardam.** A rotina de acerto os grava no objeto atingido:
  `+$C4` recebe o word de tipo da caixa que colidiu (`$16292` e `$162FE`) e `+$C8` o
  deslocamento de quem acertou; quando quem acertou é um efeito (bit 4 do seu `+$1C`),
  `+$C8` recebe o lutador dono (`+$13E`, `$1626E`–`$1629C`). Então o `$169CA` lê o ID
  do lutador que acertou o jogador e só vê o `$30` quando o clone acerta o adversário e
  o tipo de caixa gravado está em `$60`–`$7F`, tipo que nenhum golpe da varredura
  (do Kyo ou das equipes da CPU) produziu. Quando acontecer, a leitura é a entrada
  `$30`, o conjunto do Kyo.
- **`$0641E8`.** Nenhuma leitura em `$0641E8`–`$064267` nos dois logs de 39.300 quadros
  (modo de demonstração, duas seleções, lutas versus e contra a CPU, telas de vitória e
  de fim de jogo). Código só alcançado por telas fora dessa rota (finais, demonstrações
  de história) ainda não está excluído.
- **Trava do som.** Os logs do ticket 20 já mostram: em `trace14-t20a1` o leitor do
  clone lê o word de ID `$10109E` em `$18E90` e segue em `$18EA6` com D0 = `$0030`, sem
  leitura em `$18E9E`; a referência lê `$06CFA4` ali com D0 = `$003C`. A trava não
  depende de qual das 16 tabelas o chamador escolhe. Na varredura o leitor escolheu as
  tabelas 0–4, 6 e 10–14; a tabela 14 (`$06D32A`) foi lida em deslocamentos até `$3E`
  (IDs até `$1F`) e a 15 nunca.
- **Outros leitores na mesma execução.** `$06BDC0` em `$E906`: deslocamentos `$32`,
  `$36`, `$3C`, `$3E` no clone; `$06E9D0` em `$1F89C`: até `$3F`; `$6C62E` em `$15D1A`:
  `$C0` (entrada `$30`) entre outros. Nenhuma leitura no deslocamento `$60` (ou
  `$60`/`$61`) dessas tabelas: o clone continua lendo as entradas do Kyo.

### Pontos em aberto

1. Qual tipo de caixa (7 bits baixos `$60`–`$7F`) dispara o `$169A2`, e em que golpe de
   qual lutador. Não muda a resposta para o `$30` (a leitura cai no conjunto do Kyo);
   só importa para uma vaga futura cujo lutador de origem tenha outro conjunto.
2. Se o `$0641E8` é lido em telas fora dessa rota (finais, demonstrações de história).
3. As listas de rivais da tela de vitória não reconhecem um `$30` perdedor. Se as
   frases específicas do Kyo contra certos perdedores devem valer para o clone como
   perdedor, `$E0A2` ou `$E8F2` precisa do mapa: decisão do dono.
