---
id: 27
title: "Choose how Guile's own sounds reach KOF 2003"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
blocked_by: [25, 26]
research:
---

## Question

With what [25](25-kof2003-sound-playback.md) and [26](26-svc-guile-sounds.md) found, how do Guile's own SVC sounds, voice and effects get into native KOF 2003, and at what cost? Which sounds are in this slice, which wait, and what is silent meanwhile? The answer is an import rule for every SVC fighter, like the animation rules.

_PT-BR: com o que os tickets 25 e 26 acharam, como os sons do próprio Guile no SVC, voz e efeitos, entram no KOF 2003 nativo, e a que custo? Quais sons entram nesta fatia, quais esperam e o que fica mudo enquanto isso? A resposta é uma regra de importação para todo lutador do SVC, como as regras de animação._

## Decision recorded

On 2026-11-16 the owner chose to use KOF 2003's reusable sounds for shared effects on Guile and every other Imported Character. SVC audio imports are limited to sounds specific to the Imported Character, including their voice. The choice of KOF 2003 equivalents and the route for adding character-specific samples are still open.

_PT-BR: em 16/11/2026, o dono escolheu usar os sons reaproveitáveis do KOF 2003 para os efeitos compartilhados do Guile e dos demais Personagens Importados. A importação de áudio do SVC fica restrita aos sons próprios de cada personagem, incluindo a voz. A escolha dos equivalentes no KOF 2003 e o caminho para acrescentar as amostras próprias seguem em aberto._
