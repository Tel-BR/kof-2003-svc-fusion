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

- [x] Document a reproducible build from the validated cartridge and BIOS inputs. Keep third-party source and game-derived artifacts out of Git.
- [x] Replay the native MVS control with original fighters and record coverage, fallback, state divergences and cycle differences. Reproduce the zero-state-divergence result.
- [x] Consult the owner before starting noisy or resource-intensive builds.

## Português (Brasil)

Gerar um executável Windows modificável com os dumps validados e repetir a verificação MVS original.

### Bloqueios

Nenhum.

### Critérios de aceitação

- [x] Documentar um build reproduzível com o cartucho e a BIOS validados. Manter fontes de terceiros e artefatos derivados dos jogos fora do Git.
- [x] Repetir o controle nativo de MVS com lutadores originais e registrar cobertura, retornos ao interpretador, divergências de estado e diferenças de ciclos. Reproduzir o resultado de zero divergências de estado.
- [x] Consultar o dono antes de iniciar builds barulhentos ou que afetem muito o desempenho da máquina.

The owner approved compilation on 2026-11-13 with one job at a time and separate phases that can be resumed.

Em 13/11/2026, o dono autorizou a compilação com um processo por vez e etapas separadas que podem ser retomadas.

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

## Resolution / Resolução

On 2026-11-13, the locally rebuilt Windows player completed the same 6,000-frame control. The first run profiled 385 runtime entry points, which were added before regenerating and compiling the native C. The rebuilt player reached Iori vs. Whip at frame 5,400, with a capture identical by SHA-256 to the published player's capture. Rerunning the build targets with the same inputs required no work.

Em 13/11/2026, o executável Windows recompilado localmente completou o mesmo controle de 6.000 quadros. O primeiro perfil registrou 385 pontos de entrada, incluídos antes da geração e compilação final do C nativo. O executável recompilado chegou à luta de Iori contra Whip no quadro 5.400, com captura de SHA-256 idêntico ao da versão publicada. Repetir os alvos de build com as mesmas entradas dispensou recompilação.

| Metric / Métrica | Local build / Build local |
| --- | ---: |
| Recompiled entry points / Pontos de entrada recompilados | 18,222 |
| Native blocks checked / Blocos nativos verificados | 3,583,419 |
| Native 68000 instructions / Instruções 68000 nativas | 118,359,669 |
| Native instruction coverage / Cobertura de instruções nativas | 100.00% |
| Fallback instructions / Instruções executadas pelo interpretador | 0 |
| Uncovered entry points / Pontos de entrada sem cobertura | 0 |
| State divergences / Divergências de estado | 0 |
| Cycle-count differences / Diferenças de contagem de ciclos | 2,669 |

The port's full Windows headless script also completed with zero state divergences in its two verification runs. Its separate 2,000-frame boot used 198 fallback instructions. The 9,000-frame gameplay run used 18,817 fallback instructions and reported 99.99% native coverage. The local profile was built for the 6,000-frame control.

O script completo de testes do port para Windows em modo sem janela também terminou com zero divergências de estado nas duas verificações. A inicialização separada de 2.000 quadros usou 198 instruções em fallback. A luta de 9.000 quadros usou 18.817 instruções em fallback e teve 99,99% de cobertura nativa. O perfil local foi preparado para o controle de 6.000 quadros.
