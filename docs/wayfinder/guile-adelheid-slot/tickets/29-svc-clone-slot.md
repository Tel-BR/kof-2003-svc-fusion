---
id: 29
title: "Clone a fighter into a new SVC Chaos slot"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: []
research:
---

## Question

Would cloning a fighter into a new SVC Chaos slot, as the Kyo Rehearsal did in
KOF 2003, teach how to export a fighter from SVC?

_PT-BR: clonar um lutador num slot novo do SVC Chaos, como o Ensaio com o Kyo no
KOF 2003, ensinaria a exportar um lutador do SVC?_

## Resolution

Out of scope (owner, 2026-11-18). A clone in SVC tests how SVC **receives** a
fighter, which belongs to the later Versus direction, not to exporting Guile,
whose data already sits in his own slot. It would also need a modifiable SVC:
there is no native SVC player and MAME expects the encrypted cartridge. The
completeness the clone gave in KOF 2003 is sought instead with
[Inventory everything SVC reads by Guile's fighter ID](28-guile-svc-reader-inventory.md).

_PT-BR: fora de escopo (dono, 18/11/2026). Um clone no SVC testa como o SVC
**recebe** um lutador, o que pertence à direção futura do Versus, não à
exportação do Guile, cujos dados já estão no slot dele. Também exigiria um SVC
modificável: não há player nativo do SVC e o MAME exige o cartucho criptografado.
A completude que o clone trouxe no KOF 2003 será buscada pelo ticket 28._
