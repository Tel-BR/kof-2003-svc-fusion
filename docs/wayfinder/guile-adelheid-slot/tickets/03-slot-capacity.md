---
id: 03
title: "How many fighter IDs KOF 2003's tables hold and how much free space its files have"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/03-slot-capacity:docs/wayfinder/guile-adelheid-slot/research/03-slot-capacity.md
---

## Question

What is the highest fighter ID each ID-indexed table can hold without moving it, which IDs are unused or used by non-selectable entries, and what bounds checks or hard-coded counts exist? How much free space is there in the decrypted program file and in the graphics files the native player loads, and is the Neo Geo address space or the graphics bank layout a hard ceiling? Compare with the space Guile's SVC tiles would need, as a count. This feeds the slot strategy for 26 SVC Exclusive Characters.

_PT-BR: Qual é o maior ID que cada tabela indexada por lutador comporta sem ser mudada de lugar, quais IDs estão livres ou usados por entradas não selecionáveis, e que verificações de limite ou contagens fixas existem? Quanto espaço livre há no programa decifrado e nos arquivos gráficos que o executável nativo carrega, e o espaço de endereços do Neo Geo ou a organização dos bancos gráficos é um teto rígido? Comparar com o espaço que os tiles do Guile no SVC exigiriam, como contagem. Isto alimenta a estratégia de vagas para 26 exclusivos do SVC._

## Resolution

**ID ceiling.** The slot format caps IDs at 64 (`$00`–`$3F`, masked with `$3F`). Poking Player 1's slot showed that `$00`–`$24` load (`$24` is Maki, a 37th fighter), `$25` starts a match with no fighter drawn, and `$30`/`$3F` fall back to the attract sequence.

**Tables.** The 64-entry tables reach `$3F` (two of them only `$3E`), but in the two banked directories `$25`–`$2F` are non-fighter object types. Nineteen 37-entry tables, packed back to back, and fixed guards (`≤$24`, `<$25`, mod 37) stop at `$24`. Without moving anything, the common reach is `$24`. Relocating the 37-entry tables and raising the guards frees 15 clean IDs (`$30`–`$3E`); renumbering the object types as well gives up to 27 (`$25`–`$3F`); more than that needs a wider slot format.

**Free space.** The 9 MB program holds about 4.1 MB of `$FF` filler that nothing read in 8,000 frames: 360 KB in the fixed 1 MB, room for relocated tables and new per-fighter blocks, and the rest banked. The game's bank routine reaches 8 MB of banked data, exactly today's image. The 64 MiB graphics set has only 2,399 blank tiles, the longest run 47: **no usable free graphics space**. The hardware tile format addresses 128 MiB and the native renderer reads all 20 bits; whether KOF 2003's frame data can carry tile numbers of `$80000` and above is unverified.

**Guile.** One SVC session showed 756 distinct body tiles inside a block of about 9,100 tile numbers (`$42B6F`–`$44EF8`). Either count is above KOF 2003's free tiles. At about 9,100 tiles each, 26 fighters fit in the extra 64 MiB.

**PT-BR**

**Teto do ID.** O formato da vaga limita os IDs a 64 (`$00`–`$3F`, mascarados com `$3F`). Gravando na vaga do jogador 1: `$00`–`$24` carregam (`$24` é a Maki, uma 37ª lutadora), `$25` inicia a luta sem lutador desenhado, e `$30`/`$3F` voltam à demonstração.

**Tabelas.** As tabelas de 64 entradas chegam a `$3F` (duas só a `$3E`), mas nos dois diretórios com banco `$25`–`$2F` são tipos de objeto que não são lutadores. Dezenove tabelas de 37 entradas, coladas umas nas outras, e verificações fixas (`≤$24`, `<$25`, módulo 37) param em `$24`. Sem mover nada, o alcance comum é `$24`. Mover as tabelas de 37 e ajustar as verificações libera 15 IDs limpos (`$30`–`$3E`); renumerar também os tipos de objeto dá até 27 (`$25`–`$3F`); mais que isso exige outro formato de vaga.

**Espaço livre.** O programa de 9 MB tem cerca de 4,1 MB de preenchimento `$FF` que nada leu em 8.000 quadros: 360 KB no 1 MB fixo, que cabem tabelas movidas e blocos novos de lutador, e o resto com banco. A rotina de banco do jogo alcança 8 MB, exatamente o tamanho atual. O conjunto gráfico de 64 MiB só tem 2.399 tiles vazios, com o maior trecho de 47: **não há espaço gráfico livre útil**. O formato do hardware endereça 128 MiB e o renderizador nativo lê os 20 bits; falta verificar se os dados de quadro do KOF 2003 aceitam tiles a partir de `$80000`.

**Guile.** Uma sessão do SVC mostrou 756 tiles distintos do corpo dele, num bloco de cerca de 9.100 números de tile (`$42B6F`–`$44EF8`). As duas contagens passam dos tiles livres do KOF 2003. Com cerca de 9.100 tiles cada, 26 lutadores cabem nos 64 MiB a mais.

Research / Pesquisa: `research/03-slot-capacity:docs/wayfinder/guile-adelheid-slot/research/03-slot-capacity.md` (commit `d108752`).
