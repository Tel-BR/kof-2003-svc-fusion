---
id: 24
title: "How Neo Geo recompilation projects grew past a 64 MB graphics set"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/24-recomp-growth-prior-art:docs/wayfinder/guile-adelheid-slot/research/24-recomp-growth-prior-art.md
---

## Question

This project's port generator has a fixed `crom_size` of 64 MB, and [19](19-guile-tile-placement.md) chose to grow it to 128 MiB. The repository does not say which project the generator came from. Which public Neo Geo recompilation projects is it derived from, including its forks and similar recompilations, and did any of them move `crom_size` from a fixed 64 MB to 128 MB or more? What did they change (graphics file pairs, tile cache size, address arithmetic, checks), and what broke?

Read published code, issues and write-ups; do not run or download game ROMs. Record project names, links, what changed and what broke, each marked *unverified* until tried here. Say which of those changes the generator in this repository already has and which it lacks, using [the generator findings](04-port-generator.md).

_PT-BR: o gerador do port deste projeto tem `crom_size` fixo em 64 MB, e o ticket 19 escolheu ampliar para 128 MiB. O repositório não diz de que projeto o gerador veio. De quais projetos públicos de recompilação de Neo Geo ele deriva, incluindo forks e recompilações parecidas, e algum deles passou o `crom_size` de 64 MB fixo para 128 MB ou mais? O que mudaram (pares de arquivos gráficos, tamanho do cache de tiles, aritmética de endereços, verificações) e o que quebrou? Ler só código, issues e textos publicados; não baixar nem rodar ROMs. Registrar nomes, links, o que mudou e o que quebrou, cada item *não verificado* até ser testado aqui. Dizer quais dessas mudanças o gerador deste repositório já tem e quais faltam, usando os achados do ticket 04._

## Resolution

All items *unverified* in this project. Full notes with sources: `research/24-recomp-growth-prior-art.md`.

**Where the generator comes from.** `neogeorecomp` is the public MIT repo `sp00nznet/neogeorecomp` (not a fork, v0.2.0, commit af96b2b). Public Neo Geo recomps vendor it: omegakatana92's ports (including KOF 2003), `danilopaulinodasilva/kof98recomp` (own toolkit fork with banked P-ROM and AES mode) and `tdstdx627/kof2002-recomp-mod` (adds `entries.txt` and a `profile` target). The local layout (`crom_size` 0x4000000, four C pairs, 24 generated files, `profile` target) matches omegakatana92's KOF 2003 port; the exact local lineage is inferred, not proven.

**Growth past 64 MB: nobody documents it.** Every `game.c` read sets 64 MB, and the upstream repo has no issue or PR about it (code search was unavailable, so an unseen 128 MB variant may exist). Upstream's loader just allocates `crom_size`, with up to 8 pairs, so 64 MB is a per-game descriptor value, not a toolkit cap. Upstream decodes the whole C-ROM at load into 256 bytes per tile (2x), which matches the local 128 MiB cache and the planned 256 MiB, and derives the tile mask from the tile count, so raising the size also removes the wrap at `$7FFFF`. The hardware ceiling is 20 bits = 128 MiB.

**What broke elsewhere, and what the generator lacks.** The only related documented change is Rage of the Dragons' patch: the decoded buffer is padded to a power of two, because sets that are not a power of two (KOF '97, 40 MB) read past the heap. Upstream and, probably, this generator lack that padding, so after adding C files the total must be a power of two (simplest: always size to 128 MiB) or the padding must be added. Still open for the plan: the integer types in the local address arithmetic, and any extra cap in the local adapted loader. Both are cheap to read in the local copy.

**PT-BR**

Tudo *não verificado* neste projeto. Notas completas com fontes em `research/24-recomp-growth-prior-art.md`.

**De onde vem o gerador.** O `neogeorecomp` é o repositório público MIT `sp00nznet/neogeorecomp` (não é fork, v0.2.0, commit af96b2b). Os recomps públicos de Neo Geo o embutem: os portes do omegakatana92 (inclusive o KOF 2003), `danilopaulinodasilva/kof98recomp` (fork próprio com P-ROM em bancos e modo AES) e `tdstdx627/kof2002-recomp-mod` (acrescenta `entries.txt` e o alvo `profile`). O layout local (`crom_size` 0x4000000, quatro pares, 24 arquivos gerados, alvo `profile`) bate com o porte KOF 2003 do omegakatana92; a linhagem exata local é inferida, não provada.

**Crescer além de 64 MB: ninguém documenta.** Todo `game.c` lido usa 64 MB e o upstream não tem issue nem PR sobre isso (a busca de código estava indisponível, então pode existir uma variante de 128 MB que não vi). O carregador do upstream só aloca `crom_size`, com até 8 pares: os 64 MB são valor do descritor de cada jogo, não teto do kit. O upstream decodifica a C-ROM inteira na carga em 256 bytes por tile (2x), o que bate com o cache local de 128 MiB e o de 256 MiB planejado, e tira a máscara de tile da contagem de tiles, então aumentar o tamanho também elimina a volta em `$7FFFF`. O teto do hardware é 20 bits = 128 MiB.

**O que quebrou em outros e o que falta no gerador.** A única mudança relacionada documentada é o patch do Rage of the Dragons: o buffer decodificado é preenchido até potência de 2, porque conjuntos que não são potência de 2 (KOF '97, 40 MB) liam além do heap. O upstream e, provavelmente, este gerador não têm esse preenchimento; depois de acrescentar arquivos C, o total precisa ser potência de 2 (o mais simples: sempre dimensionar para 128 MiB) ou o preenchimento precisa ser acrescentado. Segue aberto para o plano: os tipos inteiros da aritmética de endereços local e qualquer teto extra no carregador local adaptado. Os dois são baratos de ler na cópia local.
