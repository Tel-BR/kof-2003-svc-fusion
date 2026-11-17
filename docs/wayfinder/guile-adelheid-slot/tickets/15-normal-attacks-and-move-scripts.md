---
id: 15
title: "How KOF 2003 runs normal attacks and what its move scripts hold"
label: wayfinder:research
mode: AFK
status: closed
assignee:
blocked_by: []
research: research/15-normal-attacks-and-move-scripts:docs/wayfinder/guile-adelheid-slot/research/15-normal-attacks-and-move-scripts.md
---

## Question

[How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) found that every universal action runs on common code (states below `$70`), and that Adelheid's own code (`$3B09C`–`$3B721`, 1,670 bytes) serves only states `$70`–`$BF`, her tail states `$2C5`–`$2D0` and a 14-entry table. Most of it is stubs that call `$02A5B2`, which picks a move script from the `$7DC28` directory and continues in the shared interpreters `$02A600`, `$02B07E` or `$02B1D2`. It did not measure normal attacks.

Which states and handlers run KOF 2003's standing and crouching normal attacks (light and heavy punch and kick), common or per-fighter? What does a move script in the `$7DC28` directory hold: its layout, how it reaches the step scripts, and where a normal's hit properties live (damage, hitstun, guard type, cancel windows)? Use Adelheid's normals as the worked example. The answer tells the map whether Guile's one basic attack is data only or needs new or patched 68000 code; [How the native port's generator handles changed or added 68000 code and data](04-port-generator.md) already says where native code can live. Record addresses, strides, sizes and counts only.

Leads from [KOF 2003's sprite frame and collision record format](20-frame-and-collision-format.md): an attack box carries an attack index in its second byte, which picks the row of the attacker's 64-entry tables at `$706A2` onward; a box only attacks if its kind is marked in the fighter's 128-bit map at `$6C62E`; and each step carries four flag bytes (`+$50`–`+$53`) that the move-script code at `$02AE86` reads.

_PT-BR: a pesquisa 01 mostrou que toda ação universal roda em código comum (estados abaixo de `$70`) e que o código próprio da Adelheid (`$3B09C`–`$3B721`, 1.670 bytes) só atende os estados `$70`–`$BF`, os finais `$2C5`–`$2D0` e uma tabela de 14 entradas. Quase tudo são atalhos para `$02A5B2`, que escolhe um script de golpe no diretório `$7DC28` e segue nos interpretadores comuns `$02A600`, `$02B07E` ou `$02B1D2`. Os golpes normais não foram medidos. Quais estados e rotinas executam os normais do KOF 2003 em pé e agachado (socos e chutes fracos e fortes), comuns ou do lutador? O que guarda um script de golpe do diretório `$7DC28`: formato, como chega aos scripts de passos e onde ficam as propriedades de acerto de um normal (dano, atordoamento, tipo de defesa, janelas de cancelamento)? Usar os normais da Adelheid como exemplo. A resposta diz se o golpe básico do Guile é só dado ou se precisa de código 68000 novo ou modificado; a pesquisa 04 já diz onde o código nativo pode ficar. Registrar só endereços, espaçamentos, tamanhos e contagens. Pistas da pesquisa 20: a caixa de golpe traz no segundo byte um índice que escolhe a linha das tabelas de 64 entradas de quem ataca, a partir de `$706A2`; uma caixa só ataca se o tipo dela estiver marcado no mapa de 128 bits do lutador em `$6C62E`; e cada passo traz quatro bytes de indicadores (`+$50`–`+$53`) que o código de scripts de golpe em `$02AE86` lê._

## Resolution

Findings: `research/15-normal-attacks-and-move-scripts:docs/wayfinder/guile-adelheid-slot/research/15-normal-attacks-and-move-scripts.md` (commit `f9b7131`, local throwaway branch). Resolved by a research subagent; static reading only, nothing measured in MAME.

**Answer for the map.** A one-button basic attack for Guile needs **no new 68000 instructions** if it reuses an existing state stub and uses no per-fighter hook (move-script bits 6-7). It needs data in six places, listed in section 8 of the findings.

**How a normal starts.** Every frame `$029436` walks a per-fighter command list (12-byte records; tables `$79872` and `$798F2`) and sets the state to the first matching record's target. Adelheid's list is at `$7D8BC` with 20 records and 17 target states.

**State code and scripts.** Each per-fighter state is a 22-byte stub that loads a number and calls `$02A5B2`, which picks a move script from `$7DC28` (her block is at `$8711C`). A script is a stream of 32-bit masks plus wait conditions; the cancel window is wait condition 1 (`$02AE86`), which tests nibbles of the step's `+$52`/`+$53`. Her 23 scripts total 572 bytes in `$871E0`-`$874F6`; a plain attack script is 14 bytes.

**Hit properties.** Rows of 64 bytes per ID in the tables from `$706A2` to `$74762`, plus `$75C22`, indexed by the box's attack index. The per-ID defence factors come from `$77A22`/`$77AB6` (4 bytes per ID).

**Left open.** (1) Which state a plain standing or crouching A/B/C/D enters: the low attack rows (`$00`-`$17`, actions `$6A`-`$93`) were not traced to their caller, and whether Adelheid's own normals are among her listed states is not resolved. (2) The button-to-state mapping, hit-stun and guard-type sources, and jump normals. Section 6 of the findings has a MAME recipe to settle these; the owner can run it and confirm visually. (3) The note still says "Guile in Adelheid's slot" and "once the ID is `$22`": that is stale, Guile takes `$30` ([Choose how fighter slots are found for the SVC Exclusive Characters](06-slot-strategy.md)), and the per-ID rows are read for `$30` instead.

**PT-BR**

Achados: `research/15-normal-attacks-and-move-scripts:docs/wayfinder/guile-adelheid-slot/research/15-normal-attacks-and-move-scripts.md` (commit `f9b7131`, branch local descartável). Resolvido por um subagente de pesquisa; só leitura estática, nada medido no MAME.

**Resposta para o mapa.** Um golpe básico de um botão para o Guile **não precisa de instruções 68000 novas** se reaproveitar um atalho de estado existente e não usar rotina própria do lutador (bits 6-7 do script). Precisa de dados em seis lugares, listados na seção 8 dos achados.

**Como um normal começa.** A cada quadro `$029436` percorre uma lista de comandos do lutador (registros de 12 bytes; tabelas `$79872` e `$798F2`) e põe o estado no alvo do primeiro registro que casa. A lista da Adelheid fica em `$7D8BC`, com 20 registros e 17 estados alvo.

**Código de estado e scripts.** Cada estado do lutador é um atalho de 22 bytes que carrega um número e chama `$02A5B2`, que escolhe um script de golpe em `$7DC28` (o bloco dela fica em `$8711C`). O script é um fluxo de máscaras de 32 bits e condições de espera; a janela de cancelamento é a condição 1 (`$02AE86`), que testa nibbles de `+$52`/`+$53` do passo. Os 23 scripts dela somam 572 bytes em `$871E0`-`$874F6`; um script de ataque simples tem 14 bytes.

**Propriedades de acerto.** Linhas de 64 bytes por ID nas tabelas de `$706A2` a `$74762`, mais `$75C22`, indexadas pelo índice de ataque da caixa. Os fatores de defesa por ID vêm de `$77A22`/`$77AB6` (4 bytes por ID).

**Em aberto.** (1) Que estado um A/B/C/D simples em pé ou agachado aciona: as linhas baixas de ataque (`$00`-`$17`, ações `$6A`-`$93`) não foram rastreadas até quem as chama, e não se resolveu se os normais da Adelheid estão entre os estados listados dela. (2) Mapa botão para estado, origem do atordoamento e do tipo de defesa, e normais de pulo. A seção 6 dos achados traz uma receita de MAME para resolver isso; o dono pode rodá-la e confirmar visualmente. (3) A nota ainda diz "Guile na vaga da Adelheid" e "quando o ID for `$22`": está desatualizado, o Guile assume o `$30` ([ticket 06](06-slot-strategy.md)), e as linhas por ID são lidas para o `$30`.
