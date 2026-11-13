---
id: 09
title: "Run the KOF 2003 port with my dumps"
label: wayfinder:task
mode: HITL
status: closed
assignee: codex
blocked_by: [01]
research:
---

## Question

Does the existing KOF 2003 port run and pass `--verify` with the owner's dumps? Record the version used and the result.

_PT-BR: o port existente do KOF 2003 roda e passa no `--verify` com os meus dumps? Registrar a versão usada e o resultado._

## Notes

Local use only: the port is PolyForm Noncommercial and none of its code enters this repository. Clone it outside the repository or under `private/`.

_PT-BR: só uso local; o port é PolyForm Noncommercial e nada do código dele entra no repositório. Clonar fora do repositório ou dentro de `private/`._

## Resolution

With the owner's dumps, the Windows port `v0.1.0` ran 6,000 frames in native MVS mode. The `--verify` run reported zero state divergences and 2,669 cycle differences. The Universe BIOS 4.0 test reported 34,787 divergences. Validation of Single mode in the port remains pending.

_PT-BR: com os dumps do dono do repositório, o port Windows `v0.1.0` rodou 6.000 quadros em modo nativo no MVS. O `--verify` registrou zero divergências de estado e 2.669 diferenças de ciclos. O teste com Universe BIOS 4.0 registrou 34.787 divergências. A validação do modo Single no port segue pendente._
