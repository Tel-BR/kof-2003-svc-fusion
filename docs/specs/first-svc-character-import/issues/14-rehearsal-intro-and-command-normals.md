---
title: "Diagnose the Kyo rehearsal intro and command normals"
triage: ready-for-agent
---

# 14 Diagnose the Kyo rehearsal intro and command normals

[Parent specification](../spec.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

Compare the `$30` Kyo rehearsal with original Kyo from reproducible initial
states. The owner reported that the clone missed the frozen starting frame
before the intro and that forward + B was unavailable. After the move-directory
correction removed the observed duplicates, he reported that most commands
responded but their behaviour was incorrect, including grabs and cancels.
Establish which data or
rules cause each difference and repair the reusable infrastructure when it is
needed for the first import. The recorded projectile-special defect is tracked
in ticket 04; it must not be used as proof that command normals are fixed.

## Acceptance criteria

- [x] Reproduce the reported starting-frame and forward + B differences with
  known inputs, recording setup and observations separately.
- [x] Compare clone and original at the same meaningful action and game state;
  account for facing, spacing, intro timing and opponent behaviour.
- [ ] Identify whether each cause is shared slot infrastructure or rehearsal
  presentation; fix the shared cause required by the first import and record
  any clone-only work separately.
- [x] Record the observed grab and cancel discrepancies and determine whether
  they reveal shared infrastructure defects or clone-specific moveset work.
- [ ] Check the affected original Kyo path and other relevant original fighters
  for regression. Keep all game data, captures and traces in `private/`.

## Português (Brasil)

# 14 Diagnosticar a intro e os normais de comando do Kyo do ensaio

Comparar o Kyo do ensaio `$30` com o Kyo original a partir de estados iniciais
reproduzíveis. O dono relatou que faltou o quadro inicial congelado antes da
intro e que frente + B não estava disponível. Após a correção do diretório de
golpes eliminar as duplicações observadas, relatou que a maioria dos comandos
respondia, mas o comportamento ainda estava incorreto, inclusive em agarrões e
cancelamentos. Descobrir quais dados ou regras
causam cada diferença e corrigir a infraestrutura reaproveitável necessária à
primeira importação. O defeito registrado no especial de projétil está no
ticket 04; sua correção não comprova que os normais de comando funcionam.

### Critérios de aceitação

- [x] Reproduzir as diferenças do quadro inicial e de frente + B com entradas
  conhecidas, registrando preparação e observações separadamente.
- [x] Comparar clone e original na mesma ação e no mesmo estado significativo,
  considerando lado, distância, tempo da intro e comportamento do adversário.
- [ ] Identificar se cada causa pertence à infraestrutura compartilhada ou à
  apresentação do ensaio; corrigir a causa compartilhada necessária à primeira
  importação e registrar trabalho exclusivo do clone separadamente.
- [x] Registrar as diferenças observadas em agarrões e cancelamentos e decidir
  se revelam defeitos da infraestrutura compartilhada ou trabalho específico do
  repertório do clone.
- [ ] Conferir regressão do caminho afetado do Kyo original e dos demais
  originais relevantes. Dados dos jogos, capturas e traces ficam em `private/`.

## Comments

### 2026-11-18 — Owner decision: rehearsal bar is "no unexplained difference"

The owner set the bar for the Kyo Rehearsal before Guile takes `$30`: every
difference between the clone and original Kyo must be explained, but the clone
does not need to be a perfect copy. Differences caused by the slot (ID-indexed
or pair-indexed tables not yet wired to `$30`) are fixed now, because Kyo has a
reference to compare against and Guile does not, and the same slot serves IDs
`$30`–`$3E`. Grabs, cancels and forward + B are treated as part of the route,
not polish. The frozen pre-intro frame is diagnosed; if its cause is an
un-extended table it is extended, otherwise it is recorded as clone-only work.
Clone-only cosmetic matters (Kyo art quality, pixel-identical intro, the
clone's colour variants, broader same-team checks) are recorded, not polished.
Native coverage is still collected for phase 7. The causes listed here are
hypotheses until this ticket's diagnosis establishes them.

_PT-BR: o dono definiu o critério do Ensaio do Kyo antes de o Guile ocupar o
`$30`: toda diferença entre o clone e o Kyo original precisa ser explicada, mas
o clone não precisa ser cópia perfeita. Diferenças causadas pela vaga (tabelas
indexadas por ID ou por par ainda não ligadas ao `$30`) são corrigidas agora,
porque o Kyo tem gabarito para comparação e o Guile não, e a mesma vaga serve
aos IDs `$30`–`$3E`. Agarrões, cancelamentos e frente + B contam como parte do
caminho, não como polimento. O quadro congelado antes da intro é diagnosticado;
se a causa for uma tabela não estendida, ela é estendida, senão fica registrada
como trabalho exclusivo do clone. Questões cosméticas do clone (qualidade da
arte do Kyo, intro idêntica pixel a pixel, variações de cor do clone,
conferências mais amplas na mesma equipe) são registradas, não polidas. A
cobertura nativa continua sendo recolhida para a fase 7. As causas citadas são
hipóteses até o diagnóstico deste ticket comprová-las._

### 2026-11-18 — Duplicate report at 17:15 traced to the pre-fix ROM directory

The owner reported that the duplicate fighter returned in a monitored session
with the `candidate-manual-build` executable. The session's input was replayed
headless with that executable against two private ROM directories that differ
only in the two bytes of the `$7DC28` move-script directory entry for `$30`.
At the first special (action `$79`, frame 1,642) the session's trace matches the
pre-fix directory exactly (the `$30` lookup reads `$FFFF`) and diverges from the
corrected directory. The executable was therefore run with ROMs that lack the
move-directory correction; this is not evidence of a new defect. The earlier
`manual-fixed` session, whose grab and cancel feedback this ticket records, has
no `$FFFF` lookup for `$30` in its trace. Manual runs must pass the corrected
ROM directory explicitly with `--rom-path`.

_PT-BR: o dono relatou que o lutador duplicado voltou numa sessão monitorada com
o executável `candidate-manual-build`. As entradas da sessão foram repetidas sem
janela com esse executável contra duas pastas privadas de ROMs que só diferem
nos dois bytes da entrada de `$30` no diretório de scripts de golpes `$7DC28`.
No primeiro especial (ação `$79`, quadro 1.642) o trace da sessão coincide
exatamente com a pasta anterior à correção (a busca do `$30` lê `$FFFF`) e
diverge da pasta corrigida. Portanto o executável rodou com ROMs sem a correção
do diretório de golpes; isso não indica defeito novo. A sessão anterior
`manual-fixed`, cujo retorno sobre agarrões e cancelamentos este ticket
registra, não tem leitura `$FFFF` do `$30` no trace. Execuções manuais precisam
indicar explicitamente a pasta de ROMs corrigida com `--rom-path`._

### 2026-11-18 — Differential diagnosis: causes found

**Loop.** A private headless pair runs the same input twice with the
`candidate-manual-build` sources: original Kyo, and Kyo with the fighter turned
into `$30` by the rehearsal monitor (test aids `KOF_REHEARSAL_FORCE`,
`KOF_REHEARSAL_POKE`, `KOF_REHEARSAL_DUMP`, `KOF_REHEARSAL_P2_TEAM`, all off
unless set). Two variants: swap after team order (frame 4,874, before the
fighter is created), which tests creation and the intro; and swap of the object,
team bytes and second copy while idle in the fight (frame 6,030), which tests
in-fight lookups from an identical state. An interpreter-only PC trace (private,
removed afterwards) located the first divergent branch each time. The CPU team
order changed when the swap happened during selection, so that variant was not
used for comparisons.

**Causes confirmed by prediction, all shared slot infrastructure:**

1. Four ID guards still stopped at `$24`/`$25` in front of tables already
   relocated to 64 rows (`$166A8`, `$240F0`, `$24124`, `$27E06`); `$30` fell back
   to fighter `$00`'s rows. First divergence at frame 4,924 (`$24128`).
2. Two 37-entry special-intro tables were not relocated (`$A5DB6`, read at
   `$407EA`/`$40866`; `$A5E4A`, read at `$409E8`/`$40C70`). These are two of the
   19 tables counted by the slot research; the tool had handled 17.
3. 64-entry tables whose entries above `$24` hold a shared default:
   command-list offsets `$79872`/`$798F2` (empty list for `$30`; needed for
   forward + B), command-to-action offsets `$B3204` (37 filled entries with
   header room; needed for the grab), and `$79672`, `$79772`, `$B8250` and the
   banked proximity directory at file `$62B9AC`.
4. Per-opponent proximity records: readers at `$216AC` and `$21836` index
   42-byte rows by the other fighter's ID in tables of 37 rows. When an original
   fighter faces `$30`, it reads past them. A diagnostic proxy mapping `$30` to
   `$1E` at those two readers was required for an identical grab.
5. The frame directory copy at `$2FB000` overlaps KOF 2003's NEO-PVC RAM window
   (`$2FE000`–`$2FFFFF`), which shadows ROM in the frame bank: 154 of the 585
   Kyo frame records read chip RAM. This is the missing frozen pre-intro frame.
   A diagnostic placement elsewhere in the frame bank restored it. Only about
   12 KiB of the frame bank is free below the window, less than Kyo's 18 KiB
   directory.

**Result.** With 1–5 applied, the clone's traced state matched original Kyo
for all 1,070 frames after the in-fight swap (walk, grab, forward + B, standing
C, run and back + D), and for the whole intro after the creation swap. The
remaining difference is a voice: sound guards `$18D08`/`$18E90` protect
37-entry sound tables (tickets 10–12). Original Kyo's trace and object RAM were
identical between the unmodified candidate (native) and the corrected image
(interpreter) for the frames compared. A cancel was not exercised: the scripted
standing C whiffed for both fighters. Not established: other originals,
P2-side, cancels on hit.

**Ablation.** Removing the opponent proxy diverged at frame 6,239; removing the
command-list entries diverged at 6,341 (forward + B). The proximity-directory
entry and the three pointer-table entries made no difference in this in-fight
test; `$B8250` lies on the creation path.

**Tooling.** `wire_slot_lookups.py` applies 1–3 with checks; on the real
candidate its output equals the tested image outside the diagnostic-only parts
(4 and 5). `relocate_frames.py` now refuses a copy reaching the PVC window, so
the current rehearsal pipeline stops there until frame placement is decided.

**Owner decisions needed:** where imported frame data lives (the frame bank has
no room), and how original fighters read per-opponent data for imported IDs.

_PT-BR — Diagnóstico diferencial: causas encontradas._

_**Ciclo.** Um par privado sem janela roda as mesmas entradas duas vezes com as
fontes do `candidate-manual-build`: Kyo original e Kyo transformado em `$30`
pelo monitor do ensaio (auxílios de teste `KOF_REHEARSAL_FORCE`,
`KOF_REHEARSAL_POKE`, `KOF_REHEARSAL_DUMP`, `KOF_REHEARSAL_P2_TEAM`, desligados
se não definidos). Duas variantes: troca depois da ordem da equipe (quadro
4.874, antes de o lutador ser criado), que testa a criação e a intro; e troca do
objeto, dos bytes da equipe e da segunda cópia com o lutador parado na luta
(quadro 6.030), que testa as consultas em luta a partir de um estado idêntico.
Um trace de PC só no interpretador (privado, removido depois) localizou a
primeira ramificação divergente a cada vez. A ordem da equipe da CPU mudava
quando a troca acontecia na seleção, então essa variante não foi usada nas
comparações._

_**Causas confirmadas por previsão, todas da infraestrutura de vagas:**_

_1. Quatro travas de ID ainda paravam em `$24`/`$25` antes de tabelas já
movidas para 64 linhas (`$166A8`, `$240F0`, `$24124`, `$27E06`); o `$30` caía
nas linhas do lutador `$00`. Primeira divergência no quadro 4.924 (`$24128`)._
_2. Duas tabelas de intro especial de 37 entradas não tinham sido movidas
(`$A5DB6`, lida em `$407EA`/`$40866`; `$A5E4A`, lida em `$409E8`/`$40C70`).
São duas das 19 tabelas contadas na pesquisa de vagas; a ferramenta tratava 17._
_3. Tabelas de 64 entradas cujas entradas acima de `$24` têm um padrão comum:
deslocamentos das listas de comandos `$79872`/`$798F2` (lista vazia para o
`$30`; necessária para frente + B), deslocamentos comando → ação `$B3204`
(37 entradas preenchidas e espaço no cabeçalho; necessária para o agarrão), e
`$79672`, `$79772`, `$B8250` e o diretório de proximidade em banco no arquivo
`$62B9AC`._
_4. Registros de proximidade por adversário: os leitores em `$216AC` e `$21836`
indexam linhas de 42 bytes pelo ID do outro lutador em tabelas de 37 linhas.
Quando um original enfrenta o `$30`, lê além delas. Um proxy de diagnóstico que
mapeia `$30` para `$1E` nesses dois leitores foi necessário para um agarrão
idêntico._
_5. A cópia do diretório de quadros em `$2FB000` sobrepõe a janela de RAM do
NEO-PVC do KOF 2003 (`$2FE000`–`$2FFFFF`), que encobre a ROM no banco de
quadros: 154 dos 585 registros de quadro do Kyo liam a RAM do chip. É o quadro
congelado que faltava antes da intro. Uma posição de diagnóstico em outro ponto
do banco de quadros o restaurou. Só cerca de 12 KiB do banco de quadros estão
livres abaixo da janela, menos que os 18 KiB do diretório do Kyo._

_**Resultado.** Com 1–5 aplicados, o estado traçado do clone coincidiu com o do
Kyo original em todos os 1.070 quadros após a troca em luta (andar, agarrão,
frente + B, C em pé, corrida e trás + D), e na intro inteira após a troca na
criação. A diferença restante é uma voz: as travas de som `$18D08`/`$18E90`
protegem tabelas de som de 37 entradas (tickets 10–12). O trace e a RAM de
objetos do Kyo original foram idênticos entre a candidata sem alterações
(nativa) e a imagem corrigida (interpretador) nos quadros comparados. Não se
exercitou cancelamento: o C em pé do roteiro errou para os dois lutadores. Não
comprovado: outros originais, lado do P2, cancelamentos com acerto._

_**Ablação.** Sem o proxy de adversário a divergência surgiu no quadro 6.239;
sem as entradas das listas de comandos, em 6.341 (frente + B). A entrada do
diretório de proximidade e as três entradas de tabelas de ponteiros não fizeram
diferença neste teste em luta; `$B8250` fica no caminho da criação._

_**Ferramentas.** `wire_slot_lookups.py` aplica 1–3 com verificações; na
candidata real sua saída é igual à imagem testada fora das partes só de
diagnóstico (4 e 5). `relocate_frames.py` agora recusa uma cópia que alcance a
janela do PVC, então o pipeline atual do ensaio para ali até a decisão sobre
onde ficam os quadros._

_**Decisões do dono necessárias:** onde ficam os dados de quadros importados (o
banco de quadros não tem espaço) e como os originais leem dados por adversário
para IDs importados._

### 2026-11-18 — Owner decisions: frame bank and opponent proxy

**Frames.** Imported fighters' frame data will live in another ROM bank selected
per ID: research first how to make every frame reader use a different bank for
IDs `$30` and above, since about 4 MB of banked space is free. Growing the
program in the native player and skipping the clone's frame copy were not
chosen.

**Per-opponent data.** Original fighters will read an imported fighter's
per-opponent rows through a proxy table: one byte per imported ID naming the
original fighter whose rows are used. For the Kyo rehearsal the proxy is Kyo
(`$1E`); Guile's proxy is chosen later. Extending every original's tables was
not chosen.

_PT-BR — Decisões do dono: banco de quadros e proxy de adversário._

_**Quadros.** Os dados de quadros dos importados ficarão em outro banco da ROM
selecionado por ID: primeiro pesquisar como fazer todo leitor de quadros usar um
banco diferente para IDs `$30` em diante, já que há cerca de 4 MB livres em
bancos. Ampliar o programa no player nativo e dispensar a cópia de quadros do
clone não foram escolhidos._

_**Dados por adversário.** Os originais lerão as linhas por adversário de um
importado por uma tabela de proxy: um byte por ID importado indicando o
lutador original cujas linhas são usadas. No ensaio do Kyo o proxy é o próprio
Kyo (`$1E`); o do Guile será escolhido depois. Estender as tabelas de todos os
originais não foi escolhido._

### 2026-11-18 — Owner's manual check and resolution

The owner played a native build of the corrected diagnostic candidate (all
causes 1–5 applied, including the diagnostic proxy and frame placement) through
`private/work/first-import/manual/Jogar-Candidato.cmd`. He reported that the
`$30` clone now behaves exactly like Kyo in all normal and special moves. A
headless check of the same executable matched the interpreter results: the
traced clone state equalled original Kyo for 1,070 in-fight frames and the whole
intro, with 15 interpreted instructions per run. The remaining observed
difference is presentation: no name under the life bars, portraits and icon
(ticket 13).

Resolution: the causes are identified and recorded. Fixes 1–3 are in
`wire_slot_lookups.py`. Fix 4 (opponent proxy) and fix 5 (frame placement)
exist only as diagnostic patches, so they continue in
[15](15-imported-frame-bank.md) and [16](16-imported-opponent-proxy.md), which
also carry the original-roster regression check: the diagnostic candidate
overwrote fighter `$00`'s frames and cannot serve as that check. The third and
fifth criteria move to those tickets. What a new ID touches, the memory limits
and the checking method are consolidated in [slot anatomy](../slot-anatomy.md).

_PT-BR — Teste manual do dono e resolução._

_O dono jogou um build nativo da candidata de diagnóstico corrigida (causas 1–5
aplicadas, incluindo o proxy e a posição de quadros de diagnóstico) pelo
`private/work/first-import/manual/Jogar-Candidato.cmd`. Relatou que o clone
`$30` agora se comporta exatamente como o Kyo em todos os golpes normais e
especiais. Uma conferência sem janela do mesmo executável coincidiu com os
resultados do interpretador: o estado traçado do clone igualou o do Kyo original
em 1.070 quadros de luta e na intro inteira, com 15 instruções interpretadas por
execução. A diferença restante observada é de apresentação: sem nome abaixo das
barras de vida, retratos e ícone (ticket 13)._

_Resolução: as causas estão identificadas e registradas. As correções 1–3 estão
no `wire_slot_lookups.py`. A correção 4 (proxy de adversário) e a 5 (posição dos
quadros) existem só como remendos de diagnóstico e continuam nos
[tickets 15](15-imported-frame-bank.md) e [16](16-imported-opponent-proxy.md),
que também levam a conferência de regressão do elenco original: a candidata de
diagnóstico sobrescreveu os quadros do lutador `$00` e não serve para essa
conferência. O terceiro e o quinto critérios passam para esses tickets. O que um novo ID
afeta, os limites de memória e o método de conferência estão consolidados em
[anatomia da vaga](../slot-anatomy.md)._

### 2026-11-19 — Fight divergence found while closing ticket 13

With `$30` as the other player's fighter, the first seconds of the fight differ
from the reference ROM (4,789 px at frame 6,100 on the ticket 13 script; the
opponent and the background animate differently). The same script without the
presentation map gives 4,922 px, so it is not caused by it. The player 1 side
differs only by the Rehearsal clone's intended palette change (1,408 px, largest
channel difference 24). Treat the other-side divergence as part of this ticket's
cause search. See [13](13-rehearsal-selection-presentation.md).

_PT-BR: com o `$30` como lutador do outro jogador, os primeiros segundos da luta
diferem da ROM de referência (4.789 px no quadro 6.100 do roteiro do ticket 13;
adversário e cenário animam diferente). O mesmo roteiro sem o mapa de
apresentação dá 4.922 px, então não é causado por ele. O lado do jogador 1 só
difere pela mudança de paleta pretendida do clone (1.408 px, maior diferença de
canal 24). Tratar a divergência do outro lado como parte da busca de causa deste
ticket. Ver [13](13-rehearsal-selection-presentation.md)._
