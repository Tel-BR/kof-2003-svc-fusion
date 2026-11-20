---
title: "Place imported frame data in a per-ID frame bank"
triage: ready-for-agent
assignee: claude
---

# 15 Place imported frame data in a per-ID frame bank

[Parent specification](../spec.md) · [Diagnosis](14-rehearsal-intro-and-command-normals.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

All fighter frame directories live in one program bank, whose top 8 KiB is
covered by the NEO-PVC RAM window at `$2FE000`; only about 12 KiB is free below
it, less than Kyo's 18 KiB directory. By the owner's decision, frame data for IDs
`$30` and above lives in another bank selected per ID. Find every reader of
frame data (the lookup at `$010AF8`–`$010B42` and later reads through the frame
pointer at object `+$60`), make them select the right bank for imported IDs, and
place the clone's frame copy there with its tiles in the Added Space.

## Acceptance criteria

- [x] List every routine that reads frame directories or frame bodies, with how
  it selects the bank; record any reader that assumes the current bank.
- [x] The preparation tooling places the `$30` frame copy outside the frame bank
  and the PVC window, and refuses unchecked placements.
- [x] In the differential loop, the clone's frozen pre-intro frame, intro and
  in-fight trace equal original Kyo's; the native build reports no new fallback.
- [x] Original fighters are unchanged: no original frame directory is
  overwritten, and a regression check covers originals beyond Kyo, including
  `$00`. (Shadow-phase residual accepted by the owner; see the last comment.)

## Português (Brasil)

# 15 Colocar os quadros dos importados num banco de quadros por ID

_Todos os diretórios de quadros ficam num único banco do programa, cujos 8 KiB
finais são cobertos pela janela de RAM do NEO-PVC em `$2FE000`; só cerca de
12 KiB estão livres abaixo dela, menos que os 18 KiB do diretório do Kyo. Por
decisão do dono, os quadros dos IDs `$30` em diante ficam em outro banco,
escolhido por ID. Achar todo leitor de dados de quadro (a busca em
`$010AF8`–`$010B42` e as leituras posteriores pelo ponteiro de quadro em
`+$60` do objeto), fazê-los escolher o banco certo para IDs importados e
colocar ali a cópia de quadros do clone, com os tiles no Espaço acrescentado._

### Critérios de aceitação

- [x] Listar toda rotina que lê diretórios ou corpos de quadro e como ela
  escolhe o banco; registrar qualquer leitor que suponha o banco atual.
- [x] As ferramentas de preparo colocam a cópia de quadros do `$30` fora do
  banco de quadros e da janela do PVC e recusam posições não verificadas.
- [x] No ciclo diferencial, o quadro congelado antes da intro, a intro e o trace
  em luta do clone igualam os do Kyo original; o build nativo não mostra novo
  fallback.
- [x] Os originais ficam inalterados: nenhum diretório original é sobrescrito, e
  uma conferência de regressão cobre originais além do Kyo, inclusive o `$00`.
  (Resíduo de fase das sombras aceito pelo dono; ver o último comentário.)

## Comments

### 2026-11-20 — Progress (session stopped early): readers found, tool written, native check pending

**Readers (first criterion, done).** Static scan of every write to `$2FF000` and every
reference to `+$60`/`+$6E`/`+$7C`, plus a private interpreter census of every read whose
file address falls in the frame bank (five routes: Kyo, clone, ticket 13 P2 route, original
regression, victory route; tracer `diag-t15/runtime-t15`, never committed):

| Routine | What it reads | How it selects the bank |
|---|---|---|
| Lookup `$0109F4` (layers at `$010B0A`, `$010C38`, `$010D66`; reads `$010B10`–`$010B3E`, `$010C3E`–`$010C6C`, `$010D6C`–`$010D9A`) | directory table, directory, frame header; stores `+$60`, `+$6E`, `+$7C` | explicit `$100000` at `$010AB8`, `$010BF8`, `$010D26`; restores the step-script bank afterwards |
| Drawer, three layers (`$0F85D4`, `$0F8704`, `$0F8834`; copies the pointer to `$7A6(a5)`, calls `$0F9452`; body reads `$0F971E`–`$0FA7D4`) | frame bodies | explicit `$100000` before each layer; leaves it selected |
| Copiers `$028B14`/`$028B3E`/`$028B68`, `$04143E`/`$041468`/`$041492` | none (copy the pointers into another object) | — |
| `$01411E`, `$014526` (fixed index, bank `$1D99A8`) | a non-fighter block after the directories | explicit; not ID-indexed |

No reader of frame data relies on a bank selected by someone else. Layer 3 of the lookup
was not reached in the routes (static only). The bank register has 2-byte granularity;
bank values below `$100000` mean "fixed area" to the game's pointer conversions.

**Design.** `relocate_frames.py` was rewritten (tests: 4, green): it copies the source
directory to `--file-offset` (must be even, after the frame bank, ≤ one window below the
PVC RAM, inside the program and all `$FF`), redirects tiles to the Added Space as before,
and leaves the frame bank untouched (entry `$30` keeps pointing at the source fighter).
It writes a 64-long bank table at `$53340` (frame bank for every ID except `$30`) and three
routines at `$53440`–`$534B3`: the lookup's three bank selects and three directory sites
call them, so an own-bank ID reads its directory at the start of its window and its frame
pointers carry the ID in their top byte (ignored by the 24-bit bus; the runtime masks
addresses too); the drawer's three bank selects take the bank from that top byte, so a
pointer copied into another object still reads its own bank. Originals keep untagged
pointers.

**Checks so far.** Private chain `diag-t15/chain15.py` (tool-chain-1/tables.bin → new
frames step at `0x700000` → the existing steps): the result differs from `roms-t20` only
in the nine reader sites, `$53340`–`$534B3`, the restored fighter `$00` directory and entry
`$30`, the removed old copy at `$2FB000` and the new copy at `$700000`. A private Musashi
check with a NEO-PVC bank model (`diag-t15/cpu15.c`): 22,200 original lookups (37 IDs ×
600 frames, each running all three layers) identical to the control program; all 585 clone frames give
Kyo's results with the pointer tagged `$30` at the same directory offset; unassigned IDs
untagged; drawer bank correct for all 64 tags with registers kept.

**Still to do.** (1) Native build `diag-t15/build-t15` of `roms-t15` was started; check it
links and that coverage shows no new fallback against `build-t16`. (2) Differential loop:
creation swap and in-fight swap (slot anatomy §4) with screenshots of the frozen pre-intro
frame, intro and fight, clone against original Kyo (palette tolerance). (3) Regression of
original teams (including `$00`) against the unmodified control. (4) Rerun the census on
`roms-t15` and confirm no other PC reads under the clone's bank. (5) Update the import_slot
README (new `--file-offset` argument; the chain line for `relocate_frames.py`) and slot
anatomy §3; `/code-review`; repoint `Jogar-Ensaio.cmd` to `roms-t15` + `build-t15`.

_PT-BR — Progresso (sessão interrompida): leitores achados, ferramenta escrita, conferência
nativa pendente._

_**Leitores (primeiro critério, feito).** Varredura estática e censo no interpretador das
leituras no banco de quadros: a busca (`$0109F4`, três camadas) e o desenhista (três
camadas, `$0F85D4`/`$0F8704`/`$0F8834`, leituras em `$0F971E`–`$0FA7D4`) escolhem o banco
`$100000` explicitamente; os copiadores só copiam os ponteiros; `$01411E`/`$014526` leem um
bloco que não é de lutador. Nenhum leitor depende do banco deixado por outro. A camada 3 da
busca não foi alcançada nas rotas (só estática)._

_**Projeto.** O `relocate_frames.py` foi reescrito (4 testes verdes): copia o diretório para
`--file-offset` (par, depois do banco de quadros, cabendo numa janela abaixo da RAM do PVC,
dentro do programa e todo `$FF`), não mexe no banco de quadros e instala uma tabela de bancos
por ID em `$53340` e três rotinas em `$53440`–`$534B3`. O ponteiro de quadro do ID com banco
próprio leva o ID no byte de cima (ignorado pelo barramento de 24 bits); o desenhista escolhe
o banco por esse byte, então um ponteiro copiado para outro objeto continua no banco certo._

_**Conferido.** A cadeia privada difere do `roms-t20` só onde devia; a conferência de CPU
(Musashi) deu os originais idênticos ao controle em 22.200 buscas e os 585 quadros do clone
iguais aos do Kyo._

_**Falta.** Build nativo `build-t15` (iniciado) e cobertura; ciclo diferencial (quadro
congelado, intro, luta); regressão dos originais com o `$00`; censo no `roms-t15`; README,
anatomia da vaga, `/code-review` e o atalho do Ensaio._

### 2026-11-20 — Resolution: checks done; shadow-phase residual accepted

**Native build.** `diag-t15/build-t15` (runtime with the PVC byte-write fix, `roms-t15`)
links. On the four ticket 16 routes (attack, grabbed, P2 route, original regression) its
per-frame traces equal those of the ticket 20 candidate (`build-t16`, `roms-t20`, the
diagnostic frame placement) on all 6,101 or 9,001 frames, with the same interpreted
instruction counts (20, 20, 0, 6,755) and the same missed entry points (dumped for two
routes): no new fallback.

**Differential loop (third criterion).** Creation swap (`KOF_REHEARSAL_FORCE=0x1e:0x30@4874`,
`diag-t14/moves.txt`, 7,000 frames), same image, original Kyo against the clone: state
words equal on all 7,000 frames, in the interpreter and native. Screenshots at 4,930
(before the fighters appear), 4,960 and 5,000 (frozen pre-intro frame and intro), 5,100–6,400
(intro and fight) and 6,900: no pixel differs by more than 25 per channel (the clone's
intended palette change); 4,930 and 6,900 are identical. The clone's screenshots equal
those of the diagnostic placement (`roms-t20`) exactly.

**Census on the new image.** With the clone playing (creation swap route, frames 0–7,000)
every read under the clone's bank comes from the lookup (`$010B1C`–`$010B3E`) or the
drawer's body readers (`$0F9772`–`$0FA7D4`); no other routine reads there. On the
original-only P1 route (frames 0–6,000) no read happened under the clone's bank.

**Regression (fourth criterion).** Interpreter, unmodified control program against
`roms-t15`: the P2-attacking route is identical at tolerance 0 (traces on 9,001 frames,
screenshots at 5,400–9,000). The P1 route, also with P1's leader forced to `$00` after team
order, has identical traces on all 9,001 frames; its screenshots differ only in the bottom
strip (52–716 px at six frames): a fighter's ground shadow is shown one frame earlier or
later. Ablation located it: the copy of the frames and the table changes nothing; patching
only the drawer reproduces it; the same drawer code returning a constant, or with three
extra no-ops, does not; with one extra no-op it does. It is therefore a timing effect of the
CPU time added to every sprite, not a wrong bank: the drawer's table read always returns the
frame bank for originals (no original pointer is tagged; checked by a probe). The native
player shows the same kind of difference (5,000–6,000, identical from 7,000).

**Review notes.** The one-window size check in the tool cannot fail for a source that lies in
the frame bank below the PVC RAM; it is kept as a guard. The fallback comparison is against
the ticket 20 candidate, whose native coverage was itself compared with the earlier builds
(tickets 14, 16 and 20).

**Owner decision.** Accept the shadow-phase residual and record it (slot anatomy §2). It is
cosmetic and transient; any later change in the drawer path can move it.

**Candidate.** `private/work/first-import/diag-t15/roms-t15` with `build-t15`; the
`Jogar-Ensaio.cmd` shortcut opens it.

_PT-BR — Resolução: conferências feitas; resíduo de fase das sombras aceito._

_**Build nativo.** O `diag-t15/build-t15` compila. Nas quatro rotas do ticket 16 os traces
por quadro são iguais aos do candidato do ticket 20 em todos os quadros, com as mesmas
contagens de instruções interpretadas e os mesmos pontos de entrada não cobertos: nenhum
fallback novo._

_**Ciclo diferencial.** Troca na criação, mesma imagem, Kyo original contra o clone: estados
iguais nos 7.000 quadros, no interpretador e no nativo. Capturas do quadro congelado antes
da intro, da intro e da luta: nenhuma diferença acima de 25 por canal (a mudança de paleta
pretendida do clone). As capturas do clone são idênticas às da posição de diagnóstico._

_**Regressão.** Programa de controle contra o `roms-t15`: a rota com o P2 atacando é idêntica
com tolerância 0. A rota do P1, também com o líder do P1 trocado pelo `$00`, tem traces
idênticos nos 9.001 quadros; as capturas só diferem na faixa de baixo: a sombra de um
lutador aparece um quadro antes ou depois. A ablação mostrou que é efeito de tempo de CPU do
desenhista (uma instrução a mais reproduz, três a mais não), não um banco errado. O player
nativo mostra o mesmo tipo de diferença._

_**Decisão do dono.** Aceitar o resíduo de fase das sombras e registrá-lo (anatomia da vaga
§2)._

_**Candidato.** `private/work/first-import/diag-t15/roms-t15` com `build-t15`; o atalho
`Jogar-Ensaio.cmd` abre esse candidato._
