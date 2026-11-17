---
id: 07
title: "Choose how Guile is reached in the selection screen"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: [02, 06, 22]
research:
---

## Question

Guile now gets a new fighter ID, not Adelheid's `$22` (see [Choose how fighter slots are found for the SVC Exclusive Characters](06-slot-strategy.md)). [How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md) found a 39-cell table of 6 bytes (X, Y, ID) with the grid drawn as one fixed image and no hidden rows, and a hide rule for the label and portrait that applies only to `$22`-`$24`. How does a player reach Guile through the game's own selection flow while every original fighter stays available: a new cell in the table and the grid image, a code, or another route the research exposes? The answer must also work for the next SVC fighters.

_PT-BR: O Guile agora recebe um ID novo, não o `$22` da Adelheid (ticket 06). A pesquisa 02 achou uma tabela de 39 células de 6 bytes (X, Y, ID), com a grade desenhada como uma imagem fixa sem linhas ocultas, e uma regra que esconde nome e retrato só para `$22`-`$24`. Como o jogador chega ao Guile pelo fluxo de seleção do próprio jogo, mantendo todos os lutadores originais: uma célula nova na tabela e na imagem da grade, um código ou outro caminho que a pesquisa revelar? A resposta também precisa servir para os próximos lutadores do SVC._

**Owner update (2026-11-16).** For now the owner wants 4 imported fighters. The final layout is left for later: imported fighters may form teams, and the selection screen may be recreated for widescreen. Those are recorded as possibilities, not decided. So this ticket decides only the cheapest, reversible way to reach the first 4 fighters, and must not close the door on those later options.

_PT-BR: **Atualização do dono (16/11/2026).** Por enquanto o dono quer 4 lutadores importados. O desenho final fica para depois: os importados podem formar times e a tela de seleção pode ser recriada para widescreen. Isso fica registrado como possibilidade, não decidido. Este ticket decide só o jeito mais barato e reversível de chegar aos 4 primeiros, sem fechar as portas dessas opções futuras._

## Resolution

Decided with the owner on 2026-11-16, a round of questions at a time.

**Route.** Imported fighters are reached through the game's own selection flow by new cells at the end of the cell table, in extra rows just below the hidden rows (near the boss fighters). The owner called the position provisional; the final layout (imported fighters forming teams, a selection screen recreated for widescreen) stays open and this route does not block it. No code route (the game's two official codes do not scale) and no reuse of existing cells (it would hide original fighters).

**Table.** The 39-cell table ends where code starts, so it cannot grow in place: it moves with stage 1 of [Choose how fighter slots are found for the SVC Exclusive Characters](06-slot-strategy.md), and the 39-cell limit of the cursor and the row wrap (today gated by the BIOS developer-mode word) are raised to cover the new rows. Each new cell carries its own screen X/Y, so its position is free to choose.

**IDs and order.** Cells follow import order: Guile (`$30`) takes the first new cell, the next fighter (`$31`) the next one, and so on. The first target of 4 imported fighters takes two extra rows.

**Grid image.** No thumbnails for imported cells for now: the grid stays one fixed image of 11 rows, as with the hidden rows today. The player sees the cursor, the name label and the portrait, which are looked up by ID. Thumbnails come with the later selection-screen redesign.

**Switch.** The native port has a setting that turns the imported cells on or off, on by default. Off, the selection is plain KOF 2003, which also serves the rehearsal's check that the original fighters are unchanged.

**Team rule.** An imported fighter is an ordinary team member (team of 3). The boss rule ([How KOF 2003's boss selection rule works and whether a new ID can use it](22-boss-selection-rule.md)) is left alone; the early-end test is not edited.

**Random cell.** It keeps drawing only from the 32 original fighters for now. Including imported fighters is for after the import phase ends, not decided here.

**Test shortcut.** A separate development option of the native port picks a fighter ID and starts a lone-fighter match (the two last team slots emptied after selection), so the rehearsal and Guile's first test do not wait for the cells.

**For the review.** [Review ticket 04's five phases with every decision in place](14-review-the-five-phases.md) places the cell-table move with the table relocation and the test shortcut before the rehearsal. The name label, portrait, team icon and match HUD name of an imported ID stay with the portrait and icon work.

**PT-BR**

Decidido com o dono em 16/11/2026, uma rodada de perguntas por vez.

**Caminho.** Os importados são alcançados pelo fluxo de seleção do próprio jogo, por células novas no fim da tabela de células, em linhas extras logo abaixo das ocultas (perto dos chefes). O dono chamou a posição de provisória; o desenho final (importados formando times, tela de seleção recriada para widescreen) segue em aberto e este caminho não o bloqueia. Sem rota por código (os dois códigos oficiais não escalam) e sem reaproveitar células existentes (esconderia lutadores originais).

**Tabela.** A tabela de 39 células termina onde começa código, então não cresce no lugar: ela é movida junto com a etapa 1 do [ticket 06](06-slot-strategy.md), e o limite de 39 células do cursor e a volta das linhas (hoje presa à palavra de modo desenvolvedor da BIOS) sobem para cobrir as linhas novas. Cada célula nova traz o próprio X/Y de tela, então a posição é livre.

**IDs e ordem.** As células seguem a ordem de importação: o Guile (`$30`) ocupa a primeira célula nova, o próximo (`$31`) a seguinte, e assim por diante. A primeira meta de 4 importados ocupa duas linhas extras.

**Imagem da grade.** Sem miniaturas para as células importadas por enquanto: a grade segue uma imagem fixa de 11 linhas, como acontece hoje com as linhas ocultas. O jogador vê o cursor, o nome e o retrato, buscados pelo ID. As miniaturas vêm com o redesenho da tela de seleção.

**Interruptor.** O port nativo tem uma opção que liga ou desliga as células importadas, ligada por padrão. Desligada, a seleção é a do KOF 2003 puro, o que também serve à verificação do ensaio de que os originais ficam iguais.

**Regra de time.** O importado é membro comum do time de 3. A regra de chefe ([ticket 22](22-boss-selection-rule.md)) fica como está; o teste que encerra a seleção não é editado.

**Célula aleatória.** Continua sorteando só entre os 32 originais por enquanto. Incluir importados fica para depois do fim da fase de importações, sem decisão agora.

**Atalho de teste.** Uma opção de desenvolvimento à parte do port nativo escolhe um ID e inicia uma luta com um lutador sozinho (as duas últimas vagas do time esvaziadas depois da seleção), para o ensaio e o primeiro teste do Guile não esperarem pelas células.

**Para a revisão.** O [ticket 14](14-review-the-five-phases.md) encaixa a mudança da tabela de células junto da mudança das tabelas e o atalho de teste antes do ensaio. Nome, retrato, ícone da vaga e nome no placar de um ID importado ficam com o trabalho de retrato e ícone.
