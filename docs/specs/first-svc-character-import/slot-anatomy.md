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
| Special-intro rival rows: the other fighter's ID read at `$40BE2` and compared as a literal ID, or through a group code (`$F0`+, lists behind `$A5EDE`), against the row of the fighter whose intro is chosen (routine `$40BCA`, rows in the relocated tables at `$52D00` and `$52C00`) | rivals are written as literal opponent IDs (Iori's row names Kyo, `$1E`), so the imported `$30` found no rival and the opponent got the default intro | map the other fighter's ID through the presentation map at `$53100` (routine at `$53240`; originals map to themselves; `$30` is recognised as its source fighter) | `map_intro_opponent.py` ([ticket 14](issues/14-rehearsal-intro-and-command-normals.md)) |
| Per-fighter routine tables: two dispatchers (`$2B30E`, `$2B432`) index a 37-entry table of pointers (`$2B336`, `$2B45A`) with `4 × (ID & $3F)` and `jsr` the routine chosen from the fighter's own table | for the imported `$30` the index ran past the end of the table and other data was called; in the Orochinagi replay the flames of the move never ended and stayed on screen | map the ID through the presentation map at `$53100` (routine at `$53280`; originals map to themselves; `$30` uses its source fighter's routines) | `map_fighter_handlers.py` ([ticket 19](issues/19-imported-fighter-routine-tables.md)) |
| ID guards `≤$24`/`<$25` before relocated tables | `$166A8`, `$240F0`, `$24124`, `$27E06` | raise to `$3F`/`$40` | `wire_slot_lookups.py` |
| 64-entry tables whose entries above `$24` share a default | `$79672`, `$79772`, `$B8250` (pointers); `$79872`, `$798F2` (command lists); file `$62B9AC` (banked proximity directory) | own entry | `wire_slot_lookups.py` |
| Word-offset header with free room | `$B3204` (command → action) | own entry | `wire_slot_lookups.py` |
| Directories | master `$704A2`, move scripts `$7DC28`, four palette tables, banked `$200000` (frames) and `$380000` (step scripts) | own entry; frames: own bank (the frame-bank entry keeps the source's) | tools; frames see §3 (`relocate_frames.py`) |
| Per-opponent rows, 42 bytes × 37 | under file `$62B9AC`: self ID → 8 modes → 6 tables; readers `$216AC`, `$21836` | proxy byte per imported ID (owner decision): 64-byte table at `$532C0` (identity for originals, `$30` = `--proxy`), routine at `$53300` | `map_opponent_rows.py` ([ticket 16](issues/16-imported-opponent-proxy.md)) |
| Fighter-pair byte table, 64 × 64 | `$6F312` (word row offsets, then rows), read at `$21332` | row and column; zero for Kyo | already equal to Kyo's on both axes for `$30` (ticket 16 check); no tool needed for a clone |
| Identity lists | `$A5F1F` (FF-separated ID groups used by intro codes `$D0`+); 64-bit set `$25028` (tested via `$277E6`) | membership only if the import should belong | per character |
| Hit-box kind sets, 64 pointers to 16-byte bit sets | `$6C62E`, read by the box owner's ID at `$15D08` and `$169CA` | own entry (entries above `$24` share fighter `$24`'s set) | `map_hitbox_kinds.py` ([ticket 20](issues/20-imported-hitbox-kind-set.md)) |
| Sound | 16 tables of 37 words at `$6CF1E` (via `$18EAA`), flags `$18D38`; guards `$18D08`, `$18E90` | relocation or own data | tickets 10–12 |
| Presentation: name, portraits, thumbnail, group/palette, in-fight name plate | selection per-ID readers add a constant to the ID and only handle IDs up to `$24`: name `$9042`, portrait `$9124`, thumbnail `$91FE`, group `$9338`; order screen portrait `$9E00` and group `$9F26`; the in-fight name plate is written by `$1F864`–`$1F8CE` from byte table `$6E9D0` (read at `$1F886`), then drawn by the fix-layer text engine (`$1ED44`, offsets `$6EA9E`) | a shared presentation map: 64-byte table at `$53100` (identity, `$30` = source fighter), routine `$53140`, trampolines from `$53150`, jumped to from the seven sites | `wire_slot_lookups.py` for the clone; Guile phase 4 adds its own art ([ticket 13](issues/13-rehearsal-selection-presentation.md)) |
| Victory screen: winner sprite and animation, win quote, name plate | the winning team's three bytes (colour bits 7-6, ID 5-0) are copied at `$E202` into the screen object (`$144`–`$146`), which then reads a word table of 37 entries at `$E756` (animation, zero for `$30`), a 16-byte-per-ID quote table in the `$200000` bank (read at `$E44A`), the rival-pair lists behind `$06BDC0` (via `$E8F2`; 64 entries, shared default) and the name table at `$0B8D90` | route the copy through the presentation map: routine at `$53200` keeps the colour bits and maps the ID (`$30` = source fighter) | `map_victory_screen.py` ([ticket 17](issues/17-victory-screen-native-and-clone.md)) |

**Found by scan, not yet exercised:** 64-entry tables with a shared default above
`$24` at `$0641E8`, `$06BDC0` (exercised by the victory screen, ticket 17), `$06D32A`, `$06D374` and `$06E9D0`. Each new slot
should check them before relying on the Rehearsal result. For `$30`, see the
[research note](research-id30-table-reads.md): only `$06BDC0` and `$06E9D0` are read,
at Kyo's entry through the presentation map.

**Known and accepted ([ticket 18](issues/18-stage-and-victory-background-clone-leader.md), owner decision; the lookup was not located):** the fight stage and the victory-screen background follow the leader's ID, so a team led by `$30` gets the default stage and background instead of the source fighter's. A second route to the same screen with the clone not leading (position 2 or 3) shows the right background.

**Known and accepted ([ticket 14](issues/14-rehearsal-intro-and-command-normals.md), owner decision; cause not identified):** with the clone as the other player's fighter, a short flame effect in the clone's intro differs from original Kyo (124 px at frame 5,000 and 17 px at frame 5,040 on the recorded route; identical from frame 5,400). It is almost unnoticeable and no fix was attempted. A new slot may show the same difference; do not treat it as a regression of the tools.

**Known and accepted ([ticket 15](issues/15-imported-frame-bank.md), owner decision):** the frame-bank routines add CPU time to every sprite the drawer draws. The game logic of original fighters is unchanged (identical per-frame traces), but whether a fighter's ground shadow is shown in a given frame depends on that time, so in some frames an original fighter's shadow appears or disappears one frame apart from the unmodified game (bottom strip only; 52–716 px in the recorded routes, both in the interpreter and native). Adding one instruction more or fewer to the drawer path changes which frames are affected. Do not treat it as a regression of a later tool.

**Guards left on purpose:** `$7A9C` (object `$2C` uses ID + `$176` as an
animation), `$19396` (team group as ID ÷ 3), the selection guards around
`$118FE` and the boss/Maki checks (`$9056`, `$D62C`).

## 3. Memory and space

- **Fixed area.** Relocated tables use `$44020`–`$52A20`; the palette and
  selection steps write up to `$52B51`; the intro tables use `$52C00`–`$52DFF`.
  `$52E00`–`$530FF` is free again (`map_opponent_rows.py` removes the diagnostic proxy
  that used `$52E00`–`$52E11`). The presentation map uses `$53100`–`$531FF`, the
  victory-screen routine `$53200`–`$5323F`, the intro-opponent routine `$53240`–`$5327F`,
  the fighter-routine index `$53280`–`$532BF`, the opponent proxy table `$532C0`–`$532FF`
  and its routine `$53300`–`$5333F`; `$53340`–`$5FFFF` is free (filler, unread in the
  observed runs).
- **Frame bank.** Every original frame directory lives in one bank (file
  `$200000`, bank value `$100000`). KOF 2003's NEO-PVC protection chip maps 8 KiB
  of RAM over `$2FE000`–`$2FFFFF` of the window: file data placed there reads back
  as chip RAM. Only about 12 KiB is free below it, less than one fighter. Imported
  frames have a bank per ID ([ticket 15](issues/15-imported-frame-bank.md),
  `relocate_frames.py`): a 64-entry table of bank values at `$53340` and routines
  at `$53440`–`$534B3`. The only frame readers are the lookup (`$0109F4`, three
  layers, bank select at `$010AB8`/`$010BF8`/`$010D26`, directory at
  `$010B0A`/`$010C38`/`$010D66`) and the drawer (three layers, bank select at
  `$0F85D4`/`$0F8704`/`$0F8834`, body reads under `$0F9452`); both select the bank
  themselves. An own-bank frame pointer (`+$60`, `+$6E`, `+$7C`) carries its ID in
  the top byte, so the copies made at `$028B14` and `$04143E` keep their bank. The
  Rehearsal's copy is at file `$700000`; free banked space is `$300000`–`$37FFFF`
  and `$69D1C6`–`$8FFFFF` (bank values below `$100000` mean "fixed area").
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
   Log the data registers with each read: a read whose register holds the ID
   times the entry size (`$30`×2, ×4, ×8, ×16) in the clone run, and `$1E` times
   the same in the reference run, names an ID-indexed table; compare windows that
   cover the same screen, because the two runs do not reach it on the same frame.
7. For the victory screen (ticket 17): a deterministic two-player route (P1 joins,
   P2 joins and stays idle, P1 attacks, buttons stop 30 frames before the WIN
   banner so nothing skips the screen) reaches it in every position and on both
   sides; compare the clone with the reference ROM at the same screen, and an
   original team before and after the change (identical frames).
8. For effects that depend on the pair (ticket 14): when the clone is the other
   player's fighter, an original on the first side can behave differently without any
   visible difference in the clone. Run the same input twice (clone and reference ROM),
   ignore per-channel colour differences up to the intended palette change (24), find the
   first frame where a fighter's pixels differ, then dump the fighters' work-RAM block
   (`KOF_REHEARSAL_DUMP`) to find the first differing byte and diff the ROM reads of that
   frame window by program counter. Change the first side's leader to a fighter that does
   not have the source fighter as a rival: the difference must vanish, or the cause is
   not a pair rule.
9. For effects that never end (ticket 14, found with the Orochinagi): record a session
   with the monitor trace on, convert the recorded P1 input transitions into a player
   input script, and replay it on the clone and the reference ROM. Equal fighter state
   words with different effect objects point at a table read by an object's owner ID.
   Diff the work RAM in 0x400-byte windows (offsets from `$100000`), diff the ROM reads of
   the frame window by program counter, and for every pair of reads at addresses
   `ID × entry size` apart compare the bytes in the clone's program image: equal bytes are
   an entry a tool already copied, different bytes are a table that still ends at `$24`.
   Quote a screenshot threshold above the palette change of the clone (40 here), because
   the colour change of the clone is larger than 24 in a few hundred pixels of the body.

## 5. Checklist for the next ID

- [ ] Run `relocate_action_tables.py`, then `wire_slot_lookups.py`, for the ID.
- [ ] Check the scan-only tables of §2.
- [ ] Place frames in the per-ID bank with `relocate_frames.py --file-offset` (ticket 15; one window, after the frame bank) and set the opponent proxy (ticket 16).
- [ ] Sound and identity lists as the character needs. Presentation: `wire_slot_lookups.py` maps the lookups; the character's own art and icon go in their tables (ticket 13 sites).
- [ ] Run `map_victory_screen.py` after `wire_slot_lookups.py`; check the winner screen in all three positions and both sides.
- [ ] Run `map_intro_opponent.py` after `map_victory_screen.py`; the map entry of `$30` decides which fighters treat it as a rival (the same entry is its presentation source).
- [ ] Run `map_fighter_handlers.py` after `map_intro_opponent.py`; replay a recorded Orochinagi-style super on the clone and the reference ROM and check that no effect outlives the move.
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
`wire_slot_lookups.py`; as linhas por adversário usam proxy (ticket 16, `map_opponent_rows.py`: tabela em `$532C0`, rotina em `$53300`); os conjuntos de tipos de caixa em `$6C62E` dão ao `$30` a entrada do lutador de origem (ticket 20, `map_hitbox_kinds.py`); os
quadros vão para um banco por ID (ticket 15); som (tickets 10–12) e apresentação
(ticket 13: mapa compartilhado em `$53100`, pelo `wire_slot_lookups.py`; arte própria na fase 4 do Guile); listas de identidade são
decididas por personagem.

**Achadas por varredura, ainda não exercitadas:** tabelas de 64 entradas com
padrão comum acima de `$24` em `$0641E8`, `$06BDC0` (exercitada pela tela de vitória, ticket 17), `$06D32A`, `$06D374` e
`$06E9D0`. Cada nova vaga deve conferi-las. Para o `$30`, veja a
[nota de pesquisa](research-id30-table-reads.md): só `$06BDC0` e `$06E9D0` são lidas,
na entrada do Kyo, pelo mapa de apresentação.

**Conhecido e aceito ([ticket 18](issues/18-stage-and-victory-background-clone-leader.md), decisão do dono; a busca não foi localizada):** o cenário da luta e o fundo da tela de vitória seguem o ID do líder; uma equipe liderada pelo `$30` recebe o cenário e o fundo padrão em vez dos do lutador de origem. Uma segunda rota até a mesma tela com o clone fora da liderança (posição 2 ou 3) mostra o fundo certo.

**Conhecido e aceito ([ticket 14](issues/14-rehearsal-intro-and-command-normals.md), decisão do dono; causa não identificada):** com o clone como lutador do outro jogador, um efeito curto de chama na intro do clone difere do Kyo original (124 px no quadro 5.000 e 17 px no quadro 5.040 na rota gravada; idêntico a partir do quadro 5.400). Quase não se nota e nenhuma correção foi tentada. Um slot novo pode mostrar a mesma diferença; não tratar como regressão das ferramentas.

**Intros de rivais (ticket 14):** a leitura do ID do outro lutador em `$40BE2` (rotina `$40BCA`, linhas nas tabelas de intro em `$52D00` e `$52C00`) passa pelo mapa de apresentação (rotina em `$53240`), pelo `map_intro_opponent.py`; rivais são escritos como IDs literais (a linha do Iori cita o Kyo), então sem o mapa o `$30` não era reconhecido como rival.

**Rotinas por lutador (ticket 19):** dois despachantes (`$2B30E` e `$2B432`) indexam uma tabela de 37 ponteiros (`$2B336` e `$2B45A`) por `4 × (ID & $3F)` e chamam com `jsr` a rotina da tabela do próprio lutador; o `$30` lia além do fim e chamava outros dados (no replay do Orochinagi as chamas do golpe não acabavam). O `map_fighter_handlers.py` passa o ID pelo mapa de apresentação (rotina em `$53280`), então o `$30` usa as rotinas do lutador de origem.

**Tela de vitória (ticket 17):** a cópia dos três bytes da equipe vencedora em `$E202` passa pelo mapa de apresentação (rotina em `$53200`, bits de cor preservados), pelo `map_victory_screen.py`. Isso corrige sprite, animação, frase e placa de nome do clone.

**Conhecido e aceito ([ticket 15](issues/15-imported-frame-bank.md), decisão do dono):** as rotinas do banco de quadros acrescentam tempo de CPU a cada sprite desenhado. A lógica dos originais não muda (traces por quadro idênticos), mas a sombra de um lutador no chão aparecer ou não num quadro depende desse tempo, então em alguns quadros a sombra de um original aparece ou some um quadro antes ou depois do jogo sem modificação (só a faixa de baixo; 52 a 716 px nas rotas gravadas, no interpretador e no nativo). Uma instrução a mais ou a menos no desenhista muda quais quadros são afetados. Não tratar como regressão de uma ferramenta posterior.

**Travas mantidas de propósito:** `$7A9C`, `$19396`, as travas da seleção perto
de `$118FE` e as checagens de chefes/Maki (`$9056`, `$D62C`).

### 3. Memória e espaço

- **Área fixa.** Tabelas movidas em `$44020`–`$52A20`; os passos de paletas e
  seleção escrevem até `$52B51`; as tabelas de intro usam `$52C00`–`$52DFF`.
  `$52E00`–`$530FF` voltou a ficar livre (o `map_opponent_rows.py` remove o proxy de
  diagnóstico). O mapa de apresentação usa `$53100`–`$531FF`; rotinas e tabelas dos
  tickets 17, 14, 19 e 16 ocupam `$53200`–`$5333F`; `$53340`–`$5FFFF` está livre.
- **Banco de quadros.** Todos os diretórios originais ficam num banco (arquivo
  `$200000`, valor de banco `$100000`). O chip de proteção NEO-PVC mapeia 8 KiB de
  RAM sobre `$2FE000`–`$2FFFFF` da janela: dado do arquivo colocado ali é lido como
  RAM do chip. Só cerca de 12 KiB estão livres abaixo dela, menos que um lutador.
  Os importados têm banco por ID ([ticket 15](issues/15-imported-frame-bank.md),
  `relocate_frames.py`): tabela de 64 valores de banco em `$53340` e rotinas em
  `$53440`–`$534B3`. Os únicos leitores de quadros são a busca (`$0109F4`, três
  camadas) e o desenhista (três camadas, leituras sob `$0F9452`), e os dois
  escolhem o banco por conta própria. O ponteiro de quadro de banco próprio leva o
  ID no byte de cima, então as cópias feitas em `$028B14` e `$04143E` continuam no
  banco certo. A cópia do Ensaio fica no arquivo em `$700000`; espaço livre com
  banco: `$300000`–`$37FFFF` e `$69D1C6`–`$8FFFFF`.
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
   Registre também os registradores de dados em cada leitura: uma leitura cujo
   registrador vale o ID vezes o tamanho da entrada (`$30`×2, ×4, ×8, ×16) na
   execução do clone, e `$1E` vezes o mesmo na de referência, nomeia uma tabela
   indexada por ID; compare janelas que cubram a mesma tela, pois as duas
   execuções não chegam a ela no mesmo quadro.
7. Para a tela de vitória (ticket 17): uma rota determinística de dois jogadores
   (P1 entra, P2 entra e fica parado, P1 ataca, botões param 30 quadros antes do
   banner WIN para nada pular a tela) chega a ela em qualquer posição e nos dois
   lados; compare o clone com a ROM de referência na mesma tela, e uma equipe
   original antes e depois da mudança (quadros idênticos).
8. Para efeitos que dependem do par (ticket 14): quando o clone é o lutador do outro
   jogador, um original do primeiro lado pode se comportar diferente sem nenhuma
   diferença visível no clone. Rodar a mesma entrada duas vezes (ROM do clone e de
   referência), ignorar diferenças de cor por canal até a mudança de paleta pretendida
   (24), achar o primeiro quadro em que os pixels de um lutador diferem, despejar o bloco
   de RAM dos lutadores (`KOF_REHEARSAL_DUMP`) para achar o primeiro byte diferente e
   comparar as leituras da ROM da janela por contador de programa. Trocar o líder do
   primeiro lado por um lutador que não tenha o lutador de origem como rival: a diferença
   precisa sumir, senão a causa não é uma regra de par.
9. Para efeitos que não acabam (ticket 14, achado com o Orochinagi): gravar uma sessão com
   o rastreio do monitor ligado, converter as transições de entrada do P1 gravadas num
   roteiro de entrada do player e repetir no clone e na ROM de referência. Palavras de
   estado do lutador iguais com objetos de efeito diferentes apontam uma tabela lida pelo ID
   do dono do objeto. Comparar a RAM em janelas de 0x400 bytes (deslocamentos a partir de
   `$100000`), comparar as leituras da ROM da janela por contador de programa e, para cada
   par de leituras em endereços separados por `ID × tamanho da entrada`, comparar os bytes na
   imagem do clone: bytes iguais são entrada que uma ferramenta já copiou, bytes diferentes
   são tabela que ainda termina em `$24`. Usar um limite de captura acima da mudança de paleta
   do clone (40 aqui), porque a cor do clone muda mais que 24 em algumas centenas de pixels do corpo.

### 5. Checklist para o próximo ID

- [ ] Rodar `relocate_action_tables.py` e depois `wire_slot_lookups.py` para o ID.
- [ ] Conferir as tabelas só achadas por varredura (seção 2).
- [ ] Quadros no banco por ID com `relocate_frames.py --file-offset` (ticket 15; uma janela, depois do banco de quadros) e proxy de adversário (ticket 16).
- [ ] Som e listas de identidade conforme o personagem. Apresentação: `wire_slot_lookups.py` mapeia as buscas; a arte e o ícone do personagem entram nas tabelas dos pontos do ticket 13.
- [ ] Rodar `map_victory_screen.py` depois do `wire_slot_lookups.py`; conferir a tela de vencedor nas três posições e nos dois lados.
- [ ] Rodar `map_intro_opponent.py` depois do `map_victory_screen.py`; a entrada do `$30` no mapa decide quais lutadores o tratam como rival (a mesma entrada é a origem da apresentação).
- [ ] Rodar `map_fighter_handlers.py` depois do `map_intro_opponent.py`; repetir um super gravado, como o Orochinagi, no clone e na ROM de referência e conferir que nenhum efeito sobrevive ao golpe.
- [ ] Conferência diferencial contra a origem e regressão dos originais.
