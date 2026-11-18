---
title: "Repair the Kyo rehearsal selection presentation"
triage: ready-for-agent
---

# 13 Repair the Kyo rehearsal selection presentation

[Parent specification](../spec.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

Make the provisional `$30` Kyo rehearsal identify itself consistently in the
selection flow. In the owner's manual test, its name, small thumbnail, large
portrait and team position were missing or corrupted; some displayed material
belonged to Jhun. Reuse the Kyo original's presentation for this rehearsal where
appropriate and preserve all original fighters' selection entries. Do not treat
this as Guile's later portrait, icon or palette acceptance.

## Acceptance criteria

- [ ] Reproduce and record which selection and order-selection components fail
  for `$30`, including team positions 1, 2 and 3.
- [ ] Show the intended Kyo name, small and large images, and team position for
  the clone without changing the original Kyo or Jhun entries.
- [ ] Check original Kyo and `$30` selected together on the same team and check
  the other player side where the same presentation path is used.
- [ ] Keep game-derived art, captures and logs in `private/`; record only
  addresses, counts, hashes and observations in tracked files.

## Português (Brasil)

# 13 Corrigir a apresentação do Kyo do ensaio na seleção

Fazer o Kyo provisório `$30` identificar-se de forma consistente na seleção.
No teste manual do dono, nome, miniatura, retrato grande e posição de equipe
faltaram ou apareceram corrompidos; parte do material exibido era do Jhun.
Reaproveitar a apresentação do Kyo original neste ensaio quando adequado e
preservar as entradas de todos os lutadores originais. Isso não aprova o
retrato, o ícone nem as paletas que serão preparados depois para o Guile.

### Critérios de aceitação

- [ ] Reproduzir e registrar quais componentes da seleção e da escolha de ordem
  falham para `$30`, inclusive nas posições 1, 2 e 3 da equipe.
- [ ] Mostrar nome, imagem pequena, imagem grande e posição de equipe esperados
  para o clone, sem mudar as entradas originais do Kyo ou do Jhun.
- [ ] Conferir Kyo original e `$30` juntos na mesma equipe e o outro lado do
  jogador quando usar o mesmo caminho de apresentação.
- [ ] Manter artes derivadas do jogo, capturas e logs em `private/`; registrar
  nos arquivos rastreados somente endereços, contagens, hashes e observações.

## Comments

### 2026-11-18 — Owner decision: extend the tables, do not polish the art

Under the owner's "no unexplained difference" bar for the Rehearsal (see
[14](14-rehearsal-intro-and-command-normals.md)), the goal here is that `$30`
reads its own entries in every selection and order-selection table instead of
falling into a neighbour such as Jhun. Pointing those entries at Kyo's existing
presentation is enough; art quality for the clone is not a goal. The tables
found here are the map phase 4 will fill with Guile's presentation.

_PT-BR: pelo critério do dono de "nenhuma diferença inexplicada" para o Ensaio
(ver [14](14-rehearsal-intro-and-command-normals.md)), o objetivo aqui é o `$30`
ler as próprias entradas em todas as tabelas da seleção e da escolha de ordem,
em vez de cair num vizinho como o Jhun. Apontar essas entradas para a
apresentação existente do Kyo basta; a qualidade da arte do clone não é
objetivo. As tabelas encontradas aqui são o mapa que a fase 4 preencherá com a
apresentação do Guile._
