---
id: 09
title: "Choose Guile's run and backstep animations"
label: wayfinder:prototype
mode: HITL
status: open
assignee:
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
