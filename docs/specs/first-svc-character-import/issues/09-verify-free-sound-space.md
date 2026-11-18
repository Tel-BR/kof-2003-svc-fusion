---
title: "Verify the free V tail and the M1 room for imported sounds"
triage: ready-for-agent
assignee: codex
---

# 09 Verify the free V tail and the M1 room for imported sounds

[Parent specification](../spec.md)

## What to build

Prove, by reading only, that native KOF 2003 can take new samples for an Imported Character through its original sound route, as decided in [wayfinder ticket 27](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md). The free tail of the sample region (16,384 bytes at the end) must be unused by every reader. The M1 sound program must have room and valid indices for the new entries. The result is a short note and a go or stop decision. On stop, work returns to the owner with the options and their costs; the native separate audio path is not built on its own.

## Blocked by

None (can start immediately)

## Acceptance criteria

- [x] The note lists every code path that writes the chip's sample page registers and shows that none can reach the free tail, or names the ones that can.
- [x] The note shows where two new descriptors fit in the M1 program, which sound group and index they use, and what the packed validity map of that group requires.
- [x] The note gives the exact tail placement for the two Guile voices (1,792 and 2,048 bytes, 3,840 in total) and the space left.
- [x] The note ends in a go or stop decision. Nothing in it carries game bytes, only addresses, sizes, counts and hashes, and nothing under `private/` is added to git.

## Português (Brasil)

Provar, só por leitura, que o KOF 2003 nativo aceita amostras novas de um Personagem Importado pela rota original de som, como decidido no [ticket 27 do wayfinder](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md). A faixa livre no fim da região de amostras (16.384 bytes) precisa estar fora do alcance de qualquer leitor. O programa de som M1 precisa ter espaço e índices válidos para as entradas novas. O resultado é uma nota curta e uma decisão de seguir ou parar. Se for parar, o trabalho volta ao dono com as opções e seus custos, e o caminho nativo separado de áudio não é construído por conta própria.

### Bloqueios

Nenhum (pode começar já)

### Critérios de aceitação

- [x] A nota lista todo caminho de código que escreve os registradores de página de amostras do chip e mostra que nenhum alcança a faixa livre, ou nomeia os que alcançam.
- [x] A nota mostra onde cabem dois descritores novos no programa M1, qual grupo de som e qual índice eles usam e o que o mapa compactado de validade desse grupo exige.
- [x] A nota dá a colocação exata na faixa das duas vozes do Guile (1.792 e 2.048 bytes, 3.840 no total) e o espaço que sobra.
- [x] A nota termina com a decisão de seguir ou parar. Nada nela carrega bytes dos jogos, só endereços, tamanhos, contagens e hashes, e nada de `private/` entra no git.

## Resolution / Resolução

The read-only verification passed and the result is **Go**. The page-register paths, V-tail boundary, two group-1 descriptor slots, validity-map requirement and exact placement are recorded in [Imported-sound space verification](../sound-space-verification.md). No item under `private/` was added.

A verificação somente de leitura passou e o resultado é **Seguir**. Os caminhos dos registradores de página, o limite da cauda V, os dois slots de descritor do grupo 1, a exigência do mapa de validade e a colocação exata estão registrados em [Verificação de espaço para sons importados](../sound-space-verification.md). Nenhum item de `private/` foi adicionado.
