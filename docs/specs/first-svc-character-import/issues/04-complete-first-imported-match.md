---
title: "Complete the first Imported Character match"
triage: ready-for-agent
---

# 04 Complete the first Imported Character match

[Parent specification](../spec.md)

## What to build

Select the SVC import in native KOF 2003 and finish a scripted MVS team match against original fighters with a small, working set of combat actions.

## Blocked by

[02 Complete a native team match](02-complete-native-single-match.md) · [03 Capture the SVC Exclusive Character reference](03-capture-svc-fighter-reference.md)

## Acceptance criteria

- [ ] The Imported Character is selectable through the game's selection flow and original roster entries remain available.
- [ ] Movement, guarding and a basic attack work with recognizable visuals and timing. The scripted checks distinguish hit, block and whiff and verify the KOF 2003 outcomes.
- [ ] A replay from known initial state reaches the normal match result and shows native execution of the exercised behavior. Start recording reusable work, manual adaptation and blockers.

## Português (Brasil)

Selecionar o importado do SVC no KOF 2003 nativo e terminar uma luta de equipes MVS por script contra lutadores originais, com um conjunto inicial de ações de combate.

### Bloqueios

[02 Complete a native team match](02-complete-native-single-match.md) · [03 Capture the SVC Exclusive Character reference](03-capture-svc-fighter-reference.md)

### Critérios de aceitação

- [ ] O personagem importado pode ser escolhido pela seleção do jogo e o elenco original continua disponível.
- [ ] Movimentação, defesa e um golpe básico funcionam com visuais e duração reconhecíveis. Os testes por script distinguem acerto, defesa e golpe no vazio e conferem os resultados sob as regras do KOF 2003.
- [ ] Uma repetição a partir de um estado inicial conhecido chega ao resultado normal e mostra execução nativa do comportamento exercitado. Começar a registrar trabalho reaproveitável, adaptação manual e bloqueios.

## Comments

### 2026-11-15 — Plan and decisions

Plan in five phases: (1) map KOF 2003's selection table, per-fighter code and animation lookup, free graphics space and palettes in MAME; (2) add a per-frame memory probe to the local native runtime copy and rebuild; (3) make Guile visible in selection, idle and walking; (4) add guarding and one basic attack with KOF 2003 collision, validated with the scripted versus test used in ticket 03; (5) run a scripted team match to the normal result with `--verify`, recording reusable and manual work.

The owner asked for the lowest-effort options and authorized the native rebuild. Guile goes into an existing KOF 2003 fighter slot that the official MVS selection does not show (Adelheid or Mukai), so no original fighter is removed and no table needs enlarging. Guile is translated into the KOF 2003 ROM data rather than written as C in the port, so the port's generator produces native code for him and the same build also runs in MAME for comparison.

_PT-BR: plano em cinco fases: (1) mapear no MAME a tabela de seleção do KOF 2003, o código e a busca de animações de cada lutador, o espaço livre para gráficos e as paletas; (2) acrescentar à cópia local do runtime nativo uma sonda de memória por quadro e recompilar; (3) tornar Guile visível na seleção, parado e andando; (4) acrescentar defesa e um golpe básico com a colisão do KOF 2003, validados com o versus por roteiro usado no ticket 03; (5) jogar uma partida de equipes por roteiro até o resultado normal com `--verify`, registrando o trabalho reaproveitável e o manual._

_O dono pediu as opções de menor esforço e autorizou a recompilação do nativo. Guile entra num espaço de lutador existente no KOF 2003 que a seleção oficial do MVS não mostra (Adelheid ou Mukai), de modo que nenhum lutador original sai e nenhuma tabela precisa ser ampliada. Guile é traduzido para os dados da ROM do KOF 2003, e não escrito em C no port, para que o gerador do port produza o código nativo dele e a mesma montagem também rode no MAME para comparação._

### 2026-11-15 — Phase 1: team slots and hidden fighters

In MAME, KOF 2003 keeps both teams' fighter IDs at `$107D0C`, three bytes for Player 1 then three for Player 2, with a second copy at `$107D12`. The default Iori team was `1F 03 19` against `1D 1B 1C` (Whip, K' and Maxima). Writing an ID into both copies of Player 1's first slot after team selection, at frame 4,900, replaced the first fighter completely: graphics, name and moves. `$20` loads Chizuru, `$21` Kusanagi, `$22` Adelheid and `$23` Mukai, and `$11` is Yamazaki. Written later, at frame 5,230, only the name on the HUD changed, so the fighter's data is loaded between those frames.

Adelheid and Mukai, outside the official MVS selection, load and fight normally. Either can carry the import without removing an original fighter. Adelheid is the first candidate, because a final boss like Mukai is more likely to carry boss-specific behaviour. The next step is to find how the selection screen maps cursor positions to IDs and how an ID leads to the fighter's code, animations and graphics.

_PT-BR: no MAME, o KOF 2003 guarda os IDs dos lutadores das duas equipes em `$107D0C`, três bytes para o jogador 1 e três para o jogador 2, com uma segunda cópia em `$107D12`. A equipe padrão do Iori era `1F 03 19` contra `1D 1B 1C` (Whip, K' e Maxima). Escrever um ID nas duas cópias da primeira vaga do jogador 1 depois da seleção das equipes, no quadro 4.900, trocou o primeiro lutador por completo: gráficos, nome e golpes. `$20` carrega Chizuru, `$21` Kusanagi, `$22` Adelheid e `$23` Mukai, e `$11` é Yamazaki. Escrito mais tarde, no quadro 5.230, só o nome no placar mudou, então os dados do lutador são carregados entre esses quadros._

_Adelheid e Mukai, fora da seleção oficial do MVS, carregam e lutam normalmente. Qualquer um pode receber a importação sem remover um lutador original. Adelheid é o primeiro candidato, porque um chefe final como Mukai tem mais chance de trazer comportamentos próprios de chefe. O próximo passo é descobrir como a tela de seleção associa as posições do cursor aos IDs e como um ID leva ao código, às animações e aos gráficos do lutador._

### 2026-11-15 — Correction: native build only

The owner corrected the plan. The import targets the native KOF 2003 port, which is why KOF 2003 is the Base Game. Guile goes into the decrypted program and graphics files that the native player loads, and the port's generator recompiles them, so translating him into ROM data still reuses the fighter code the game already has. Running the modified game in MAME is no longer a goal, because MAME expects the encrypted cartridge. MAME stays a reading instrument for studying how KOF 2003 and SVC lay out their data. Validation moves to the native player, so the memory probe of phase 2 now comes before the first visible slice of Guile. Guile's SVC data comes from the decrypted SVC program already produced for the base-direction research.

_PT-BR: o dono corrigiu o plano. A importação tem como alvo o port nativo do KOF 2003, motivo pelo qual o KOF 2003 é o jogo base. Guile entra nos arquivos de programa e gráficos decifrados que o executável nativo carrega, e o gerador do port os recompila, de modo que traduzi-lo para dados da ROM continua aproveitando o código de lutador que o jogo já tem. Rodar o jogo modificado no MAME deixa de ser objetivo, porque o MAME espera o cartucho criptografado. O MAME continua como instrumento de leitura para estudar como o KOF 2003 e o SVC organizam seus dados. A validação passa para o executável nativo, então a sonda de memória da fase 2 vem antes da primeira fatia visível do Guile. Os dados do Guile no SVC vêm do programa do SVC já decifrado na pesquisa de direção._
