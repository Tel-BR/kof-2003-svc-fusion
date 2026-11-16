---
title: "Prove the 64 MiB reference build repeats itself"
triage: ready-for-agent
---

# 01 Prove the 64 MiB reference build repeats itself

[Parent specification](../spec.md)

## What to build

Keep today's native player, with its 64 MiB Graphics Set, as build A, apart from every build that will change. Add the step that compares two sets of captures by hash and reports equal or the first differing frame. Run A twice with the coin-and-start script and the team-match script, with captures from boot, attract mode, selection and the fight, and record whether the same inputs always give the same frames. Without this, no later comparison means anything.

_PT-BR: manter o player nativo de hoje, com Conjunto gráfico de 64 MiB, como build A, à parte de qualquer build que vá mudar. Acrescentar a etapa que compara dois conjuntos de capturas por hash e informa igual ou o primeiro quadro diferente. Rodar o A duas vezes com o roteiro de moeda e início e o de luta de equipe, com capturas de abertura, demonstração, seleção e luta, e registrar se as mesmas entradas dão sempre os mesmos quadros. Sem isso, nenhuma comparação posterior vale._

**Suggested model and effort:** Sonnet 5.5, medium. Escalate to Opus 5.5 only if A is not deterministic and the cause needs digging in the runtime. / _Sonnet 5.5, esforço médio. Escalar para o Opus 5.5 só se o A não for determinístico e a causa exigir investigar o runtime._

## Blocked by

None.

## Acceptance criteria

- [x] Build A is built from the unchanged descriptor and kept where later tickets cannot overwrite it.
- [x] The comparison step reports equal, or the first differing frame, for two capture sets, with Python tests in the style of the existing match tests (equal sets, one differing frame, a missing frame).
- [x] A is run twice with both scripts and every capture pair is identical; if not, the first differing frame and the likely cause are recorded here and the stage stops until the cause is found.
- [x] Captures stay under `private/`. This ticket records only hashes, frame numbers and counts.
- [x] The commands to rebuild A and rerun the comparison are recorded under `tools/kof2003/`.

_PT-BR:_

- _O build A é compilado a partir do descritor sem mudança e guardado onde os tickets seguintes não possam sobrescrevê-lo._
- _A etapa de comparação informa igual, ou o primeiro quadro diferente, para dois conjuntos de capturas, com testes Python no estilo dos testes de `match` existentes (conjuntos iguais, um quadro diferente, um quadro faltando)._
- _O A roda duas vezes com os dois roteiros e todo par de capturas é idêntico; se não for, o primeiro quadro diferente e a causa provável são registrados aqui e a etapa para até a causa ser achada._
- _As capturas ficam em `private/`. Este ticket registra só hashes, números de quadro e contagens._
- _Os comandos para recompilar o A e repetir a comparação ficam registrados em `tools/kof2003/`._

## Status (2026-11-16)

**Closed: A repeats itself (see Result below).** _Earlier note, kept for history:_  Everything the ticket needs is in place, but the player is a Windows executable and this session's shell is Linux, so A has not been run yet. Run on Windows, from `tools/kof2003`: `py -3 -m match.repeat_reference`. It runs A twice on `coin-start` (6,000 frames; captures at 600, 2,000, 3,000, 4,000, 5,400) and `team-match` (8,000 frames; captures at 600, 2,000, 3,000, 4,000, 5,400, 6,000, 7,000), compares each pair by hash, and prints the hashes. Record the result here; if any pair differs, record the first differing frame and the likely cause, and the stage stops.

Done: build A kept read-only in `private/work/graphics-growth/build-a/` (copy of the 2026-11-13 native build, descriptor graphics size still `0x4000000`; `KOF 2003.exe` SHA-256 `a3d2cab5…cfe75`); `match/compare_captures.py` with 8 tests (equal sets, one differing frame, lowest frame first, frame missing either side, empty sets, other files ignored, exit codes); `match/repeat_reference.py`; `scripts/coin-start.txt`; commands in `tools/kof2003/match/README.md`.

_PT-BR: **Em aberto: as duas execuções do A.** Tudo o que o ticket pede está pronto, mas o player é um executável de Windows e o shell desta sessão é Linux, então o A ainda não foi rodado. No Windows, a partir de `tools/kof2003`: `py -3 -m match.repeat_reference`. Ele roda o A duas vezes com `coin-start` (6.000 quadros; capturas em 600, 2.000, 3.000, 4.000, 5.400) e `team-match` (8.000 quadros; capturas em 600, 2.000, 3.000, 4.000, 5.400, 6.000, 7.000), compara cada par por hash e imprime os hashes. Registrar o resultado aqui; se algum par diferir, registrar o primeiro quadro diferente e a causa provável, e a etapa para. Pronto: build A guardado em somente leitura em `private/work/graphics-growth/build-a/` (cópia do build nativo de 13/11/2026, tamanho gráfico do descritor ainda `0x4000000`); `match/compare_captures.py` com 8 testes; `match/repeat_reference.py`; `scripts/coin-start.txt`; comandos em `tools/kof2003/match/README.md`._

## Result (2026-11-16, Windows)

`py -3 -m match.repeat_reference` ran build A twice per script, headless, with 0 `--verify` state mismatches in all four runs. Every capture pair is identical by SHA-256: `coin-start` 5 of 5 (frames 600, 2,000, 3,000, 4,000, 5,400), `team-match` 7 of 7 (those plus 6,000 and 7,000). Capture hashes at the shared frames, for the later comparison with B:

| Frame | SHA-256 |
|---|---|
| 600 | `8f92866c…21c3a2` |
| 2,000 | `b6cb2c44…f9b2` |
| 3,000 | `6e5147fd…ffb2a` |
| 4,000 | `a5e82aba…1675` |
| 5,400 | `fa9c6abd…6d53` |
| 6,000 | `229b6074…cf2` |
| 7,000 | `84462783…7b342b1` |

Full hashes are in `private/work/graphics-growth/repeat-a.log`. One thing to know: the number of blocks `--verify` checked differs slightly between the two runs of the same script (3,575,508 vs 3,575,422 for `coin-start`; 5,826,109 vs 5,826,056 for `team-match`), while the frames are identical. It is a count of checked blocks, not drawn output, so it does not affect the comparison; it is recorded in case it matters later.

_PT-BR: **Resultado (16/11/2026, Windows).** O build A rodou duas vezes por roteiro, sem janela, com 0 divergências de estado no `--verify` nas quatro execuções. Todo par de capturas é idêntico por SHA-256: `coin-start` 5 de 5 e `team-match` 7 de 7 (quadros listados acima). Os hashes completos estão em `private/work/graphics-growth/repeat-a.log`. Observação: o número de blocos conferidos pelo `--verify` varia um pouco entre as duas execuções do mesmo roteiro (3.575.508 contra 3.575.422 no `coin-start`; 5.826.109 contra 5.826.056 no `team-match`), com quadros idênticos. É uma contagem de blocos conferidos, não imagem desenhada, então não afeta a comparação; fica registrada por precaução._
