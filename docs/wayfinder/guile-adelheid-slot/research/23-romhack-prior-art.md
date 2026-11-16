# Research 23: What documented ROM hacks learned about adding fighters and growing graphics

Ticket: [23](../tickets/23-romhack-prior-art.md) · Map: [guile-adelheid-slot](../map.md)

No game data here (AGENTS.md hard rule): only names, sizes, counts, tile numbers and addresses. Nothing was downloaded except public source files and web pages (MAME and FBNeo driver sources, read as text); no ROM, patch or modified ROM was downloaded, and nothing was run. Research date: 2026-11-16. Sources are numbered S1 to S13 at the end.

## Resumo (PT-BR)

- Não achei nenhuma documentação publicada dos autores de hacks sobre IDs livres, tamanho de tabelas, tela de seleção, paletas ou sons para o KOF 2002, o KOF 2003 ou o SVC Chaos. O que existe são listas de arquivos (tamanhos de ROM) nos drivers do FBNeo e do MAME, o texto do Neo Geo Dev Wiki e páginas de catálogo. Quase tudo abaixo é inferência a partir de tamanhos de arquivos.
- O que muda decisão: (1) o formato de hardware aceita tiles de 20 bits, ou seja, 128 MiB, e mais que isso só com troca de banco; os 128 MiB do ticket 19 são o teto, e cobrem com folga os 26 exclusivos (conta aproximada). (2) Há hacks de KOF 2002 (dois), KOF 2001 (dois) e KOF 98/99 com 80 a 112 MiB de gráficos, acrescentados como pares de chips de 16 MiB logo depois dos 64 MiB originais, ou seja, tiles a partir de `$80000`, mas só em emulador; nenhum hack documentado de KOF 2003 ou SVC passa de 64 MiB. (3) O carregador do FBNeo completa o conjunto até a próxima potência de 2 e marca o resto como transparente, o que confirma o risco já visto na pesquisa 24. (4) Hacks do KOF 2003 que "liberam" lutadores ocultos mantêm o tamanho do programa e dos gráficos originais; nenhum hack documentado cria ID novo acima de `$24`.
- Nada achado que mude os tickets 08 e 22 de forma firme; há uma pista sobre os bytes `$107D64`/`$107D66` do ticket 22 (a luta final depende de como o Kusanagi é derrotado).
- Tudo é *não verificado* (nada foi medido no MAME nem no port).

## Evidence labels and method

- **[U]** unverified: published web source, with its URL (S-number). Nothing from the web is verified until measured in MAME or in the port.
- **[I]** inference drawn from [U] facts; also unverified.
- **[N]** not found: I looked and found nothing; said plainly.
- Method: web search; MAME `neogeo.cpp`, `neopcb.cpp`, `slot.cpp` and FBNeo `d_neogeo.cpp`, `neo_run.cpp`, `neo_sprite.cpp` read as text (master branch, 2026-11-16; line numbers are approximate and will drift); Neo Geo Dev Wiki pages; catalog pages. File sizes in section 19 were added up by a script over the FBNeo ROM lists (chip count times 8 MiB).
- Third-party caution: S9 (a community README about 27 hack sets) is not by the hack authors; I use it only for the physical-board limit it states.

## What I looked for and did not find

- **[N]** Any published hack-author document (readme, forum thread, wiki) for a KOF 2002 hack that adds King and Geese. The only candidate is the FBNeo entry `kf2k2ps2re`, "PlayStation 2 Plus 2025 ver 1.0, Hack", credited to GSC2007 and Dream (S3). Its title suggests PS2 content, but FBNeo lists files only; I did not find which fighters it adds or how.
- **[N]** Any hack that adds a fighter to KOF 2003 or SVC Chaos as a new ID. For KOF 2003 I found only a hack that makes "secret characters" available (S3) and "Plus"/PS2 hacks whose file sizes equal the original. For SVC Chaos I found only unlock hacks (S7).
- **[N]** Any documentation of free fighter IDs, table sizes, `$24`-style guards, the number of selection cells, palettes or frame and collision formats in any hack. General web searches (including Reddit, Romhacking.net and Neo Geo forum terms) returned catalog and wiki pages only. No Assembler Games or EmuDev thread surfaced. Three pages that might have helped could not be read: a MiSTer forum thread on running a KOF 2002 hack (https://misterfpga.org/viewtopic.php?p=94525, failed to load), a MAME cheat forum thread on `kf2k2ps2` player select (https://www.mamecheat.co.uk/forums/viewtopic.php?t=3716, failed to load) and the zengfr/romhack repository on GitHub (blocked for automated fetch; it also hosts hack patches, which this ticket forbids downloading).
- **[N]** Any hack of KOF 2003 or SVC Chaos above 64 MiB of graphics, in MAME or FBNeo.
- Premise check: the owner names King and Geese as PS2-only in KOF 2002. The FightersGeneration page tags both as PS2 additions (S11); The Cutting Room Floor says King is also in the Dreamcast and Xbox versions (S12). Not decision-relevant.

## Ticket 19: growing the graphics set to 128 MiB

1. **[U] 128 MiB is the ceiling of the game's own tile numbers.** The sprite tile number is 20 bits (16 low bits in one word, 4 high bits in the next), so 1,048,576 tiles of 128 bytes = 128 MiB; more graphics need bankswitching (S1; "Max sprite tileset: 128 MiB" in S2). Holds for KOF 2003, KOF 2002 and every Neo Geo game (hardware). *Effect on 19:* record 128 MiB as the last stop; a fourth step would need a scheme the game code does not have. **[I]** Capacity: the added 64 MiB is 524,288 tiles; at about 9,100 tiles per fighter (Guile's SVC block, ticket 19) that is about 57 blocks, against 26 x 9,100 = 236,600 tiles for all Exclusive Characters. Per-fighter sizes vary; ticket 21 measures Guile's.
2. **[U] Documented hack sets above 64 MiB exist, only on other KOF engines, only in emulator.** FBNeo's driver lists these sets (S3), sizes counted as chips of 8 MiB: KOF 2002 "Mugen" `kof2002m` (2023) 80 MiB; KOF 2002 `kf2k2ps2re` (2025) 80 MiB; KOF 2001 "PS2 Krizalid" `kf2k1pkz` (2021) 80 MiB; KOF 2001 "All Boss Plus" `kf2k1ult` (2026) 112 MiB (14 chips, two of them named after KOF 2002 chips); KOF '98 and '99 sets 80 to 96 MiB. Every KOF 2003 and SVC Chaos hack or bootleg in MAME (S4) and FBNeo (S3) keeps 8 chips of 8 MiB = 64 MiB. **Holds for:** KOF 2002, 2001, '98, '99; **not documented for KOF 2003 or SVC.** *Effect on 19:* growth past 64 MiB has precedent on sister engines, so the idea is sound, but KOF 2003 would be first of its kind, which agrees with research 24 ("none found") and with 19's decision to make the first native draw of a tile at `$80000` or above part of Guile's slice.
3. **[I] Added tiles start at `$80000`.** In those lists the extra chips come right after the original eight (c9, c10 and up), so their tiles begin at tile `$80000` (64 MiB / 128 bytes) and the 80 MiB sets end at `$9FFFF`. This is the same range 19 plans for Guile. Whether each engine's own program accepted such tile numbers unchanged is **[N]** in the hack documentation.
4. **[U] Chips are added in pairs of 16 MiB, and non-power-of-two totals are padded by the loader.** FBNeo's loader grows the sprite set in steps of two 8 MiB chips for hack patches (S5), sizes its tile mask to the next power of two of the total, allocates the whole masked range and marks every tile beyond the loaded data as transparent, so an 80 MiB or 112 MiB set loads with a 128 MiB mask (S5, S6). MAME computes its mask the same way (S4b). Holds for any game on those loaders (KOF 2002, 2001, '98, '99; KOF 2003 would behave the same). *Effect on 19:* matches "add or enlarge C-file pairs" and confirms research 24's hazard: if the new total is not a power of two, pad the decoded buffer or size the set to exactly 128 MiB.

Not changing 19 but checked: MAME's graphics decryption (CMC code) treats the first 64 MiB of the 96 MB KOF 2003 PCB set specially (S4c), takes the fix-layer data from the tail of the C set (S4c), and FBNeo's comment says the last 16 MB of that PCB set are unused (S5); so retail KOF 2003 graphics are 64 MiB of tiles on every dump this project can meet. In FBNeo the fix-layer data of CMC games is read from the end of the C set, which is why its hack loader subtracts the growth before reading it (S5). The port reads `271-s1.s1` as a separate file (research 24), so growing `crom_size` does not move it; re-running `kof2003_decrypt` after growth is the only place that could still assume the old size (research 24).

## Ticket 06: how fighter slots are found

1. **[N]** No hack documents free fighter IDs, table sizes or guards. Nothing found changes the choice between relocating the 37-entry tables, renumbering object types or widening the ID.
2. **[U] Program size in hacks.** KOF 2002's program is 5 MB; its hacks grow to 8 MB (Magic Plus, 10th Anniversary line) and 9 MB (`kf2k2ps2re`: 1 MB + 5 MB + a 1 MB block mapped by FBNeo at `$900000`, and 2 more MB present in the source but disabled) (S3, S4). The KOF 2003 hacks found show no growth: the original is 9 MB (8 MB + 1 MB, S4); `kof2003t` and `kf2k3ps2` are packaged as one 8 MB part, like the fully decrypted original `kof2k3fd`; `kf2k3p2s` is 4 + 4 + 1 MB, the original layout (S3). **Holds:** growth for KOF 2002 only; for KOF 2003 no documented hack shows enlarged program space. *Effect on 06:* the only precedent for "adding fighters costs program space" is the KOF 2002 PS2 hack; for KOF 2003 the free room is still ticket 03's measured 4.1 MB, and the real constraint is where new code can live (see "Cannot be copied").
3. **[U] One character, several cells.** The KOF 2002 "10th Anniversary" hack redraws the selection grid with smaller portraits and lists several characters more than once, each pickable once (S8). Holds for KOF 2002 only; whether the repeats are separate IDs or data swaps under one ID is **[N]**. *Effect on 06 (second round, SVC versions of shared characters):* shows a KOF 2002-engine hack that offered variants of one character as separate entries; it does not say how.
4. **[U] Boss data may be incomplete.** In the SVC hack that unlocks every boss, Geese's and Zero's sounds are reported missing (S7); TCRF lists unused win quotes for Athena and Red Arremer (S13). Holds for SVC. *Effect on 06 (the 26 Exclusive Characters):* expect gaps in bosses' sound and quote data when counting what can be imported; check per fighter, as ticket 05 did for Guile.

## Ticket 07: reaching Guile in the selection screen

1. **[U] A KOF 2003 hack that makes hidden fighters selectable on MVS.** FBNeo's entry `kf2k3p2s`, "PS2 Style Portraits", carries the note "Secret Characters available in MVS" and has the original program (4 + 4 + 1 MB) and eight C chips (S3). Holds for KOF 2003. *Effect on 07:* releasing the existing hidden IDs (the map's "selectable by default" step) was done by others without growing the program or graphics; how (cell flags, the developer-mode word, a code) is **[N]**, and nothing shows a cell for a new ID above `$24`.
2. **[U] The only documented redrawn grid** is the KOF 2002 10th Anniversary one (smaller portraits, repeated entries, S8). Holds for KOF 2002 only. *Effect on 07:* hack authors replaced the grid art instead of reusing the fixed image, which supports keeping widescreen or a recreated grid as a later option; the cost is **[N]**.
3. **[U] Official codes and boss routes in KOF 2003 (not hacks).** Input sequences exist for Evil Kusanagi and for Chizuru and Maki; Adelheid and Mukai have none and are reached as final bosses (S10). Holds for KOF 2003. Same as research 02 and 22; no change.

## Ticket 08: frames and collision

- **[N]** No hack documentation found at the level of frame, collision or step-script formats. Hack sets are described only by file lists and CRCs. Nothing here changes 08.

## Ticket 22: boss selection rule

1. **[U] Lead for the unmeasured `$107D64` and `$107D66`.** A catalog page says the final boss depends on how mid-boss Kusanagi is beaten: without a Desperation Move on the last hit, Adelheid; with one, Chizuru and Maki and then Mukai (S10); TCRF mentions the hidden Chizuru and Maki fight in 1P mode (S14). Holds for KOF 2003 only. *Effect on 22:* suggests one of the two unmeasured bytes (or the column choice in the `$6B626` table) carries a "how the mid-boss ended" branch; this is a lead to measure, not a finding, and no address-level documentation exists **[N]**.
2. **[N]** No hack documents the early end of selection or lone-fighter play.

## KOF 2003 vs only KOF 2002

| Fact | KOF 2003 (this project) | Only KOF 2002 | Other games |
|---|---|---|---|
| 20-bit tile number, 128 MiB ceiling, more needs banking [U] S1, S2 | Yes (hardware) | Yes | Yes |
| Hack sets above 64 MiB of graphics [U] S3 | None documented | `kof2002m`, `kf2k2ps2re` (80 MiB) | KOF 2001 (80, 112 MiB), KOF '98 and '99 (80 to 96 MiB); none for SVC |
| New chips in 16 MiB pairs, loader pads to power of two [U] S5, S6 | Loader-level; would apply | Used | Used |
| Program grown to 8 to 9 MB, block at `$900000` [U] S3 | Not documented (hacks keep original size) | Yes | not read |
| Selection grid redrawn, characters repeated [U] S8 | Not documented | 10th Anniversary hack | not read |
| "Secret characters available in MVS", portraits redone, sizes unchanged [U] S3 | `kf2k3p2s` | n/a | n/a |
| Bosses unlocked by hack, some sounds missing [U] S7 | n/a | n/a | SVC Plus and Super Plus |
| Final-boss branch depends on last hit on Kusanagi [U] S10 | Yes | n/a | n/a |
| Free IDs, table sizes, palettes, frame formats documented [N] | Not found | Not found | Not found |

## Cannot be copied

These hacks patch the original ROM and run on emulator loaders; this project's limit is the port generator (ticket 04, 19).

1. **Code in other banks or at a mapped block.** The KOF 2002 PS2 hack puts 1 MB at `$900000` through an FBNeo mapping, and hack carts use the whole bank window (S3, S4). The generator decodes only the fixed 1 MB and the first banked MB; code anywhere else runs in the interpreter and is not checked by `--verify` (ticket 04). Relocated tables are data and are read live, so they may sit in free space of the image; any new code that reads them must sit in the fixed MB or the first banked MB.
2. **Growth by adding chips to a ROM set.** In the hacks the loader sizes everything from the file list; here `crom_size` is a fixed descriptor constant, and the 128 MiB step is the descriptor, C-file-pair and tile-cache work already recorded in 19.
3. **Real-board limits.** The 64 MiB window of the decryption chips, the 96 MB KOF 2003 PCB and the cartridge boards that hack builders target (8 chips of 8 MiB = 64 MB, according to S9, third party) do not apply to the port, which reads decrypted prepared files. Their space-saving tricks (dropping empty chips, moving pixels into fewer chips; S9) are not needed with 128 MiB.
4. **Encrypted graphics.** On CMC games a change to one chip scatters through all chips after encryption (S9); the port edits decrypted files in place, so this cost does not exist here. Conversely, the hack route of editing before re-encrypting has no counterpart.
5. **Sounds.** The KOF 2001 PS2 Krizalid set changes the sound program and one voice file while the voice total stays 16 MiB (S3). Not one of the five tickets here; noted for 13.

## Sources

All retrieved 2026-11-16; none verified in this project.

- S1: Neo Geo Dev Wiki, Sprites: https://wiki.neogeodev.org/index.php/Sprites
- S2: Neo Geo Dev Wiki, General specifications: https://wiki.neogeodev.org/index.php/General_specifications
- S3: FBNeo `d_neogeo.cpp` (sets `kof2002m`, `kf2k2ps2re`, `kf2k1pkz`, `kf2k1ult`, `kof2003t`, `kf2k3ps2`, `kf2k3p2s`, `kof2k3br`, `NeoMapExtraRom`): https://raw.githubusercontent.com/finalburnneo/FBNeo/master/src/burn/drv/neogeo/d_neogeo.cpp
- S4: MAME `neogeo.cpp` (KOF 2002, 2003, SVC hack and bootleg ROM lists, bank handlers): https://raw.githubusercontent.com/mamedev/mame/master/src/mame/snk/neogeo.cpp ; S4b: MAME `slot.cpp` (`get_region_mask`, power-of-two mask): https://raw.githubusercontent.com/mamedev/mame/master/src/devices/bus/neogeo/slot.cpp ; S4c: MAME `prot_cmc.cpp` (64 MiB handling for kf2k3pcb, fix data from the end of the C set): https://raw.githubusercontent.com/mamedev/mame/master/src/devices/bus/neogeo/prot_cmc.cpp and `neopcb.cpp` (kf2k3pcb, 96 MB): https://raw.githubusercontent.com/mamedev/mame/master/src/mame/snk/neopcb.cpp
- S5: FBNeo `neo_run.cpp` (tile mask, IPS memory expansion, S data from the end of C, comment on the KOF 2003 PCB): https://raw.githubusercontent.com/finalburnneo/FBNeo/master/src/burn/drv/neogeo/neo_run.cpp
- S6: FBNeo `neo_sprite.cpp` (`NeoInitSprites`, tail marked transparent): https://raw.githubusercontent.com/finalburnneo/FBNeo/master/src/burn/drv/neogeo/neo_sprite.cpp
- S7: Arcade-History, SVC Chaos Plus and Super Plus (unlocked bosses, missing sounds): https://www.arcade-history.com/game/4964/snk-vs-capcom-svc-chaos-plus , https://www.arcade-history.com/game/4965/
- S8: Arcade-History, KOF 10th Anniversary (KOF 2002 hack): https://www.arcade-history.com/game/4739/
- S9: community README for 27 hack sets (third party, Traditional Chinese): https://github.com/setsuna362/kof-GOTVG_offline_pack
- S10: Arcade-History, KOF 2003 (codes, final-boss condition): https://www.arcade-history.com/game/3264/
- S11: FightersGeneration, KOF 2002 (King and Geese tagged PS2): https://fightersgeneration.com/games/kof2002.html
- S12: The Cutting Room Floor, KOF 2002 (Neo Geo): https://tcrf.net/The_King_of_Fighters_2002_(Neo_Geo)
- S13: The Cutting Room Floor, SvC Chaos (Neo Geo): https://new.tcrf.net/SvC_Chaos:_SNK_vs._Capcom_(Neo_Geo)
- S14: The Cutting Room Floor, KOF 2003 (Neo Geo): https://tcrf.net/The_King_of_Fighters_2003_(Neo_Geo)
