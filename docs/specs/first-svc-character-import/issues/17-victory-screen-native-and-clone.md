---
title: "Diagnose the native victory screen and the clone's missing victory assets"
triage: ready-for-agent
---

# 17 Diagnose the native victory screen and the clone's missing victory assets

[Parent specification](../spec.md) · [Rehearsal ticket](04-complete-first-imported-match.md) · [Presentation ticket](13-rehearsal-selection-presentation.md) · Runs before [14](14-rehearsal-intro-and-command-normals.md)

Run with `/diagnosing-bugs`, following the method and checklist of
[slot anatomy](../slot-anatomy.md). Build the feedback loop first.

## What to build

Find and fix two defects of the victory screen shown after a team match. They
were found by the owner on 2026-11-19 while playing the Rehearsal candidate
([13](13-rehearsal-selection-presentation.md) mapped the selection screen, the
order screen and the name plate under the life bars, but not this screen).

**A. Native player, no clone involved.** With a team of original fighters, the
native victory screen shows the winner's name plates and win quote correctly,
but the large winner sprite is only a black silhouette and its animation does
not complete. The reference emulator (FBNeo) running the same game shows the
full-colour sprite for the same kind of team. This is a defect of the native
build or of the data it reads, and it would hit every imported fighter too.

**B. Clone (`$30`) wins.** With a team of the clone, Iori Yagami and original
Kyo Kusanagi, when the clone wins: the large sprite is wrong and a displaced
silhouette covers the "WINNER" banner and part of the screen (the owner does not
know whether it is the clone's); the win quote is wrong (a different language
and cut off at the start); and the winner's name plate is empty (the screen
shows the full name of each fighter, not only the first name). Teammates' plates
(here Iori Yagami and Kyo Kusanagi) are shown. Check the clone's plate as a
teammate when another fighter wins as well.

Start with A, because B cannot be judged while the original sprite is also a
silhouette. The owner's three prints (native with the clone winning, native with
an original team winning, and FBNeo) are in
`private/work/first-import/victory-prints/`; they are game images and never
enter git.

## Blocked by

None. [14](14-rehearsal-intro-and-command-normals.md) is blocked by this ticket.

## Acceptance criteria

- [x] A scripted, deterministic run reaches the victory screen for an original
  team and for a team with the clone winning (positions 1, 2 and 3), takes
  screenshots at fixed frames and goes red on the owner's symptoms. Record its
  command and output; keep captures and logs in `private/`.
- [x] Defect A: the cause of the silhouette-only sprite is found and classified
  (native port or runtime defect, graphics or palette loading, timing, or data);
  the fix or the decision to leave it is recorded; the winner sprite of several
  original fighters, including the owner's three, renders complete in the native
  player and agrees with the reference emulator. If the fix lives outside this
  repository's tracked files, say so and ask the owner.
- [x] Upstream check for defect A: run the same original-team victory in the
  unmodified control build (the published `v0.1.0` player and ROM preparation,
  no imported fighter, no patched program). If the silhouette appears there too,
  it is a defect of the upstream project the port comes from
  ([KOF 2003 recomp](https://github.com/omegakatana92/The-King-of-Fighters-2003),
  whose toolkit is the one adapted in the
  [Samurai Shodown recomp](https://github.com/omegakatana92/Samurai-Shodown-Recomp));
  record that, find whether the cause is in the player, the toolkit or the
  generator input, and prepare a minimal report (version, input script, frame,
  description) for the owner. On 2026-11-19 the KOF 2003 repository showed no open
  issues; its closed issues were not checked. Whether to report it or contribute a
  fix is the owner's decision; any patch is prepared in a clone under `private/`,
  not copied into this repository (see `AGENTS.md`, third-party code).
- [x] Defect B: every ID-indexed lookup of the victory screen (winner sprite and
  its position, silhouette or background group and palette, win quote text and its
  language block, full-name plate) is found and listed with its address; `$30`
  reads Kyo's entries through the presentation map or a new table; the original
  entries are unchanged. A tool step with byte checks and tests on invented data
  carries any code change.
- [x] Clone wins at each team position and on the other player side, and the
  clone appears on the plates as a teammate when another fighter wins; each
  component equals the same screen with original Kyo (the stage and background
  excepted: the owner accepted the default on 2026-11-19, ticket 18).
- [x] Original fighters winning are unchanged by the fix (regression check).
- [x] Slot anatomy gets the victory-screen tables; the Rehearsal shortcut points
  at the new candidate (see `AGENTS.md`).

## Resolution (2026-11-19)

**A: runtime defect, upstream too.** Winning hypothesis: the toolkit's byte-write
handler for the NEO-PVC chip (`pvc_w8`) only updated the bank and never ran the
colour pack or unpack, while the game fills those inputs with byte writes; every
palette fade came out as zero and sprites rendered as flat silhouettes. A loop of
two parallel runs with a determinism check and a verifier (flat dark colour
dominant, or fewer than 24 colours, in the sprite region) was red on the published
`v0.1.0` player, on the candidate and in the interpreter, and green with the
fix. The published `v0.1.0` and the current upstream `main` have the same
defect. The fix is [`pvc_byte_writes.py`](../../../../tools/kof2003/import_slot/pvc_byte_writes.py),
a hash-checked patcher for the runtime copy under `private/`. A report and a
patch for the upstream author (with an invitation to this fork) are drafted under
`private/work/first-import/diag-t17/upstream-report/`; posting them is the
owner's decision.

**B: the victory screen read the raw team bytes.** Winning hypothesis: at
`$E202` the screen copies the winning team's three bytes into its object and then
looks up the animation (word table `$E756`, 37 entries, zero for `$30`), the win
quote (16 bytes per ID in the `$200000` bank, read at `$E44A`), the rival-pair
list (`$06BDC0`, via `$E8F2`) and the name plate (`$0B8D90`) by that ID; the
tables only cover the original roster, which gave the wrong sprite and a
displaced silhouette, a quote from garbage and an empty plate. The fix is
[`map_victory_screen.py`](../../../../tools/kof2003/import_slot/map_victory_screen.py):
the six-byte copy calls a routine at `$53200` that keeps the colour bits and
maps the ID through the presentation map. Checked by screenshots at fixed
frames: the clone wins as Kyo (sprite, animation, quote, plate) at team positions
1 and 3 and on the other player side; at position 2 Gato wins and the clone's
plate shows Kyo; 21 frames of an original-team win are byte-identical with and
without the change.

**Left open.** The fight stage and the victory background follow the leader's
ID: a team led by `$30` fights on, and wins in front of, the default background
(red pagoda) instead of Kyo's; with the clone not leading the background is
right. Mapping the leader's stage lookup is a new ticket:
[18](18-stage-and-victory-background-clone-leader.md). The acceptance line
"each component equals the same screen with original Kyo" holds for sprite,
animation, quote and plates, not for this background.

## Português (Brasil)

# 17 Diagnosticar a tela de vitória nativa e os recursos de vitória que faltam no clone

Rodar com `/diagnosing-bugs`, seguindo o método e o checklist da
[anatomia da vaga](../slot-anatomy.md). Primeiro construir o laço de feedback.

Achar e corrigir dois defeitos da tela de vitória mostrada depois de uma luta de
equipe, encontrados pelo dono em 19/11/2026 ao jogar o candidato do Ensaio (o
[13](13-rehearsal-selection-presentation.md) mapeou a seleção, a tela de ordem e
o nome sob as barras de vida, mas não esta tela).

**A. Player nativo, sem clone.** Com uma equipe de lutadores originais, a tela de
vitória nativa mostra bem as placas de nome e a frase de vitória, mas o sprite
grande do vencedor é só uma silhueta preta e a animação não termina. O emulador
de referência (FBNeo) mostra o sprite colorido completo para o mesmo tipo de
equipe. É defeito do build nativo ou dos dados que ele lê, e atingiria também
todo lutador importado.

**B. Vitória do clone (`$30`).** Com uma equipe do clone, Iori Yagami e o Kyo
Kusanagi original, quando o clone vence: o sprite grande está errado e uma
silhueta deslocada cobre a faixa "WINNER" e parte da tela (o dono não sabe se é
a do clone); a frase de vitória está errada (outro idioma e cortada no começo); e
a placa do vencedor está vazia (a tela mostra o nome completo de cada lutador, não
só o primeiro nome). As placas dos companheiros (Iori Yagami e Kyo Kusanagi)
aparecem. Conferir também a placa do clone como companheiro quando outro lutador
vence.

Começar pelo A, porque o B não pode ser julgado enquanto o sprite original também
é uma silhueta. Os três prints do dono (nativo com o clone vencendo, nativo com
equipe original vencendo e FBNeo) estão em
`private/work/first-import/victory-prints/`; são imagens do jogo e nunca entram no
git.

### Bloqueios

Nenhum. O [14](14-rehearsal-intro-and-command-normals.md) fica bloqueado por este
ticket.

### Critérios de aceitação

- [x] Um roteiro determinístico chega à tela de vitória com equipe original e com
  o clone vencendo (posições 1, 2 e 3), tira capturas em quadros fixos e fica
  vermelho nos sintomas do dono. Registrar o comando e a saída; capturas e logs em
  `private/`.
- [x] Defeito A: a causa da silhueta é encontrada e classificada (defeito do port
  ou do runtime, carga de gráficos ou paleta, temporização ou dados); a correção
  ou a decisão de deixar fica registrada; o sprite do vencedor de vários
  lutadores originais, incluindo os três do dono, aparece completo no player
  nativo e concorda com o emulador de referência. Se a correção ficar fora dos
  arquivos rastreados, dizer e perguntar ao dono.
- [x] Conferência no projeto de origem para o defeito A: repetir a mesma vitória de
  equipe original no build de controle sem modificação (o player publicado
  `v0.1.0` e a preparação das ROMs, sem lutador importado nem programa remendado).
  Se a silhueta aparecer ali também, é defeito do projeto de origem do port
  ([recomp do KOF 2003](https://github.com/omegakatana92/The-King-of-Fighters-2003),
  cujo toolkit é o adaptado no
  [recomp do Samurai Shodown](https://github.com/omegakatana92/Samurai-Shodown-Recomp));
  registrar isso, descobrir se a causa está no player, no toolkit ou na entrada do
  gerador e preparar um relatório mínimo (versão, roteiro de entrada, quadro,
  descrição) para o dono. Em 19/11/2026 o repositório do KOF 2003 não tinha issues
  abertas; as fechadas não foram conferidas. Reportar ou contribuir com uma correção
  é decisão do dono; qualquer patch é preparado num clone em `private/`, sem copiar
  para este repositório (ver `AGENTS.md`, código de terceiros).
- [x] Defeito B: toda busca por ID da tela de vitória (sprite do vencedor e sua
  posição, grupo e paleta da silhueta ou do fundo, texto da frase e seu bloco de
  idioma, placa de nome completo) é achada e listada com o endereço; o `$30` lê as
  entradas do Kyo pelo mapa de apresentação ou por uma tabela nova; as entradas
  originais não mudam. Uma etapa de ferramenta com conferência de bytes e testes
  em dados inventados carrega qualquer mudança de código.
- [x] O clone vence em cada posição da equipe e do outro lado do jogador, e
  aparece nas placas como companheiro quando outro lutador vence; cada componente
  é igual ao da mesma tela com o Kyo original (exceto cenário e fundo: o dono
  aceitou o padrão em 19/11/2026, ticket 18).
- [x] Lutadores originais vencendo ficam inalterados pela correção (regressão).
- [x] A anatomia da vaga recebe as tabelas da tela de vitória; o atalho do Ensaio
  aponta para o novo candidato (ver `AGENTS.md`).

### Resolução (19/11/2026)

**A: defeito do runtime, também no upstream.** Hipótese vencedora: o tratador de
escrita de byte do chip NEO-PVC no toolkit (`pvc_w8`) só atualizava o banco e
nunca rodava o pack nem o unpack de cor, enquanto o jogo preenche essas entradas
com escritas de byte; todo fade de paleta saía zerado e os sprites viravam
silhuetas chapadas. Um laço de duas execuções paralelas com verificação de
determinismo e um verificador (cor escura chapada dominante, ou menos de 24 cores,
na região do sprite) ficou vermelho no player `v0.1.0` publicado, na candidata e no
interpretador, e verde com a correção. O `v0.1.0` publicado e o `main` atual do
upstream têm o mesmo defeito. A correção é o
[`pvc_byte_writes.py`](../../../../tools/kof2003/import_slot/pvc_byte_writes.py),
um ajustador com conferência de hash da cópia do runtime em `private/`. Um relato
e um patch para o autor do upstream (com convite para este fork) estão
rascunhados em `private/work/first-import/diag-t17/upstream-report/`; publicar é
decisão do dono.

**B: a tela de vitória lia os bytes crus da equipe.** Hipótese vencedora: em
`$E202` a tela copia os três bytes da equipe vencedora para o seu objeto e depois
busca por esse ID a animação (tabela de palavras `$E756`, 37 entradas, zero para o
`$30`), a frase de vitória (16 bytes por ID no banco `$200000`, lida em `$E44A`),
a lista de pares de rivais (`$06BDC0`, por `$E8F2`) e a placa de nome (`$0B8D90`);
as tabelas só cobrem o elenco original, o que dava sprite errado e silhueta
deslocada, frase de lixo e placa vazia. A correção é o
[`map_victory_screen.py`](../../../../tools/kof2003/import_slot/map_victory_screen.py):
a cópia de seis bytes chama uma rotina em `$53200` que preserva os bits de cor e
mapeia o ID pelo mapa de apresentação. Conferido por capturas em quadros fixos: o
clone vence como Kyo (sprite, animação, frase, placa) nas posições 1 e 3 e do outro
lado do jogador; na posição 2 o Gato vence e a placa do clone mostra Kyo; 21
quadros de uma vitória de equipe original ficam idênticos byte a byte com e sem a
mudança.

**Em aberto.** O cenário da luta e o fundo da vitória seguem o ID do líder: uma
equipe liderada pelo `$30` luta e vence diante do fundo padrão (pagode vermelho) em
vez do fundo do Kyo; com o clone fora da liderança o fundo está certo. Mapear a
busca de cenário do líder é um ticket novo: [18](18-stage-and-victory-background-clone-leader.md). A linha "cada componente é igual ao da
mesma tela com o Kyo original" vale para sprite, animação, frase e placas, não
para esse fundo.
