---
title: "Explain the in-fight input divergence between native and MAME"
triage: wontfix
---

# 07 Explain the in-fight input divergence between native and MAME

[Parent specification](../spec.md)

## What to build

Find why the native KOF 2003 player and the MAME MVS reference diverge right after the first player input during a fight. Fix it if the native port is at fault, or document the difference if MAME is.

## Blocked by

None. Found in [02 Complete a native team match](02-complete-native-single-match.md).

## Acceptance criteria

- [ ] Reproduce the divergence with `tools/kof2003/match/` and identify the first frame and the first state that differ, such as an input register, a BIOS input variable, a random number or the CPU opponent's state.
- [ ] Establish which runtime departs from the Neo Geo hardware behaviour, with a source.
- [ ] If the native port is at fault, change the local copy outside this repository and show a scripted fight that stays identical in both runtimes. Otherwise document the difference and how comparisons work around it.

## Português (Brasil)

Descobrir por que o executável nativo do KOF 2003 e a referência MVS no MAME divergem logo após o primeiro comando do jogador durante uma luta. Corrigir se a falha for do port nativo, ou documentar a diferença se for do MAME.

### Bloqueios

Nenhum. Encontrado no ticket [02 Complete a native team match](02-complete-native-single-match.md).

### Critérios de aceitação

- [ ] Reproduzir a divergência com `tools/kof2003/match/` e identificar o primeiro quadro e o primeiro estado que diferem, como um registrador de entrada, uma variável de entrada da BIOS, um número aleatório ou o estado do adversário da CPU.
- [ ] Determinar, com fonte, qual dos runtimes se afasta do comportamento do hardware Neo Geo.
- [ ] Se a falha for do port nativo, alterar a cópia local fora deste repositório e mostrar uma luta por roteiro que permaneça idêntica nos dois runtimes. Caso contrário, documentar a diferença e como as comparações a contornam.

## Comments

### 2026-11-15 — Observation

With identical inputs through coin, start and team selection, both runtimes stay identical up to the fight. A plain walk forward from frame 5,600 for 30 frames makes the CPU-controlled Whip react differently by frame 5,605: she attacks low in MAME and stays standing in the native player. Without in-fight input both runs stay identical to at least frame 6,000. Shifting MAME's input alignment by one frame either way does not remove the difference. Details in [ticket 02](02-complete-native-single-match.md#2026-11-15--replay-tooling-and-first-comparison).

_PT-BR: com as mesmas entradas nas fichas, no start e na seleção, os dois runtimes ficam idênticos até a luta. Uma caminhada simples para a frente a partir do quadro 5.600, por 30 quadros, faz a Whip controlada pela CPU reagir de forma diferente já no quadro 5.605: ela ataca agachada no MAME e continua de pé no nativo. Sem comandos durante a luta, as duas execuções ficam idênticas até pelo menos o quadro 6.000. Deslocar o alinhamento das entradas do MAME em um quadro para qualquer lado não elimina a diferença._

### 2026-11-15 — Closed by the owner

Both runtimes had the same opponent, Whip, on the same stage with identical teams, and the captures matched up to frame 5,600. The owner closed the ticket as wontfix. Later comparisons check each runtime on its own instead of expecting a scripted fight to stay identical across them.

_PT-BR: os dois runtimes tinham o mesmo adversário, Whip, no mesmo cenário e com equipes idênticas, e as capturas coincidiam até o quadro 5.600. O dono fechou o ticket como wontfix. As próximas comparações avaliam cada runtime por conta própria, sem esperar que uma luta por roteiro continue idêntica entre eles._

### 2026-11-15 — Other opponents stay identical

At the owner's request, the same 30-frame walk forward from frame 5,600 was repeated with two other teams chosen by moving the selection cursor. Yamazaki vs. Maxima and Kyo vs. K' stayed identical in both runtimes through frame 6,000, apart from the usual one-frame sprite latch. Only the Iori vs. Whip fight diverged. The divergence is therefore specific to Whip or to that pairing, not a general difference in CPU behaviour. Difficulty and the calendar clock are unlikely causes, because they apply equally to all three fights. Both runtimes start with empty MVS backup RAM, and each reads the calendar from the host clock. The ticket stays closed unless the owner reopens it.

_PT-BR: a pedido do dono, a mesma caminhada para a frente de 30 quadros a partir do quadro 5.600 foi repetida com outras duas equipes, escolhidas movendo o cursor da seleção. Yamazaki contra Maxima e Kyo contra K' continuaram idênticos nos dois runtimes até o quadro 6.000, exceto pela diferença habitual de um quadro nos sprites. Só a luta de Iori contra Whip divergiu. A divergência é, portanto, específica da Whip ou desse confronto, e não uma diferença geral no comportamento da CPU. Dificuldade e relógio do calendário são causas improváveis, porque valem igualmente para as três lutas. Os dois runtimes começam com a memória de backup do MVS vazia e cada um lê o calendário do relógio do PC. O ticket continua fechado, a menos que o dono o reabra._
