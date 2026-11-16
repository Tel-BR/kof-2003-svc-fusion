---
id: 06
title: "Choose how fighter slots are found for the SVC Exclusive Characters"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
blocked_by: [01, 03, 23]
research:
---

## Question

**Owner update (2026-11-16).** Guile does not take Adelheid's slot. The owner wants to import as many SVC Exclusive Characters as possible, and fears Guile may not fit or work well in her slot, so new slots are created instead. [Choose where Guile's tiles go in the graphics files](19-guile-tile-placement.md) was decided the same way: the graphics set grows to 128 MiB with Guile.

Which route creates the new fighter IDs, and how far does it go? [How many fighter IDs KOF 2003's tables hold and how much free space its files have](03-slot-capacity.md) leaves: relocate the nineteen 37-entry tables and raise the `$24` guards to use `$30`-`$3E` (15 IDs); also renumber the non-fighter object types that hold `$25`-`$2F` in the banked directories (up to 27 IDs, which in number covers the 26 Exclusive Characters); or widen the ID past 6 bits. Which ID does Guile get? Adelheid (`$22`), Mukai (`$23`) and Maki (`$24`) keep their slots, so what, if anything, is done with them? What does the route mean for the selection screen? Implementing the expansion is out of scope.

_PT-BR: **Atualização do dono (16/11/2026).** O Guile não ocupa a vaga da Adelheid. O dono quer importar o máximo possível de exclusivos do SVC e teme que o Guile não caiba ou não funcione bem na vaga dela, então vagas novas são criadas. O ticket 19 foi decidido do mesmo jeito: os gráficos crescem para 128 MiB junto com o Guile._

_Qual caminho cria os IDs novos, e até onde ele vai? A pesquisa 03 deixa: mover as dezenove tabelas de 37 entradas e ajustar as verificações de `$24` para usar `$30`-`$3E` (15 IDs); renumerar também os tipos de objeto que ocupam `$25`-`$2F` nos diretórios com banco (até 27 IDs, o que em número cobre os 26 exclusivos); ou alargar o ID além de 6 bits. Que ID o Guile recebe? Adelheid (`$22`), Mukai (`$23`) e Maki (`$24`) mantêm suas vagas, então o que se faz com elas, se algo? O que o caminho significa para a tela de seleção? Implementar a ampliação fica fora do escopo._

**Owner update, second round (2026-11-16).**
- Only after the Exclusive Characters are done, the owner may bring one or a few hand-picked SVC versions of Shared Characters (for example SVC's Terry, who plays very differently from KOF 2003's Terry), chosen in some special way over the existing slot. Not all six. With 26 Exclusive Characters and 27 free 6-bit IDs, only one such version fits with its own ID; more would have to swap their data under the existing ID or the ID would have to be widened. Which one is open.
- The first target is 4 imported fighters, which the 15 IDs of the table-relocation route already cover.
- The rehearsal before Guile (clone a reference fighter into a new ID, see [Review ticket 04's five phases with every decision in place](14-review-the-five-phases.md)) needs an ID above `$24`, so the table relocation comes first in any case; renumbering objects and widening the ID stay open.
- The hidden fighters, Adelheid, Mukai and Maki among them, stay in the game and are made selectable by default until the owner decides their fate after importing the others.

_PT-BR: **Atualização do dono, segunda rodada (16/11/2026).** Só depois de fechar os exclusivos, o dono pode trazer uma ou poucas versões do SVC de personagens compartilhados, escolhidas a dedo (por exemplo o Terry do SVC, que joga bem diferente do Terry do KOF 2003), de um jeito especial sobre a vaga existente. Não os seis. Com 26 exclusivos e 27 IDs de 6 bits livres, só uma dessas versões cabe com ID próprio; mais que isso exigiria trocar os dados sob o ID existente ou alargar o ID. Isso está em aberto. A primeira meta é 4 lutadores importados, que os 15 IDs do caminho de mover tabelas já cobrem. O ensaio antes do Guile (clonar um lutador de referência num ID novo) precisa de um ID acima de `$24`, então mover as tabelas vem primeiro de qualquer forma; renumerar objetos e alargar o ID seguem em aberto. Os lutadores ocultos, entre eles Adelheid, Mukai e Maki, ficam no jogo e selecionáveis por padrão até o dono decidir o destino deles depois de importar os outros._
