---
id: 02
title: "Existing documentation of both engines"
label: wayfinder:research
mode: AFK
status: closed
assignee: Tel-BR
blocked_by: []
research: research/02-existing-documentation:docs/wayfinder/base-direction/research/02-existing-documentation.md
---

## Question

Starting from [the starting leads](../research/00-starting-leads.md):

- Is SVC Chaos really built on the KOF 2003 engine? What public evidence exists?
- What do fbneo-training-mode, the hitbox scripts and the recomp projects already document about memory, the fighter structure, animation and hitboxes of both games?
- Does fbneo-training-mode support svc?

_PT-BR: partindo das pistas iniciais: o SVC é mesmo baseado no motor do KOF 2003, e que evidência pública existe? O que fbneo-training-mode, os scripts de hitbox e os projetos de recomp já documentam sobre memória, estrutura do lutador, animação e hitbox dos dois jogos? O fbneo-training-mode suporta svc?_

## Resolution

**Engine evidence.** MAME and FBNeo document the same cartridge hardware family (NEO-PVC, CMC and PCM2). SVC reached MVS in July 2003 and KOF 2003 in December. SuperCombo says SVC is based on the KOF 2003 engine, with no source attached. The documented SVC fighter fields for health, meter, facing and combos line up with KOF '96–2002. KOF 2003 uses different object and hitbox layouts and exposes team state in PVC RAM. The field overlap suggests older KOF lineage. The relationship between the game engines remains unverified.

**Available tools.** peon2's `fbneo-training-mode` has game and hitbox modules for both titles. It explicitly lists `svc`, `svcsplus` and `kof2003`. It also matches by parent set, so other clones can be recognized, with their memory layouts still to be checked. The separate JAMMA PCB sets are outside that detection. The modules map health, meter, facing, combo and timer, plus collision boxes. SVC's box-type table was borrowed from older KOF scripts. KOF 2003's viewer has a projectile/throw color bug. The dev-dem and Jesuszilla scripts cover older KOF games. The KOF 2003 recomp documents cartridge protection and the memory map. The other recomp projects reviewed supply runtime or PVC references. Animation frames, move scripts and the fighter API remain undocumented in the sources reviewed. [Animation format](08-animation-format.md) is where Shared Characters can be used to compare those layouts.

**PT-BR**

**Evidência sobre os motores.** MAME e FBNeo documentam a mesma família de hardware de cartucho (NEO-PVC, CMC e PCM2). O SVC saiu no MVS em julho de 2003 e o KOF 2003 em dezembro. A SuperCombo afirma que o SVC se baseia no motor do KOF 2003, sem citar uma fonte. Os campos documentados de vida, barra de especial, direção e combo no SVC coincidem com os do KOF '96–2002. O KOF 2003 usa outras estruturas de objetos e hitboxes e expõe o estado do time na RAM do PVC. A coincidência dos campos sugere parentesco com os KOF anteriores. A relação entre os motores segue sem comprovação.

**Ferramentas disponíveis.** O `fbneo-training-mode` de peon2 tem módulos de jogo e hitboxes para os dois títulos. Lista explicitamente `svc`, `svcsplus` e `kof2003`. Também reconhece outros clones pelo conjunto pai, com os endereços desses clones ainda por conferir. As placas JAMMA independentes ficam fora dessa detecção. Os módulos mapeiam vida, barra de especial, direção, combo, cronômetro e caixas de colisão. A tabela de tipos de caixas do SVC veio de scripts dos KOF anteriores. O visualizador do KOF 2003 tem um erro na cor de caixas de projéteis e arremessos. Os scripts de dev-dem e Jesuszilla cobrem KOFs anteriores. O recomp do KOF 2003 documenta a proteção do cartucho e o mapa de memória. Os demais recomps consultados servem de referência para o runtime ou o PVC. As fontes consultadas deixam em aberto os quadros de animação, os scripts de golpes e a API do lutador. O ticket [Animation format](08-animation-format.md) pode comparar essas estruturas usando os personagens compartilhados.

Research / Pesquisa: `research/02-existing-documentation:docs/wayfinder/base-direction/research/02-existing-documentation.md` (commit `9b6ceca`).
