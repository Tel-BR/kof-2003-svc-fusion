---
id: 01
title: "How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/01-fighter-id-to-data:docs/wayfinder/guile-adelheid-slot/research/01-fighter-id-to-data.md
---

## Question

Starting from the team slots at `$107D0C`/`$107D12` and the load window between frames 4,900 and 5,230 found in [ticket 04](../../../specs/first-svc-character-import/issues/04-complete-first-imported-match.md), which tables does KOF 2003 index by fighter ID, and what does each entry point to: per-fighter code, the animation and pose table, collision records, tile ranges in the graphics ROM, palettes and sound calls? For each universal action in this map (walk, guard, run, backstep, the four jumps, evasive rolls, both Guard Cancels), is the behaviour driven by common engine code reading per-fighter data, or by per-fighter code? Use Adelheid (`$22`) as the worked example. Record addresses, strides, entry sizes and counts only.

_PT-BR: Partindo das vagas de equipe em `$107D0C`/`$107D12` e da janela de carga entre os quadros 4.900 e 5.230 do ticket 04, quais tabelas o KOF 2003 indexa pelo ID do lutador e para onde aponta cada entrada: código próprio do lutador, tabela de animações e poses, registros de colisão, faixas de tiles na ROM gráfica, paletas e chamadas de som? Para cada ação universal deste mapa (andar, defender, corrida, passo para trás, os quatro pulos, esquivas, os dois Guard Cancels), o comportamento vem de código comum do motor lendo dados do lutador ou de código próprio do lutador? Usar a Adelheid (`$22`) como exemplo. Registrar só endereços, espaçamentos, tamanhos e contagens._

## Resolution

**ID and load.** The fighter ID is the low 6 bits of the team-slot byte; bits 6–7 pick one of four colour tables. Fighter objects start at `$101080`, `$300` apart, with the ID at `+$1E`. In the load window only the copy at `$107D12` is read, at frames 4,925–4,926, by the palette setup (`$0010BC`) and the object creation (`$023BEA`).

**What the ID indexes.** The per-fighter state-handler block (`$704A2`; Adelheid `$9FAAE`, 721 entries), the move-script directory (`$7DC28`; Adelheid `$8711C`), the sprite-frame directory (file `$200000`; Adelheid's 335 animations), the step-script directory (file `$380000`; Adelheid at file `$5EEF50`), four palette-index tables (Adelheid `$980`–`$9B0`, 64 palettes) and 16 sound-code tables (`$6CF1E`). Collision boxes (four 6-byte boxes), velocity commands and sound calls sit inside the step scripts. Tile numbers sit in each frame's data; there is no per-ID tile base. Several smaller ID tables have roles not yet identified.

**Universal actions.** Walk, crouch, run, backstep, the four jumps (hop, jump, super jump and hyper hop, all measured), evasive rolls, standing and crouching guard and both Guard Cancels use states below `$70`, whose handlers are the same for all 37 fighters: **common engine code reading per-fighter data**. Adelheid's own code (`$3B09C`–`$3B721`, 1,670 bytes) is mostly stubs that pick a move script and jump into shared interpreters; it serves only states `$70`–`$BF`, her tail states `$2C5`–`$2D0` and a 14-entry table. No compare with `$22` was found in common code; Mukai (`$23`) has some.

**Left open.** Adelheid's complete tile range (1,592 tiles observed in `$68032`–`$6933C`; the frame layout is not fully decoded), the roles of several tables, and whether the back Guard Cancel roll has its own path. The forward Guard Cancel roll reuses the normal forward roll's state `$30` and actions `$4A`–`$4C`; the Guard Cancel CD is state `$47`, action `$83`.

**PT-BR**

**ID e carga.** O ID do lutador são os 6 bits de baixo do byte da vaga; os bits 6–7 escolhem uma de quatro tabelas de cor. Os objetos dos lutadores começam em `$101080`, a cada `$300`, com o ID em `+$1E`. Na janela de carga só a cópia `$107D12` é lida, nos quadros 4.925–4.926, pela preparação das paletas (`$0010BC`) e pela criação dos objetos (`$023BEA`).

**O que o ID indexa.** O bloco de rotinas por estado (`$704A2`; Adelheid `$9FAAE`, 721 entradas), o diretório de scripts de golpe (`$7DC28`; Adelheid `$8711C`), o diretório de quadros de sprite (arquivo `$200000`; 335 animações da Adelheid), o diretório de scripts de passos (arquivo `$380000`; Adelheid no arquivo `$5EEF50`), quatro tabelas de índice de paleta (Adelheid `$980`–`$9B0`, 64 paletas) e 16 tabelas de códigos de som (`$6CF1E`). Caixas de colisão (quatro caixas de 6 bytes), comandos de velocidade e chamadas de som ficam dentro dos scripts de passos. Os números de tile ficam nos dados de cada quadro; não há base de tiles por ID. Várias tabelas menores ainda têm função desconhecida.

**Ações universais.** Andar, agachar, correr, passo para trás, os quatro pulos (pulinho, pulo, super pulo e hiper pulinho, todos medidos), esquivas, defesa em pé e agachado e os dois Guard Cancels usam estados abaixo de `$70`, cujas rotinas são as mesmas nos 37 lutadores: **código comum do motor lendo dados do lutador**. O código próprio da Adelheid (`$3B09C`–`$3B721`, 1.670 bytes) é quase todo atalho que escolhe um script de golpe e salta para interpretadores comuns; só atende os estados `$70`–`$BF`, os estados finais `$2C5`–`$2D0` e uma tabela de 14 entradas. Nenhuma comparação com `$22` apareceu no código comum; com `$23` (Mukai), sim.

**Em aberto.** A faixa completa de tiles da Adelheid (1.592 tiles observados em `$68032`–`$6933C`; o formato de quadro não está todo decodificado), a função de várias tabelas e se a esquiva de Guard Cancel para trás tem caminho próprio. A esquiva de Guard Cancel para a frente reaproveita o estado `$30` e as ações `$4A`–`$4C` da esquiva normal; o Guard Cancel CD é o estado `$47`, ação `$83`.

Research / Pesquisa: `research/01-fighter-id-to-data:docs/wayfinder/guile-adelheid-slot/research/01-fighter-id-to-data.md` (commit `e67d4f6`).
