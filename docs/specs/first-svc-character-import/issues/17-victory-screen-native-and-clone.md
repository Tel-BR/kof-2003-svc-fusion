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

- [ ] A scripted, deterministic run reaches the victory screen for an original
  team and for a team with the clone winning (positions 1, 2 and 3), takes
  screenshots at fixed frames and goes red on the owner's symptoms. Record its
  command and output; keep captures and logs in `private/`.
- [ ] Defect A: the cause of the silhouette-only sprite is found and classified
  (native port or runtime defect, graphics or palette loading, timing, or data);
  the fix or the decision to leave it is recorded; the winner sprite of several
  original fighters, including the owner's three, renders complete in the native
  player and agrees with the reference emulator. If the fix lives outside this
  repository's tracked files, say so and ask the owner.
- [ ] Upstream check for defect A: run the same original-team victory in the
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
- [ ] Defect B: every ID-indexed lookup of the victory screen (winner sprite and
  its position, silhouette or background group and palette, win quote text and its
  language block, full-name plate) is found and listed with its address; `$30`
  reads Kyo's entries through the presentation map or a new table; the original
  entries are unchanged. A tool step with byte checks and tests on invented data
  carries any code change.
- [ ] Clone wins at each team position and on the other player side, and the
  clone appears on the plates as a teammate when another fighter wins; each
  component equals the same screen with original Kyo.
- [ ] Original fighters winning are unchanged by the fix (regression check).
- [ ] Slot anatomy gets the victory-screen tables; the Rehearsal shortcut points
  at the new candidate (see `AGENTS.md`).

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

- [ ] Um roteiro determinístico chega à tela de vitória com equipe original e com
  o clone vencendo (posições 1, 2 e 3), tira capturas em quadros fixos e fica
  vermelho nos sintomas do dono. Registrar o comando e a saída; capturas e logs em
  `private/`.
- [ ] Defeito A: a causa da silhueta é encontrada e classificada (defeito do port
  ou do runtime, carga de gráficos ou paleta, temporização ou dados); a correção
  ou a decisão de deixar fica registrada; o sprite do vencedor de vários
  lutadores originais, incluindo os três do dono, aparece completo no player
  nativo e concorda com o emulador de referência. Se a correção ficar fora dos
  arquivos rastreados, dizer e perguntar ao dono.
- [ ] Conferência no projeto de origem para o defeito A: repetir a mesma vitória de
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
- [ ] Defeito B: toda busca por ID da tela de vitória (sprite do vencedor e sua
  posição, grupo e paleta da silhueta ou do fundo, texto da frase e seu bloco de
  idioma, placa de nome completo) é achada e listada com o endereço; o `$30` lê as
  entradas do Kyo pelo mapa de apresentação ou por uma tabela nova; as entradas
  originais não mudam. Uma etapa de ferramenta com conferência de bytes e testes
  em dados inventados carrega qualquer mudança de código.
- [ ] O clone vence em cada posição da equipe e do outro lado do jogador, e
  aparece nas placas como companheiro quando outro lutador vence; cada componente
  é igual ao da mesma tela com o Kyo original.
- [ ] Lutadores originais vencendo ficam inalterados pela correção (regressão).
- [ ] A anatomia da vaga recebe as tabelas da tela de vitória; o atalho do Ensaio
  aponta para o novo candidato (ver `AGENTS.md`).
