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

- [ ] Reproduce the reported starting-frame and forward + B differences with
  known inputs, recording setup and observations separately.
- [ ] Compare clone and original at the same meaningful action and game state;
  account for facing, spacing, intro timing and opponent behaviour.
- [ ] Identify whether each cause is shared slot infrastructure or rehearsal
  presentation; fix the shared cause required by the first import and record
  any clone-only work separately.
- [ ] Record the observed grab and cancel discrepancies and determine whether
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

- [ ] Reproduzir as diferenças do quadro inicial e de frente + B com entradas
  conhecidas, registrando preparação e observações separadamente.
- [ ] Comparar clone e original na mesma ação e no mesmo estado significativo,
  considerando lado, distância, tempo da intro e comportamento do adversário.
- [ ] Identificar se cada causa pertence à infraestrutura compartilhada ou à
  apresentação do ensaio; corrigir a causa compartilhada necessária à primeira
  importação e registrar trabalho exclusivo do clone separadamente.
- [ ] Registrar as diferenças observadas em agarrões e cancelamentos e decidir
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
