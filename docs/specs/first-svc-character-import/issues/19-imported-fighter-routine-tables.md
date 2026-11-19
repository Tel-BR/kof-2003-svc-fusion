---
title: "Dispatch imported fighters' routine tables through the presentation map"
triage: ready-for-agent
---

# 19 Dispatch imported fighters' routine tables through the presentation map

[Parent specification](../spec.md) · [Diagnosis](14-rehearsal-intro-and-command-normals.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

After the Kyo clone (`$30`) performs Orochinagi, the flames of the move stay
attached to it for the rest of the match, even when it is off screen or defeated,
and remain where it fell until some buffer empties. Original Kyo does not do this.
Find the table that the imported ID reads past its end, repair the reusable
infrastructure with a checked tool step, and record how a new slot should check the
same class of table.

## Blocked by

None.

## Acceptance criteria

- [x] Reproduce the stuck flames with a recorded input script, run on the clone and on
  the reference ROM, with a command that goes red on this symptom and green when fixed.
- [x] Identify the table and the reader that give the imported ID a different result
  from the source fighter, with the evidence kept in `private/`.
- [x] Fix it with a checked tool step and byte-level tests on invented data.
- [x] The clone equals the reference in the recorded replay (above the intended palette
  change); an original-only team and ticket 13's route are unchanged.
- [ ] Before Guile's phase 4, give the new fighter its own entries in the routine
  tables instead of reusing a source fighter's routines (see the comment below).

## Português (Brasil)

# 19 Despachar as tabelas de rotinas dos importados pelo mapa de apresentação

Depois que o Kyo clone (`$30`) executa o Orochinagi, as chamas do golpe ficam presas
a ele até o fim da luta, mesmo fora da tela ou derrotado, e permanecem onde ele caiu
até algum buffer esvaziar. O Kyo original não faz isso. Achar a tabela que o ID
importado lê além do fim, corrigir a infraestrutura reaproveitável com um passo de
ferramenta conferido e registrar como um slot novo deve checar a mesma classe de tabela.

### Bloqueios

Nenhum.

### Critérios de aceitação

- [x] Reproduzir as chamas presas com um roteiro de entrada gravado, rodado no clone e
  na ROM de referência, com um comando que fica vermelho neste sintoma e verde quando
  corrigido.
- [x] Identificar a tabela e o leitor que dão ao ID importado um resultado diferente do
  lutador de origem, com a evidência guardada em `private/`.
- [x] Corrigir com um passo de ferramenta conferido e testes de bytes com dados
  inventados.
- [x] O clone fica igual à referência no replay gravado (acima da mudança de paleta
  pretendida); uma equipe só de originais e a rota do ticket 13 ficam inalteradas.
- [ ] Antes da fase 4 do Guile, dar ao novo lutador entradas próprias nas tabelas de
  rotinas em vez de reutilizar as rotinas de um lutador de origem (ver o comentário
  abaixo).

## Comments

### 2026-11-19 — Stuck Orochinagi flames: cause found and fixed (routine tables)

**Symptom, reported and reproduced.** The owner ran Orochinagi with the clone leading
player 1 (first retreating from the opponent): the flames stayed attached to the clone,
and after it was defeated they stayed where it fell. Original Kyo does not show it. The
session was recorded with the monitor and per-frame trace on (1,994 frames), the P1
input transitions were converted into an input script (59 intervals), and the script
was replayed headless on the clone and on the reference ROM.

**Loop.** `python -W ignore p2loop.py --tag oro --exe build-t14\"KOF 2003.exe" --clone
roms-t14 --script oro.txt --frames 1994 --shots 1600,1700,1800,1993 --tol 40` in
`private/work/first-import/diag-t17/` (about 12 s native): RED, 1,200 to 2,700 px at
frames 1,600 to 1,993, with no flame in the reference at those frames; the interpreter
gives the same counts. `--tol 40` is needed: the clone's palette change already
differs by more than 24 in 75 to 190 px of the body (hair and jacket) at every frame.

**Evidence.** The fighter's state words (ID, state, action, frame word) are equal in all
1,994 frames, so the fighter's logic is the same; what differs are effect objects (owner
ID byte `$30` against `$1E`, a frame pointer shifted by the constant of the relocated
frame copy, expected). A ROM-read diff by program counter over frames 1,446 to 1,451 and
1,519 to 1,523 lists every read indexed by the fighter ID (`d0` = `$C0` against `$78`).
For each pair the bytes in the clone's program image were compared: all but one are equal,
that is, entries that the tools already copied to `$30`. The exception is the dispatcher
at `$2B432`: the clone reads `$2B51A`, the reference `$2B4D2`, and the contents differ
(the clone gets a pointer into neighbouring data), so the second read and the `jsr`
that follows go to other code. The table of 37 pointers starts at `$2B45A` and ends well
before `$2B51A`.

**One-variable test.** In a private copy, only the three instructions that compute the
index at `$2B432` were rerouted through the presentation map. Interpreter, same script:
1,200 to 2,700 px before, 75 to 117 px after (the palette baseline); the flames are gone in
the images.

**Search.** The index arithmetic (`moveq #$3F`, `and.w ($1E,A4)`, two doublings) appears at
seven places. Five are followed by an absolute table address and read directory tables
that earlier tools extend (their reads compared equal in the clone image). Two use a table
relative to the program counter: `$2B30E` (table `$2B336`) and `$2B432` (table `$2B45A`).
`$2B30E` is not reached in this replay; it is changed because it has the same structure,
not because it was observed to fail.

**Fix.** `tools/kof2003/import_slot/map_fighter_handlers.py` (after
`map_intro_opponent.py`): both index computations call a 28-byte routine at `$53280` that
maps the ID through the presentation map at `$53100` first; originals map to themselves.
Four new byte tests on invented data (wrong map, wrong site bytes, used space, wrong
hash, paths outside `private/`); the neighbouring test files still pass (8 tests).

**Verification (native `build-t14d`, `roms-t14d`).** The replay: 0 px at `--tol 40` on
frames 1,600, 1,700, 1,800 and 1,993. Ticket 13's route against the reference: 0 px at
`--tol 24` on frames 4,800 to 6,100. An original-only team against `roms-v`: 0 px at five
frames from 5,400 to 9,000. No new native fallback: the clone run reports 9 uncovered
entry points and 40 interpreted instructions, against 10 and 40 for the reference run.

**Not established.** The short flame of the clone's *intro* (ticket 14, residual: 124 px at
frame 5,000 and 17 px at frame 5,040 with three different leaders; 830 and 367 px with
original Kyo leading) is the same before and after this fix, so it has another cause. `$2B30E` was not exercised.

**Owner decision for later.** The map entry of `$30` now also decides whose routines the
clone runs. For Guile that would run Kyo's routines. Before Guile's phase 4 her own
entries must be written in these two tables (ticket 05, moveset), and this mapping must
not stand in for them.

_PT-BR — Chamas presas do Orochinagi: causa encontrada e corrigida (tabelas de rotinas)._

_**Sintoma, relatado e reproduzido.** O dono executou o Orochinagi com o clone liderando o
jogador 1 (antes se afastando do oponente): as chamas ficaram presas ao clone e, depois
que ele foi derrotado, ficaram onde ele caiu. O Kyo original não mostra isso. A sessão foi
gravada com o monitor e o rastreio por quadro ligados (1.994 quadros), as transições de
entrada do P1 foram convertidas num roteiro de entrada (59 intervalos) e o roteiro foi
repetido sem janela no clone e na ROM de referência._

_**Laço.** `python -W ignore p2loop.py --tag oro --exe build-t14\"KOF 2003.exe" --clone
roms-t14 --script oro.txt --frames 1994 --shots 1600,1700,1800,1993 --tol 40` em
`private/work/first-import/diag-t17/` (uns 12 s no nativo): VERMELHO, de 1.200 a 2.700 px
nos quadros 1.600 a 1.993, sem chama na referência nesses quadros; o interpretador dá as
mesmas contagens. O `--tol 40` é necessário: a mudança de paleta do clone já difere em
mais de 24 em 75 a 190 px do corpo (cabelo e jaqueta) em todos os quadros._

_**Evidência.** As palavras de estado do lutador (ID, estado, ação, quadro) são iguais nos
1.994 quadros, então a lógica do lutador é a mesma; o que difere são objetos de efeito (byte
de ID do dono `$30` contra `$1E`, ponteiro de quadro deslocado pela constante da cópia
relocada de quadros, esperado). A comparação das leituras da ROM por contador de programa nos
quadros 1.446 a 1.451 e 1.519 a 1.523 lista toda leitura indexada pelo ID do lutador (`d0` =
`$C0` contra `$78`). Para cada par comparei os bytes na imagem do programa do clone: todos
menos um são iguais, isto é, entradas que as ferramentas já copiaram para o `$30`. A exceção é
o despachante em `$2B432`: o clone lê `$2B51A`, a referência `$2B4D2`, e o conteúdo difere (o
clone recebe um ponteiro para dados vizinhos), então a segunda leitura e o `jsr` seguinte vão
para outro código. A tabela de 37 ponteiros começa em `$2B45A` e termina bem antes de
`$2B51A`._

_**Teste de uma variável.** Numa cópia privada, só as três instruções que calculam o índice em
`$2B432` foram desviadas pelo mapa de apresentação. Interpretador, mesmo roteiro: de 1.200 a
2.700 px antes, de 75 a 117 px depois (a base da paleta); as chamas somem nas imagens._

_**Busca.** A aritmética do índice (`moveq #$3F`, `and.w ($1E,A4)`, duas duplicações) aparece
em sete lugares. Cinco são seguidos por um endereço absoluto de tabela e leem tabelas de
diretório que ferramentas anteriores estendem (as leituras deram iguais na imagem do clone).
Dois usam uma tabela relativa ao contador de programa: `$2B30E` (tabela `$2B336`) e `$2B432`
(tabela `$2B45A`). O `$2B30E` não é alcançado neste replay; ele foi alterado por ter a mesma
estrutura, não porque se observou que falha._

_**Correção.** `tools/kof2003/import_slot/map_fighter_handlers.py` (depois do
`map_intro_opponent.py`): os dois cálculos de índice chamam uma rotina de 28 bytes em `$53280`
que primeiro mapeia o ID pelo mapa de apresentação em `$53100`; os originais mapeiam para si
mesmos. Quatro testes de bytes novos com dados inventados (mapa errado, bytes do ponto errados,
espaço usado, hash errado, caminhos fora de `private/`); os arquivos de teste vizinhos
continuam passando (8 testes)._

_**Verificação (nativo `build-t14d`, `roms-t14d`).** O replay: 0 px com `--tol 40` nos quadros
1.600, 1.700, 1.800 e 1.993. A rota do ticket 13 contra a referência: 0 px com `--tol 24` nos
quadros 4.800 a 6.100. Uma equipe só de originais contra `roms-v`: 0 px em cinco quadros de
5.400 a 9.000. Sem novo recurso de contingência no nativo: a execução do clone relata 9 pontos
de entrada não cobertos e 40 instruções interpretadas, contra 10 e 40 da execução de
referência._

_**Não estabelecido.** A chama curta da *intro* do clone (ticket 14, resíduo: 124 px no quadro
5.000 e 17 px no quadro 5.040 com três líderes diferentes; 830 e 367 px com o Kyo original
de líder) é igual antes e depois desta correção, então tem outra causa. O `$2B30E` não foi exercitado._

_**Decisão do dono para depois.** A entrada do `$30` no mapa agora também decide de quem são as
rotinas que o clone executa. Para o Guile isso executaria as rotinas do Kyo. Antes da fase 4
do Guile as entradas próprias dela precisam ser escritas nessas duas tabelas (ticket 05,
repertório), e este mapeamento não pode ficar no lugar delas._
