# KOF 2003 × SVC Chaos Recomp

A native PC port that unites the rosters of The King of Fighters 2003 and SNK vs. Capcom: SVC Chaos, bringing fighters from one game into the other.

_PT-BR: um port nativo para PC que une os elencos de The King of Fighters 2003 e SNK vs. Capcom: SVC Chaos, trazendo personagens de um jogo para o outro._

## Language / Linguagem

### Games / Jogos

**Base Game**:
The game whose engine and fighting system receive the fighters.
_Avoid_: host, main game

_PT-BR — **Jogo base**: o jogo cujo motor e sistema de luta recebem os personagens. Evitar: host, jogo principal._

**Donor Game**:
The game the Imported Characters come from.
_Avoid_: source game, guest

_PT-BR — **Jogo doador**: o jogo de onde vêm os personagens importados. Evitar: jogo fonte, guest._

### Characters / Personagens

**Shared Character**:
A fighter present in both games; the reference used to correlate the two engines.
_Avoid_: common character, repeated character

_PT-BR — **Personagem compartilhado**: presente nos dois jogos; referência para correlacionar os motores. Evitar: personagem comum, repetido._

**Character Version**:
A Shared Character as represented in one of the two games, such as Terry from KOF 2003 or Terry from SVC Chaos. In the planned local Versus mode, either version can be selected under either game's rules.

_PT-BR — **Versão do personagem**: um personagem compartilhado tal como aparece em um dos jogos, como Terry do KOF 2003 ou Terry do SVC Chaos. No Versus local planejado, qualquer uma das versões pode ser escolhida sob as regras de qualquer um dos jogos._

**Exclusive Character**:
A fighter present only in the Donor Game.

_PT-BR — **Personagem exclusivo**: presente apenas no jogo doador._

**Imported Character**:
Any fighter brought from the Donor Game into the Base Game, whether shared or exclusive.
_Avoid_: ported character, converted character

_PT-BR — **Personagem importado**: qualquer personagem trazido do jogo doador para o jogo base, seja compartilhado ou exclusivo. Evitar: portado, convertido._

### Graphics / Gráficos

**Graphics Set**:
All the tile data the native player loads and draws from; 64 MiB today, growing to 128 MiB, the most a tile number can address.
_Avoid_: crom, graphics set size, tile ROM

_PT-BR — **Conjunto gráfico**: todos os dados de tiles que o player nativo carrega e de onde desenha; hoje 64 MiB, crescendo para 128 MiB, o máximo que um número de tile alcança. Evitar: crom, tile ROM._

**Added Space**:
The half of the grown Graphics Set above tile `$80000`, which holds no KOF 2003 data and is reserved for tiles of Imported Characters.
_Avoid_: expansion, extra graphics, new C files

_PT-BR — **Espaço acrescentado**: a metade do conjunto gráfico ampliado acima do tile `$80000`, que não guarda dados do KOF 2003 e é reservada aos tiles dos personagens importados. Evitar: expansão, gráficos extras, arquivos C novos._

**Rehearsal**:
The trial that precedes Guile: a complex regular fighter is cloned into a new ID with its tiles in the Added Space, to prove the growth of the Graphics Set, the relocated ID tables and a new ID before any Imported Character depends on them.
_Avoid_: dry run, clone test

_PT-BR — **Ensaio**: a prova que antecede o Guile: um lutador regular e complexo é clonado num ID novo com os tiles no espaço acrescentado, para provar a ampliação do conjunto gráfico, as tabelas de ID movidas e um ID novo antes de qualquer personagem importado depender deles. Evitar: teste a seco, teste de clone._

### Sound / Som

**Pending Voice**:
A character-specific voice of an Imported Character that SVC plays but that did not fit the free sound space, so the fighter stays without it until the space grows; it is recorded in a per-fighter register so the voice can be added later.
_Avoid_: missing voice, skipped sample

_PT-BR — **Voz pendente**: voz própria de um personagem importado que o SVC toca mas que não coube no espaço de som livre, então o lutador fica sem ela até o espaço crescer; fica anotada num registro por lutador para poder ser acrescentada depois. Evitar: voz faltando, amostra pulada._

