---
id: 15
title: "How KOF 2003 runs normal attacks and what its move scripts hold"
label: wayfinder:research
mode: AFK
status: open
assignee:
blocked_by: []
research:
---

## Question

[How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) found that every universal action runs on common code (states below `$70`), and that Adelheid's own code (`$3B09C`–`$3B721`, 1,670 bytes) serves only states `$70`–`$BF`, her tail states `$2C5`–`$2D0` and a 14-entry table. Most of it is stubs that call `$02A5B2`, which picks a move script from the `$7DC28` directory and continues in the shared interpreters `$02A600`, `$02B07E` or `$02B1D2`. It did not measure normal attacks.

Which states and handlers run KOF 2003's standing and crouching normal attacks (light and heavy punch and kick), common or per-fighter? What does a move script in the `$7DC28` directory hold: its layout, how it reaches the step scripts, and where a normal's hit properties live (damage, hitstun, guard type, cancel windows)? Use Adelheid's normals as the worked example. The answer tells the map whether Guile's one basic attack is data only or needs new or patched 68000 code; [How the native port's generator handles changed or added 68000 code and data](04-port-generator.md) already says where native code can live. Record addresses, strides, sizes and counts only.

Leads from [KOF 2003's sprite frame and collision record format](20-frame-and-collision-format.md): an attack box carries an attack index in its second byte, which picks the row of the attacker's 64-entry tables at `$706A2` onward; a box only attacks if its kind is marked in the fighter's 128-bit map at `$6C62E`; and each step carries four flag bytes (`+$50`–`+$53`) that the move-script code at `$02AE86` reads.

_PT-BR: a pesquisa 01 mostrou que toda ação universal roda em código comum (estados abaixo de `$70`) e que o código próprio da Adelheid (`$3B09C`–`$3B721`, 1.670 bytes) só atende os estados `$70`–`$BF`, os finais `$2C5`–`$2D0` e uma tabela de 14 entradas. Quase tudo são atalhos para `$02A5B2`, que escolhe um script de golpe no diretório `$7DC28` e segue nos interpretadores comuns `$02A600`, `$02B07E` ou `$02B1D2`. Os golpes normais não foram medidos. Quais estados e rotinas executam os normais do KOF 2003 em pé e agachado (socos e chutes fracos e fortes), comuns ou do lutador? O que guarda um script de golpe do diretório `$7DC28`: formato, como chega aos scripts de passos e onde ficam as propriedades de acerto de um normal (dano, atordoamento, tipo de defesa, janelas de cancelamento)? Usar os normais da Adelheid como exemplo. A resposta diz se o golpe básico do Guile é só dado ou se precisa de código 68000 novo ou modificado; a pesquisa 04 já diz onde o código nativo pode ficar. Registrar só endereços, espaçamentos, tamanhos e contagens. Pistas da pesquisa 20: a caixa de golpe traz no segundo byte um índice que escolhe a linha das tabelas de 64 entradas de quem ataca, a partir de `$706A2`; uma caixa só ataca se o tipo dela estiver marcado no mapa de 128 bits do lutador em `$6C62E`; e cada passo traz quatro bytes de indicadores (`+$50`–`+$53`) que o código de scripts de golpe em `$02AE86` lê._
