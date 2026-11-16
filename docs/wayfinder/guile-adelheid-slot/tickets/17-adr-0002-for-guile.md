---
id: 17
title: "Decide whether ADR 0002 holds for Guile, whose SVC break-fall is not a roll"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: owner
blocked_by: []
research:
---

## Question

[ADR 0002](../../../adr/0002-evasive-rolls-from-recovery-animation.md) draws every imported fighter's evasive rolls and Guard Cancel roll from that fighter's SVC knockdown recovery roll, on the owner's report that every SVC fighter has one. [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md) found that Guile's break-fall, A+B on landing after a sweep and after an uppercut, is a 7-frame slide in the jump's landing-crouch poses, not a roll. Other knockdowns were not tested, and the ADR describes A+B before landing while the research pressed it at landing. [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) found that KOF 2003's forward Guard Cancel roll reuses the normal forward roll's state `$30` and actions `$4A`–`$4C`, and that the back Guard Cancel roll was inconclusive.

Does ADR 0002 stand for Guile as written, change its source animation (for example the back step or the knockdown get-up), or wait for more measurement first? A change supersedes the ADR with a new one, and it bears on every later SVC import.

_PT-BR: a ADR 0002 faz as esquivas e a esquiva de Guard Cancel de todo importado a partir da cambalhota de recuperação de queda do próprio lutador no SVC, com base no relato do dono de que todo lutador do SVC a tem. A pesquisa 05 viu que a recuperação do Guile, A+B ao tocar o chão depois de rasteira e de gancho, é um deslize de 7 quadros nas poses agachadas do pouso do pulo, não uma cambalhota. Outras quedas não foram testadas, e a ADR fala em A+B antes de tocar o chão, enquanto a pesquisa apertou ao tocar. A pesquisa 01 viu que a esquiva de Guard Cancel para a frente do KOF 2003 reaproveita o estado `$30` e as ações `$4A`–`$4C` da esquiva normal, e que a de trás ficou inconclusiva. A ADR 0002 vale para o Guile como está, muda a animação de origem (por exemplo o passo para trás ou o levantar da queda) ou espera mais medições? Uma mudança substitui a ADR por outra e vale para os próximos importados._

## Resolution

**ADR 0002 stands for Guile exactly as written.** The owner (2026-11-16) clarified that "recovery roll" (_cambalhota_) in the ADR was only vocabulary: it names the knockdown recovery performed with A+B, whatever it looks like, not a claim that it is a tumbling roll. So the source animation for Guile's evasive rolls and Guard Cancel roll is his own SVC break-fall, which [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md) measured as a 7-frame slide, retimed to KOF 2003's roll duration with KOF 2003 supplying distance, invulnerability and cost. No new ADR; the ADR's text is untouched. Still facts for implementation, not decisions: other knockdown types were not tested, and the back Guard Cancel roll was inconclusive in [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md).

**PT-BR**

**A ADR 0002 vale para o Guile exatamente como está escrita.** O dono (16/11/2026) esclareceu que "cambalhota de recuperação" na ADR era só vocabulário: nomeia a recuperação de queda feita com A+B, seja qual for a aparência, e não afirma que ela seja uma cambalhota de verdade. Assim, a animação de origem das esquivas e da esquiva de Guard Cancel do Guile é a recuperação de queda dele no SVC, que a pesquisa 05 mediu como um deslize de 7 quadros, reajustado à duração da esquiva do KOF 2003, com o KOF 2003 definindo distância, invencibilidade e custo. Não há ADR nova e o texto da ADR não muda. Continuam como fatos para a implementação, não como decisões: outros tipos de queda não foram testados, e a esquiva de Guard Cancel para trás ficou inconclusiva na pesquisa 01.
