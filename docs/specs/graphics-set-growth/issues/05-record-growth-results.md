---
title: "Record the results of the Graphics Set growth"
triage: ready-for-agent
---

# 05 Record the results of the Graphics Set growth

[Parent specification](../spec.md)

## What to build

Close the stage in the documents the Rehearsal will read. Correct the research ticket on recompilation projects: the local loader already pads the decoded tile buffer to a power of two, so the risk it described does not exist. Add a pointer in the map's "Decisions so far". Record the rule for graphics file pairs and the measured memory use where whoever starts the Rehearsal will find them.

_PT-BR: fechar a etapa nos documentos que o Ensaio vai ler. Corrigir o ticket de pesquisa sobre projetos de recompilação: o carregador local já preenche o buffer de tiles decodificados até potência de 2, então o risco que ele descrevia não existe. Acrescentar um ponteiro nas "Decisões até aqui" do mapa. Registrar a regra dos pares de arquivos gráficos e o uso de memória medido onde quem começar o Ensaio os encontre._

**Suggested model and effort:** Sonnet 5.5, low. The care needed is not to stage or commit the owner's unrelated pending changes in the wayfinder files. / _Sonnet 5.5, esforço baixo. O cuidado é não fazer stage nem commit das alterações pendentes do dono nos arquivos do wayfinder._

## Blocked by

- [02 Grow the Graphics Set to 128 MiB and match the reference frame by frame](02-grow-and-match-reference.md)
- [03 Test the grown loader with synthetic graphics files](03-grown-loader-synthetic-test.md)
- [04 Draw a tile from the Added Space](04-draw-added-space-tile.md)

## Acceptance criteria

- [x] The resolution of the research ticket on recompilation projects (ticket 24 of the map) is corrected, in both languages, with a pointer to the evidence and a note that the padding is now seen in the local loader.
- [x] Wherever the research ticket on the port generator (ticket 04 of the map) says the graphics size is fixed at 64 MB, a note says that this stage raised it and where the record is.
- [x] The map's "Decisions so far" gets one bilingual line for this stage, with the measured memory use.
- [x] The rule for graphics file pairs is recorded: up to 8 pairs laid end to end, the four original pairs fill 64 MiB, the Added Space starts at the fifth pair, and four more pairs of 16 MiB complete 128 MiB.
- [x] Only the lines added by this ticket are staged or committed; the owner's other pending changes in the wayfinder files stay as they were.

_PT-BR:_

- _A resolução do ticket de pesquisa sobre projetos de recompilação (ticket 24 do mapa) é corrigida, nos dois idiomas, com ponteiro para a evidência e nota de que o preenchimento agora foi visto no carregador local._
- _Onde o ticket de pesquisa sobre o gerador do port (ticket 04 do mapa) diz que o tamanho gráfico é fixo em 64 MB, uma nota diz que esta etapa o subiu e onde está o registro._
- _As "Decisões até aqui" do mapa ganham uma linha bilíngue para esta etapa, com o uso de memória medido._
- _A regra dos pares de arquivos gráficos é registrada: até 8 pares um depois do outro, os quatro pares originais preenchem 64 MiB, o Espaço acrescentado começa no quinto par, e mais quatro pares de 16 MiB completam 128 MiB._
- _Só as linhas acrescentadas por este ticket entram em stage ou commit; as demais alterações pendentes do dono nos arquivos do wayfinder ficam como estavam._

## Result (2026-11-16)

**Closed: the stage's results are recorded where the Rehearsal will read them.**

- Research ticket 24 ([tickets/24](../../../wayfinder/guile-adelheid-slot/tickets/24-recomp-growth-prior-art.md)): a correction in both languages. The local loader (`src/video.c` of the adapted toolkit, `private/work/samsho-runtime-source/neogeorecomp/`) rounds the tile count up to a power of two and masks tile numbers with it, so the "probably lacks it" risk does not exist; the evidence is the loader code plus tickets 02 and 03.
- Research ticket 04 ([tickets/04](../../../wayfinder/guile-adelheid-slot/tickets/04-port-generator.md)): a note, in both languages, next to "fixed at 64 MB" saying this stage raised it to 128 MiB and pointing to the growth tools README and to this ticket.
- Map ([map.md](../../../wayfinder/guile-adelheid-slot/map.md)): one bilingual line in "Decisions so far", with peak working set 420 MiB while loading and 300-310 MiB steady on a 32,606 MiB machine.
- Rule for graphics file pairs and the measured memory: section "For whoever starts the Rehearsal" of [`tools/kof2003/growth/README.md`](../../../../tools/kof2003/growth/README.md), in both languages: up to 8 pairs end to end, four original pairs fill 64 MiB, the Added Space starts at the fifth pair (tile `$80000`), four more pairs of 16 MiB complete 128 MiB.
- The owner's pending changes in the wayfinder files (map, tickets 06, 07, 15 and 21, partly staged) were not staged or committed by this ticket: the commit took only the lines added here, by building it in a temporary index.

_PT-BR: **Fechado: os resultados da etapa estão registrados onde o Ensaio vai lê-los.** Ticket de pesquisa 24: correção nos dois idiomas; o carregador local (`src/video.c` do kit adaptado) arredonda a contagem de tiles até potência de 2 e mascara os números de tile com ela, então o risco do "provavelmente não tem" não existe; a evidência é o código do carregador mais os tickets 02 e 03. Ticket de pesquisa 04: nota nos dois idiomas junto de "fixo em 64 MB" dizendo que esta etapa o subiu para 128 MiB, com ponteiro para o README das ferramentas e para este ticket. Mapa: uma linha bilíngue em "Decisões até aqui", com pico de memória de trabalho de 420 MiB na carga e 300-310 MiB estável numa máquina de 32.606 MiB. Regra dos pares de arquivos gráficos e memória medida: seção "Para quem começar o Ensaio" do README de `tools/kof2003/growth/`, nos dois idiomas: até 8 pares um depois do outro, os quatro originais preenchem 64 MiB, o Espaço acrescentado começa no quinto par (tile `$80000`), mais quatro pares de 16 MiB completam 128 MiB. As alterações pendentes do dono nos arquivos do wayfinder (mapa, tickets 06, 07, 15 e 21, em parte em stage) não entraram em stage nem em commit por este ticket: o commit levou só as linhas acrescentadas aqui, montado num índice temporário._
