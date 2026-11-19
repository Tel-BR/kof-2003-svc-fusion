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

`relocate_frames.py` takes that intermediate image, copies the selected fighter's
frame directory to unused banked space and redirects ID `$30` to the copy. It
keeps each frame's palette header and changes the decoded tile indices by
`$80000`. It checks the input identity and refuses unknown or truncated frame
layouts. This is still not playable: use a 128 MiB descriptor that loads the
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

O `relocate_frames.py` recebe essa imagem intermediária, copia o diretório de
quadros do lutador escolhido para espaço livre com banco e aponta o ID `$30`
para a cópia. Preserva o cabeçalho de paleta de cada quadro e aumenta os índices
de tile decodificados em `$80000`. Confere a identidade da entrada e recusa
formatos desconhecidos ou incompletos. Ainda não é jogável: é necessário um
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

