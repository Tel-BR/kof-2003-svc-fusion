---
id: 04
title: "How the native port's generator handles changed or added 68000 code and data"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/04-port-generator:docs/wayfinder/guile-adelheid-slot/research/04-port-generator.md
---

## Question

Reading the local port under `private/work/kof2003-port/`: how does the generator decide what 68000 code becomes native C (static analysis, traces, a function list)? What happens when program bytes change, when new code is added in free space, or when only data changes? What falls back to the interpreter, how is that reported, and what must be rerun so `--verify` stays meaningful? How are the graphics files consumed, and do they carry any checksum or fixed-size expectation?

_PT-BR: Lendo o port local em `private/work/kof2003-port/`: como o gerador decide que código 68000 vira C nativo (análise estática, traces, lista de funções)? O que acontece quando bytes do programa mudam, quando entra código novo em espaço livre ou quando só dados mudam? O que cai no interpretador, como isso é informado e o que precisa ser rodado de novo para o `--verify` continuar valendo? Como os arquivos gráficos são lidos e se há checksum ou tamanho fixo esperado?_

## Resolution

**How code is chosen.** The generator lives in the adapted `neogeorecomp` toolkit, not in the port. It finds code by static recursive descent from vectors, header entry points, static branch targets, jump tables, a pointer scan over the whole ROM and the profile list `entries.txt`; it uses no traces. It decodes only the fixed 1 MB, the first banked MB and the BIOS, so 7 MB of KOF 2003's banked image never becomes C.

**What a change does.** Any change to the prepared `271-pd.bin` or to `entries.txt` regenerates all 24 parts. The player never checks that the C matches the ROM: stale native code runs silently until `--verify` or a bad-dispatch abort shows it. Data reached through memory operands is read live; immediates inside instructions are code and are baked into the C. New code in fixed free space becomes native when a static branch, a ROM pointer or a profile run reaches it; new code in the banked image beyond its first MB always runs in the interpreter.

**Fallback and `--verify`.** Uncovered addresses run in Musashi and are reported in the `[exec]` summary and by `--dump-misses`, which merges into `entries.txt` and never prunes it. The exit code is always 0. `--verify` compares only the native blocks a session executes, so it checks translation, not game behaviour. After a program change: regenerate, rebuild, profile with a script that exercises the change (today's `play.txt` reaches neither Guile nor Adelheid) until no entries are added, then verify.

**Graphics.** Four C pairs of equal size, up to a `crom_size` fixed at 64 MB in the port descriptor; larger files fail to load and smaller ones are accepted. There are no run-time checksums. Tile codes above `$7FFFF` wrap. Changing graphics needs no regeneration. _Update 2026-11-16: the 64 MB size is no longer fixed; the graphics-set growth stage raised it to 128 MiB (record: [graphics-set growth tools](../../../../tools/kof2003/growth/README.md) and [ticket 05](../../../specs/graphics-set-growth/issues/05-record-growth-results.md))._ Rerunning the preparation tool rewrites the whole prepared folder.

**PT-BR**

**Como o código é escolhido.** O gerador fica no kit `neogeorecomp` adaptado, não no port. Ele acha o código por análise estática a partir dos vetores, dos pontos de entrada do cabeçalho, dos alvos fixos de salto, das tabelas de salto, de uma varredura de ponteiros na ROM inteira e da lista de perfil `entries.txt`; não usa traces. Só decodifica o 1 MB fixo, o primeiro MB com banco e a BIOS, então 7 MB da área com bancos do KOF 2003 nunca viram C.

**O que uma mudança provoca.** Qualquer mudança no `271-pd.bin` preparado ou no `entries.txt` gera as 24 partes de novo. O executável nunca confere se o C bate com a ROM: código nativo velho roda calado até o `--verify` ou um abort de dispatch revelar. Dados lidos por operandos de memória são lidos ao vivo; imediatos dentro das instruções são código e ficam gravados no C. Código novo em espaço livre do 1 MB fixo vira nativo quando um salto fixo, um ponteiro na ROM ou uma rodada de perfil o alcança; código novo na área com bancos além do primeiro MB sempre roda no interpretador.

**Interpretador e `--verify`.** Endereços sem entrada rodam no Musashi e aparecem no resumo `[exec]` e no `--dump-misses`, que junta as entradas no `entries.txt` e nunca apaga as antigas. O código de saída é sempre 0. O `--verify` só compara os blocos nativos que a sessão executa, então confere a tradução, não o comportamento do jogo. Depois de mudar o programa: gerar, compilar, fazer o perfil com um roteiro que passe pela mudança (o `play.txt` atual não chega ao Guile nem à Adelheid) até não surgirem entradas, e então verificar.

**Gráficos.** Quatro pares de arquivos C de tamanhos iguais, até um `crom_size` fixo de 64 MB no descritor do port; arquivos maiores falham e menores são aceitos. Não há checksum em tempo de execução. Tiles acima de `$7FFFF` dão a volta. Trocar gráficos não exige gerar o C de novo. _Atualização 16/11/2026: os 64 MB deixaram de ser fixos; a etapa de ampliação do Conjunto gráfico os subiu para 128 MiB (registro: [ferramentas da ampliação](../../../../tools/kof2003/growth/README.md) e [ticket 05](../../../specs/graphics-set-growth/issues/05-record-growth-results.md))._ Rodar de novo a ferramenta de preparo reescreve a pasta preparada inteira.

Research / Pesquisa: `research/04-port-generator:docs/wayfinder/guile-adelheid-slot/research/04-port-generator.md` (commit `e276239`).
