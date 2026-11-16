---
id: 24
title: "How Neo Geo recompilation projects grew past a 64 MB graphics set"
label: wayfinder:research
mode: AFK
status: open
assignee:
blocked_by: []
research:
---

## Question

This project's port generator has a fixed `crom_size` of 64 MB, and [19](19-guile-tile-placement.md) chose to grow it to 128 MiB. The repository does not say which project the generator came from. Which public Neo Geo recompilation projects is it derived from, including its forks and similar recompilations, and did any of them move `crom_size` from a fixed 64 MB to 128 MB or more? What did they change (graphics file pairs, tile cache size, address arithmetic, checks), and what broke?

Read published code, issues and write-ups; do not run or download game ROMs. Record project names, links, what changed and what broke, each marked *unverified* until tried here. Say which of those changes the generator in this repository already has and which it lacks, using [the generator findings](04-port-generator.md).

_PT-BR: o gerador do port deste projeto tem `crom_size` fixo em 64 MB, e o ticket 19 escolheu ampliar para 128 MiB. O repositório não diz de que projeto o gerador veio. De quais projetos públicos de recompilação de Neo Geo ele deriva, incluindo forks e recompilações parecidas, e algum deles passou o `crom_size` de 64 MB fixo para 128 MB ou mais? O que mudaram (pares de arquivos gráficos, tamanho do cache de tiles, aritmética de endereços, verificações) e o que quebrou? Ler só código, issues e textos publicados; não baixar nem rodar ROMs. Registrar nomes, links, o que mudou e o que quebrou, cada item *não verificado* até ser testado aqui. Dizer quais dessas mudanças o gerador deste repositório já tem e quais faltam, usando os achados do ticket 04._
