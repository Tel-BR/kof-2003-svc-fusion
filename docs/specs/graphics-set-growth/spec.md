---
title: "Grow the Graphics Set from 64 to 128 MiB with no visible change"
triage: ready-for-agent
---

# Grow the Graphics Set from 64 to 128 MiB with no visible change

_PT-BR: a versão em português fica logo depois da versão em inglês._

## Problem Statement

Every Imported Character needs thousands of tiles, and KOF 2003's 64 MiB Graphics Set has only 2,399 blank tiles, the longest run 47. The owner decided on 2026-11-16 that the Graphics Set grows to 128 MiB, the most a tile number can address, and that Imported Characters' tiles go into the Added Space ([Choose where Guile's tiles go in the graphics files](../../wayfinder/guile-adelheid-slot/tickets/19-guile-tile-placement.md), [Choose how fighter slots are found for the SVC Exclusive Characters](../../wayfinder/guile-adelheid-slot/tickets/06-slot-strategy.md)). Before any fighter depends on it, the owner wants this first stage of the Rehearsal done alone: the native game must open and behave exactly like the original, with no fighter added. Nothing today proves that the player, built with a larger Graphics Set, still draws the same game, or that it can draw a tile from the Added Space at all. That second point has so far only been read in the code ([How KOF 2003's sprite-frame records number their tiles](../../wayfinder/guile-adelheid-slot/tickets/18-sprite-frame-tiles.md)).

## Solution

The native player is built with a 128 MiB Graphics Set. The Added Space starts empty and the build has no new graphics files. Scripted runs of the same inputs on the 64 MiB reference build and on the grown build produce identical frames. A separate test build proves that a tile in the Added Space is loaded and drawn, and that it no longer aliases to a tile in the lower half. The change is applied by a repeatable, reversible script, so the Rehearsal and later work start from a known state.

## User Stories

1. As the project owner, I want the native game with a 128 MiB Graphics Set to open and play like the original, so that growing the Graphics Set costs nothing in what the player sees.
2. As the project owner, I want proof by frame comparison rather than by eye, so that a one-tile difference cannot slip by.
3. As the project owner, I want no fighter added in this stage, so that any difference found can only come from the growth.
4. As a tester, I want a 64 MiB reference build kept alongside, so that the same inputs can be run on both and compared.
5. As a tester, I want the reference build run twice first, so that I know the same script always gives the same frames before I trust a comparison.
6. As a tester, I want the comparison to cover boot, attract mode, selection and a team match, so that the screens with the most varied tiles are checked.
7. As a tester, I want the first differing frame reported, so that I can find where the two builds diverge.
8. As a tester, I want any difference to stop the stage instead of being accepted as noise, so that a real change in behaviour is never waved through.
9. As a tester, I want a test build that draws one synthetic tile from the Added Space, so that I know tiles above `$80000` are loaded, decoded and drawn.
10. As a tester, I want that synthetic tile to differ from tile 0, so that I know tile numbers no longer wrap from `$80000` back to `$00000`.
11. As a tester, I want the test-only code and file kept out of the build that must equal the original, so that the proof does not weaken the comparison.
12. As a contributor, I want the growth applied by a script in the repository, so that I can reproduce it without copying third-party code.
13. As a contributor, I want the script to be reversible, so that I can go back to the 64 MiB reference at any time.
14. As a contributor, I want the grown build to need no regeneration of the native code, no profiling run and no new entries, so that this stage touches nothing else.
15. As a contributor, I want the layout rule of graphics file pairs recorded (up to 8 pairs, laid end to end, the Added Space starting at the fifth), so that the Rehearsal adds its tiles in the right place.
16. As the project owner, I want the machine's memory use recorded for the grown build, so that I know the 256 MiB tile cache and the load peak are acceptable.
17. As a contributor, I want a small loader test with synthetic data, so that errors in pair interleaving and tile numbering appear before any frame is drawn.
18. As a contributor, I want no game data in the repository, so that the hard rule of `AGENTS.md` still holds: captures stay in `private/` and only hashes, counts and sizes are recorded.
19. As the project owner, I want the earlier finding about the decoded buffer's power-of-two padding corrected in the research ticket, so that the plan does not carry a risk that does not exist.

## Implementation Decisions

- The Graphics Set grows from 64 MiB to 128 MiB by raising the graphics size in the cartridge descriptor of the native player. The loader zero-fills whatever the graphics files do not cover, so the Added Space starts empty and the grown build adds no graphics files.
- The player's tile code already has 20 bits. Raising the size moves the tile mask from 19 to 20 bits. From then on a tile number at or above `$80000` no longer wraps to a low tile; it reads the Added Space. This is the one behaviour change the growth can cause, and the frame comparison exists to catch it.
- The decoded tile cache doubles from 128 to 256 MiB, with a transient peak of about 384 MiB while loading. The generator already pads the decoded buffer to a power of two, which corrects the "probably lacks it" note of [How Neo Geo recompilation projects grew past a 64 MB graphics set](../../wayfinder/guile-adelheid-slot/tickets/24-recomp-growth-prior-art.md). The 128 MiB size is a power of two in any case.
- No 68000 program byte changes, so the native code is not regenerated, no profile run is needed and no entries are added ([How the native port's generator handles changed or added 68000 code and data](../../wayfinder/guile-adelheid-slot/tickets/04-port-generator.md)). Only the player is rebuilt.
- The descriptor and the toolkit are third-party code under `private/`, and the licence is not decided. A script in the repository applies the one-value change to the private copy, repeatably and idempotently, and can undo it. It copies none of the third-party code.
- Three builds. **A**: the reference, 64 MiB as today. **B**: 128 MiB with no test code and no extra file; this is the build that stays and must equal A frame by frame. **C**: 128 MiB for the Added Space proof only.
- Build C loads a temporary pair of graphics files under `private/` that holds synthetic tiles (a pattern, not game art) from tile `$80000`, listed only in C's descriptor. A compile-time option present only in C plants one sprite in video memory that points at one of those tiles; with this the 20-bit tile code assembly is exercised. The option and the file exist in neither A nor B.
- The loader lays graphics file pairs end to end, up to 8 pairs, and the four original pairs fill exactly 64 MiB, so the Added Space starts at the fifth pair. Four more pairs of 16 MiB complete 128 MiB. This is recorded for the Rehearsal, which is where real tiles first enter the Added Space.
- A comparison step reads the capture sets of two runs and reports equal or the first differing frame, by hash. It runs on top of the existing scripted-run entry point.
- If A differs from A, the comparison is invalid and the source of non-determinism is found first. If A differs from B, the stage stops and reopens [Choose how fighter slots are found for the SVC Exclusive Characters](../../wayfinder/guile-adelheid-slot/tickets/06-slot-strategy.md) with the cause found; a difference is never accepted as noise.
- Records to update when the stage closes: the correction in the research ticket 24, a pointer in the map's "Decisions so far", and the measured memory use.
- Vocabulary follows the glossary: Graphics Set, Added Space, Rehearsal. No ADR is proposed: the change is easy to reverse.

## Testing Decisions

- A good test observes external behaviour only: what the player draws for a given script and what a loaded set contains at a given tile number. It does not inspect internal variables of the renderer.
- **First seam, the highest: the native player run headless with a fixed input script and captures at chosen frames.** It carries three checks. The reference build run twice gives identical captures. The reference build and the grown build, given the same script and frames, give identical captures. The test build's capture shows the synthetic tile, and that tile differs from tile 0. The scripts are the coin-and-start script and the team-match script, with captures from boot, attract mode, selection and the fight.
- **Second seam: a small loader test with synthetic data**, added at the owner's request. It builds pairs of synthetic graphics files, loads them with the grown size and checks that bytes interleave as expected, that a tile placed at the fifth pair is found at tile number `$80000`, that the unfilled part reads as zero and that the tile mask is 20 bits. It uses no game data.
- Prior art: the scripted native and MAME runs with captures, the report reader for the native run, and the existing Python tests of the same tools; for the loader, the toolkit's conformance harness is the nearest example.
- Captures contain game graphics, so they stay under `private/`. Only hashes, counts, frame numbers and sizes go into tickets and documents.

## Out of Scope

- Any new fighter, relocated ID table, clone of Kyo or Kusanagi, or change to the selection screen: all of that belongs to the Rehearsal's next stages and to [Choose how fighter slots are found for the SVC Exclusive Characters](../../wayfinder/guile-adelheid-slot/tickets/06-slot-strategy.md).
- Real tiles in the Added Space, converted from SVC or cloned from KOF 2003, and the pipeline that produces them.
- Any change to the 68000 program or to the generated native code.
- The graphics files' final layout beyond the rule recorded here.
- Running the modified game in MAME; MAME stays a reading instrument.

## Further Notes

The next step is `/to-tickets`. Respect the hard rule: no game data in the repository, and no `git add -f` under `private/`. The owner has uncommitted changes in the wayfinder map and tickets; this stage does not touch them.

---

# Ampliar o Conjunto gráfico de 64 para 128 MiB sem mudança visível

## Problema

Todo Personagem importado precisa de milhares de tiles, e o Conjunto gráfico de 64 MiB do KOF 2003 só tem 2.399 tiles vazios, com o maior trecho de 47. O dono decidiu em 16/11/2026 que o Conjunto gráfico cresce para 128 MiB, o máximo que um número de tile alcança, e que os tiles dos personagens importados vão para o Espaço acrescentado (tickets 19 e 06 do mapa). Antes de qualquer lutador depender disso, o dono quer esta primeira etapa do Ensaio feita sozinha: o jogo nativo abre e se comporta exatamente como o original, sem nenhum lutador novo. Hoje nada prova que o player, compilado com um conjunto gráfico maior, continua desenhando o mesmo jogo, nem que ele consegue desenhar um tile do Espaço acrescentado. Esse segundo ponto só foi lido no código até agora (ticket 18).

## Solução

O player nativo é compilado com um Conjunto gráfico de 128 MiB. O Espaço acrescentado começa vazio e o build não tem arquivos gráficos novos. Execuções por roteiro com as mesmas entradas no build de referência de 64 MiB e no build ampliado produzem quadros idênticos. Um build de teste à parte prova que um tile do Espaço acrescentado é carregado e desenhado, e que ele não dá mais a volta para um tile da metade baixa. A mudança é aplicada por um script repetível e reversível, para que o Ensaio e os trabalhos seguintes partam de um estado conhecido.

## Histórias de usuário

1. Como dono do projeto, quero que o jogo nativo com Conjunto gráfico de 128 MiB abra e jogue como o original, para que ampliar o conjunto não custe nada no que o jogador vê.
2. Como dono do projeto, quero prova por comparação de quadros e não a olho, para que uma diferença de um tile não passe batida.
3. Como dono do projeto, quero nenhum lutador novo nesta etapa, para que qualquer diferença só possa vir da ampliação.
4. Como testador, quero um build de referência de 64 MiB mantido ao lado, para rodar as mesmas entradas nos dois e comparar.
5. Como testador, quero rodar a referência duas vezes antes, para saber que o mesmo roteiro sempre dá os mesmos quadros antes de confiar numa comparação.
6. Como testador, quero que a comparação cubra abertura, demonstração, seleção e uma luta de equipe, para checar as telas com tiles mais variados.
7. Como testador, quero o primeiro quadro diferente informado, para achar onde os dois builds se separam.
8. Como testador, quero que qualquer diferença pare a etapa em vez de ser aceita como ruído, para que uma mudança real de comportamento nunca passe.
9. Como testador, quero um build de teste que desenha um tile sintético do Espaço acrescentado, para saber que tiles acima de `$80000` são carregados, decodificados e desenhados.
10. Como testador, quero que esse tile sintético seja diferente do tile 0, para saber que o número de tile não dá mais a volta de `$80000` para `$00000`.
11. Como testador, quero o código e o arquivo só de teste fora do build que tem de ser igual ao original, para que a prova não enfraqueça a comparação.
12. Como contribuidor, quero a ampliação aplicada por um script no repositório, para reproduzi-la sem copiar código de terceiros.
13. Como contribuidor, quero que o script seja reversível, para voltar à referência de 64 MiB quando quiser.
14. Como contribuidor, quero que o build ampliado não precise regerar o código nativo, fazer perfil nem acrescentar entradas, para que esta etapa não toque em mais nada.
15. Como contribuidor, quero a regra de disposição dos pares de arquivos gráficos registrada (até 8 pares, um depois do outro, com o Espaço acrescentado começando no quinto), para que o Ensaio ponha seus tiles no lugar certo.
16. Como dono do projeto, quero o uso de memória da máquina registrado para o build ampliado, para saber se o cache de tiles de 256 MiB e o pico da carga são aceitáveis.
17. Como contribuidor, quero um teste pequeno do carregador com dados sintéticos, para que erros de intercalação dos pares e de numeração de tiles apareçam antes de qualquer quadro ser desenhado.
18. Como contribuidor, quero nenhum dado dos jogos no repositório, para que a regra obrigatória do `AGENTS.md` continue valendo: capturas ficam em `private/` e só hashes, contagens e tamanhos são registrados.
19. Como dono do projeto, quero a conclusão anterior sobre o preenchimento do buffer decodificado até potência de 2 corrigida no ticket de pesquisa, para que o plano não carregue um risco que não existe.

## Decisões de implementação

- O Conjunto gráfico cresce de 64 MiB para 128 MiB ao subir o tamanho gráfico no descritor do cartucho do player nativo. O carregador zera o que os arquivos gráficos não cobrem, então o Espaço acrescentado começa vazio e o build ampliado não acrescenta arquivos gráficos.
- O código de tile do player já tem 20 bits. Subir o tamanho muda a máscara de tile de 19 para 20 bits. A partir daí um número de tile igual ou maior que `$80000` não dá mais a volta para um tile baixo; ele lê o Espaço acrescentado. Essa é a única mudança de comportamento que a ampliação pode causar, e a comparação de quadros existe para pegá-la.
- O cache de tiles decodificados dobra de 128 para 256 MiB, com pico transitório de cerca de 384 MiB durante a carga. O gerador já preenche o buffer decodificado até potência de 2, o que corrige a nota "provavelmente não tem" do ticket 24. O tamanho de 128 MiB já é potência de 2 de qualquer modo.
- Nenhum byte do programa 68000 muda, então o código nativo não é regerado, não há rodada de perfil e nenhuma entrada é acrescentada (ticket 04). Só o player é recompilado.
- O descritor e o kit são código de terceiros em `private/`, e a licença não foi decidida. Um script no repositório aplica a troca de um valor na cópia privada, de forma repetível e idempotente, e sabe desfazê-la. Ele não copia nada do código de terceiros.
- Três builds. **A**: a referência, 64 MiB como hoje. **B**: 128 MiB sem código nem arquivo de teste; é o build que fica e que tem de ser igual ao A quadro a quadro. **C**: 128 MiB só para a prova do Espaço acrescentado.
- O build C carrega um par temporário de arquivos gráficos em `private/` com tiles sintéticos (um padrão, não arte do jogo) a partir do tile `$80000`, listado só no descritor do C. Uma opção de compilação presente só no C planta um sprite na memória de vídeo apontando para um desses tiles; com isso a montagem do código de tile de 20 bits é exercitada. A opção e o arquivo não existem no A nem no B.
- O carregador dispõe os pares de arquivos gráficos um depois do outro, até 8 pares, e os quatro pares originais preenchem exatamente 64 MiB, então o Espaço acrescentado começa no quinto par. Mais quatro pares de 16 MiB completam 128 MiB. Isso fica registrado para o Ensaio, que é onde os primeiros tiles de verdade entram no Espaço acrescentado.
- Uma etapa de comparação lê os conjuntos de capturas de duas execuções e informa igual ou o primeiro quadro diferente, por hash. Ela roda em cima da entrada de execução por roteiro que já existe.
- Se o A difere do A, a comparação é inválida e a fonte de não determinismo é achada primeiro. Se o A difere do B, a etapa para e reabre o ticket 06 com a causa encontrada; uma diferença nunca é aceita como ruído.
- Registros a atualizar quando a etapa fechar: a correção no ticket de pesquisa 24, um ponteiro nas "Decisões até aqui" do mapa e o uso de memória medido.
- O vocabulário segue o glossário: Conjunto gráfico, Espaço acrescentado, Ensaio. Nenhuma ADR é proposta: a mudança é fácil de desfazer.

## Decisões de teste

- Um bom teste observa só o comportamento externo: o que o player desenha para um dado roteiro e o que um conjunto carregado contém num dado número de tile. Ele não inspeciona variáveis internas do renderizador.
- **Primeiro ponto de teste, o mais alto: o player nativo rodado sem janela com roteiro fixo de entradas e capturas em quadros escolhidos.** Ele carrega três verificações. O build de referência rodado duas vezes dá capturas idênticas. O build de referência e o ampliado, com o mesmo roteiro e os mesmos quadros, dão capturas idênticas. A captura do build de teste mostra o tile sintético, e esse tile é diferente do tile 0. Os roteiros são o de moeda e início e o de luta de equipe, com capturas de abertura, demonstração, seleção e luta.
- **Segundo ponto de teste: um teste pequeno do carregador com dados sintéticos**, acrescentado a pedido do dono. Ele monta pares de arquivos gráficos sintéticos, carrega com o tamanho ampliado e confere que os bytes se intercalam como esperado, que um tile colocado no quinto par é achado no número de tile `$80000`, que a parte não preenchida lê como zero e que a máscara de tile tem 20 bits. Não usa dados dos jogos.
- Referências existentes: as execuções por roteiro no nativo e no MAME com capturas, o leitor do relatório da execução nativa e os testes Python das mesmas ferramentas; para o carregador, o conjunto de conformidade do kit é o exemplo mais próximo.
- As capturas contêm gráficos do jogo, então ficam em `private/`. Só hashes, contagens, números de quadro e tamanhos vão para tickets e documentos.

## Fora do escopo

- Qualquer lutador novo, tabela de ID movida, clone do Kyo ou do Kusanagi, ou mudança na tela de seleção: tudo isso pertence às próximas etapas do Ensaio e ao ticket 06.
- Tiles de verdade no Espaço acrescentado, convertidos do SVC ou clonados do KOF 2003, e o processo que os produz.
- Qualquer mudança no programa 68000 ou no código nativo gerado.
- A disposição final dos arquivos gráficos além da regra registrada aqui.
- Rodar o jogo modificado no MAME; o MAME continua sendo só instrumento de leitura.

## Notas adicionais

O próximo passo é o `/to-tickets`. Respeitar a regra obrigatória: nenhum dado dos jogos no repositório e nenhum `git add -f` em `private/`. O dono tem alterações sem commit no mapa e nos tickets do wayfinder; esta etapa não mexe nelas.
