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

### 2026-11-18 — Rehearsal implementation in progress

Prepared private intermediate images with expanded fighter tables, both axes of
the fighter-pair matrix, Kyo's copied frame directory and provisional selection
cells. An independent frame decoder compared all 585 Kyo frame references: the
palette headers and geometry matched and the decoded tile numbers moved by
`$80000`. The private descriptor loads the original graphics pairs a second
time in the Added Space; it has not yet proved the cloned fighter on screen.

At the owner's request for this Kyo clone only, all four candidate colours are
varied: A/C derive from original A and B/D from original B, with opposite hue
directions per pair and a small tint for neutral colours. Numeric checks found
233, 237, 233 and 237 changed nontransparent entries respectively, with no
channel changing by more than three 5-bit levels; transparent entries, dark
bits and original fighter palette indices stayed unchanged. Palette placement
and rendered appearance remain unverified. This exception does not change the
approved Guile rule or its mandatory phase-4 gate.

One original-team run of an earlier intermediate build matched seven control
captures and had zero verification state mismatches, but used 17,507
interpreted instructions at 24 uncovered entries; profiling collected those
entries for the next build. It is not proof for all original fighters. The
selection switch, remaining guards and tables, actual clone match, same-team
test and original-roster regression remain open. [Export notes](../kof2003-export-notes.md).

An exploratory interpreter-only run of the provisional selection image picked
the original Kyo first, but the intended second pick was a different original
fighter, not `$30`. The selection route and scripted cursor movement still need
diagnosis. This was not a native or completed-match validation.

_PT-BR: foram preparadas imagens intermediárias privadas com tabelas de lutador
ampliadas, os dois eixos da matriz de pares, o diretório de quadros copiado do
Kyo e células provisórias de seleção. Um decodificador independente comparou as
585 referências de quadro do Kyo: cabeçalhos de paleta e geometria coincidiram,
e os números de tile decodificados subiram `$80000`. O descritor privado carrega
os pares gráficos originais novamente no Espaço acrescentado; ainda não se
comprovou o desenho do clone na tela._

_A pedido do dono, apenas para este clone do Kyo, as quatro cores candidatas são
variadas: A/C partem do A original e B/D do B original, em sentidos opostos por
par e com leve tonalidade para cores neutras. As conferências numéricas acharam
233, 237, 233 e 237 entradas não transparentes alteradas, respectivamente, sem
variação maior que três níveis de 5 bits por canal; entradas transparentes,
bits escuros e índices de paleta do lutador original ficaram iguais. A posição
das paletas e sua aparência renderizada ainda não foram verificadas. Essa
exceção não muda a regra aprovada do Guile nem seu gate obrigatório da fase 4._

_Uma execução de equipe original de um build intermediário anterior coincidiu
com sete capturas do controle e teve zero divergências de estado, mas usou
17.507 instruções interpretadas em 24 entradas não cobertas; o perfil recolheu
essas entradas para o próximo build. Isso não comprova todos os originais.
Continuam abertos o interruptor de seleção, as demais verificações e tabelas, a
luta real do clone, o teste na mesma equipe e a regressão do elenco original.
[Notas para exportação](../kof2003-export-notes.md)._

_Uma execução exploratória da imagem com seleção provisória, apenas no
interpretador, escolheu primeiro o Kyo original, mas a segunda escolha pretendida
foi outro lutador original, não `$30`. Ainda é preciso diagnosticar a rota de
seleção e o movimento de cursor do roteiro. Isso não validou a execução nativa
nem uma luta completa._

### 2026-11-18 — Owner's first manual selection

The owner selected the `$30` clone and also reached Adelheid, Maki, Chizuru and
Mukai. He reported that the clone behaved strangely and did not reproduce Kyo
Kusanagi's behaviour. The private monitor confirms `$30` in a P1 team; it did
not observe `$30` and original Kyo together in that team. The run reported 253
interpreted instructions and 11 uncovered entry points. The manual run did not
use `--verify` or record the missing entry addresses, so neither a zero-mismatch
claim nor attribution of the fallback to the clone is justified. The cause of
the reported behaviour is under investigation; selection alone does not pass
the Rehearsal.

_PT-BR: o dono escolheu o clone `$30` e também alcançou Adelheid, Maki, Chizuru
e Mukai. Ele relatou que o clone teve comportamentos estranhos e não reproduziu
o comportamento de Kyo Kusanagi. O monitor privado confirma `$30` numa equipe
do P1; ele não observou `$30` e o Kyo original juntos nessa equipe. A execução
registrou 253 instruções interpretadas e 11 entradas não cobertas. Ela não usou
`--verify` nem registrou os endereços das entradas faltantes, portanto não se
pode afirmar ausência de divergência nem atribuir o interpretador ao clone. A
causa do comportamento relatado está em investigação; a seleção isolada não
aprova o Ensaio._

### 2026-11-18 — Minimum rehearsal priority

The owner prioritized Guile and chose a minimum Kyo Rehearsal: retain the
planned selection, lone-match and original-roster checks and the requested
same-team check, without polishing the clone beyond what establishes the route.
The first automated same-team route moved to the random cell after the first
pick. Removing that movement made an interpreter-only replay select original
Kyo and `$30` together on P1's team at frame 3,802. The replay has not shown
that they load and fight correctly, and is not native verification.

_PT-BR: o dono priorizou o Guile e escolheu um Ensaio mínimo com Kyo: manter as
verificações previstas de seleção, luta solo e elenco original e a conferência
pedida da mesma equipe, sem polir o clone além do necessário para comprovar o
caminho. O primeiro roteiro automático foi à célula aleatória após a primeira
escolha. Ao retirar esse movimento, uma repetição apenas no interpretador
selecionou Kyo original e `$30` juntos no time do P1 no quadro 3.802. A
repetição não demonstrou que eles carregam e lutam corretamente e não é uma
verificação nativa._

### 2026-11-18 — Recorded special and follow-ups

In a monitored native session the owner selected original Kyo and `$30` on the
same team. He reported that basic buttons worked, then the first forward
quarter-circle + A caused the duplicated-fighter defect. Input transitions and
frame observations were recorded under `private/`. The native replay matched
the original session's logged fighter ID, state, action and frame word for all
3,215 recorded frames and
reproduced the duplicate. `--verify` reported zero state mismatches, 1,466
cycle differences and 13 interpreted instructions at four uncovered entries.

In a private one-variable candidate, copying original Kyo's move-script
directory entry at `$7DC28` to `$30` removed the duplicate in the recorded
replay. The image at the affected frame showed one fighter; a native `--verify`
replay reported zero state mismatches, 1,468 cycle differences and 26 interpreted
instructions at six uncovered entries. This establishes a cause for that
observed defect in this replay, not completion of the moveset or native coverage.
The preparation tool now installs that directory entry.

Local reproduction: `private/work/first-import/check_duplicate_replay.py` runs
the recorded private input against the preserved experimental executable and
compares a reference detail with the affected capture. It reports the duplicate
on the old ROM directory; `DIAGNOSTIC_ROM_PATH` can point it at the corrected
candidate. It is a narrow visual heuristic for this recorded scene, not a
general fighter detector. Its inputs, captures and executable stay in `private/`.

The owner also reported missing selection name, team-position indicator,
thumbnail and portrait, an absent frozen frame before the intro, and unavailable
forward + B. These are recorded separately in [13](13-rehearsal-selection-presentation.md)
and [14](14-rehearsal-intro-and-command-normals.md). An initial forward + B
comparison did not start both fighters in equivalent states, so it proves
nothing about that command. The palette gate remains open.

_PT-BR: numa sessão nativa monitorada, o dono escolheu Kyo original e `$30` na
mesma equipe. Relatou que os botões básicos funcionaram e que o primeiro quarto
de círculo para a frente + A causou o defeito de lutadores duplicados. As
mudanças de entrada e as observações por quadro foram gravadas em `private/`.
A repetição nativa coincidiu com o ID, estado, ação e palavra de quadro do
lutador registrados nos 3.215 quadros e reproduziu a duplicação. O `--verify` registrou zero
divergências de estado, 1.466 diferenças de ciclos e 13 instruções interpretadas
em quatro entradas não cobertas._

_Numa candidata privada com uma única alteração, copiar para `$30` a entrada do
diretório de scripts de golpes do Kyo original em `$7DC28` eliminou a duplicação
na repetição gravada. A imagem do quadro afetado mostrou um lutador; uma
repetição nativa com `--verify` registrou zero divergências de estado, 1.468
diferenças de ciclos e 26 instruções interpretadas em seis entradas não cobertas.
Isso estabelece uma causa para o defeito observado nessa repetição, não a
conclusão do repertório nem da cobertura nativa. A ferramenta de preparação
agora instala essa entrada de diretório._

_Reprodução local: `private/work/first-import/check_duplicate_replay.py`
executa as entradas privadas gravadas com o executável experimental preservado
e compara um detalhe de referência com a captura afetada. Ele aponta a
duplicação na pasta de ROMs anterior; `DIAGNOSTIC_ROM_PATH` pode apontar para a
candidata corrigida. É uma heurística visual restrita a essa cena gravada, não
um detector geral de lutadores. Entradas, capturas e executável ficam em
`private/`._

_O dono relatou também ausência de nome, indicador de posição na equipe,
miniatura e retrato na seleção, falta do quadro congelado antes da intro e
indisponibilidade de frente + B. Eles estão registrados separadamente nos
[tickets 13](13-rehearsal-selection-presentation.md) e
[14](14-rehearsal-intro-and-command-normals.md). Uma comparação inicial de
frente + B não colocou os lutadores em estados equivalentes, portanto não
comprova o comportamento desse comando. O gate de paletas continua aberto._

### 2026-11-18 — Lone-fighter shortcut, interpreter check

The opt-in development hook empties P1's second and third slots only after the
selected first ID matches its requested value and both team copies agree. An
invented-RAM harness checks the option off, matching and non-matching teams and
the two copies. In the candidate with the move-directory correction, an
interpreter replay selected `$30` first, activated the hook and reached a solo
fight with three blue life bars. With no further combat input, the CPU won: the
normal winner screen was captured at frame 11,600 (SHA-256
`0db4b66061c85b660949f06eb893efae355b7b684e57b7499ae0300720b65c9c`), and
continue at 11,900 (SHA-256
`b52c9e914e239aecdfebc7dff8aea9e220750b744128a40d5d6530850740fdd7`).
This checks an interpreter loss path only; the native replay, zero-fallback
requirement, original-roster regression and other reported defects remain open.
The reusable input route is `tools/kof2003/import_slot/kyo-lone-match.txt`.

The subsequent native profiling run followed the same scripted solo loss and
its winner/continue captures matched the interpreter's at frames 11,600 and
11,900. It reported 58,621 interpreted instructions at 38 uncovered entries;
those entries were collected for recompilation. This run was not `--verify`
and does not establish zero state mismatches or zero fallback.

An independent static comparison against the control checked the 37 original
rows in the 16 relocated tables, both original-ID axes of the pair matrix,
the 37 original entries in eight modified directories, and Kyo's original
frame directory; they matched. This is not a gameplay regression for all 37.
Local command: `python private/work/first-import/verify_original_tables.py`.

_PT-BR: o atalho opcional de desenvolvimento esvazia a segunda e terceira vagas
do P1 somente depois de o primeiro ID corresponder ao solicitado e as duas
cópias da equipe coincidirem. Um pequeno teste com RAM inventada confere opção
desligada, equipe correspondente e não correspondente e as duas cópias. Na
candidata com a correção do diretório de golpes, uma repetição pelo interpretador
escolheu `$30` primeiro, acionou o atalho e chegou à luta solo com três barras
azuis. Sem novos comandos de combate, a CPU venceu: a tela normal de vencedor
foi capturada no quadro 11.600 e a tela de continuação no 11.900, com os hashes
acima. Isso confere apenas o caminho de derrota no interpretador; continuam
abertos a repetição nativa, a exigência de zero fallback, a regressão do elenco
original e os demais defeitos relatados. A rota de entradas reaproveitável é
`tools/kof2003/import_slot/kyo-lone-match.txt`._

_O perfil nativo posterior percorreu a mesma derrota solo por roteiro e suas
capturas de vencedor/continuação coincidiram com as do interpretador nos quadros
11.600 e 11.900. Ele registrou 58.621 instruções interpretadas em 38 entradas
não cobertas, recolhidas para recompilação. Essa execução não usou `--verify` e
não comprova zero divergências de estado ou zero fallback._

_Uma comparação estática independente com o controle conferiu as 37 linhas
originais nas 16 tabelas movidas, os dois eixos de IDs originais da matriz de
pares, as 37 entradas originais em oito diretórios alterados e o diretório de
quadros original do Kyo; eles coincidiram. Isso não é uma regressão jogável dos
37 lutadores. Comando local: `python private/work/first-import/verify_original_tables.py`._

### 2026-11-18 — Owner checked the move-directory candidate

The owner tested the candidate with the corrected move-script directory. He
reported that the duplicate fighters disappeared and most commands responded,
but command behaviour was still incorrect, including grabs and cancels. The
private session reported 43,417 interpreted instructions and 32 uncovered entry
points. The session was not run under `--verify`; the feedback does not close
the command or native-coverage checks. The remaining behavioural investigation
is recorded in [14](14-rehearsal-intro-and-command-normals.md).

_PT-BR: o dono testou a candidata com o diretório de scripts de golpes corrigido.
Relatou que os lutadores duplicados desapareceram e que a maioria dos comandos
respondeu, mas que o comportamento dos comandos ainda estava incorreto,
inclusive em agarrões e cancelamentos. A sessão privada registrou 43.417
instruções interpretadas e 32 entradas não cobertas. A sessão não usou
`--verify`; esse retorno não encerra as verificações de comandos ou cobertura
nativa. A investigação comportamental restante está registrada no
[ticket 14](14-rehearsal-intro-and-command-normals.md)._

**Effort record.** This session's active wall-clock effort was not measured, so
no duration or estimate is claimed. Reusable work includes the partial table,
frame, palette and selection preparation, the monitor and replay route; the
Kyo-specific work includes the cloned frame/palette candidates and the diagnosed
move-directory entry. These observations do not establish Guile's effort.

_**Registro de esforço.** O tempo ativo desta sessão não foi medido, portanto
nenhuma duração ou estimativa é afirmada. O trabalho reaproveitável inclui a
preparação parcial de tabelas, quadros, paletas e seleção, o monitor e a rota de
repetição; o trabalho específico do Kyo inclui as candidatas de quadros/paletas
do clone e a entrada de diretório de golpes diagnosticada. Essas observações não
estabelecem o esforço do Guile._
