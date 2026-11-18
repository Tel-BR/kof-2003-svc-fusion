# KOF 2003 fighter data: notes for a future export

These notes collect findings from the first-import Rehearsal that may also help
translate a KOF 2003 fighter into another game. They describe addresses,
formats and counts, not game assets. A future destination will have its own
animation, palette, collision and combat rules; copying KOF records alone does
not establish equivalent play.

## Identity and lookup

- A team-slot byte carries a six-bit fighter ID and two colour-selection bits.
  Kyo's original ID is `$1E`; `$30` is the new Rehearsal ID, not another KOF
  fighter. There are 37 original IDs, `$00`–`$24`; some other IDs are used by
  non-fighter objects. A fighter ID is not itself an asset address.
- The master directory at `$0704A2` points to fighter-specific data. Other
  ID-indexed tables hold combat, palette and presentation information. Two
  banked directories at program file offsets `$200000` and `$380000` lead to
  frame and animation data. Several tables and guards stop at 37 entries; some
  per-fighter data are shared or accessed through other objects.
- The original roster must remain a separate control when adding an ID. For a
  two-fighter matrix, changing only one axis is insufficient: both the selected
  fighter and the opponent can supply an ID. A same-team original/clone match
  is a separate behavioural test, not proof that the matrix or all originals
  work in every situation.

Sources: [fighter lookup](../../wayfinder/guile-adelheid-slot/tickets/01-fighter-id-to-data.md),
[ID capacity](../../wayfinder/guile-adelheid-slot/tickets/03-slot-capacity.md),
[selection lookup](../../wayfinder/guile-adelheid-slot/tickets/02-selection-screen.md).

## Frames and tiles

- A fighter's frame directory starts with a count and word offsets, measured in
  two-byte units, relative to its directory. The frame number in a step is a
  10-bit value. Kyo has 585 frame references in the examined program; his
  directory and records occupy the interval `$294CC0`–`$2995C6` in the prepared
  program file. These are specific to the validated input, not universal file
  offsets for every release.
- Each frame begins with palette offset, format, column count and row count.
  Its body uses one of eleven formats (`0`–`$A`). Some represent consecutive
  tiles, others individual tiles; masks can omit cells. Formats differ in the
  placement of the tile's upper address bits, so an exporter must decode the
  format and masks instead of assuming one fixed record size. Frame placement
  and flip flags come from animation steps, not the tile image alone.
- The tile number has 20 bits; the native renderer supports the upper half of a
  128 MiB Graphics Set. Earlier work proved that a synthetic tile in Added Space
  can be drawn. In this session, an independent existing decoder compared all
  585 original Kyo frames with a private relocated copy: frame formats, palette
  offsets, dimensions and per-cell attributes matched, and decoded tile numbers
  increased by `$80000`. This is a data comparison, **not yet a rendered or
  gameplay validation** of the relocated fighter.
- Kyo's 585 records used formats 0, 1, 2, 5, 6, 7, 8, 9 and `$A`; none used
  formats 3 or 4. In this particular directory all 585 records were distinct.
  A general exporter must still handle all eleven formats, including records
  shared by multiple references.
- Loading the original four graphics pairs a second time in positions five to
  eight is a Rehearsal technique: the same tile content then exists at the old
  index plus `$80000`. It avoids creating a second collection of game files,
  but duplicates the complete Graphics Set in memory. It is not an export
  format or a final import design.

Source: [sprite-frame formats](../../wayfinder/guile-adelheid-slot/tickets/18-sprite-frame-tiles.md)
and its linked research branch; [Graphics Set growth](../../specs/graphics-set-growth/issues/04-draw-added-space-tile.md).

| Format | Tile representation | Cell masks | Upper tile bits |
| --- | --- | --- | --- |
| 0, 1 | Consecutive run per frame | Word per column (0); byte per column (1) | Low nibble of start tile's high word |
| 2 | Three bytes per drawn tile | None | High nibble of each tile attribute |
| 3, 4 | Per-tile word (3) or byte (4) | None | Shared frame attribute |
| 5, 6 | Three bytes per drawn tile | Word per column (5); padded byte masks (6) | High nibble of each tile attribute |
| 7, 8 | Per-tile word | Word per column (7); padded byte masks (8) | Shared frame attribute |
| 9, `$A` | Per-tile byte | Word per column (9); unpadded byte masks (`$A`) | Shared frame attribute |

Masks are read most-significant bit first; formats 2, 5 and 6 pack tile words
and attributes in alternating order. Empty cells do not consume tile records.
The frame's palette offset is not part of the tile number and must not be
modified while shifting tile indices.

## Animation, collision and colour

- Animation steps carry duration, flags, frame selection, position and optional
  extra layers, boxes, sound and command operands. Positions use signed values;
  a destination exporter must handle facing and flips. The same sprite frames
  alone do not preserve movement or action timing.
- A collision box records a kind, attack index, offsets and half-sizes. KOF's
  classifications and per-attack properties have to be translated to the
  destination's collision and damage model; pixels that look the same are not
  evidence of identical hit, block or whiff behaviour. Push boxes are obtained
  separately from the fighter's special action, not from each ordinary step.
- Preserve the palette reference of each frame, along with the colour values,
  and identify the source and destination of every referenced palette slot.
  This session checked that Kyo's relocated headers stayed equal; it did not
  establish a complete palette exporter. The Guile phase-4 gate remains open:
  identify and exercise all 33 frames with upper palette offsets, verify their
  sources and destinations, and compare the rendered results before accepting
  that mapping.
- In the validated program, the four ID-indexed palette tables are at
  `$06090A`, `$06098A`, `$060A0A` and `$060A8A`. Each entry selects the first
  of 16 consecutive palette slots; each slot has 16 colour words. Kyo's original
  starting indices are `$880`, `$890`, `$8A0` and `$8B0`. The palette loader
  reads the colour data from the bank starting at file `$100000`, using a
  32-byte stride per palette index. These facts identify a source candidate;
  they do not prove every frame's destination slot on screen.
- The Neo Geo colour word carries five bits per RGB channel, split between a
  four-bit field and a separate low bit, plus a dark bit. The Rehearsal tool
  preserves that dark bit and entry zero; export to ordinary RGB requires
  decoding the split channels and defining how the destination represents
  transparency and the dark bit.
- The Rehearsal makes a private copy of 16 palette slots for each of four
  colour choices, with new per-ID indices; it does not overwrite Kyo's original
  indices. At the owner's request specifically for this clone, all four
  candidates vary the original A/B sets: A/C and B/D use opposite 30-degree
  hue directions, neutral colours receive a small tint, each 5-bit channel is
  limited to three levels, and entry zero and the dark bit stay unchanged.
  Numeric checks confirmed those bounds on the generated candidates; the slots
  and rendered appearance still need an in-game check. This exception does not
  change the separately approved Guile rule.

Sources: [step and collision format](../../wayfinder/guile-adelheid-slot/tickets/20-frame-and-collision-format.md),
[palette decision](../../wayfinder/guile-adelheid-slot/tickets/16-guile-colours.md),
[ticket 04 gate](issues/04-complete-first-imported-match.md).

## Work still required for an export

Identify the target game's supported image, colour and animation formats;
decode the complete source action and step graph; resolve layers, palette
references, sounds and all required collision and movement semantics; translate
them explicitly; and compare representative poses, timings and interactions in
both games. Keep extracted art, generated game data, recordings and captures in
`private/`. The current Rehearsal tools are partial and do not produce an
exported or playable character.

# Dados de lutador do KOF 2003: notas para uma futura exportação

Estas notas reúnem descobertas do Ensaio que também podem ajudar a traduzir um
lutador do KOF 2003 para outro jogo. Elas descrevem endereços, formatos e
contagens, sem incluir assets do jogo. O destino terá regras próprias de
animação, paleta, colisão e combate; copiar registros do KOF não comprova jogo
equivalente.

## Identidade e consulta

- Um byte de vaga de equipe leva um ID de lutador de seis bits e dois bits de
  escolha de cor. O ID original do Kyo é `$1E`; `$30` é o novo ID do Ensaio,
  não outro lutador do KOF. Há 37 IDs originais, `$00`–`$24`; outros IDs são
  usados por objetos que não são lutadores. O ID não é um endereço de asset.
- O diretório principal em `$0704A2` aponta para dados específicos de cada
  lutador. Outras tabelas indexadas por ID guardam informações de combate,
  paleta e apresentação. Dois diretórios com banco nos offsets de arquivo
  `$200000` e `$380000` levam aos dados de quadros e animações. Várias tabelas
  e verificações param em 37 entradas; alguns dados são compartilhados ou
  acessados por outros objetos.
- O elenco original precisa continuar como controle separado ao acrescentar um
  ID. Numa matriz de dois lutadores, mudar só um eixo não basta: tanto o
  lutador escolhido como o adversário podem fornecer um ID. Uma luta com
  original e clone na mesma equipe é um teste comportamental à parte, não
  prova de que a matriz ou todos os originais funcionam em qualquer situação.

Fontes: os três tickets ligados na seção em inglês sobre consulta, capacidade
de IDs e seleção.

## Quadros e tiles

- O diretório de quadros começa com uma contagem e deslocamentos em palavras,
  medidos em unidades de dois bytes a partir do próprio diretório. O número de
  quadro de um passo tem 10 bits. No programa examinado, Kyo tem 585 referências
  de quadro; diretório e registros ocupam o intervalo de arquivo `$294CC0` a
  `$2995C6`. Esses endereços são da entrada validada, não universais.
- Cada quadro começa com deslocamento de paleta, formato, número de colunas e
  número de linhas. O corpo usa um de onze formatos (`0`–`$A`). Alguns guardam
  sequências de tiles e outros, tiles individuais; máscaras podem omitir células.
  Os formatos colocam os bits superiores do tile em posições diferentes; um
  exportador precisa decodificar formato e máscaras, sem supor tamanho fixo.
  Posição e espelhamento vêm dos passos da animação, não só da imagem do tile.
- O número do tile tem 20 bits; o renderizador nativo suporta a metade superior
  de um Conjunto gráfico de 128 MiB. A etapa anterior comprovou o desenho de
  um tile sintético no Espaço acrescentado. Nesta sessão, um decodificador de
  pesquisa independente comparou os 585 quadros originais do Kyo com uma cópia
  privada relocada: formatos, deslocamentos de paleta, dimensões e atributos
  por célula coincidiram, e os números de tile decodificados subiram `$80000`.
  É uma comparação de dados, **ainda não uma validação visual ou de jogo**.
- Os 585 registros do Kyo usaram os formatos 0, 1, 2, 5, 6, 7, 8, 9 e `$A`;
  nenhum usou 3 ou 4. Nesse diretório específico, todos eram distintos. Um
  exportador geral ainda precisa tratar os onze formatos e registros
  compartilhados por várias referências.
- Carregar os quatro pares gráficos originais uma segunda vez nas posições cinco
  a oito é uma técnica do Ensaio: o mesmo conteúdo passa a existir no índice
  antigo mais `$80000`. Ela dispensa uma segunda coleção de arquivos do jogo,
  mas duplica o Conjunto gráfico inteiro em memória. Não é um formato de
  exportação nem o projeto final da importação.

Fontes: os tickets de formato de quadros e ampliação gráfica ligados acima.
Na tabela da seção em inglês, "word" é uma palavra, "byte" é um byte,
"per column" significa por coluna e "shared frame attribute" indica um
atributo compartilhado pelo quadro. As máscaras são lidas do bit mais
significativo ao menos significativo; os formatos 2, 5 e 6 alternam a ordem de
palavras de tile e atributos. Células vazias não consomem registros de tile.
O deslocamento de paleta do quadro não integra o número de tile e não deve ser
alterado ao deslocar seus índices.

## Animação, colisão e cor

- Os passos de animação contêm duração, indicadores, escolha de quadro, posição
  e camadas extras, caixas, som e operandos de comando opcionais. Posições têm
  sinal; um exportador precisa tratar direção e espelhamentos. Os sprites
  isolados não preservam o movimento nem a duração das ações.
- Uma caixa de colisão registra tipo, índice de ataque, deslocamentos e meias
  dimensões. As classificações e propriedades de golpe do KOF precisam ser
  traduzidas para a colisão e o dano do destino; aparência igual não comprova
  o mesmo acerto, defesa ou golpe no vazio. Caixas de empurrão vêm de uma ação
  especial do lutador, não de cada passo comum.
- Preserve a referência de paleta de cada quadro junto aos valores de cor e
  identifique origem e destino de cada slot referenciado. Nesta sessão os
  cabeçalhos relocados do Kyo ficaram iguais; isso não estabelece um exportador
  completo de paletas. O gate da fase 4 do Guile continua aberto: identificar e
  exercitar os 33 quadros com deslocamentos superiores, verificar origem e
  destino e comparar resultados renderizados antes de aceitar o mapeamento.
- No programa validado, as quatro tabelas de paleta indexadas por ID ficam em
  `$06090A`, `$06098A`, `$060A0A` e `$060A8A`. Cada entrada seleciona o primeiro
  de 16 slots consecutivos; cada slot tem 16 palavras de cor. Os índices iniciais
  originais do Kyo são `$880`, `$890`, `$8A0` e `$8B0`. O carregador lê os
  dados do banco iniciado no offset de arquivo `$100000`, com distância de 32
  bytes por índice de paleta. Esses fatos identificam uma origem candidata;
  não comprovam o slot de destino na tela para todos os quadros.
- A palavra de cor do Neo Geo tem cinco bits por canal RGB, divididos entre um
  campo de quatro bits e um bit baixo separado, além de um bit escuro. A
  ferramenta do Ensaio preserva esse bit e a entrada zero; exportar para RGB
  comum exige decodificar os canais e definir como o destino representa
  transparência e o bit escuro.
- O Ensaio cria uma cópia privada de 16 slots para cada uma das quatro opções
  de cor, com novos índices por ID, sem sobrescrever os índices do Kyo original.
  A pedido do dono apenas para este clone, as quatro candidatas variam os
  conjuntos A/B originais: A/C e B/D usam sentidos opostos de 30 graus de matiz,
  cores neutras recebem leve tonalidade, cada canal de 5 bits varia até três
  níveis e a entrada zero e o bit escuro ficam iguais. Conferências numéricas
  confirmaram esses limites; os slots e a aparência ainda precisam de teste no
  jogo. Essa exceção não altera a regra aprovada separadamente para o Guile.

Fontes: os tickets de passos e colisão, decisão de paletas e gate do ticket 04
ligados acima.

## O que ainda falta para exportar

Identificar os formatos de imagem, cor e animação aceitos pelo jogo de destino;
decodificar todo o grafo de ações e passos da origem; resolver camadas,
referências de paleta, sons e a semântica de colisão e movimento; traduzir tudo
explicitamente; e comparar poses, durações e interações representativas nos
dois jogos. Artes extraídas, dados gerados dos jogos, gravações e capturas ficam
em `private/`. As ferramentas atuais do Ensaio são parciais e não produzem um
personagem exportado ou jogável.
