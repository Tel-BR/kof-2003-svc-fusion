---
title: "Capture the SVC Exclusive Character reference"
triage: needs-info
---

# 03 Capture the SVC Exclusive Character reference

[Parent specification](../spec.md)

## What to build

Record reproducible combat with the owner-selected Exclusive Character in SVC Chaos. The owner's fighter choice gates this ticket. It can then run in parallel with the KOF 2003 baseline work.

## Blocked by

Owner selection of the SVC Exclusive Character.

## Acceptance criteria

- [ ] Confirm the owner's choice from the approved SVC MVS roster and record the moveset used as the reference for the import.
- [ ] Replay recorded inputs in a working SVC reference and capture commands, animation timing, observable attack behavior and the relevant cancel sequences.
- [ ] Record Exceed eligibility, cost and when it becomes available again. Keep raw captures and game-derived data private.

## Português (Brasil)

Registrar uma luta reproduzível no SVC Chaos com o personagem exclusivo escolhido pelo dono. O ticket depende dessa escolha. Depois, pode avançar em paralelo à preparação do KOF 2003.

### Bloqueios

Escolha do personagem exclusivo do SVC pelo dono.

### Critérios de aceitação

- [ ] Confirmar a escolha do dono na lista aprovada do SVC MVS e registrar o repertório que servirá de referência para a importação.
- [ ] Repetir entradas gravadas numa referência funcional do SVC e registrar comandos, duração das animações, comportamento observável dos ataques e sequências de cancelamento relevantes.
- [ ] Registrar as condições de uso do Exceed, o custo e quando volta a ficar disponível. Manter capturas brutas e dados derivados do jogo em área privada.

## Comments

### 2026-11-15 — Owner's choice: Guile

The owner chose Guile as the first SVC Exclusive Character to import. His reasons: Guile has charge moves like Ash Crimson in KOF 2003, and he has fewer moves than Ryu. The owner accepts that Guile's supers may be problematic. Ryu was the alternative considered for his motion-based commands.

_PT-BR: o dono escolheu Guile como o primeiro personagem exclusivo do SVC a importar. Motivos dele: Guile tem golpes de carga como os de Ash Crimson no KOF 2003, e tem menos golpes que Ryu. O dono aceita que os supers de Guile possam dar problema. Ryu foi a alternativa considerada, por usar comandos de movimento._

### 2026-11-15 — Measured in MAME

The owner played a recorded MAME session with Guile against the CPU (Iori) using the Europe MVS v2 BIOS. The session inputs were logged frame by frame and replayed exactly. Scripted tests then started from the same state at the beginning of the fight. A scripted replay of the owner's own inputs matched the recorded playback pixel for pixel. Recordings, logs and captures stay in `private/work/svc-guile/`.

| Check | Result |
|---|---|
| Sonic Boom, [←] → + A | Comes out with 30 or more frames of charge, not with 29. Matches the 30-frame figure in the research. |
| Somersault Kick, [↓] ↑ + D | Comes out after 59 frames of charge both with and without frames at neutral between down and up. The neutral rule described for SVC does not apply to this move in the MVS game. |
| Total Wipeout, [←] → ← → + D | Super activates. |
| Somersault Slash and Strike, [↙] ↘ ↙ ↗ + A or D | Both supers activate. The delta motion read from the research is correct. |
| Throw that misses, A+B away from the opponent | Guile performs the throw whiff animation. |
| Exceed, Sonic Hurricane, [←] → ← → + A+C | In the owner's session, the first attempt was interrupted when Iori hit Guile. The second came out with Guile below half health, and the gauge level did not change. A giant Sonic Boom travels toward the opponent. |

In the owner's session, 5 of 11 Somersault Kick attempts came out cleanly, all with 2–3 frames at neutral. Two attempts were interrupted by hits, one had only 8 frames of charge, and three were inconclusive.

The owner's report that the Exceed can be used only once per fight is accepted. Still open for this ticket: Guile's air throw and SVC's cancels in MAX mode, which the owner will record in a new session.

### 15/11/2026 — Medições no MAME

O dono jogou uma sessão gravada no MAME com Guile contra a CPU (Iori), usando a BIOS Europe MVS v2. As entradas da sessão foram registradas quadro a quadro e repetidas com exatidão. Os testes por roteiro partiram do mesmo estado no início da luta. Uma repetição por roteiro das próprias entradas do dono coincidiu pixel a pixel com a gravação. Gravações, logs e capturas ficam em `private/work/svc-guile/`.

| Conferência | Resultado |
|---|---|
| Sonic Boom, [←] → + A | Sai com 30 ou mais quadros de carga, e não com 29. Coincide com os 30 quadros da pesquisa. |
| Somersault Kick, [↓] ↑ + D | Sai após 59 quadros de carga, com e sem quadros na posição neutra entre baixo e cima. A regra do neutro descrita para o SVC não se aplica a esse golpe no jogo MVS. |
| Total Wipeout, [←] → ← → + D | O super é ativado. |
| Somersault Slash e Strike, [↙] ↘ ↙ ↗ + A ou D | Os dois supers são ativados. O movimento em delta lido na pesquisa está correto. |
| Arremesso no vazio, A+B longe do adversário | Guile faz a animação de agarrão no vazio. |
| Exceed, Sonic Hurricane, [←] → ← → + A+C | Na sessão do dono, a primeira tentativa foi interrompida quando Iori atingiu Guile. A segunda saiu com Guile abaixo de meia vida, e o nível da barra não mudou. Um Sonic Boom gigante avança em direção ao adversário. |

Na sessão do dono, 5 de 11 tentativas de Somersault Kick saíram de forma limpa, todas com 2 a 3 quadros na posição neutra. Duas foram interrompidas por golpes, uma teve só 8 quadros de carga e três foram inconclusivas.

O relato do dono de que o Exceed só pode ser usado uma vez por luta está aceito. Ainda em aberto neste ticket: o arremesso aéreo de Guile e os cancelamentos do SVC no modo MAX, que o dono vai gravar em uma nova sessão.

### 2026-11-15 — Air throws

The owner recorded a second session and performed Guile's air throw on Kim with both A+B and C+D. An air throw that misses has no throw whiff animation and costs no gauge: Guile performs the normal jumping attack of the buttons pressed. The owner reports that KOF 2003's air throw behaves the same way, triggered with C or D, so the import uses KOF 2003's input. The input log shows A+B and C+D presses shortly after jumps. The fight could not be replayed: the owner used MAME's soft reset (F3) to change opponents, the recording does not capture resets, and a replay from power-on reached a different opponent. Future recording sessions should restart MAME instead of using F3. MAX-mode cancels remain open.

_PT-BR: o dono gravou uma segunda sessão e executou o arremesso aéreo de Guile contra Kim, com A+B e com C+D. Um arremesso aéreo que não pega não tem animação de agarrão no vazio nem custo de barra: Guile executa o golpe normal no ar dos botões apertados. Segundo o dono, o arremesso aéreo do KOF 2003 se comporta igual, acionado com C ou D, então a importação usa o comando do KOF 2003. O log de entradas mostra A+B e C+D logo depois de pulos. A luta não pôde ser repetida: o dono usou o reset do MAME (F3) para trocar de adversário, a gravação não registra resets, e uma repetição a partir da inicialização chegou a outro adversário. Nas próximas sessões gravadas, é melhor reabrir o MAME do que usar F3. Os cancelamentos no modo MAX continuam em aberto._

### 2026-11-15 — Cancels in MAX mode

The owner reports that Guile cannot cancel a special move into a super in SVC, even in MAX mode. He could not do it and has never seen it done.

_PT-BR: o dono relata que, no SVC, Guile não consegue cancelar um movimento especial em super, nem mesmo no modo MAX. Ele não conseguiu fazer isso e nunca viu ninguém fazer._

The owner adds that Guile can cancel certain normal attacks. Decision: imported fighters keep the cancels found in their SVC data and get no new ones ([ADR 0003](../../../adr/0003-imported-cancels-come-from-svc-data.md)).

_PT-BR: o dono acrescenta que Guile cancela certos golpes normais. Decisão: os importados mantêm os cancelamentos encontrados nos dados do SVC e não ganham novos ([ADR 0003](../../../adr/0003-imported-cancels-come-from-svc-data.md))._
