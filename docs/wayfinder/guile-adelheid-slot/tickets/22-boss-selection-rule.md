---
id: 22
title: "How KOF 2003's boss selection rule works and whether a new ID can use it"
label: wayfinder:research
mode: AFK
status: closed
assignee:
blocked_by: []
research: research/22-boss-selection-rule:docs/wayfinder/guile-adelheid-slot/research/22-boss-selection-rule.md
---

## Question

[How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md) found that picking Adelheid (`$22`) or Mukai (`$23`) ends team selection after one fighter and that fighter fights alone, and that the label and portrait are hidden for `$22`-`$24`. [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) found no comparison against `$22` in the common fight code and two comparisons against `$23`. Earlier, in [04 Complete the first Imported Character match](../../../specs/first-svc-character-import/issues/04-complete-first-imported-match.md), writing `$22` or `$23` into the first team slot after selection made that fighter fight normally inside a team, so the "alone" behaviour may belong to the selection screen rather than to the fight. The owner suspects a boss rule that could suit overpowered SVC fighters and gives a single-fighter mode that keeps team play intact, which would also let Guile be tested without a team.

Questions from the owner (2026-11-16):
1. Selection order: once a team fighter is picked, can Mukai (or Adelheid) still be picked afterwards, or is it blocked? And once Mukai is picked, is a team impossible?
2. Fairness: compared with a normal team of three that has the same three life bars, does a lone fighter get any advantage or disadvantage: life in points, defence, special-gauge gain, damage dealt or taken, stocks, Leader Super? The owner notes that all three bars would be blue, the leader's, while a normal team has only one leader fighter; verify what blue means and how it applies.

Also answer, as the researcher sees fit:
- What triggers the rule: an ID range, a flag in a per-ID table, or per-ID data? Does it apply to `$20`, `$21` and `$24` (Chizuru, Kusanagi, Maki) too?
- What the three team slots hold when selection ends early (copies of the same ID, empty, other), and whether the "three life bars" are one fighter's or the same fighter entering three times; what happens when a bar is emptied (entry, position, health and gauge carried over).
- Which fight flow differs: intro, taunt, entry and exit, order-select skip, timer, round and match result, win and continue after a win, and the opposing team's size. What happens when both sides use such a fighter.
- Whether the rule can be applied to a new ID, and switched on for an ordinary fighter as a solo mode.
- Which parts need the BIOS developer-mode word, and which work without it, in MAME and as far as the native player can tell from the code.

Measure in MAME with scripted inputs and read the code only as far as needed to name the trigger. Facts only; list the choices this opens for the owner.

_PT-BR: a pesquisa 02 achou que escolher a Adelheid (`$22`) ou o Mukai (`$23`) encerra a seleção de equipe depois de um lutador, que esse lutador luta sozinho e que nome e retrato ficam escondidos para `$22`-`$24`. A pesquisa 01 não achou comparação com `$22` no código comum de luta e achou duas com `$23`. Antes, no ticket 04, escrever `$22` ou `$23` na primeira vaga da equipe depois da seleção fez esse lutador lutar normalmente dentro de uma equipe, então o comportamento "sozinho" pode ser da tela de seleção e não da luta. O dono suspeita de uma regra de chefe que serviria a lutadores overpower do SVC e dá um modo de lutador único mantendo o jogo em equipe, o que também permitiria testar o Guile sem time._

_Perguntas do dono (16/11/2026):_
1. _Ordem da seleção: depois de escolher um lutador de equipe, ainda dá para escolher o Mukai (ou a Adelheid), ou fica bloqueado? E, depois de escolher o Mukai, é impossível formar equipe?_
2. _Justiça: comparando com uma equipe normal de três com as mesmas três barras de vida, o lutador sozinho tem alguma vantagem ou desvantagem: vida em pontos, defesa, ganho de barra especial, dano causado ou recebido, estoques, Leader Super? O dono nota que as três barras seriam azuis, as do líder, enquanto numa equipe normal só um lutador é líder; verificar o que o azul significa e como se aplica._

_Responder também, como o pesquisador achar melhor: o que dispara a regra (faixa de IDs, indicador numa tabela por ID ou dados por ID) e se vale para `$20`, `$21` e `$24` (Chizuru, Kusanagi, Maki); o que as três vagas da equipe guardam quando a seleção termina cedo (cópias do mesmo ID, vazias, outras), se as "três barras" são de um lutador ou o mesmo lutador entrando três vezes, e o que acontece quando uma barra zera (entrada, posição, vida e barra carregadas); que partes do fluxo da luta diferem (introdução, provocação, entrada e saída, pulo da escolha de ordem, tempo, resultado de round e partida, vitória e continuação, tamanho da equipe adversária, os dois lados com esse tipo de lutador); se a regra pode valer para um ID novo e ser ligada para um lutador comum como modo solo; e que partes exigem a palavra do modo desenvolvedor do BIOS, no MAME e, pelo código, no player nativo._

_Medir no MAME com entradas por script e ler o código só até nomear o gatilho. Só fatos; listar as escolhas que isso abre para o dono._

**Owner observation (2026-11-16).** In ordinary team play, when the CPU opponent is Kusanagi or Maki, it comes alone, exactly as in single play. So the game already runs one fighter against a team of three, even if only the CPU uses it. The research should find out how the CPU opponent's side is set up in that case (team slots, life bars, order, entry), which IDs it applies to (the owner names `$21` and `$24`), and whether the same setup can be given to the player's side, with and without the developer-mode word.

_PT-BR: **Observação do dono (16/11/2026).** No jogo em equipe convencional, quando o adversário da CPU é o Kusanagi ou a Maki, ele vem sozinho, exatamente como no modo single. Então o jogo já executa um lutador contra uma equipe de três, mesmo que só a CPU use isso. A pesquisa deve descobrir como o lado do adversário da CPU é montado nesse caso (vagas da equipe, barras de vida, ordem, entrada), a quais IDs vale (o dono cita `$21` e `$24`) e se o mesmo arranjo pode ser dado ao lado do jogador, com e sem a palavra do modo desenvolvedor._

**Second owner observation (2026-11-16).** Adelheid also comes alone, without a team, when she is the CPU opponent. With Kusanagi and Maki, that makes `$21`, `$22` and `$24` seen alone in the CPU's side; whether `$20` and `$23` do too is not yet known.

_PT-BR: **Segunda observação do dono (16/11/2026).** A Adelheid também vem sozinha, sem time, quando é a adversária da CPU. Com o Kusanagi e a Maki, são `$21`, `$22` e `$24` vistos sozinhos no lado da CPU; se `$20` e `$23` também vêm assim ainda não se sabe._

**Third owner observation (2026-11-16).** Chizuru and Maki appear together: both names show, they tag-swap normally, but there are three blue life bars shared between them, as if both had the same life bar. They are defeated only when all three bars are empty. The owner calls it a big hack and wants to understand it, not use it. The research should say how this is set up (shared life, two fighters on one side, how defeat is decided) and whether it is the same mechanism as the "alone" cases.

_PT-BR: **Terceira observação do dono (16/11/2026).** Chizuru e Maki aparecem juntas: os dois nomes aparecem, elas trocam de tag normalmente, mas são três barras azuis compartilhadas, como se ambas tivessem a mesma barra de vida. Só são derrotadas quando as três barras se esvaziam. O dono chama de gambiarra grande e quer entender, não usar. A pesquisa deve dizer como isso é montado (vida compartilhada, dois lutadores num lado, como a derrota é decidida) e se é o mesmo mecanismo dos casos "sozinho"._

## Owner corrections and statements (2026-11-16, after research)

Stated by the owner as verified; no emulator check needed.

- **Blue bar.** In a normal team only the team leader has the blue life bar; the other fighters have yellow. The research line "only the active fighter's bar is blue" is wrong. Blue means this fighter can perform the Leader Super. A lone fighter therefore has three blue bars and the Leader Super.
- **Intro.** Only the fighter chosen to start the match does the intro, leader or not.
- **Taunt.** Any fighter can taunt during the fight, leader or not.
- **Tag-out animation.** Sometimes the exit animation reuses the taunt animation and voice lines. That can be a **fallback** (a provisional solution) for SVC fighters, who have no such animation. The ideal is an exclusive, distinct animation for the swap and another for the taunt.
- **Special KOF 2003 swap** (hit, then the partner enters): SVC has none. The Guard Cancel animation can be its fallback.
- **Life.** Keep the lone fighter's 336 life as it is. Not to be touched for now.

_PT-BR: **Correções e afirmações do dono (16/11/2026), após a pesquisa.** Verificadas pelo dono, sem checagem no emulador. Só o líder da equipe tem a barra azul; os outros têm a amarela, e azul significa que o lutador pode executar o Leader Super (a linha da pesquisa estava errada). Intro: só o lutador escolhido para iniciar, líder ou não. Provocação: qualquer lutador, a qualquer momento. A saída da luta às vezes reaproveita a provocação, o que serve de **fallback** (solução provisória) para o SVC; o ideal é animação exclusiva para a troca e outra para a provocação. A troca especial do KOF 2003 (bate e o parceiro entra) não existe no SVC; o Guard Cancel pode ser o fallback. Manter a vida de 336 por enquanto._

## Documented for future game modes

Facts from research 22, kept here because they may help build game modes later:

- Writing `$FF` into team slots 2 and 3 after selection gives a lone fighter without the developer-mode word (measured with Iori, Adelheid, Maki and the Chizuru+Maki pair).
- The selection ends early when the first member is `$22` or `$23`, or when it is `$20` followed by `$24`. The test is at `$96FE`; editing it would change which fighters end selection alone.
- The CPU builds its opponent team from a 16x16 table at `$6B626`; the opponent's shape comes from a column.
- The classifier at `$2817A` reads the team shape (empty third slot plus the ID in slot 1 or 2).

_PT-BR: `$FF` nas vagas 2 e 3 depois da seleção dá lutador sozinho sem o modo desenvolvedor; o teste em `$96FE` decide quando a seleção encerra cedo; a CPU monta o adversário por uma tabela 16x16 em `$6B626`; o classificador `$2817A` lê a forma da equipe. Registrados para criar modos de jogo no futuro._

## Resolution

Selection ends early only when the first team member is `$22` or `$23`, or `$20` followed by `$24` (test at `$96FE`); Adelheid or Mukai can still be picked after a team fighter. The rule is not an ID range: the classifier at `$2817A` reads the team shape (empty third slot plus the ID in slot 1 or 2). A lone fighter has one 336 life bar (3 x 112, one pool, no swap), with three blue bars; the owner confirms blue marks the Leader Super fighter, only the leader is blue in a normal team, and the 336 life stays as is. Chizuru+Maki share one pool because damage always goes to slot 1's record. The CPU builds opponents from a 16x16 table at `$6B626`. Writing `$FF` into slots 2 and 3 after selection gives a lone fighter without developer mode, so a lone imported fighter (Guile included) is possible. Intro, taunt and tag-out behaviour and their SVC fallbacks are recorded in the ticket's owner section. Game-mode ideas from `$FF`, `$96FE` and the CPU table are kept above for later. Still unmeasured: defence, meter gain, stocks, KO, intro/taunt/continue flows, both sides lone at once, and the meaning of `$107D64` and `$107D66`.

_PT-BR: a seleção só encerra cedo quando o primeiro membro é `$22` ou `$23`, ou `$20` seguido de `$24` (teste em `$96FE`); dá para escolher Adelheid ou Mukai depois de um lutador de equipe. Não é faixa de IDs: o classificador em `$2817A` lê a forma da equipe. O lutador sozinho tem uma barra de vida de 336 (3 x 112, um só reservatório, sem troca), com três barras azuis; o dono confirma que azul marca quem faz o Leader Super, que numa equipe normal só o líder é azul e que a vida de 336 fica como está. Chizuru+Maki dividem um reservatório porque o dano vai sempre ao registro da vaga 1. A CPU monta adversários por uma tabela 16x16 em `$6B626`. Escrever `$FF` nas vagas 2 e 3 depois da seleção dá lutador sozinho sem modo desenvolvedor, então um importado sozinho (o Guile inclusive) é possível. Intro, provocação, troca e seus fallbacks do SVC estão na seção do dono. Ideias de modos de jogo ficam acima. Falta medir: defesa, ganho de barra, estoques, KO, fluxos de intro/provocação/continue, os dois lados sozinhos e o sentido de `$107D64` e `$107D66`._
