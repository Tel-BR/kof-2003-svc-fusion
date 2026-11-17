---
id: 13
title: "Choose how Adelheid's sounds map to Guile's actions"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: [01, 05]
research:
---

## Question

Guile uses Adelheid's sounds (owner, 2026-11-15). Which sound plays for each of Guile's actions in this slice, where his actions do not line up one to one with hers? What is silent?

_PT-BR: O Guile usa os sons da Adelheid (dono, 15/11/2026). Que som toca em cada ação do Guile nesta fatia, onde as ações dele não correspondem uma a uma às dela? O que fica mudo?_

## Notes

- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): sound codes sit in the per-fighter step scripts (a code word after a flag bit) and in 16 per-fighter situation tables at `$6CF1E` (Adelheid's entry `$22` in each). Guile's converted step scripts will carry whichever of Adelheid's codes this ticket assigns.

_PT-BR: os códigos de som ficam nos scripts de passos do lutador e em 16 tabelas de situação em `$6CF1E` (entrada `$22` da Adelheid). Os scripts de passos convertidos do Guile levam os códigos da Adelheid que este ticket escolher._

## Resolution

**Superseded (owner, 2026-11-16).** Nothing is reused from Adelheid: Guile uses his own SVC sounds, voice and effects, including the sound of his break-fall recovery for the evasive rolls. The question of which Adelheid sound plays for each of his actions no longer applies, and the earlier decision of 2026-11-15 ("Guile uses Adelheid's sounds") is replaced. Out of scope until now ("Guile's own SVC voice and sound conversion"), sound conversion is back in scope and needs research first: [25](25-kof2003-sound-playback.md) and [26](26-svc-guile-sounds.md), then the decision in [27](27-guile-sounds-route.md).

What was read for this ticket stays as reference for where sounds sit in a fighter's data: in Adelheid's step scripts, the universal actions with sounds are the run loop (one code at the first step), the jumps (take-off and landing codes), the backstep (hop and landing), the rolls, and the start of most attacks; walking, crouching, guarding and idling have none.

**PT-BR**

**Substituído (dono, 16/11/2026).** Nada é reaproveitado da Adelheid: o Guile usa os sons dele no SVC, voz e efeitos, inclusive o som da recuperação de queda dele nas esquivas. A pergunta de qual som da Adelheid toca em cada ação não vale mais, e a decisão anterior de 15/11/2026 ("o Guile usa os sons da Adelheid") fica substituída. Fora do escopo até aqui ("voz do Guile no SVC e conversão de som"), a conversão de som volta ao escopo e precisa de pesquisa antes: [25](25-kof2003-sound-playback.md) e [26](26-svc-guile-sounds.md), depois a decisão em [27](27-guile-sounds-route.md).

O que foi lido para este ticket fica como referência de onde os sons ficam nos dados de um lutador: nos scripts de passos da Adelheid, as ações universais com som são o ciclo de corrida (um código no primeiro passo), os pulos (códigos de saída e de pouso), o passo para trás (salto e pouso), os rolamentos e o começo da maioria dos golpes; andar, agachar, defender e ficar parado não têm.
