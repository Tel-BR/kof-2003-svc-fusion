---
title: "Grow the Graphics Set to 128 MiB and match the reference frame by frame"
triage: ready-for-agent
---

# 02 Grow the Graphics Set to 128 MiB and match the reference frame by frame

[Parent specification](../spec.md)

## What to build

A script in the repository raises the graphics size in the private copy of the cartridge descriptor from 64 to 128 MiB, repeatably, and can undo it. It copies none of the third-party code. The player is rebuilt as build B, with no test code and no new file; the Added Space starts empty. The same scripts and frames of [01](01-reference-build-repeats.md) are run on B and compared with A. The memory use of B is measured. No 68000 program byte changes, so the native code is not regenerated.

_PT-BR: um script no repositório sobe o tamanho gráfico na cópia privada do descritor do cartucho de 64 para 128 MiB, de forma repetível, e sabe desfazer. Ele não copia código de terceiros. O player é recompilado como build B, sem código de teste e sem arquivo novo; o Espaço acrescentado começa vazio. Os mesmos roteiros e quadros do ticket 01 rodam no B e são comparados com o A. O uso de memória do B é medido. Nenhum byte do programa 68000 muda, então o código nativo não é regerado._

**Suggested model and effort:** Sonnet 5.5, medium. If B differs from A, escalate to Opus 5.5, high, to diagnose; that is also the only case that reopens [ticket 06 of the map](../../../wayfinder/guile-adelheid-slot/tickets/06-slot-strategy.md). / _Sonnet 5.5, esforço médio. Se o B diferir do A, escalar para o Opus 5.5, esforço alto, para diagnosticar; esse também é o único caso que reabre o ticket 06 do mapa._

## Blocked by

- [01 Prove the 64 MiB reference build repeats itself](01-reference-build-repeats.md)

## Acceptance criteria

- [x] The script applies the change to the private descriptor idempotently, and undoing it restores the original, confirmed by comparing hashes before and after.
- [x] Build B contains no test code and no extra graphics file, opens, and reaches selection and a fight.
- [x] For both scripts and the same frames as in 01, every capture of B is identical to the capture of A. Any difference stops this ticket, is never accepted as noise, and reopens ticket 06 of the map with the cause found.
- [x] The prepared program file's hash is the same for A and B, and the `--verify` summary of B is not worse than that of A.
- [x] The memory use of B is recorded (peak while loading and steady) next to the machine's total memory, and the game still opens.
- [x] The commands to apply, undo, build and compare are recorded under `tools/kof2003/`. No game data enters the repository.

_PT-BR:_

- _O script aplica a mudança no descritor privado de forma idempotente, e desfazê-la restaura o original, confirmado por hashes antes e depois._
- _O build B não tem código de teste nem arquivo gráfico extra, abre e chega à seleção e a uma luta._
- _Para os dois roteiros e os mesmos quadros do ticket 01, toda captura do B é idêntica à do A. Qualquer diferença para este ticket, nunca é aceita como ruído e reabre o ticket 06 do mapa com a causa achada._
- _O hash do arquivo de programa preparado é o mesmo no A e no B, e o resumo do `--verify` do B não é pior que o do A._
- _O uso de memória do B é registrado (pico na carga e regime) ao lado da memória total da máquina, e o jogo continua abrindo._
- _Os comandos para aplicar, desfazer, compilar e comparar ficam registrados em `tools/kof2003/`. Nenhum dado dos jogos entra no repositório._

## Result (2026-11-16, Windows)

**Closed: B equals A frame by frame.** Commands are in `tools/kof2003/growth/README.md`.

- Descriptor script `growth/graphics_size.py` (12 tests): apply, apply again, undo, undo again on the real private descriptor. SHA-256 before `a20ef4a7…ab6a3`, after apply `6ff7e426…d551c`, after undo `a20ef4a7…ab6a3` (original restored); the second apply and the second undo wrote nothing.
- Build B: 128 MiB, no test code, no new graphics file, in `private/work/graphics-growth/build-b/`. It opens and runs both scripts to the end.
- Native code: `ninja` ran the generator again (it embeds the descriptor), and all 26 files in `generated/` are byte-identical before and after. The prepared program file `271-pd.bin` is the same for A and B (`f6ad2e2d…43215`).
- Frames: `py -3 -m match.compare_builds` ran A and B once on each script. `coin-start` 5 of 5 and `team-match` 7 of 7 captures are identical by SHA-256; the hashes are the ones in the table of ticket 01 (frames 600, 2,000, 3,000, 4,000, 5,400, 6,000, 7,000), so B also equals the earlier A runs. `--verify`: 0 mismatches for A and B in both scripts. Blocks checked differ by a few dozen between runs of the same script, as already noted in 01 (`coin-start` A 3,575,402 and B 3,575,415; `team-match` A 5,826,054 and B 5,826,136).
- Memory of B, on a machine with 32,606 MiB installed: peak working set 420 MiB (`coin-start`) and 419 MiB (`team-match`); peak commit 416 MiB in both; steady working set 310 and 300 MiB (median of the second half of the run). The spec expected a transient peak near 384 MiB while loading; the measured peak is a little above it and well inside the machine's memory.
- Restored: the descriptor is back at 64 MiB and `mvs-native-build` was rebuilt from it. That executable is not byte-identical to the saved `build-a` (hash differs, probably link-time stamps), so `build-a` stays as the only reference and is never rebuilt over.
- Not done here: the pointer in the map's "Decisions so far" and the correction in research ticket 24 (the owner has uncommitted changes in the wayfinder files; ticket 05 records those).

_PT-BR: **Fechado: o B é igual ao A quadro a quadro.** Os comandos estão em `tools/kof2003/growth/README.md`. Script do descritor (12 testes): aplicar, aplicar de novo, desfazer e desfazer de novo no descritor privado real; hash antes `a20ef4a7…ab6a3`, depois de aplicar `6ff7e426…d551c`, depois de desfazer `a20ef4a7…ab6a3` (original restaurado), e a segunda aplicação e o segundo desfazer não gravaram nada. Build B com 128 MiB, sem código de teste nem arquivo gráfico novo, em `private/work/graphics-growth/build-b/`; abre e roda os dois roteiros até o fim. Código nativo: o `ninja` rodou o gerador de novo (ele embute o descritor) e os 26 arquivos de `generated/` ficaram idênticos byte a byte; o arquivo de programa preparado `271-pd.bin` é o mesmo no A e no B. Quadros: `coin-start` 5 de 5 e `team-match` 7 de 7 capturas idênticas por SHA-256, com os mesmos hashes da tabela do ticket 01, então o B também é igual às rodadas anteriores do A. `--verify`: 0 divergências no A e no B nos dois roteiros. Memória do B, numa máquina com 32.606 MiB: pico de memória em uso 420 MiB (`coin-start`) e 419 MiB (`team-match`), pico comprometido 416 MiB, regime 310 e 300 MiB. O spec previa pico transitório perto de 384 MiB; o medido fica um pouco acima e bem dentro da memória da máquina. O descritor voltou a 64 MiB e o `mvs-native-build` foi recompilado; esse executável não é igual byte a byte ao `build-a` guardado, que continua sendo a única referência. Não feito aqui: o ponteiro em "Decisions so far" do mapa e a correção no ticket de pesquisa 24 (o dono tem alterações sem commit no wayfinder; o ticket 05 registra isso)._

