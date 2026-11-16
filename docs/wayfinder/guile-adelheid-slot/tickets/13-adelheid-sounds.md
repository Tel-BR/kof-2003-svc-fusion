---
id: 13
title: "Choose how Adelheid's sounds map to Guile's actions"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
blocked_by: [01, 05]
research:
---

## Question

Guile uses Adelheid's sounds (owner, 2026-11-15). Which sound plays for each of Guile's actions in this slice, where his actions do not line up one to one with hers? What is silent?

_PT-BR: O Guile usa os sons da Adelheid (dono, 15/11/2026). Que som toca em cada ação do Guile nesta fatia, onde as ações dele não correspondem uma a uma às dela? O que fica mudo?_

## Notes

- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): sound codes sit in the per-fighter step scripts (a code word after a flag bit) and in 16 per-fighter situation tables at `$6CF1E` (Adelheid's entry `$22` in each). Guile's converted step scripts will carry whichever of Adelheid's codes this ticket assigns.

_PT-BR: os códigos de som ficam nos scripts de passos do lutador e em 16 tabelas de situação em `$6CF1E` (entrada `$22` da Adelheid). Os scripts de passos convertidos do Guile levam os códigos da Adelheid que este ticket escolher._
