---
id: 09
title: "Choose Guile's run and backstep animations"
label: wayfinder:prototype
mode: HITL
status: closed
assignee: tel
blocked_by: [05]
research:
---

## Question

KOF 2003 runs while forward is held and hops back on back-back; SVC has a short dash and backdash. Which of Guile's SVC animations stands in for the run loop and for the backstep, and how is it retimed? KOF 2003 sets speed, distance and duration. Show the candidates as frame strips or a GIF from MAME captures kept in `private/`.

_PT-BR: O KOF 2003 corre enquanto se segura frente e dá um passo para trás com trás-trás; o SVC tem dash curto para frente e para trás. Qual animação do Guile no SVC faz o papel do ciclo de corrida e do passo para trás, e como ela é reajustada no tempo? O KOF 2003 define velocidade, distância e duração. Mostrar as opções em tiras de quadros ou GIF capturados no MAME, guardados em `private/`._

## Notes

- [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md): SVC has no run; holding forward after the 19-frame, 72 px front step returns to the walk loop (30 frames, 6 poses). The back step is a 25-frame, 86 px hop of height 16, mostly walk poses.
- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): KOF 2003's run is state `$23` (actions `$44`–`$46`) and its backstep state `$24` (actions `$47`–`$49`), common code; speeds come from per-fighter step scripts.
- KOF 2003's own speeds, distances and durations were not measured. The prototype session measures the reference it retimes to.

_PT-BR: o SVC não tem corrida; segurar frente depois do dash de 19 quadros e 72 px volta ao ciclo de andar. O passo para trás é um saltinho de 25 quadros, 86 px e altura 16. No KOF 2003 a corrida é o estado `$23` e o passo para trás o `$24`, código comum, com velocidades nos scripts de passos do lutador. As medidas do KOF 2003 não foram feitas; a sessão de protótipo mede a referência._

## Resolution

Decided with the owner on 2026-11-16, looking at frame strips captured from SVC in MAME (kept in `private/work/svc-guile/tests/` as `run-walk`, `run-dash` and `run-backstep`; nothing from them is in the repository).

**Run.** SVC Guile has no run, so the run loop (KOF 2003 state `$23`, actions `$44`-`$46`) is his front step, the low sliding dash, repeated in a loop while forward is held, **played a little faster** than in SVC. The owner rejected a sped-up walk (it reads as a fast walk, not a run) and the mix of dash and walk.

**Backstep.** The backstep (state `$24`, actions `$47`-`$49`) is his SVC back-step hop as it is (25 frames, 86 px, height 16), with only its timing adjusted to fit the state.

**Refinement of the run loop (owner, 2026-11-16).** Measured, KOF 2003's run loop (action `$45`) lasts 24 frames in 19 of the 37 fighters, and in 18 of them it is 6 poses of 4 frames each; its start (`$44`) lasts 2-5 frames and its stop (`$46`) 2-8, typically 3. SVC Guile's dash is 19 frames in 7 poses lasting 1, 1, 2, 3, 7, 2 and 3 frames. The adapted loop must end with the same number of frames as KOF 2003's and change poses at the same pace. Three candidates were shown as GIFs of Guile crossing a plain screen: A (6 poses of 4 frames, dropping the 1-frame start pose), B (7 poses stretched to 24: 1, 1, 3, 4, 9, 3, 3) and C (8 steps of 3 frames, repeating the long pose). **A is the choice**: same shape and uniform pace as the most common KOF 2003 run, one duration for the converter and the fewest distinct frames and tiles; it needs no 68000 code in any case (frames and timing are data, [ticket 20](20-frame-and-collision-format.md)). Where the dropped start pose goes (for example the run start `$44`) was not checked and is left to the implementation tickets. The GIFs are in `private/work/svc-guile/tests/cut-key/`.

**Scope (owner).** This holds for every SVC fighter imported, not only Guile, like the jumps of [ticket 10](10-four-jumps.md).

**Left open.** KOF 2003's own run and backstep speeds, distances and durations were not measured, so how much faster than SVC the run plays, and the exact retiming of both, are set when the reference is measured; this belongs to the implementation tickets, not to the map.

**PT-BR**

Decidido com o dono em 16/11/2026, olhando tiras de quadros capturadas do SVC no MAME (ficam em `private/work/svc-guile/tests/` como `run-walk`, `run-dash` e `run-backstep`; nada delas está no repositório).

**Corrida.** O Guile do SVC não tem corrida, então o ciclo de corrida (estado `$23` do KOF 2003, ações `$44`-`$46`) é o passo para frente dele, o dash baixo deslizante, repetido em ciclo enquanto se segura frente, **tocado um pouco mais rápido** que no SVC. O dono recusou o andar acelerado (parece andar rápido, não corrida) e a mistura de dash com andar.

**Passo para trás.** O passo para trás (estado `$24`, ações `$47`-`$49`) é o saltinho de costas do Guile no SVC como está (25 quadros, 86 px, altura 16), só com o tempo ajustado para caber no estado.

**Refinamento do ciclo de corrida (dono, 16/11/2026).** Medido, o ciclo de corrida do KOF 2003 (ação `$45`) dura 24 quadros em 19 dos 37 lutadores, e em 18 deles são 6 poses de 4 quadros cada; a partida (`$44`) dura 2 a 5 quadros e a parada (`$46`) 2 a 8, tipicamente 3. O dash do Guile no SVC tem 19 quadros em 7 poses de 1, 1, 2, 3, 7, 2 e 3 quadros. O ciclo adaptado precisa terminar com o mesmo número de quadros do KOF 2003 e trocar de pose no mesmo ritmo. Três candidatos foram mostrados em GIFs do Guile cruzando uma tela lisa: A (6 poses de 4 quadros, sem a pose inicial de 1 quadro), B (7 poses esticadas até 24: 1, 1, 3, 4, 9, 3, 3) e C (8 passos de 3 quadros, repetindo a pose longa). **A é a escolha**: mesma forma e ritmo uniforme da corrida mais comum do KOF 2003, uma duração só para o conversor e o menor número de quadros e tiles distintos; não pede código 68000 em nenhum caso (quadros e tempos são dados, [ticket 20](20-frame-and-collision-format.md)). Para onde vai a pose inicial tirada (por exemplo, a partida `$44`) não foi verificado e fica para os tickets de implementação. Os GIFs estão em `private/work/svc-guile/tests/cut-key/`.

**Alcance (dono).** Vale para todo lutador do SVC importado, não só o Guile, como os pulos do [ticket 10](10-four-jumps.md).

**Em aberto.** As velocidades, distâncias e durações da corrida e do passo para trás do próprio KOF 2003 não foram medidas, então quanto mais rápido que no SVC a corrida toca, e o reajuste exato dos dois, ficam para quando a referência for medida; isso é dos tickets de implementação, não do mapa.
