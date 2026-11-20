---
title: "Read imported fighters' per-opponent rows through a proxy"
triage: ready-for-agent
assignee: claude
---

# 16 Read imported fighters' per-opponent rows through a proxy

Claimed by Codex on 2026-11-19; continued and closed by Claude on 2026-11-20. /
Assumido pelo Codex em 19/11/2026; continuado e concluído pelo Claude em 20/11/2026.

[Parent specification](../spec.md) · [Diagnosis](14-rehearsal-intro-and-command-normals.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

The readers at `$216AC` and `$21836` index 42-byte per-opponent rows by the
other fighter's ID, in tables of 37 rows. By the owner's decision, an imported
ID is read through a proxy: a 64-entry byte table maps each ID to the original
fighter whose rows are used (identity for `$00`–`$24`; `$1E` for the `$30`
rehearsal; Guile's proxy is chosen later). Replace the diagnostic patch with
this table and a checked tool step, and search for other readers that index
per-opponent data by ID.

## Acceptance criteria

- [x] Search for every reader that indexes rows by the other fighter's ID
  (including multiples other than 42) and list them.
- [x] A preparation step installs the proxy table and the reader changes with
  byte checks and tests on invented data; the proxy for `$30` is a parameter.
- [x] In the differential loop, the grab and its aftermath equal original Kyo's
  with the clone attacking and being grabbed; the native build reports no new
  fallback after profiling.
- [x] Original fighters facing originals are unchanged in a regression check
  beyond Kyo.

## Português (Brasil)

# 16 Ler as linhas por adversário dos importados por um proxy

_Os leitores em `$216AC` e `$21836` indexam linhas de 42 bytes por adversário
pelo ID do outro lutador, em tabelas de 37 linhas. Por decisão do dono, um ID
importado é lido por um proxy: uma tabela de 64 bytes associa cada ID ao lutador
original cujas linhas são usadas (identidade para `$00`–`$24`; `$1E` para o
ensaio no `$30`; o proxy do Guile será escolhido depois). Trocar o remendo de
diagnóstico por essa tabela e um passo de ferramenta verificado, e procurar
outros leitores que indexem dados por adversário pelo ID._

### Critérios de aceitação

- [x] Procurar todo leitor que indexe linhas pelo ID do outro lutador
  (inclusive múltiplos diferentes de 42) e listá-los.
- [x] Um passo de preparo instala a tabela de proxy e as mudanças nos leitores,
  com conferência de bytes e testes com dados inventados; o proxy do `$30` é um
  parâmetro.
- [x] No ciclo diferencial, o agarrão e o que vem depois igualam os do Kyo
  original com o clone agarrando e sendo agarrado; o build nativo não mostra
  novo fallback após o perfil.
- [x] Originais contra originais ficam inalterados numa conferência de regressão
  além do Kyo.

## Comments

### 2026-11-19 — Evidence from ticket 13

The fight divergence with `$30` as the other player's fighter (4,789 px at frame
6,100 on the ticket 13 script) exists with the diagnostic proxy at `$52E00`
already installed, so another reader of per-opponent data may still index by the
raw ID; use that script as one of the loops for the reader search in the first
criterion. See [13](13-rehearsal-selection-presentation.md).

_PT-BR: a divergência de luta com o `$30` como lutador do outro jogador (4.789 px
no quadro 6.100 do roteiro do ticket 13) existe com o proxy de diagnóstico em
`$52E00` já instalado, então outra leitura de dados por adversário pode ainda
indexar pelo ID bruto; usar esse roteiro como um dos laços da busca de leitores
do primeiro critério. Ver [13](13-rehearsal-selection-presentation.md)._

### 2026-11-20 — Resolution: proxy table installed by a checked tool

**Tool.** `tools/kof2003/import_slot/map_opponent_rows.py SOURCE DEST --sha256 HASH
--proxy 0x1E` (after `map_fighter_handlers.py`). It writes a 64-byte proxy table at
`$532C0` (identity for `$00`–`$24`, the `--proxy` value for `$30`, `$1E` for the other
unassigned IDs until each import chooses its own) and a 24-byte routine at `$53300` that
reads the other fighter's ID, maps it through the table and returns the 42-byte row
offset, preserving `a0`. Both readers (`$216AC`, `$21836`) call it in place of their
original eight bytes. It accepts the original readers (checked by fingerprint) or the old
diagnostic patch, which it removes (`$52E00`–`$52E11` returns to filler). `--proxy` must be
an original ID. Four tests on invented data cover the result, refused inputs and refused
paths. A private CPU check (Musashi, outside the repository) ran the patched readers for
all 64 IDs at both sites: offset `42 × proxy(ID)`, registers preserved (128 cases).
Like the original readers, the routine indexes by the whole byte at `+$1F` (IDs stay
below `$40`). The tool takes one proxy, for `$30`; when Guile gets his own ID the tool
needs a proxy per imported ID.

**Reader search (first criterion).** Static: every program reference to the ID fields
(`+$1E`, `+$1F`, `+$19F`) of a second object was listed privately and read in context.
Dynamic: ROM reads were traced by program counter in the interpreter for the clone and
the reference in five windows (clone throwing and being thrown, frames 5,488–5,600 and
5,788–5,900; the ticket 13 route, 5,400–6,100), and every pair of reads whose register
held `$30 × k` against `$1E × k` was checked in the clone image.

| Reader | Data | Indexed by | State |
|---|---|---|---|
| `$216AC`, `$21836` | 42-byte per-opponent rows | other fighter's ID | proxy (this ticket) |
| `$240E6`, `$24CF6`/`$24D06` | fighter-pair matrix, relocated to `$4EA20` | own ID × `$100` + other ID × 4 | both axes equal to Kyo's (75 cells checked) |
| `$21332` | 64 × 64 pair byte table `$6F312` | row: one fighter, column: the other | equal to Kyo's for both axes (77 cells); no change needed |
| `$166A8`, `$28C30`–`$28CA0` | 64-byte rows `$44020`–`$4C020` | ID × 64 + other value | relocated tables; reads equal in all windows |
| `$40B90` | identity lists `$A5F1F` | the other object's ID, compared literally | `$1E` is in two groups, `$30` in none; membership is a per-character choice (slot anatomy) |
| `$193B0`, `$1941E` | team group, ID ÷ 3 | the other object's ID | guard left on purpose |
| `$15D08`, `$169CA` | 64-entry pointer table `$6C62E` to 16-byte hit-box kind sets | the box owner's ID | **not covered**: `$30` gets the shared default (fighter `$24`'s set), which differs from Kyo's in 2 bits. Read with `$30` in the ticket 13 window. See [20](20-imported-hitbox-kind-set.md) |

Other ID-indexed reads at different addresses were the clone's own frame data in its
bank (`$010B10`–`$010B3E`, `$0FA3AC`, `$0FA408`; different by design, ticket 15).

**Differential loop (third criterion).** Interpreter, `roms-t16` against `roms-ref`:
after the fight starts the clone's state words (state, action, frame) are equal to
original Kyo's on every frame, with the clone throwing and with the clone thrown (the
only differences are one extra event at frame 5,199, before the fight, from the accepted
ticket 14 intro residual). The stage differs because the clone leads (ticket 18), so
whole-screen captures are not comparable on this route. The ticket 13 route: 0 px with
`--tol 24` at 5,400, 5,800, 6,000 and 6,100, so the 4,789 px divergence noted above is
gone. Native `build-t16` against native `build-t14d` (diagnostic): identical state words
on all four routes, and the same interpreted-instruction and uncovered-entry counts
(20/3, 20/3, 0/0, 6,755/4); the new routine is compiled.

**Regression (fourth criterion).** Interpreter, `roms-t16` against the unmodified
control program: two original teams (`$1F,$10,$14` against `$1D,$1B,$1C`, P1 attacking;
`$1D,$1B,$1C` against `$1E,$0F,$13`, P2 attacking) to frame 9,000: 0 px at five frames
and identical state words on all 9,001 frames.

**Candidate.** `private/work/first-import/diag-t17/roms-t16` with `build-t16`; the
`Jogar-Ensaio.cmd` shortcut opens it.

_PT-BR: **Ferramenta.** `map_opponent_rows.py ORIGEM DESTINO --sha256 HASH --proxy 0x1E`
(depois do `map_fighter_handlers.py`) grava uma tabela de proxy de 64 bytes em `$532C0`
(identidade de `$00` a `$24`, o valor de `--proxy` no `$30`, `$1E` nos demais IDs ainda sem
dono) e uma rotina de 24 bytes em `$53300` que lê o ID do outro lutador, passa pela tabela e
devolve o deslocamento da linha de 42 bytes. Os dois leitores chamam essa rotina. Aceita os
leitores originais ou o remendo de diagnóstico, que ela remove. Quatro testes com dados
inventados; uma conferência privada de CPU executou os dois leitores para os 64 IDs (128
casos). Como os leitores originais, a rotina indexa pelo byte inteiro em `+$1F`. A
ferramenta recebe um proxy, o do `$30`; quando o Guile tiver o próprio ID, ela vai precisar
de um proxy por ID importado._

_**Busca de leitores.** Estática (todas as referências aos campos de ID de outro objeto) e
dinâmica (leituras da ROM por contador de programa no agarrão nos dois sentidos e no
roteiro do ticket 13). A tabela acima lista o resultado. Um leitor ainda não está coberto:
`$15D08`/`$169CA` (tabela `$6C62E`, conjuntos de tipos de caixa de golpe por lutador),
em que o `$30` recebe o conjunto do lutador `$24`, diferente do do Kyo em 2 bits. Vai para o
[ticket 20](20-imported-hitbox-kind-set.md)._

_**Laço diferencial.** No interpretador, depois do início da luta, as palavras de estado do
clone são iguais às do Kyo original em todos os quadros, agarrando e sendo agarrado. O
cenário difere porque o clone lidera (ticket 18), então as capturas de tela inteira não
servem nessa rota. Rota do ticket 13: 0 px com `--tol 24`; a divergência de 4.789 px
sumiu. Nativo `build-t16` contra `build-t14d`: estados idênticos nas quatro rotas e as
mesmas contagens de instruções interpretadas e entradas não cobertas._

_**Regressão.** Duas equipes só de originais contra o programa de controle sem alterações:
0 px em cinco quadros e estados idênticos nos 9.001 quadros._

_**Candidato.** `roms-t16` com `build-t16`; o atalho `Jogar-Ensaio.cmd` abre esse candidato._
