---
title: "Reproduce native KOF 2003 in MVS"
triage: ready-for-agent
---

# 01 Reproduce native KOF 2003 in MVS

[Parent specification](../spec.md)

## What to build

Build a modifiable Windows player from the validated dumps and replay the original MVS verification run.

## Blocked by

None.

## Acceptance criteria

- [ ] Document a reproducible build from the validated cartridge and BIOS inputs. Keep third-party source and game-derived artifacts out of Git.
- [x] Replay the native MVS control with original fighters and record coverage, fallback, state divergences and cycle differences. Reproduce the zero-state-divergence result.
- [ ] Consult the owner before starting noisy or resource-intensive builds.

## Português (Brasil)

Gerar um executável Windows modificável com os dumps validados e repetir a verificação MVS original.

### Bloqueios

Nenhum.

### Critérios de aceitação

- [ ] Documentar um build reproduzível com o cartucho e a BIOS validados. Manter fontes de terceiros e artefatos derivados dos jogos fora do Git.
- [x] Repetir o controle nativo de MVS com lutadores originais e registrar cobertura, retornos ao interpretador, divergências de estado e diferenças de ciclos. Reproduzir o resultado de zero divergências de estado.
- [ ] Consultar o dono antes de iniciar builds barulhentos ou que afetem muito o desempenho da máquina.

## MVS control / Controle MVS

On 2026-11-12, the published Windows x64 player `v0.1.0` replayed the original 6,000-frame `tests/play.txt` session twice with the validated `kof2003` cartridge and Europe MVS v2 BIOS. A capture from the second run showed Iori vs. Whip in a live match at frame 5,400.

Em 12/11/2026, o executável publicado para Windows x64 `v0.1.0` repetiu duas vezes a sessão original de 6.000 quadros com `tests/play.txt`, o cartucho validado `kof2003` e a BIOS Europe MVS v2. Uma captura da segunda execução mostrou Iori contra Whip em luta no quadro 5.400.

| Metric / Métrica | Run 1 / Execução 1 | Run 2 / Execução 2 |
| --- | ---: | ---: |
| Recompiled entry points / Pontos de entrada recompilados | 18,439 | 18,439 |
| Native blocks checked / Blocos nativos verificados | 3,583,431 | 3,583,432 |
| Native 68000 instructions / Instruções 68000 nativas | 118,359,695 | 118,359,695 |
| Native instruction coverage / Cobertura de instruções nativas | 100.00% | 100.00% |
| Fallback instructions / Instruções executadas pelo interpretador | 0 | 0 |
| Uncovered entry points / Pontos de entrada sem cobertura | 0 | 0 |
| State divergences / Divergências de estado | 0 | 0 |
| Cycle-count differences / Diferenças de contagem de ciclos | 2,669 | 2,669 |

The port's reference report counted 3,583,410 blocks. The local runs matched its zero state divergences, zero fallback and 2,669 cycle differences. [Original test report](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/v0.1.0/docs/TESTING.md)

O relatório de referência do port contou 3.583.410 blocos. As execuções locais repetiram o resultado de zero divergências de estado, zero fallback e 2.669 diferenças de ciclos. [Relatório original](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/v0.1.0/docs/TESTING.md)

See the [Windows build and MVS replay guide](../native-mvs-windows.md). / Consulte o [guia de build Windows e repetição do teste MVS](../native-mvs-windows.md).
