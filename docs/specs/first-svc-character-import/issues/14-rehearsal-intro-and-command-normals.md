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
