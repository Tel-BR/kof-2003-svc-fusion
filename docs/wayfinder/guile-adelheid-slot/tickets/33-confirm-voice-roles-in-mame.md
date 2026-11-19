---
id: 33
title: "Confirm in MAME the roles of Guile's inferred voices"
label: wayfinder:task
mode: HITL
status: open
assignee:
blocked_by: [31]
research:
---

## Question

[30](30-guile-svc-remaining-sounds.md) inferred the roles of Guile's remaining voices by static reading: hurt tiers, launch hurt, taunt, third attack tier, throw, knockout, which move records are specials and which are supers, and whether the eight voices with no static trigger ever play. None was confirmed in a MAME run. Run SVC Chaos in MAME on the owner's machine with Guile and record, for each candidate sample, the situation in which it plays (or that it never plays), as sample range and situation only. The answer feeds the per-fighter register of [31](31-guile-remaining-voices-choice.md), part 3, and blocks only the mapping of the hooks.

_PT-BR: o [30](30-guile-svc-remaining-sounds.md) inferiu por leitura estática os papéis das vozes restantes do Guile: níveis de dor, dor de lançamento, provocação, terceiro nível de ataque, arremesso, nocaute, quais registros de golpe são especiais e quais são supers, e se as oito vozes sem gatilho estático chegam a tocar. Nenhum foi confirmado numa execução do MAME. Rodar o SVC Chaos no MAME na máquina do dono com o Guile e anotar, para cada amostra candidata, a situação em que ela toca (ou que nunca toca), só como faixa da amostra e situação. A resposta alimenta o registro por lutador da parte 3 do [31](31-guile-remaining-voices-choice.md) e bloqueia só o mapeamento dos ganchos._

## Notes

- Task type: the work is a manual run, so the agent hands the owner a precise checklist when this ticket is taken.
- Hard rule of `AGENTS.md`: no game data in the notes; sample ranges and situations only.
