---
title: "Give imported fighters their source fighter's hit-box kind set"
triage: ready-for-agent
---

# 20 Give imported fighters their source fighter's hit-box kind set

[Parent specification](../spec.md) · [Found in ticket 16](16-imported-opponent-proxy.md) · [Slot anatomy](../slot-anatomy.md)

## What to build

The collision routine reads, at `$15D08` and `$169CA`, a 64-entry table of pointers at
`$6C62E` by the box owner's ID (`4 × (ID & $3F)`). Each pointer leads to a 16-byte bit
set of hit-box kinds that decides how that fighter's boxes are classified. Entries
above `$24` share one pointer, the set of fighter `$24`. So the imported `$30` uses a
set that differs from original Kyo's in 2 bits. The read with `$30` was observed in the
ticket 13 route (frames 5,400–6,100); no visible difference was found there, so the
moves that depend on those 2 bits are not known yet.

Give `$30` its source fighter's entry with a checked tool step, following the
"64-entry tables whose entries above `$24` share a default" row of the slot anatomy
(`wire_slot_lookups.py` already handles that kind).

## Acceptance criteria

- [ ] A preparation step writes `$30`'s entry from its source fighter, with byte checks
  and tests on invented data; original entries are unchanged.
- [ ] The private pair check of ticket 16 reports the `$15D1A` read with the same bytes
  as Kyo's in the ticket 13 window.
- [ ] Original fighters facing originals are unchanged in a regression check, and the
  native build reports no new fallback.

## Português (Brasil)

# 20 Dar aos lutadores importados o conjunto de tipos de caixa do lutador de origem

_A rotina de colisão lê, em `$15D08` e `$169CA`, uma tabela de 64 ponteiros em `$6C62E`
pelo ID do dono da caixa. Cada ponteiro leva a um conjunto de 16 bytes de tipos de caixa
de golpe. As entradas acima de `$24` compartilham um ponteiro, o conjunto do lutador `$24`;
assim o `$30` importado usa um conjunto que difere do Kyo original em 2 bits. A leitura com
o `$30` foi observada no roteiro do ticket 13; nenhuma diferença visível apareceu, então
ainda não se sabe que golpes dependem desses 2 bits. Dar ao `$30` a entrada do lutador de
origem num passo de ferramenta verificado, como na linha "tabelas de 64 entradas com padrão
compartilhado acima de `$24`" da anatomia do slot._

### Critérios de aceitação

- [ ] Um passo de preparo grava a entrada do `$30` a partir do lutador de origem, com
  conferência de bytes e testes com dados inventados; as entradas originais não mudam.
- [ ] A conferência privada de pares do ticket 16 mostra a leitura em `$15D1A` com os mesmos
  bytes do Kyo na janela do ticket 13.
- [ ] Originais contra originais ficam inalterados numa conferência de regressão e o build
  nativo não mostra novo fallback.
