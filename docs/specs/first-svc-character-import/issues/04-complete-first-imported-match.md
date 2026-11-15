---
title: "Complete the first Imported Character match"
triage: ready-for-agent
---

# 04 Complete the first Imported Character match

[Parent specification](../spec.md)

## What to build

Select the SVC import in native KOF 2003 and finish a scripted MVS team match against original fighters with a small, working set of combat actions.

## Blocked by

[02 Complete a native team match](02-complete-native-single-match.md) · [03 Capture the SVC Exclusive Character reference](03-capture-svc-fighter-reference.md)

## Acceptance criteria

- [ ] The Imported Character is selectable through the game's selection flow and original roster entries remain available.
- [ ] Movement, guarding and a basic attack work with recognizable visuals and timing. The scripted checks distinguish hit, block and whiff and verify the KOF 2003 outcomes.
- [ ] A replay from known initial state reaches the normal match result and shows native execution of the exercised behavior. Start recording reusable work, manual adaptation and blockers.

## Português (Brasil)

Selecionar o importado do SVC no KOF 2003 nativo e terminar uma luta de equipes MVS por script contra lutadores originais, com um conjunto inicial de ações de combate.

### Bloqueios

[02 Complete a native team match](02-complete-native-single-match.md) · [03 Capture the SVC Exclusive Character reference](03-capture-svc-fighter-reference.md)

### Critérios de aceitação

- [ ] O personagem importado pode ser escolhido pela seleção do jogo e o elenco original continua disponível.
- [ ] Movimentação, defesa e um golpe básico funcionam com visuais e duração reconhecíveis. Os testes por script distinguem acerto, defesa e golpe no vazio e conferem os resultados sob as regras do KOF 2003.
- [ ] Uma repetição a partir de um estado inicial conhecido chega ao resultado normal e mostra execução nativa do comportamento exercitado. Começar a registrar trabalho reaproveitável, adaptação manual e bloqueios.

## Comments

### 2026-11-15 — Plan and decisions

Plan in five phases: (1) map KOF 2003's selection table, per-fighter code and animation lookup, free graphics space and palettes in MAME; (2) add a per-frame memory probe to the local native runtime copy and rebuild; (3) make Guile visible in selection, idle and walking; (4) add guarding and one basic attack with KOF 2003 collision, validated with the scripted versus test used in ticket 03; (5) run a scripted team match to the normal result with `--verify`, recording reusable and manual work.

The owner asked for the lowest-effort options and authorized the native rebuild. Guile goes into an existing KOF 2003 fighter slot that the official MVS selection does not show (Adelheid or Mukai), so no original fighter is removed and no table needs enlarging. Guile is translated into the KOF 2003 ROM data rather than written as C in the port, so the port's generator produces native code for him and the same build also runs in MAME for comparison.

_PT-BR: plano em cinco fases: (1) mapear no MAME a tabela de seleção do KOF 2003, o código e a busca de animações de cada lutador, o espaço livre para gráficos e as paletas; (2) acrescentar à cópia local do runtime nativo uma sonda de memória por quadro e recompilar; (3) tornar Guile visível na seleção, parado e andando; (4) acrescentar defesa e um golpe básico com a colisão do KOF 2003, validados com o versus por roteiro usado no ticket 03; (5) jogar uma partida de equipes por roteiro até o resultado normal com `--verify`, registrando o trabalho reaproveitável e o manual._

_O dono pediu as opções de menor esforço e autorizou a recompilação do nativo. Guile entra num espaço de lutador existente no KOF 2003 que a seleção oficial do MVS não mostra (Adelheid ou Mukai), de modo que nenhum lutador original sai e nenhuma tabela precisa ser ampliada. Guile é traduzido para os dados da ROM do KOF 2003, e não escrito em C no port, para que o gerador do port produza o código nativo dele e a mesma montagem também rode no MAME para comparação._
