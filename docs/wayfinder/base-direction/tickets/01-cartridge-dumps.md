---
id: 01
title: "Dump the cartridges"
label: wayfinder:task
mode: HITL
status: closed
assignee: Mauricio Faganelo (owner; agent session)
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

## Resolution

**Answer.** The working dumps for this project are the three MAME-format zips already in `private/`. The owner owns the original MVS cartridges of both games and, on 2026-11-11, accepted these zips as his dumps for the work. A fresh read of the cartridges with the dumper was **not** performed and is not needed to reach this map's destination. MAME 0.289 (`C:\Users\Admin\MAME`, outside the repo) `-verifyroms` reports all three as **good**, so they match these MAME sets exactly:

| Game | MAME set | MAME description | File (git-ignored) | Zip SHA-1 |
|---|---|---|---|---|
| KOF 2003 | `kof2003` (parent) | The King of Fighters 2003 (NGM-2710, Export) | `private/dumps/kof2003/kof2003.zip` | `c72c0462885a2822bb2ad2de2bf3d1d69945303b` |
| SVC Chaos | `svc` (parent) | SNK vs. Capcom - SVC Chaos (NGM-2690 ~ NGH-2690) | `private/dumps/svc/svc.zip` | `4741c42cb0b617faa05597f8b7aaa2a4ab08272f` |
| BIOS | `neogeo` | Neo-Geo MV-6F | `private/bios/neogeo.zip` | `deb62b0074b8cae4f162c257662136733cfc76ad` |

Provenance facts, for later tickets: every zip entry carries the TorrentZip timestamp (1996-12-24 23:32) and the game zips date from 2016, so these are a curated romset rather than raw dumper output; the chip names and sizes are MAME's. Later tickets ("Decrypt with existing tools", "Run the KOF 2003 port with my dumps") should treat these hashes as the reference.

**Per-chip hashes, `kof2003`** (size in bytes, CRC32, SHA-1):

| Chip | Size | CRC32 | SHA-1 |
|---|---|---|---|
| 271-p1c.p1 | 4194304 | 530ecc14 | 812cf7e9902af3f5e9e330b7c05c2171b139ad2b |
| 271-p2c.p2 | 4194304 | fd568da9 | 46364906a1e81dc251117e91a1a7b43af1373ada |
| 271-p3c.p3 | 1048576 | aec5b4a9 | 74087f785590eda5898ce146029818f86ced42b6 |
| 271-m1c.m1 | 524288 | f5515629 | 7516bf1b0207a3c8d41dc30c478f8d8b1f71304b |
| 271-v1c.v1 | 8388608 | ffa3f8c7 | 7cf4a933973ca23b7f87c81151d8659e6ec4bd20 |
| 271-v2c.v2 | 8388608 | 5382c7d1 | 1bf999705eda80ba1e7b0d6bdd010d9bfb18bd76 |
| 271-c1c.c1 | 8388608 | b1dc25d0 | 50adc3c60d5b4b3abd10a49db2267306c6dbd772 |
| 271-c2c.c2 | 8388608 | d5362437 | 66db36522dc09106388c707252df9fe1c88b4856 |
| 271-c3c.c3 | 8388608 | 0a1fbeab | 9fe30d36ba98d00fda010832ff2f27783dd577c1 |
| 271-c4c.c4 | 8388608 | 87b19a0c | b72a8e7d9124ce859b5149bb4381ba481c161ea5 |
| 271-c5c.c5 | 8388608 | 704ea371 | e75b80422f0d72eac826f8ffadf79efeccaab124 |
| 271-c6c.c6 | 8388608 | 20a1164c | c9843b37612a16fc95f6851793b1cfb5d49d811d |
| 271-c7c.c7 | 8388608 | 189aba7f | 7152195a57ad36b28290810fe87ed8c206262ba9 |
| 271-c8c.c8 | 8388608 | 20ec4fdc | deb5f7ec5a090e419b9d1a6a74877bee081198e2 |

**Per-chip hashes, `svc`:**

| Chip | Size | CRC32 | SHA-1 |
|---|---|---|---|
| 269-p1.p1 | 4194304 | 38e2005e | 1b902905916a30969282f1399a756e32ff069097 |
| 269-p2.p2 | 4194304 | 6d13797c | 3cb71a95cea6b006b44cac0f547df88aec0007b7 |
| 269-m1.m1 | 524288 | f6819d00 | d3bbe09df502464f104e53501708ac6e2c1832c6 |
| 269-v1.v1 | 8388608 | c659b34c | 1931e8111ef43946f68699f8707334c96f753a1e |
| 269-v2.v2 | 8388608 | dd903835 | e58d38950a7a8697bb22a1cc7a371ae6664ae8f9 |
| 269-c1r.c1 | 8388608 | 887b4068 | 227cdcf7a10a415f1e3afe7ae97acc9afc2cc8e1 |
| 269-c2r.c2 | 8388608 | 4e8903e4 | 31daaa4fd6c23e8f0a8428931c513d97d2eee1bd |
| 269-c3r.c3 | 8388608 | 7d9c55b0 | 1f94a948b3e3c31b3ff05518ef525031a3cb2c62 |
| 269-c4r.c4 | 8388608 | 8acb5bb6 | 2c27d6e309646d7b84da85f78c06e4aaa74e844b |
| 269-c5r.c5 | 8388608 | 097a4157 | 54d839f55d27f68c704a94ea3c63c644ffc22ca4 |
| 269-c6r.c6 | 8388608 | e19df344 | 20448add53ab25dd3a8f0b681131ad3b9c68acc9 |
| 269-c7r.c7 | 8388608 | d8f0340b | 43114af7557361a8903bb8cf8553f602946a9220 |
| 269-c8r.c8 | 8388608 | 2570b71b | 99266e1c2ffcf324793fb5c55325fbc7e6265ac0 |

**`neogeo` BIOS** (34 entries; the ones a default MVS boot uses, plus Unibios as an option):

| Chip | Size | CRC32 | SHA-1 |
|---|---|---|---|
| sp-s2.sp1 (BIOS `euro`, "Europe MVS (Ver. 2)", first in MAME's list and used when no `-bios` is given) | 131072 | 9036d879 | 4f5ed7105b7128794654ce82b51723e16e389543 |
| sm1.sm1 | 131072 | 94416d67 | 42f9d7ddd6c0931fd64226a60dc73602b2819dcf |
| sfix.sfix | 131072 | c2ea0cfd | fd4a618cdcdbf849374f0a50dd8efe9dbab706c3 |
| 000-lo.lo | 131072 | 5a86cff2 | 5992277debadeb64d1c1c64b0a92d9293eaf7e4a |
| uni-bios_4_0.rom | 131072 | a7aab458 | 938a0bda7d9a357240718c2cec319878d36b8f72 |

The other 29 BIOS variants are listed by MAME's `neogeo` set; recompute with any CRC/SHA-1 tool if a later ticket needs one.

_PT-BR: **Resposta.** Os dumps de trabalho do projeto são os três zips no formato do MAME já em `private/`. O dono tem os cartuchos MVS originais dos dois jogos e, em 11/11/2026, aceitou esses zips como seus dumps para o trabalho. Não foi feita leitura nova dos cartuchos com o dumper, e ela não é necessária para chegar ao destino deste mapa. O MAME 0.289 confirma os três como bons: `kof2003` (Export, NGM-2710), `svc` e o BIOS `neogeo`. Fatos de origem: as entradas dos zips têm a data do TorrentZip (24/12/1996) e os zips dos jogos são de 2016, ou seja, é um romset organizado, não a saída crua do dumper. Os hashes acima (por chip e por zip) passam a ser a referência para os tickets de descriptografia e do port do KOF 2003._
