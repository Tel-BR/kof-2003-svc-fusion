---
title: "Complete the first Imported Character match"
triage: ready-for-agent
---

# 04 Complete the first Imported Character match

[Parent specification](../spec.md)

## What to build

Bring Guile in as a new Imported Character at ID `$30` in native KOF 2003. Validate the route first through a development-only lone-fighter shortcut, then select Guile through the normal flow and finish a scripted MVS team match against original fighters with a small, working set of combat actions.

## Blocked by

[02 Complete a native team match](02-complete-native-single-match.md) · [03 Capture the SVC Exclusive Character reference](03-capture-svc-fighter-reference.md)

## Acceptance criteria

- [ ] The new ID `$30` is proven first with a Kyo rehearsal in the Added Space: it is selectable, completes a lone match and leaves every original fighter unchanged.
- [ ] Guile is selectable through the normal selection flow and original roster entries remain available. The development-only lone-fighter shortcut is a test aid, not final evidence.
- [ ] Guile's idle, walk, guard and basic attack work with recognizable visuals and timing. The scripted checks distinguish hit, block and whiff and verify the KOF 2003 outcomes.
- [ ] Guile has the agreed presentation and universal actions: name, portrait, team-slot icon, colours, run, backstep, four jumps, evasive rolls and both Guard Cancels.
- [ ] A replay from known initial state reaches the normal team-match result and shows native execution of the exercised behavior. It regression-checks original fighters and records reusable work, Guile-specific adaptation and blockers separately.

## Português (Brasil)

Trazer Guile como Personagem Importado novo no ID `$30` do KOF 2003 nativo. Primeiro validar o caminho por um atalho de desenvolvimento para luta com um único lutador; depois selecionar Guile pelo fluxo normal e terminar uma luta MVS de equipes por script contra lutadores originais, com um conjunto pequeno e funcional de ações de combate.

### Bloqueios

[02 Complete a native team match](02-complete-native-single-match.md) · [03 Capture the SVC Exclusive Character reference](03-capture-svc-fighter-reference.md)

### Critérios de aceitação

- [ ] O novo ID `$30` é comprovado primeiro num ensaio com Kyo no Espaço acrescentado: ele é selecionável, completa uma luta solo e deixa todos os lutadores originais iguais.
- [ ] Guile pode ser escolhido pelo fluxo normal de seleção e o elenco original continua disponível. O atalho de desenvolvimento para luta solo é auxílio de teste, não evidência final.
- [ ] Parado, caminhada, defesa e um golpe básico do Guile funcionam com visuais e duração reconhecíveis. Os testes por script distinguem acerto, defesa e golpe no vazio e conferem os resultados sob as regras do KOF 2003.
- [ ] Guile recebe a apresentação e ações universais combinadas: nome, retrato, ícone da vaga de time, cores, corrida, passo para trás, quatro pulos, esquivas e os dois Guard Cancels.
- [ ] Uma repetição a partir de estado inicial conhecido chega ao resultado normal da luta em equipe e mostra a execução nativa do comportamento exercitado. Ela confere regressão dos lutadores originais e registra separadamente trabalho reaproveitável, adaptação específica do Guile e bloqueios.

## Delivery plan / Plano de entrega

1. **Slot infrastructure / Infraestrutura de vagas:** relocate the fighter and selection-cell tables, raise the cursor limit and row wrap for provisional imported cells, add their switch enabled by default, create ID `$30`, make existing hidden fighters selectable by default and add the development-only lone-fighter shortcut. / Mover as tabelas de lutador e células de seleção, ampliar o limite do cursor e a volta das linhas para as células provisórias dos importados, acrescentar seu interruptor ligado por padrão, criar o ID `$30`, tornar os lutadores ocultos existentes selecionáveis por padrão e criar o atalho de desenvolvimento para luta solo.
2. **Rehearsal / Ensaio:** clone Kyo into `$30` with tiles in the Added Space, then prove selection, a lone match and unchanged originals. / Clonar Kyo no `$30` com tiles no Espaço acrescentado, depois comprovar seleção, luta solo e originais inalterados.
3. **Guile solo slice / Fatia solo do Guile:** replace the rehearsal with Guile's data and graphics; exercise idle, walk, guard and one basic attack. / Trocar o ensaio pelos dados e gráficos do Guile; exercitar parado, caminhada, guarda e um golpe básico.
4. **Presentation and colours / Apresentação e cores:** add the agreed name, portrait, team-slot icon and colours. / Acrescentar o nome, retrato, ícone da vaga de time e cores combinados.
5. **Universal actions / Ações universais:** add run, backstep, four jumps, evasive rolls and both Guard Cancels. / Acrescentar corrida, passo para trás, quatro pulos, esquivas e os dois Guard Cancels.
6. **Normal team flow / Fluxo normal de equipe:** select Guile normally and finish the scripted team match. / Selecionar Guile normalmente e terminar a luta de equipe por script.
7. **Verification and evidence / Verificação e evidência:** profile and verify the scripted runs, check the original fighters and record effort. / Gerar perfil e verificar as execuções por script, conferir os lutadores originais e registrar o esforço.

For phase 4, preserve the palette reference of each converted frame and reject any reference without a verified source and destination. Identify and exercise the 33 frames with upper palette-header offsets, establish the source of those upper slots and compare rendered results before accepting the mapping. An unverified reference stops this phase. Use the owner's approved automatic C/D hue-shift pattern ([wayfinder 16](../../../wayfinder/guile-adelheid-slot/tickets/16-guile-colours.md)); the SVC preview does not validate the KOF mapping. / Na fase 4, preservar a referência de paleta de cada quadro convertido e rejeitar qualquer referência sem origem e destino verificados. Identificar e exercitar os 33 quadros com deslocamentos de paleta superiores no cabeçalho, identificar a origem desses slots e comparar os resultados renderizados antes de aceitar o mapeamento. Uma referência não verificada interrompe esta fase. Usar o padrão automático de mudança de matiz C/D aprovado pelo dono ([wayfinder 16](../../../wayfinder/guile-adelheid-slot/tickets/16-guile-colours.md)); a prévia no SVC não valida o mapeamento no KOF.

The completed Graphics Set growth is a prerequisite, not a Guile phase. The second slot stage begins only with the 16th Imported Character and is outside this milestone. Audio stays in [10](10-guile-reuses-kof-sounds.md), [11](11-guile-standing-punch-voice.md) and [12](12-guile-guard-cancel-voice-and-ledger.md) after this ticket; ticket 05 owns the full moveset, Leader Super and cancels; ticket 06 owns Multi-Shift and the final estimate. / A ampliação concluída do Conjunto gráfico é pré-requisito, não fase do Guile. A segunda etapa das vagas só começa no 16º Personagem Importado e fica fora deste marco. Áudio fica nos [tickets 10](10-guile-reuses-kof-sounds.md), [11](11-guile-standing-punch-voice.md) e [12](12-guile-guard-cancel-voice-and-ledger.md) depois deste ticket; o ticket 05 cuida do repertório completo, Leader Super e cancelamentos; o ticket 06 cuida de Multi-Shift e da estimativa final.

## Comments

### 2026-11-18 — Rehearsal preparation and same-team check

The owner asked to select the original Kyo and the `$30` Kyo rehearsal together
on one team, to check whether selection or the match prevents it. Add this to the
rehearsal checks; it does not replace the required lone match or original-roster
regression. An independent copy of the 17 prepared control files was made under
`private/work/first-import/roms`, with matching SHA-256 hashes. The preparation
command is in `tools/kof2003/import_slot/`; it does not yet alter the game or
create a playable rehearsal. Slot infrastructure and the palette gate remain open.

_PT-BR: o dono pediu para selecionar o Kyo original e o Kyo do ensaio no `$30`
na mesma equipe, para verificar se a seleção ou a luta impedem essa combinação.
Acrescentar essa conferência ao ensaio; ela não substitui a luta solo nem a
regressão do elenco original. Uma cópia independente dos 17 arquivos preparados
do controle foi criada em `private/work/first-import/roms`, com hashes SHA-256
iguais. O comando de preparo fica em `tools/kof2003/import_slot/`; ele ainda não
altera o jogo nem cria um ensaio jogável. A infraestrutura de vagas e o gate de
paletas continuam abertos._

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

### 2026-11-18 — Rehearsal readiness check

At `4b9a821`, the independent rehearsal directory still contains the same 17
files as the control, with matching SHA-256 hashes. It is not a playable `$30`
build. The Graphics Set growth proof drew a synthetic tile from the Added Space
by planting it in video memory; it did not establish that Kyo's own frame data
can address relocated tiles there. The fighter tables, selection cells, guards
and lone-fighter shortcut still need implementation and validation. In
particular, the research reports an overlap in the final `$0750A2` row and
unresolved ID-indexed readers, so table relocation must account for these
before the original-roster regression can be claimed. No match or same-team
selection was run in this check. The phase-4 palette gate remains unchanged.

_PT-BR: em `4b9a821`, a pasta independente do ensaio ainda contém os mesmos
17 arquivos do controle, com hashes SHA-256 iguais. Ela não é um build jogável
com `$30`. A prova de ampliação do Conjunto gráfico desenhou um tile sintético
do Espaço acrescentado plantando-o na memória de vídeo; ela não comprovou que os
quadros do próprio Kyo conseguem endereçar tiles movidos para lá. As tabelas de
lutador, células de seleção, verificações de limite e o atalho de lutador solo
ainda precisam ser implementados e validados. Em particular, a pesquisa relata
uma sobreposição na última linha de `$0750A2` e leitores indexados por ID ainda
não identificados; a movimentação das tabelas precisa tratar esses pontos antes
de se afirmar que não houve regressão no elenco original. Nenhuma luta ou
seleção na mesma equipe foi executada nesta conferência. O gate de paletas da
fase 4 continua inalterado._
