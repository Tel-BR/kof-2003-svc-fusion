# First imported character: workspace preparation

`prepare_workspace.py` copies an already prepared ROM directory into a new
directory under `private/`. It uses independent files, so later edits to the
experimental program do not change the original control. It refuses an existing
destination and sources containing symbolic links. Both paths must be in
`private/`. This prepares inputs only: it does not make a build or add a fighter.

```powershell
python tools/kof2003/import_slot/prepare_workspace.py `
  private/work/mvs-control-v0.1.0/roms private/work/first-import/roms
```

If copying fails, inspect any partially created destination before removing it
and retrying. Never stage its contents in git.

## Intermediate table relocation

`relocate_action_tables.py` writes a **new, incomplete program image** under
`private/`. It moves nine 64-byte-row tables, six 4-byte-row tables and one
80-byte-row table, and expands a two-fighter matrix in both dimensions, into
fixed-area space, repoints their identified readers and copies a chosen original
fighter's rows to ID `$30`. It also copies the fighter's master, move-script,
four palette and two banked-directory entries to `$30`; the banked entries still point at the
original fighter's data. The 37 original rows and other indexed values are
preserved except where the new `$30` row or column is installed. Kyo is ID
`$1E`. The command checks the input's exact
SHA-256, each expected table reference and the unused destination space before
writing; it refuses an existing output. Pass the expected hash of the known
control explicitly:

```powershell
$program = 'private/work/first-import/roms/271-pd.bin'
$hash = 'f6ad2e2d7496eb094b92108b85aca6c71cf6fb397c690e49a04048da27143215'
python tools/kof2003/import_slot/relocate_action_tables.py $program `
  private/work/first-import/program-tables.bin --sha256 $hash --fighter-id 0x1e
```

This image does not yet provide the new fighter: the remaining tables, guards,
selection, graphics and lone-fighter shortcut are not implemented. Do not use
it as the rehearsal build. The input and output must stay in `private/`.

`relocate_frames.py` takes that intermediate image and places the selected
fighter's frame directory in a bank of its own, by the owner's decision (ticket
15): all original directories share one bank whose top 8 KiB is NEO-PVC RAM, so
there is no room there. `--file-offset` names the program file offset of the
copy; it must be even, after the frame bank (`0x300000` or later), inside the
program, fit in one window below the PVC RAM, and be unused (`$FF`). The
Rehearsal uses `0x700000`. The copy keeps each frame's palette header and changes
the decoded tile indices by `$80000`. The tool adds a 64-entry bank table at
`$53340` (the frame bank for every ID except `$30`) and three routines at
`$53440`: the three frame-lookup layers select the object's bank and tag an
own-bank frame pointer with its ID in the top byte (ignored by the 24-bit bus),
and the three drawer layers select the bank named by that byte. The frame bank
and its directory table are not changed. It checks the input identity, every
reader site and the empty table area, and refuses unknown or truncated frame
layouts. Rebuild native code afterwards. This is still not playable: use a 128 MiB descriptor that loads the
same four graphics pairs a second time, and complete the remaining ID and
selection work. `rehearsal_descriptor.py` can create a separate private
descriptor with those duplicated pair references without copying game files;
its output must be compiled with the player. Neither tool changes its input.

`rehearsal_palettes.py` creates four private 16-slot palette blocks for the
clone and points only ID `$30` at them. By the owner's instruction specific to
this Rehearsal, all four variants are altered: A/C start from original A and
B/D from original B, with opposite directions in each pair. Coloured entries
rotate by 30 degrees, neutral entries receive a slight red or blue tint, and
each 5-bit channel changes by at most three levels. Entry zero and the dark bit
are preserved. This broader rule is **only for the Kyo clone**, not the approved
Guile conversion rule. It generates candidates; it does not establish that the
palette-slot mapping or on-screen results are correct.

`selection_table.py` prepares a separate program image with the original 39
selection cells copied into a larger table and six provisional cells in two new
rows. The first new cell carries `$30`; the remaining five are random cells,
not yet implemented imports. It raises cursor limits and uses a private 68000
helper to reach the new table. This does **not** yet implement the on/off switch,
presentation or all ID guards, so it is not a finished selection route.

`wire_slot_lookups.py` takes the image after `relocate_action_tables.py` (and
the selection step) and writes a new private image: it raises four ID guards,
moves the two special-intro tables to 64 rows, copies the source fighter's entry
to `$30` in the 64-entry tables that hold a shared default, and adds the
presentation map. Every selection-screen and name-plate lookup that handles only
IDs up to `$24` (sites `$9042`, `$9124`, `$91FE`, `$9338`, `$9E00`, `$9F26`,
`$1F886`) now jumps to a small trampoline that maps the ID through a 64-byte
table at `$53100` (identity, `$30` = the source fighter) before repeating the
displaced instructions; the routine is at `$53140` and the trampolines from
`$53150`. It checks the expected bytes of every site and that `$53100`–`$531FF`
is empty, and refuses a source ID of `$22`–`$24` (hidden entries). Run the tests
from a folder where temporary files can be deleted.

```powershell
python tools/kof2003/import_slot/wire_slot_lookups.py $in $out --sha256 $hash --fighter-id 0x1e
```

`map_victory_screen.py` takes the image after `wire_slot_lookups.py` and writes a
new private image. The victory screen copies the winning team's three bytes
(colour bits in bits 7-6, fighter ID in bits 5-0) from the match team list into
its own object at `$E202` and then looks up the winner sprite, the win quote and
the name plate by that ID; those tables only cover the original roster, so `$30`
read past their ends. The tool replaces that six-byte copy with a call to a short
routine at `$53200` that keeps the colour bits and maps the ID through the
presentation map at `$53100`, so the imported fighter wins as its source fighter
and shows as that fighter on the plate when a teammate wins. It checks the
expected bytes of the site, that the presentation map routine exists and that
`$53200`–`$5323F` is empty. It adds no art, palette or quote of its own, and the
fight stage and its victory background still follow the leader's ID.

```powershell
python tools/kof2003/import_slot/map_victory_screen.py $in $out --sha256 $hash
```

`map_intro_opponent.py` takes the image after `map_victory_screen.py` and writes a
new private image. The special-intro selection (routine `$40BCA`) reads the other
fighter's ID at `$40BE2` and looks for it, as a literal ID or through a group code, in
the row of the fighter whose intro is chosen; rival pairs are written that way (the
row of Iori Yagami names Kyo Kusanagi), so with the imported `$30` as the other
fighter the original got the default intro and the fight drifted from the same fight
against original Kyo. The tool replaces the eight bytes of that read and the next
instruction with a call to a short routine at `$53240` that repeats them with the ID
mapped through the presentation map at `$53100`; originals map to themselves and
`$30` is recognised as its source fighter. It checks the expected bytes of the site,
that the map is the one `wire_slot_lookups.py` writes and that `$53240`–`$5327F` is
empty. The map entry of `$30` is both the presentation source and the rival identity.

```powershell
python tools/kof2003/import_slot/map_intro_opponent.py $in $out --sha256 $hash
```

`map_fighter_handlers.py` takes the image after `map_intro_opponent.py` and writes a
new private image. Two dispatchers (`$2B30E` and `$2B432`) pick a fighter's own table
of routines by its ID, indexing a 37-entry table of pointers (`$2B336` and `$2B45A`)
with `4 * (ID & $3F)`. For the imported `$30` the index ran past the end of the
table and other data was called; in a recorded Orochinagi replay the flames of the
move stayed on screen for the rest of the match. The tool reroutes the three
instructions that compute the index at both places to a short routine at `$53280`
that maps the ID through the presentation map at `$53100` first, so the imported
fighter uses its source fighter's routines; originals map to themselves. It checks
the expected bytes of both sites, that the map is the one `wire_slot_lookups.py`
writes and that `$53280`–`$532BF` is empty.

```powershell
python tools/kof2003/import_slot/map_fighter_handlers.py $in $out --sha256 $hash
```

`map_opponent_rows.py` takes the image after `map_fighter_handlers.py` and writes a
new private image. The readers at `$216AC` and `$21836` index 42-byte per-opponent
rows (tables of 37 rows) by the other fighter's ID, so an imported ID read past the
tables. By the owner's decision an imported ID is read through a proxy: the tool writes
a 64-byte table at `$532C0` (identity for `$00`–`$24`, the `--proxy` value for `$30`,
`$1E` for the other IDs until each import chooses its own) and a 24-byte routine at
`$53300` that reads the other fighter's ID, maps it and returns the row offset. Both
readers call it. The input may have the original readers (checked by fingerprint) or
the old diagnostic patch, which the tool removes from `$52E00`–`$52E11`. It checks that
`$532C0`–`$5333F` is empty and that `--proxy` names an original fighter. The proxy only
chooses these rows; presentation, rival intros and fighter routines keep their own maps.

```powershell
python tools/kof2003/import_slot/map_opponent_rows.py $in $out --sha256 $hash --proxy 0x1E
```

`map_hitbox_kinds.py` takes the image after `map_opponent_rows.py` and writes a new
private image. The collision routine reads, at `$15D08` and `$169CA`, a 64-entry table
of pointers at `$6C62E` by the box owner's ID; each pointer leads to a 16-byte bit set
of hit-box kinds. Entries `$25`–`$3F` share fighter `$24`'s set, so the imported `$30`
classified its boxes with a set that differs from original Kyo's. The tool copies the
`--fighter-id` fighter's pointer to entry `$30`; nothing else changes and no code is
added, so the native player needs no rebuild. It checks that every unused entry still
holds fighter `$24`'s pointer, that `$30` has no own entry yet, that the source fighter
has its own set and that each original set lies in the fixed area (below `$100000`) and
off the table.

```powershell
python tools/kof2003/import_slot/map_hitbox_kinds.py $in $out --sha256 $hash --fighter-id 0x1e
```

`pvc_byte_writes.py` is a runtime patch, not a program-image step. The NEO-PVC
chip's colour pack and unpack run only on 16-bit writes in the pinned runtime,
but the game fills those inputs with byte writes, so every palette fade it
computes came out as zero and sprites turned into flat silhouettes. The tool
copies the runtime's `bus.c` to a new private file with the byte handler
triggering the same pack, unpack and bank actions as the word handler. It
checks the file's SHA-256, refuses paths outside `private/` and a file that is
already patched, and keeps the file's line endings. The published v0.1.0 player
and the upstream `main` have the same defect.

```powershell
python tools/kof2003/import_slot/pvc_byte_writes.py $bus $busFixed --sha256 $busHash
```

For a future manual build, `manual_keys.py` prepares a private SDL source with
the owner's P1 layout. `monitor_hook.py`, the CMake option
`KOF2003_REHEARSAL_MONITOR`, and `rehearsal_monitor.c` enable an optional log
of changes to the team bytes, P1 input transitions and a periodic heartbeat when
the environment variable `KOF_REHEARSAL_MONITOR` is set. Set
`KOF_REHEARSAL_TRACE` too to include a P1 object state on every frame. Keep stderr and any captures under
`private/`. The hook is off unless both the build option and environment
variable are enabled; it does not establish that a match finished successfully.
For a development-only lone-fighter check, set `KOF_REHEARSAL_LONE_ID` to the
chosen ID (for example `0x30`). After that ID is picked as P1's first fighter
and both team copies agree, the hook empties P1's two remaining slots once per
process. This is a test aid, not the normal team-selection path; without the
option it does not write team memory. A scripted interpreter check reached the
normal winner screen after a loss; native verification remains open.

## Preparação para o primeiro personagem importado

O `prepare_workspace.py` copia uma pasta de ROMs já preparada para uma pasta
nova dentro de `private/`. Os arquivos são independentes, então alterações
posteriores no programa experimental não mudam o controle original. O comando
recusa um destino existente e origens com links simbólicos. Os dois caminhos
devem ficar em `private/`. Ele apenas prepara os arquivos: não compila o jogo
nem acrescenta um lutador.

Use o comando acima no PowerShell. Se a cópia falhar, inspecione qualquer pasta
parcial antes de removê-la e tentar novamente. Nunca adicione seu conteúdo ao git.

### Relocação intermediária de tabelas

O `relocate_action_tables.py` grava uma **nova imagem de programa incompleta**
em `private/`. Ele move nove tabelas com linhas de 64 bytes, seis com linhas
de 4 bytes, uma com linhas de 80 bytes e uma matriz de dois lutadores nas duas
dimensões para espaço fixo, ajusta os leitores identificados e copia as linhas
de um lutador original escolhido para o ID `$30`. Também copia as entradas da
tabela principal, do diretório de scripts de golpes, das quatro tabelas de
paleta e dos dois diretórios com banco;
essas entradas ainda apontam para os dados do lutador original. As 37 linhas
originais e os demais valores indexados são preservados, salvo onde são criadas
a linha ou a coluna `$30`. Kyo tem ID `$1E`. O
comando confere o SHA-256 exato da entrada, as referências esperadas e o espaço
livre antes de escrever; recusa uma saída existente. Use o bloco em inglês acima
com o hash do controle conhecido. Entrada e saída ficam em `private/`.

Essa imagem ainda não oferece o novo lutador: faltam as demais tabelas, os
limites, a seleção, os gráficos e o atalho de lutador solo. Não a use como
build do ensaio.

O `relocate_frames.py` recebe essa imagem intermediária e coloca o diretório de
quadros do lutador escolhido num banco próprio, por decisão do dono (ticket 15):
todos os diretórios originais dividem um banco cujos 8 KiB finais são RAM do
NEO-PVC, então não há espaço ali. `--file-offset` indica a posição da cópia no
arquivo do programa; precisa ser par, depois do banco de quadros (`0x300000` em
diante), dentro do programa, caber numa janela abaixo da RAM do PVC e estar livre
(`$FF`). O Ensaio usa `0x700000`. A cópia preserva o cabeçalho de paleta de cada
quadro e aumenta os índices de tile decodificados em `$80000`. A ferramenta grava
uma tabela de bancos de 64 entradas em `$53340` (banco de quadros para todo ID
menos o `$30`) e três rotinas em `$53440`: as três camadas da busca de quadros
escolhem o banco do objeto e marcam o ponteiro de quadro de banco próprio com o
ID no byte de cima (ignorado pelo barramento de 24 bits), e as três camadas do
desenhista escolhem o banco indicado por esse byte. O banco de quadros e sua
tabela de diretórios não mudam. Confere a identidade da entrada, cada ponto de
leitura e a área vazia da tabela, e recusa formatos desconhecidos ou incompletos.
Depois, recompile o código nativo. Ainda não é jogável: é necessário um
descritor de 128 MiB que carregue os quatro pares gráficos novamente e concluir
o restante do trabalho de IDs e seleção. O `rehearsal_descriptor.py` cria um
descritor privado separado com essas referências duplicadas, sem copiar arquivos
do jogo; sua saída precisa ser compilada com o player. Nenhuma das ferramentas
altera a própria entrada.

O `rehearsal_palettes.py` cria quatro blocos privados de 16 slots de paleta
para o clone e aponta somente o ID `$30` para eles. Por instrução do dono
específica deste Ensaio, as quatro variantes são alteradas: A/C partem do A
original e B/D do B original, com sentidos opostos em cada par. Entradas
coloridas giram 30 graus de matiz, as neutras recebem uma leve tonalidade
vermelha ou azul, e cada canal de 5 bits varia até três níveis. A entrada zero
e o bit escuro são preservados. Essa regra ampliada vale **só para o clone do
Kyo**, não para a conversão aprovada do Guile. Ela gera candidatas; não comprova
o mapeamento dos slots nem o resultado na tela.

O `selection_table.py` prepara uma imagem separada do programa, copiando as 39
células existentes para uma tabela maior com seis células provisórias em duas
novas linhas. A primeira contém `$30`; as outras cinco são aleatórias, não
importados implementados. Ele aumenta os limites do cursor e usa uma rotina
68000 privada para alcançar a nova tabela. Isso **ainda não** implementa o
interruptor, a apresentação nem todos os limites de ID, portanto não é uma rota
de seleção concluída.

Para um futuro build manual, o `manual_keys.py` prepara o fonte SDL privado com
o teclado P1 do dono. `monitor_hook.py`, a opção CMake
`KOF2003_REHEARSAL_MONITOR` e `rehearsal_monitor.c` permitem um registro opcional
das mudanças nas equipes, das entradas do P1 e de sinais periódicos de execução
quando a variável de ambiente `KOF_REHEARSAL_MONITOR` está definida. Defina
também `KOF_REHEARSAL_TRACE` para incluir o estado de um objeto do P1 a cada
quadro. Mantenha stderr e capturas em
`private/`. A sonda só liga com a opção de build e a variável; ela não comprova
que a luta terminou normalmente.
Para a conferência de lutador solo apenas de desenvolvimento, defina
`KOF_REHEARSAL_LONE_ID` com o ID escolhido (por exemplo `0x30`). Depois que esse
ID for escolhido como primeiro lutador do P1 e as duas cópias da equipe
coincidirem, a sonda esvazia as duas vagas restantes do P1 uma vez por processo.
É um auxílio de teste, não o fluxo normal de seleção; sem a opção ela não grava
na memória da equipe. Uma verificação por roteiro no interpretador chegou à
tela normal de vencedor após uma derrota; a validação nativa segue em aberto.
O `wire_slot_lookups.py` recebe a imagem depois do `relocate_action_tables.py`
(e do passo de seleção) e grava uma nova imagem privada: sobe quatro travas de
ID, move as duas tabelas de intro especial para 64 linhas, copia a entrada do
lutador de origem para o `$30` nas tabelas de 64 entradas com padrão comum e
acrescenta o mapa de apresentação. Toda busca da tela de seleção e do nome sob as
barras que só trata IDs até `$24` (pontos `$9042`, `$9124`, `$91FE`, `$9338`,
`$9E00`, `$9F26`, `$1F886`) passa a saltar para um trampolim pequeno que mapeia o
ID por uma tabela de 64 bytes em `$53100` (identidade, `$30` = lutador de origem)
antes de repetir as instruções deslocadas; a rotina fica em `$53140` e os
trampolins a partir de `$53150`. Confere os bytes esperados de cada ponto e que
`$53100`–`$531FF` está vazio, e recusa ID de origem `$22`–`$24` (entradas
ocultas). Rode os testes numa pasta onde arquivos temporários possam ser apagados.

O `map_victory_screen.py` recebe a imagem depois do `wire_slot_lookups.py` e grava
uma nova imagem privada. A tela de vitória copia os três bytes da equipe vencedora
(bits de cor nos bits 7-6, ID do lutador nos bits 5-0) da lista de equipes da
luta para um objeto próprio em `$E202` e depois busca sprite do vencedor, frase
de vitória e placa de nome por esse ID; essas tabelas só cobrem o elenco
original, então o `$30` lia além do fim. A ferramenta troca essa cópia de seis
bytes por uma chamada a uma rotina curta em `$53200` que preserva os bits de cor
e mapeia o ID pelo mapa de apresentação em `$53100`; assim o lutador importado
vence como o lutador de origem e aparece como ele na placa quando um colega
vence. Confere os bytes esperados do ponto, que a rotina do mapa de apresentação
existe e que `$53200`–`$5323F` está vazio. Não acrescenta arte, paleta nem frase
própria, e o cenário da luta e o fundo da vitória continuam seguindo o ID do
líder.

O `map_intro_opponent.py` recebe a imagem depois do `map_victory_screen.py` e grava
uma nova imagem privada. A escolha da intro especial (rotina `$40BCA`) lê o ID do
outro lutador em `$40BE2` e o procura, como ID literal ou por código de grupo, na
linha do lutador cuja intro é escolhida; os pares de rivais são escritos assim (a
linha do Iori Yagami cita o Kyo Kusanagi), então, com o `$30` importado como outro
lutador, o original recebia a intro padrão e a luta se afastava da mesma luta
contra o Kyo original. A ferramenta troca os oito bytes dessa leitura e a instrução
seguinte por uma chamada a uma rotina curta em `$53240` que os repete com o ID
mapeado pelo mapa de apresentação em `$53100`; os originais mapeiam para si mesmos e
o `$30` é reconhecido como o lutador de origem. Confere os bytes esperados do ponto,
que o mapa é o que o `wire_slot_lookups.py` grava e que `$53240`–`$5327F` está vazio.
A entrada do `$30` no mapa é ao mesmo tempo a origem da apresentação e a identidade
de rival.

```powershell
python tools/kof2003/import_slot/map_intro_opponent.py $in $out --sha256 $hash
```

O `map_fighter_handlers.py` recebe a imagem depois do `map_intro_opponent.py` e grava
uma nova imagem privada. Dois despachantes (`$2B30E` e `$2B432`) escolhem a tabela de
rotinas do próprio lutador pelo ID, indexando uma tabela de 37 ponteiros (`$2B336` e
`$2B45A`) por `4 * (ID & $3F)`. Com o `$30` importado o índice passava do fim da
tabela e outros dados eram chamados; num replay gravado do Orochinagi as chamas do
golpe ficavam na tela até o fim da luta. A ferramenta desvia as três instruções que
calculam o índice, nos dois lugares, para uma rotina curta em `$53280` que primeiro
mapeia o ID pelo mapa de apresentação em `$53100`; assim o lutador importado usa as
rotinas do lutador de origem e os originais mapeiam para si mesmos. Confere os bytes
esperados dos dois pontos, que o mapa é o que o `wire_slot_lookups.py` grava e que
`$53280`–`$532BF` está vazio.

```powershell
python tools/kof2003/import_slot/map_fighter_handlers.py $in $out --sha256 $hash
```

O `map_opponent_rows.py` recebe a imagem depois do `map_fighter_handlers.py` e grava
uma nova imagem privada. Os leitores em `$216AC` e `$21836` indexam linhas de 42 bytes
por adversário (tabelas de 37 linhas) pelo ID do outro lutador, então um ID importado
lia além das tabelas. Por decisão do dono, um ID importado é lido por um proxy: a
ferramenta grava uma tabela de 64 bytes em `$532C0` (identidade de `$00` a `$24`, o valor
de `--proxy` no `$30`, `$1E` nos demais IDs até cada importação escolher o seu) e uma
rotina de 24 bytes em `$53300` que lê o ID do outro lutador, passa pela tabela e devolve
o deslocamento da linha. Os dois leitores chamam essa rotina. A entrada pode ter os
leitores originais (conferidos por impressão digital) ou o antigo remendo de
diagnóstico, que a ferramenta remove de `$52E00`–`$52E11`. Confere que `$532C0`–`$5333F`
está vazio e que `--proxy` é um lutador original. O proxy só escolhe essas linhas;
apresentação, intros de rivais e rotinas por lutador continuam com os próprios mapas.

```powershell
python tools/kof2003/import_slot/map_opponent_rows.py $in $out --sha256 $hash --proxy 0x1E
```

O `map_hitbox_kinds.py` recebe a imagem depois do `map_opponent_rows.py` e grava uma
nova imagem privada. A rotina de colisão lê, em `$15D08` e `$169CA`, uma tabela de 64
ponteiros em `$6C62E` pelo ID do dono da caixa; cada ponteiro leva a um conjunto de 16
bytes de tipos de caixa de golpe. As entradas `$25`–`$3F` compartilham o conjunto do
lutador `$24`, então o `$30` importado classificava as caixas com um conjunto diferente
do Kyo original. A ferramenta copia o ponteiro do lutador de `--fighter-id` para a
entrada `$30`; nada mais muda e nenhum código é acrescentado, então o player nativo não
precisa ser recompilado. Confere que toda entrada sem uso ainda tem o ponteiro do lutador
`$24`, que o `$30` ainda não tem entrada própria, que o lutador de origem tem conjunto
próprio e que cada conjunto original fica na área fixa (abaixo de `$100000`) e fora da
tabela.

```powershell
python tools/kof2003/import_slot/map_hitbox_kinds.py $in $out --sha256 $hash --fighter-id 0x1e
```

O `pvc_byte_writes.py` é um ajuste do runtime, não um passo da imagem do
programa. No runtime fixado, o pack e o unpack de cor do chip NEO-PVC só rodam
em escritas de 16 bits, mas o jogo preenche essas entradas com escritas de byte;
por isso todo fade de paleta saía zerado e os sprites viravam silhuetas chapadas.
A ferramenta copia o `bus.c` do runtime para um arquivo privado novo, com o
tratador de byte disparando as mesmas ações de pack, unpack e troca de banco do
tratador de palavra. Confere o SHA-256 do arquivo, recusa caminhos fora de
`private/` e arquivo já corrigido, e mantém as quebras de linha. O player v0.1.0
publicado e o `main` do upstream têm o mesmo defeito.

