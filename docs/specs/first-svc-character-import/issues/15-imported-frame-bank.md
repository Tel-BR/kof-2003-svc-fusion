---
title: "Place imported frame data in a per-ID frame bank"
triage: ready-for-agent
---

# 15 Place imported frame data in a per-ID frame bank

[Parent specification](../spec.md) · [Diagnosis](14-rehearsal-intro-and-command-normals.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

All fighter frame directories live in one program bank, whose top 8 KiB is
covered by the NEO-PVC RAM window at `$2FE000`; only about 12 KiB is free below
it, less than Kyo's 18 KiB directory. By the owner's decision, frame data for IDs
`$30` and above lives in another bank selected per ID. Find every reader of
frame data (the lookup at `$010AF8`–`$010B42` and later reads through the frame
pointer at object `+$60`), make them select the right bank for imported IDs, and
place the clone's frame copy there with its tiles in the Added Space.

## Acceptance criteria

- [ ] List every routine that reads frame directories or frame bodies, with how
  it selects the bank; record any reader that assumes the current bank.
- [ ] The preparation tooling places the `$30` frame copy outside the frame bank
  and the PVC window, and refuses unchecked placements.
- [ ] In the differential loop, the clone's frozen pre-intro frame, intro and
  in-fight trace equal original Kyo's; the native build reports no new fallback.
- [ ] Original fighters are unchanged: no original frame directory is
  overwritten, and a regression check covers originals beyond Kyo, including
  `$00`.

## Português (Brasil)

# 15 Colocar os quadros dos importados num banco de quadros por ID

_Todos os diretórios de quadros ficam num único banco do programa, cujos 8 KiB
finais são cobertos pela janela de RAM do NEO-PVC em `$2FE000`; só cerca de
12 KiB estão livres abaixo dela, menos que os 18 KiB do diretório do Kyo. Por
decisão do dono, os quadros dos IDs `$30` em diante ficam em outro banco,
escolhido por ID. Achar todo leitor de dados de quadro (a busca em
`$010AF8`–`$010B42` e as leituras posteriores pelo ponteiro de quadro em
`+$60` do objeto), fazê-los escolher o banco certo para IDs importados e
colocar ali a cópia de quadros do clone, com os tiles no Espaço acrescentado._

### Critérios de aceitação

- [ ] Listar toda rotina que lê diretórios ou corpos de quadro e como ela
  escolhe o banco; registrar qualquer leitor que suponha o banco atual.
- [ ] As ferramentas de preparo colocam a cópia de quadros do `$30` fora do
  banco de quadros e da janela do PVC e recusam posições não verificadas.
- [ ] No ciclo diferencial, o quadro congelado antes da intro, a intro e o trace
  em luta do clone igualam os do Kyo original; o build nativo não mostra novo
  fallback.
- [ ] Os originais ficam inalterados: nenhum diretório original é sobrescrito, e
  uma conferência de regressão cobre originais além do Kyo, inclusive o `$00`.
