---
title: "Complete a native team match"
triage: ready-for-agent
---

# 02 Complete a native team match

[Parent specification](../spec.md)

## What to build

Replay a complete MVS team match with original KOF 2003 fighters on the modifiable native port.

## Blocked by

[01 Reproduce native KOF 2003 in MVS](01-reproduce-native-mvs.md)

## Acceptance criteria

- [x] Replay fixed inputs from a known state through team selection and the normal match result. Record evidence of native execution, fallback and verification divergences.
- [x] Compare the match flow and Leader Super eligibility and meter cost with a working MVS reference.

## Português (Brasil)

Repetir uma luta completa de equipes no MVS com lutadores originais do KOF 2003 no port nativo modificável.

### Bloqueios

[01 Reproduce native KOF 2003 in MVS](01-reproduce-native-mvs.md)

### Critérios de aceitação

- [x] Repetir entradas fixas a partir de um estado conhecido, da seleção das equipes ao resultado normal da luta. Registrar execução nativa, fallback e eventuais divergências de verificação.
- [x] Comparar o fluxo da luta, as condições de uso e o custo de barra do Leader Super com uma referência MVS funcional.

## Comments

### 2026-11-13 — Change of first test

The owner chose MVS team play for the first import test. AES Single remains a reference observation and is not a prerequisite for the first imported match.

_PT-BR: o dono escolheu o modo de equipes do MVS para o primeiro teste da importação. O Single do AES permanece como observação de referência e deixa de ser pré-requisito da primeira luta com o importado._

### 2026-11-13 — Owner's manual AES reference

The owner tested the `kof2003` cartridge in MAME 0.289 with Universe BIOS 4.0 in U.S.A. console mode. After the BIOS screen and intro, pressing Start opens MODE SELECT. Its options are TEAM PLAY, TEAM VERSUS, TEAM PRACTICE, SINGLE PLAY, SINGLE VERSUS, SINGLE PRACTICE and OPTION. The cursor starts on TEAM PLAY. Press down three times and A to select SINGLE PLAY. A tutorial follows and can be skipped by pressing A twice. LEADER SELECT then opens with Iori initially selected and unlimited selection time. Selecting Iori starts the first fight.

The owner reports one fighter per side and a single round. The fight starts with three available power stocks, all blue for the Leader. Iori's Leader Super Special Move, San Shingi no Ni, was available and consumed two stocks. The reported command is `↓↘→ ↙↓← + AC`. The owner reports that certain special moves can cancel a super, including the Leader Super, at a cost of one stock.

The owner reports that Kin 1211 Shiki: Ya Otome, `↓↘→ ↘↓↙← + A/C`, is Iori's only common super shared with SVC Chaos in KOF 2003. The follow-up Ura 306 Shiki: Saika is available in KOF 2003 using the same command as in SVC and costs one additional stock, according to the owner's correction. These move comparisons remain to be checked against the SVC reference.

The opponent is random. The owner observed Maxima and Whip in different runs. After winning the single round, the owner saw Iori's victory animation, his artwork and quote, then an automatically advancing order-select screen followed by the next fight. At character select, buttons A, B, C and D select four different colors.

The owner reports canceling normals and chain combos into supers without an additional stock cost, and canceling special moves such as Iori's shoryuken into a super or Leader Super for one additional stock. An exact sequence and the conditions of the cancel remain to be established. The native AES replay and comparison remain open.

### 13/11/2026 — Referência AES testada pelo dono

O dono testou o cartucho `kof2003` no MAME 0.289 com Universe BIOS 4.0 em modo console, região U.S.A. Após a tela da BIOS e a introdução, apertar Start abre MODE SELECT. As opções são TEAM PLAY, TEAM VERSUS, TEAM PRACTICE, SINGLE PLAY, SINGLE VERSUS, SINGLE PRACTICE e OPTION. O cursor começa em TEAM PLAY. Apertar baixo três vezes e A seleciona SINGLE PLAY. Em seguida aparece um tutorial, que pode ser pulado apertando A duas vezes. A tela LEADER SELECT abre com o cursor em Iori e tempo infinito para escolher. Selecionar Iori inicia a primeira luta.

O dono relata um lutador por lado e um único round. A luta começa com três barras de especial disponíveis, todas azuis para o Leader. O Leader Super Special Move de Iori, San Shingi no Ni, estava disponível e consumiu duas barras. O comando informado é `↓↘→ ↙↓← + AC`. O dono relata que certos movimentos especiais podem cancelar um super, inclusive o Leader Super, ao custo de uma barra.

O dono relata que Kin 1211 Shiki: Ya Otome, `↓↘→ ↘↓↙← + A/C`, é o único super comum de Iori compartilhado com SVC Chaos no KOF 2003. Em correção ao relato anterior, informa que a extensão Ura 306 Shiki: Saika também está disponível no KOF 2003 com o mesmo comando do SVC e consome uma barra adicional. A comparação de golpes ainda será conferida na referência do SVC.

O primeiro adversário é aleatório. O dono encontrou Maxima e Whip em partidas diferentes. Ao vencer o round único, viu a comemoração do Iori, seu artwork e frase, a tela de order select avançar automaticamente e a luta seguinte começar. Na seleção, os botões A, B, C e D escolhem quatro cores diferentes.

O dono relata cancelamentos de golpes normais e chain combos em supers sem custo adicional de barra, e de movimentos especiais, como o shoryuken do Iori, em super ou Leader Super por uma barra adicional. Ainda falta estabelecer uma sequência exata e as condições do cancelamento. A repetição e a comparação no port nativo em AES continuam pendentes.

### 2026-11-15 — Replay tooling and first comparison

Claimed with `/implement`. New tooling in `tools/kof2003/match/` reads the native player's input script format, turns it into a MAME MVS replay, runs both silently from power-on and reads the `--verify` summary. Seven unit tests cover the script reader and the summary reader. Captures, logs and runs stay in `private/work/team-match/`.

The fixed script `tools/kof2003/match/scripts/team-match.txt` inserts coins, starts, keeps the default team with Iori as Leader, enters Iori's Leader Super command at frame 5,600 and gives no further input. Over 36,100 frames the native player reached the normal end of the match: CONTINUE?, its countdown, GAME OVER and the attract sequence. Its summary: 28,735,257 blocks checked, 0 state mismatches, 11,573 cycle-count differences, 696,322,961 native instructions, 125,533 interpreted instructions (99.98% native) and 62 uncovered entry points. Each runtime repeats itself exactly between runs. MAME 0.289 with the Europe MVS v2 BIOS reached the same sequence.

Alignment: when MAME reports its (n+1)-th completed frame, its screen shows native frame n+2. Setting each frame's inputs at that point keeps both runtimes identical through coin, start, team selection and the start of the fight. The title screen and fight frames match pixel for pixel, apart from sprites the two renderers latch one frame apart. The selection screens have a black background in the native player and a blue one in MAME.

Open: within five frames of the first player input during the fight, even a plain walk forward, the CPU opponent reacts differently in the two runtimes. Shifting MAME's alignment by one frame either way does not remove it. Without in-fight input both runs stay identical to at least frame 6,000. The cause is not established. The scripted Leader Super at frame 5,600 did not visibly start in either runtime. The Leader's stock gauge looks empty at the start of the first team fight, which would make the move unavailable there. This is unconfirmed.

### 15/11/2026 — Ferramentas de repetição e primeira comparação

Ticket assumido com `/implement`. As novas ferramentas em `tools/kof2003/match/` leem o formato de roteiro do executável nativo, convertem o roteiro em uma repetição no MAME MVS, rodam os dois sem som desde a inicialização e leem o resumo do `--verify`. Sete testes unitários cobrem o leitor de roteiro e o leitor do resumo. Capturas, logs e execuções ficam em `private/work/team-match/`.

O roteiro fixo `tools/kof2003/match/scripts/team-match.txt` insere fichas, aperta start, mantém a equipe padrão com Iori como líder, envia o comando do Leader Super de Iori no quadro 5.600 e não envia mais comandos. Em 36.100 quadros, o executável nativo chegou ao fim normal da partida: CONTINUE?, a contagem, GAME OVER e a sequência de demonstração. Resumo: 28.735.257 blocos verificados, 0 divergências de estado, 11.573 diferenças de ciclos, 696.322.961 instruções nativas, 125.533 instruções interpretadas (99,98% nativo) e 62 pontos de entrada sem cobertura. Cada runtime se repete exatamente entre execuções. O MAME 0.289 com a BIOS Europe MVS v2 percorreu a mesma sequência.

Alinhamento: quando o MAME informa seu quadro concluído de número n+1, a tela mostra o quadro nativo n+2. Aplicar as entradas de cada quadro nesse ponto mantém os dois runtimes idênticos nas fichas, no start, na seleção das equipes e no início da luta. A tela de título e os quadros da luta coincidem pixel a pixel, exceto sprites que os dois renderizadores registram com um quadro de diferença. As telas de seleção têm fundo preto no nativo e azul no MAME.

Em aberto: em até cinco quadros após o primeiro comando do jogador durante a luta, mesmo uma simples caminhada para a frente, o adversário da CPU reage de forma diferente nos dois runtimes. Deslocar o alinhamento do MAME em um quadro para qualquer lado não resolve. Sem comandos durante a luta, as duas execuções continuam idênticas até pelo menos o quadro 6.000. A causa não foi determinada. O Leader Super do roteiro no quadro 5.600 não começou de forma visível em nenhum dos dois. A barra de estoque do líder parece vazia no início da primeira luta de equipes, o que impediria o golpe nesse momento. Isso não foi confirmado.

### 2026-11-15 — Owner's decisions

The owner chose to track the in-fight divergence separately in [07 Explain the in-fight input divergence](07-explain-in-fight-input-divergence.md) and to check Leader Super eligibility and stock cost in MVS team play by hand. `tools/kof2003/Start-ManualMvs.ps1` opens the MAME MVS reference with the same Europe MVS v2 BIOS as the native player and the owner's controls. The first criterion is met. The second stays open until the owner's MVS observation and the matching native check.

_PT-BR: o dono decidiu acompanhar a divergência durante a luta em separado, no ticket 07, e conferir manualmente quando o Leader Super pode ser usado e quantos estoques custa no modo de equipes do MVS. `tools/kof2003/Start-ManualMvs.ps1` abre a referência MVS no MAME com a mesma BIOS Europe MVS v2 do executável nativo e os controles do dono. O primeiro critério está cumprido. O segundo continua aberto até a observação do dono no MVS e a conferência correspondente no nativo._

### 2026-11-15 — Owner's MVS team-play rules and resolution

The owner reports the KOF 2003 MVS team-play stock rules. The team starts with 3 stocks. The stock limit starts at 3 and rises by one for each defeated member, up to 5, and the stocks already held carry over to the next member. A super costs 1 stock. The Leader Super costs 2 stocks, can be used at any time, and only the Leader has it. Canceling a special move into a super or the Leader Super costs 1 more stock. The owner knows of Iori's shoryuken as a cancelable special, up to its second hit while he is still on the ground. A blue-and-white glow over a darkened screen marks a super. A red-and-white glow marks a Leader Super.

Supporting observations: MAME's work RAM holds Player 1's stock count at `$102EAC` and Player 2's at `$102EAD`, and the bar's progress toward the next stock at `$102FDA`. In a scripted MAME run, the CPU-controlled Whip used a blue-glow super and her count fell from 3 to 2. In the owner's recorded MAME session, Iori's Leader Super at the start of the first fight showed the red glow and the HUD count fell from 3 to 1. The scripted Leader Super inputs did not produce the move: Iori was hit during the motion, or the game read only the first half-circle as a special move.

Resolution: the native match flow matches the MVS reference through the normal end of the match. The owner judged the stock rules to be game logic that the port does not change and closed the second criterion on that basis. The Leader Super was not separately exercised in the native player. The in-fight divergence stays open in [ticket 07](07-explain-in-fight-input-divergence.md).

### 15/11/2026 — Regras de estoque do MVS em equipes e resolução

O dono informou as regras de estoque do KOF 2003 no modo de equipes do MVS. A equipe começa com 3 estoques. O limite começa em 3 e sobe um a cada membro derrotado, até 5, e os estoques acumulados passam para o próximo membro. Um super custa 1 estoque. O Leader Super custa 2 estoques, pode ser usado a qualquer momento e só o líder o possui. Cancelar um movimento especial em super ou Leader Super custa 1 estoque a mais. O cancelamento que o dono conhece com certeza é o shoryuken de Iori, até o segundo hit, enquanto ele ainda está no chão. Brilho azul e branco com a tela escurecida indica super. Brilho vermelho e branco indica Leader Super.

Observações de apoio: na RAM de trabalho do MAME, o número de estoques do jogador 1 fica em `$102EAC`, o do jogador 2 em `$102EAD`, e o progresso da barra rumo ao próximo estoque em `$102FDA`. Em uma execução por roteiro no MAME, a Whip controlada pela CPU usou um super de brilho azul e seus estoques caíram de 3 para 2. Na sessão do MAME gravada pelo dono, o Leader Super de Iori no início da primeira luta teve brilho vermelho e o número no HUD caiu de 3 para 1. Os comandos de Leader Super por roteiro não executaram o golpe: Iori foi atingido durante o movimento, ou o jogo leu apenas a primeira meia-lua como movimento especial.

Resolução: o fluxo da partida no nativo coincide com a referência MVS até o fim normal da partida. O dono considerou as regras de estoque lógica do jogo, que o port não altera, e fechou o segundo critério com base nisso. O Leader Super não foi exercitado separadamente no executável nativo. A divergência durante a luta continua aberta no [ticket 07](07-explain-in-fight-input-divergence.md).
