---
title: "Test the grown loader with synthetic graphics files"
triage: ready-for-agent
---

# 03 Test the grown loader with synthetic graphics files

[Parent specification](../spec.md)

## What to build

A small test of the graphics loader and tile decoder, using only synthetic data, so that errors in pair interleaving and tile numbering show up before any frame is drawn. It builds pairs of synthetic graphics files, loads them with the 128 MiB size and checks the layout the Rehearsal will rely on. It also shows, with the 64 MiB size, the old wrap that the growth ends.

_PT-BR: um teste pequeno do carregador de gráficos e do decodificador de tiles, só com dados sintéticos, para que erros de intercalação dos pares e de numeração de tiles apareçam antes de qualquer quadro ser desenhado. Ele monta pares de arquivos gráficos sintéticos, carrega com o tamanho de 128 MiB e confere a disposição de que o Ensaio vai depender. Também mostra, com o tamanho de 64 MiB, a volta que a ampliação elimina._

**Suggested model and effort:** Sonnet 5.5, low to medium. The effort is in compiling against the private toolkit, not in the test itself. / _Sonnet 5.5, esforço baixo a médio. O esforço está em compilar contra o kit privado, não no teste em si._

## Blocked by

None (can start immediately).

## Acceptance criteria

- [x] With the 128 MiB size, bytes of a synthetic pair interleave as the loader specifies, a tile placed at the first byte of the fifth pair is found at tile number `$80000`, and the part no file covers reads as zero.
- [x] With the 128 MiB size the tile mask has 20 bits; with the 64 MiB size, a tile number at or above `$80000` wraps to the low half. Both are asserted, so the behaviour the growth changes is documented by the test.
- [x] The test uses no game data, and the repository holds none of the third-party source: it compiles against the private toolkit.
- [x] One command builds and runs it, and the command is recorded under `tools/kof2003/`.

_PT-BR:_

- _Com o tamanho de 128 MiB, os bytes de um par sintético se intercalam como o carregador especifica, um tile colocado no primeiro byte do quinto par é achado no número de tile `$80000`, e a parte que nenhum arquivo cobre lê como zero._
- _Com o tamanho de 128 MiB a máscara de tile tem 20 bits; com o de 64 MiB, um número de tile igual ou maior que `$80000` dá a volta para a metade baixa. As duas coisas são verificadas, então o comportamento que a ampliação muda fica documentado pelo teste._
- _O teste não usa dados dos jogos, e o repositório não guarda nada do código de terceiros: ele compila contra o kit privado._
- _Um comando compila e roda o teste, e o comando fica registrado em `tools/kof2003/`._
