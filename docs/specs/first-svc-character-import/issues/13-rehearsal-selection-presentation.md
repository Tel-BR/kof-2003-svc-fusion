---
title: "Repair the Kyo rehearsal selection presentation"
triage: ready-for-agent
---

# 13 Repair the Kyo rehearsal selection presentation

[Parent specification](../spec.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

Make the provisional `$30` Kyo rehearsal identify itself consistently in the
selection flow. In the owner's manual test, its name, small thumbnail, large
portrait and team position were missing or corrupted; some displayed material
belonged to Jhun. Reuse the Kyo original's presentation for this rehearsal where
appropriate and preserve all original fighters' selection entries. Do not treat
this as Guile's later portrait, icon or palette acceptance.

## Acceptance criteria

- [x] Reproduce and record which selection and order-selection components fail
  for `$30`, including team positions 1, 2 and 3.
- [x] Show the intended Kyo name, small and large images, and team position for
  the clone without changing the original Kyo or Jhun entries.
- [x] Check original Kyo and `$30` selected together on the same team and check
  the other player side where the same presentation path is used.
- [x] Keep game-derived art, captures and logs in `private/`; record only
  addresses, counts, hashes and observations in tracked files.

## Português (Brasil)

# 13 Corrigir a apresentação do Kyo do ensaio na seleção

Fazer o Kyo provisório `$30` identificar-se de forma consistente na seleção.
No teste manual do dono, nome, miniatura, retrato grande e posição de equipe
faltaram ou apareceram corrompidos; parte do material exibido era do Jhun.
Reaproveitar a apresentação do Kyo original neste ensaio quando adequado e
preservar as entradas de todos os lutadores originais. Isso não aprova o
retrato, o ícone nem as paletas que serão preparados depois para o Guile.

### Critérios de aceitação

- [x] Reproduzir e registrar quais componentes da seleção e da escolha de ordem
  falham para `$30`, inclusive nas posições 1, 2 e 3 da equipe.
- [x] Mostrar nome, imagem pequena, imagem grande e posição de equipe esperados
  para o clone, sem mudar as entradas originais do Kyo ou do Jhun.
- [x] Conferir Kyo original e `$30` juntos na mesma equipe e o outro lado do
  jogador quando usar o mesmo caminho de apresentação.
- [x] Manter artes derivadas do jogo, capturas e logs em `private/`; registrar
  nos arquivos rastreados somente endereços, contagens, hashes e observações.

## Comments

### 2026-11-18 — Owner decision: extend the tables, do not polish the art

Under the owner's "no unexplained difference" bar for the Rehearsal (see
[14](14-rehearsal-intro-and-command-normals.md)), the goal here is that `$30`
reads its own entries in every selection and order-selection table instead of
falling into a neighbour such as Jhun. Pointing those entries at Kyo's existing
presentation is enough; art quality for the clone is not a goal. The tables
found here are the map phase 4 will fill with Guile's presentation.

_PT-BR: pelo critério do dono de "nenhuma diferença inexplicada" para o Ensaio
(ver [14](14-rehearsal-intro-and-command-normals.md)), o objetivo aqui é o `$30`
ler as próprias entradas em todas as tabelas da seleção e da escolha de ordem,
em vez de cair num vizinho como o Jhun. Apontar essas entradas para a
apresentação existente do Kyo basta; a qualidade da arte do clone não é
objetivo. As tabelas encontradas aqui são o mapa que a fase 4 preencherá com a
apresentação do Guile._

### 2026-11-18 — Owner decision: map presentation on the clone first

After the owner confirmed that the clone plays like Kyo, the remaining
differences are the name under the life bars, portraits and icon. These are
looked up by ID and Guile's phase 4 needs the same tables. The owner chose to
keep this ticket and map them on the clone first, pointing `$30` at Kyo's
existing presentation, so that table mapping is proven with known-good art
before Guile's converted art is added. Record the tables found in
[slot anatomy](../slot-anatomy.md).

_PT-BR: depois de o dono confirmar que o clone joga como o Kyo, as diferenças
restantes são o nome abaixo das barras de vida, os retratos e o ícone. Eles são
buscados por ID, e a fase 4 do Guile precisa das mesmas tabelas. O dono decidiu
manter este ticket e mapeá-las primeiro no clone, apontando o `$30` para a
apresentação existente do Kyo, para comprovar o mapeamento das tabelas com arte
que já funciona antes de acrescentar a arte convertida do Guile. Registrar as
tabelas encontradas em [anatomia da vaga](../slot-anatomy.md)._

### 2026-11-19 — Cause found, fixed in the tool and checked

**Cause.** Every per-ID presentation lookup was written for the 37 original
fighters and only handles IDs up to `$24` (`$22`–`$24` are hidden entries). It
either adds a constant to the ID and uses the sum as an animation or object
number, divides the ID by 3 for a palette group, or indexes a byte table of 37
entries. `$30` falls outside all of them. Seven code sites read the ID this way:
selection name (`$9042`), large portrait (`$9124`), thumbnail (`$91FE`), group
and palette (`$9338`); order screen portrait (`$9E00`) and group (`$9F26`); and
the name under the life bars (`$1F886`, in the writer loop `$1F864`–`$1F8CE`),
which indexes byte table `$6E9D0` and, for `$30`, reads past it into the blank
name entry. The same two selection and name-plate paths serve both players (the
name-index words are at `$10A4CC`–`$10A4D8` for player 1 and `$10A52A`–`$10A536`
for player 2).

**Fix.** `wire_slot_lookups.py` now adds a presentation map: a 64-byte table at
`$53100` (identity for every ID, `$30` holds the source fighter), a 16-byte
lookup routine at `$53140` and four small trampolines from `$53150`; each of the
seven sites is replaced by a jump to its trampoline, which repeats the displaced
instructions around the lookup. Original IDs map to themselves, so the original
Kyo and Jhun entries are not touched. The tool refuses source IDs `$22`–`$24`,
a changed site, or an occupied map area. `$52E00` is not used: the diagnostic
candidate keeps proxy code there. Tests: two new byte-level cases in
`tests/test_wire_slot_lookups.py` (red before the change, 6 of 6 now).

**Loop used.** A differential run in the headless player: the reference ROM and
the clone differ in one selection-cell byte (`$30` against `$1E` at `0x52B0F`),
so any difference is caused by `$30`. A script selects the clone on team
position 1, 2 and 3 (and, separately, on the other player side) and takes
screenshots of the selection, order screen and the first frames of the fight; a
checker compares them region by region. Before the fix the name, portraits,
thumbnail and name plate differed; with the map, positions 1, 2 and 3 compare
equal in portrait, thumbnail, order screen and name plate (12 of 12 checks), and
the other player side's selection and top-of-screen name region differ by 0
pixels. The lookup sites were found by an interpreter-only trace of ROM data
reads (private, temporary; no instrumentation is in tracked code) diffed between
the two runs. Captures, scripts and traces stay in `private/`.

**Checked later the same day (player available again).** The loop was run again
on the validated candidate in a fresh output folder: GREEN, 12 of 12 components
at 0 pixels. Original Kyo and `$30` on the same team (team bytes `1e,30,03`): the
order screen shows two Kyo portraits and the name plate reads Kyo for the
original; the original-only duplicate check against the reference ROM is not
possible because the original game does not let the same fighter be picked twice
(the reference team diverged to `1e,08,12`). Regression of the originals: a
scripted selection with only original fighters (team `1e,1f,0f`) compared with
the candidate before the presentation map gives 0 differing pixels in the
selection, the order screen and the fight start (frames 3650, 3750, 3850, 4300,
6100). Both runs used `--interp`.

**Closing checks (2026-11-19).**

- **Image made by the tool.** `wire_slot_lookups.py` ran end to end on a real
  image chain (relocated tables, palettes, selection cells, then this tool), and
  its presentation bytes (the seven sites and `$53100`–`$531FF`) equal, byte for
  byte, those of the candidate that the loop used, which was produced by the
  tool's own presentation step on the current diagnostic candidate (190 bytes
  changed). The loop on that candidate is GREEN, 12 of 12 at 0 pixels. Note: the
  frame-relocation step of the README recipe now refuses (frame bank, ticket 15),
  so the full recipe cannot be replayed until ticket 15 updates it.
- **Native build.** A separate native build of that candidate (own build folder
  under `private/`, 67 steps, the manual build untouched) gives the same GREEN,
  12 of 12 at 0 pixels, without `--interp`. `--verify` on the three team
  positions: 0 state mismatches in 3.78 M, 3.72 M and 3.78 M blocks, 100 % native
  instructions; 17, 5 and 0 interpreted instructions through 6, 2 and 0 uncovered
  entry points. None of those entries is in the code added here: they are at
  `$42574`, `$42584`, `$42784`, `$43724`, `$4372E`, `$43874`, `$43888` and
  `$43892`, six of which were already in the manual build's list of misses.
  Cycle-count differences between native and interpreted blocks (about 2,400 per
  run) are the known kind and are not state mismatches.
- **Full-frame differences at the start of the fight.** Team position 1
  (1,408 px, bounding box on player 1's fighter, largest channel difference 24,
  that is 3 levels of the 5-bit channels) is the intended palette change of the
  Rehearsal clone ([`rehearsal_palettes.py`](../../../../tools/kof2003/import_slot/README.md)),
  not a presentation defect. Positions 2 and 3 show 0 px because `$30` is not
  the fighter on screen. The other player side (4,789 px, channel differences up
  to 251) is a fight divergence: the opponent and the background animate
  differently when `$30` is the other fighter. It is also present without the
  presentation map (4,922 px on the same script and the same frame), so it is not
  caused by this change; it belongs to the behaviour work of
  [ticket 14](14-rehearsal-intro-and-command-normals.md) and to the per-opponent
  readers of [ticket 16](16-imported-opponent-proxy.md), whose reader search is
  still open.
- The tables are recorded in [slot anatomy](../slot-anatomy.md) (§2 and §4).

All four acceptance criteria are met for the clone. What remains is outside this
ticket.

_PT-BR: **Causa encontrada, correção na ferramenta e conferências finais.** Toda busca de apresentação por ID foi escrita para os 37 lutadores
originais e só trata IDs até `$24` (`$22`–`$24` são entradas ocultas): soma uma
constante ao ID e usa o resultado como animação ou objeto, divide o ID por 3
para o grupo de paleta ou indexa uma tabela de bytes de 37 entradas. O `$30`
fica fora de todas. São sete pontos de código: nome na seleção (`$9042`), retrato
grande (`$9124`), miniatura (`$91FE`), grupo e paleta (`$9338`); retrato (`$9E00`)
e grupo (`$9F26`) na escolha de ordem; e o nome sob as barras de vida (`$1F886`,
no laço `$1F864`–`$1F8CE`), que indexa a tabela de bytes `$6E9D0` e, para o
`$30`, lê além dela e cai na entrada de nome em branco. Os mesmos caminhos
atendem os dois jogadores (palavras de índice de nome em `$10A4CC`–`$10A4D8` para
o jogador 1 e `$10A52A`–`$10A536` para o 2). **Correção:** o
`wire_slot_lookups.py` agora acrescenta um mapa de apresentação: tabela de 64
bytes em `$53100` (identidade para todo ID; o `$30` guarda o lutador de origem),
rotina de busca de 16 bytes em `$53140` e quatro trampolins pequenos a partir de
`$53150`; cada um dos sete pontos vira um salto para seu trampolim, que repete as
instruções deslocadas em volta da busca. Os IDs originais mapeiam para si
mesmos, então as entradas do Kyo e do Jhun originais não são tocadas. A
ferramenta recusa origem `$22`–`$24`, ponto alterado ou área do mapa ocupada;
`$52E00` não é usado porque o candidato de diagnóstico guarda código de proxy ali.
Testes: dois casos novos de bytes (vermelhos antes, 6 de 6 agora). **Laço:**
execução diferencial no player sem janela; a ROM de referência e o clone diferem
em um byte da célula da seleção (`$30` contra `$1E` em `0x52B0F`), então toda
diferença vem do `$30`. Um roteiro escolhe o clone nas posições 1, 2 e 3 (e,
separado, no outro lado) e tira capturas da seleção, da ordem e dos primeiros
quadros da luta; um verificador compara por região. Antes da correção nome,
retratos, miniatura e nome sob as barras diferiam; com o mapa, as posições 1, 2
e 3 ficam iguais em retrato, miniatura, ordem e nome (12 de 12 conferências), e a
seleção e a região do nome no outro lado diferem 0 pixels. Os pontos foram
achados por trace, só no interpretador, das leituras de dados da ROM comparado
entre as duas execuções (privado e temporário; nada disso está no código
rastreado). Capturas, roteiros e traces ficam em `private/`. **Conferido depois, no mesmo dia (player de volta):** o laço rodou de novo no
candidato validado, em pasta nova: VERDE, 12 de 12 componentes com 0 pixels. Kyo
original e `$30` na mesma equipe (bytes `1e,30,03`): a tela de ordem mostra dois
retratos do Kyo e o nome sob a barra mostra Kyo para o original; a comparação com
a ROM de referência não vale para esse caso porque o jogo original não deixa
escolher o mesmo lutador duas vezes (a equipe da referência divergiu para
`1e,08,12`). Regressão dos originais: seleção por roteiro só com lutadores
originais (equipe `1e,1f,0f`) comparada com o candidato anterior ao mapa dá 0
pixels de diferença na seleção, na ordem e no início da luta (quadros 3650, 3750,
3850, 4300, 6100). As duas execuções usaram `--interp`. **Conferências finais (19/11/2026).** *Imagem feita pela ferramenta:* o
`wire_slot_lookups.py` rodou de ponta a ponta numa cadeia real (tabelas movidas,
paletas, células de seleção, depois esta ferramenta) e os bytes de apresentação
dela (os sete pontos e `$53100`–`$531FF`) são iguais, byte a byte, aos do
candidato usado no laço, produzido pela própria etapa de apresentação da
ferramenta sobre o candidato de diagnóstico atual (190 bytes alterados). O laço
nesse candidato dá VERDE, 12 de 12 com 0 pixels. Observação: a etapa de mover
quadros da receita do README agora recusa (banco de quadros, ticket 15), então a
receita completa só pode ser repetida quando o ticket 15 a atualizar. *Build
nativo:* um build nativo separado desse candidato (pasta própria em `private/`,
67 passos, o build manual intacto) dá o mesmo VERDE, 12 de 12 com 0 pixels, sem
`--interp`. `--verify` nas três posições: 0 divergências de estado em 3,78 M,
3,72 M e 3,78 M de blocos, 100 % das instruções nativas; 17, 5 e 0 instruções
interpretadas por 6, 2 e 0 entradas sem cobertura. Nenhuma está no código
acrescentado aqui: ficam em `$42574`, `$42584`, `$42784`, `$43724`, `$4372E`,
`$43874`, `$43888` e `$43892`, seis delas já na lista de falhas do build manual.
As diferenças de ciclos entre blocos nativos e interpretados (cerca de 2.400 por
execução) são do tipo já conhecido, não divergências de estado. *Diferenças de
quadro inteiro no início da luta:* a posição 1 (1.408 px, caixa sobre o lutador
do jogador 1, maior diferença de canal 24, ou seja 3 níveis dos canais de 5 bits)
é a mudança de paleta pretendida do clone do Ensaio (`rehearsal_palettes.py`),
não defeito de apresentação. As posições 2 e 3 dão 0 px porque o `$30` não é o
lutador na tela. O outro lado do jogador (4.789 px, diferenças de canal até 251)
é divergência de luta: o adversário e o cenário animam diferente quando o `$30` é
o outro lutador. Ela existe também sem o mapa de apresentação (4.922 px no mesmo
roteiro e no mesmo quadro), logo não é causada por esta mudança; pertence ao
trabalho de comportamento do [ticket 14](14-rehearsal-intro-and-command-normals.md)
e às leituras por adversário do [ticket 16](16-imported-opponent-proxy.md), cuja
busca de leitores segue aberta. As tabelas estão na [anatomia da vaga](../slot-anatomy.md)
(§2 e §4). Os quatro critérios de aceitação estão cumpridos para o clone; o que
resta fica fora deste ticket._
