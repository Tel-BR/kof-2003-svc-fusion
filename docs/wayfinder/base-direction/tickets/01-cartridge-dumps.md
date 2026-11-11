---
id: 01
title: "Dump the cartridges"
label: wayfinder:task
mode: HITL
status: open
assignee:
blocked_by: []
research:
---

## Question

Which MAME sets (kof2003 / svc and their variants) do the dumps of the owner's cartridges match? Record the hash of every chip and where the files are kept, outside the repository.

_PT-BR: os dumps dos meus cartuchos batem com quais conjuntos do MAME (kof2003 / svc e variantes)? Registrar os hashes por chip e onde os arquivos ficam, fora do repositório._

## Notes

- Done with the owner: he owns the MVS cartridges and an MVS cartridge dumper. Use `wizard` for the steps only he can do.
- Expected location: `private/dumps/kof2003/` and `private/dumps/svc/` (git-ignored). BIOS in `private/bios/`.
- Hashes (CRC32 + SHA-1) are fine in this ticket; file contents are not.

_PT-BR: feito com o dono, que tem os cartuchos MVS e o dumper. Local esperado: `private/dumps/kof2003/` e `private/dumps/svc/` (ignorados pelo git); BIOS em `private/bios/`. Hashes (CRC32 + SHA-1) podem constar aqui; conteúdo dos arquivos não._
