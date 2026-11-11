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

## Comments

- 2026-11-11 (agent, before the ticket was claimed): the owner placed three MAME-format zips in `private/`: `bios/neogeo.zip`, `dumps/kof2003/kof2003.zip`, `dumps/svc/svc.zip` (not one file per chip). MAME 0.289 `-verifyroms` reports `kof2003` ("The King of Fighters 2003 (NGM-2710, Export)"), `svc` and `neogeo` as **good**. Still to do in this ticket: confirm with the owner whether these zips are his own cartridge dumps or a pre-existing romset, and record per-chip hashes. MAME is unpacked at `C:\Users\Admin\MAME` (outside the repo).
  _PT-BR: o dono colocou três zips no formato do MAME em `private/`. O MAME 0.289 diz que `kof2003` (Export), `svc` e `neogeo` estão bons. Falta confirmar se os zips são dumps dos cartuchos dele ou um romset que já existia, e registrar os hashes por chip._
