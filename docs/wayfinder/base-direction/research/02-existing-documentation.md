# Research: Existing documentation of both engines

Ticket 02. Researched 2026-11-11. Every repository was read at a pinned commit (listed in **Sources**). No cloned code was run or built. No ROM was downloaded. This report contains no game data: it has only addresses, structure offsets, sizes, set names and hashes taken from emulator and script source.

Labels used below:
- **VERIFIED**: read in the primary source (file path and line given).
- **REPORTED**: a secondary source says it; not confirmed in a primary source.
- **INFERENCE**: my own deduction from verified numbers. It needs measurement.
- **UNKNOWN**: no public source found.

## Resumo (PT-BR)

- **O SVC Chaos é feito "em cima" do motor do KOF 2003? Não há prova pública disso.** Não achei nenhuma entrevista, crédito ou documento técnico que diga isso. A página da SuperCombo citada no ticket ficou bloqueada (proteção anti-robô), então a frase não foi confirmada. Além disso, o SVC chegou aos fliperamas em **24/07/2003** e o KOF 2003 só em **12/12/2003**. O SVC é o mais antigo dos dois.
- **O que é certo (forte):** os dois usam a **mesma geração de cartucho** da SNK Playmore: o chip de proteção NEO-PVC, gráficos criptografados NEO-CMC 7050, som NEO-PCM2 e a mesma placa de gráficos (CHAFIO 2003.7.24). Isso é "mesmo hardware", não "mesmo motor de jogo".
- **O que os dados de memória sugerem:** a "ficha" do lutador na memória do SVC (vida, barra de especial, lado da tela, caixas de golpe) usa **os mesmos deslocamentos internos do KOF '96–2002**. A do KOF 2003, até onde está documentada, é **bem diferente**: 3 lutadores por time, vida e barra guardadas na RAM do chip de proteção, e caixas em outras posições. Leitura provável: o SVC herda o código da linha KOF '96–2002, e o KOF 2003 mudou mais. Isso é uma pista forte, mas ainda não é prova.
- **fbneo-training-mode (peon2):** dá suporte aos dois jogos. Tem um módulo `svc` e um `kof2003`, cada um com seu script de caixas de golpe. Documenta endereços de vida, barra, direção, combo e tempo, e as posições das caixas de golpe. **Não documenta** animação, scripts de golpes nem "API" do motor.
- **Nomes de ROM aceitos:** o script reconhece o jogo pelo nome do set ou pelo nome do "set pai". Vale para `svc` e clones (`svcboot`, `svcplus`, `svcplusa`, `svcsplus`; no FBNeo também `svcfd`, `svcsplse`) e para `kof2003` e clones (`kof2003h`, `kf2k3bl`, `kf2k3pl`…). As versões de placa JAMMA (`svcpcb`, `kf2k3pcb`) **não** são reconhecidas. Só `svc`, `svcsplus` e `kof2003` aparecem como testados na lista oficial.
- **Outros scripts de hitbox:** o de dev-dem cobre só KOF '96 e '97. O de Jesuszilla cobre KOF '94 a 2002. **Nenhum dos dois cobre SVC nem KOF 2003.**
- **Projetos de "recompilação":** o port do KOF 2003 (omegakatana92) documenta muito bem o **hardware** (proteção, mapa de memória do chip PVC, decodificação), mas **nada** sobre lutadores. O neogeorecomp, o neogeo-recomp (KOF 97/98/2002), o cps2recomp e o Metal Slug 5 recomp **não tratam de SVC nem de KOF 2003**. O de Metal Slug 5 é útil só porque usa o mesmo chip PVC.
- **Consequência para a decisão do Jogo Base:** não dá para assumir "mesmo motor" sem medir. O próximo passo é um ticket de medição: rodar os dois jogos no emulador com script Lua e comparar, campo a campo, a ficha do lutador. Principalmente ponteiro de animação, quadro atual e caixas, usando os Personagens Compartilhados.

## Findings

### Q1. Is SVC Chaos built on the KOF 2003 engine? Evidence and strength

#### 1.1 Evidence inventory

| # | Evidence | Status | Source | What it supports |
|---|---|---|---|---|
| E1 | SuperCombo wiki statement that SVC was based on the KOF 2003 engine | **UNVERIFIED** (page unreachable) | https://wiki.supercombo.gg/w/SvC_Chaos:_SNK_Vs_Capcom. Fetch returned an Anubis bot-protection "Access Denied" page. The mirror srk.shib.live gave the same block. The Wayback Machine is blocked for this agent. | Nothing confirmed. Even if the sentence exists, it is a community wiki claim with no known primary citation. |
| E2 | Both titles are NEO-PVC + NEO-CMC 7050 + NEO-PCM2 carts on the same CHAFIO graphics board | **VERIFIED** | MAME `src/mame/snk/neogeo.cpp` L9905–9909 (svc: "NEO-MVS PROGBK3R (2003.9.2) (NEO-PCM2 SNKPLAYMORE) (NEO-PVC) / NEO-MVS CHAFIO (2003.7.24) (NEO-CMC 7050)") and L10057–10061 (kof2003: "NEO-MVS PROGBK3S (2003.10.1) … (NEO-PVC) / NEO-MVS CHAFIO (2003.7.24) (NEO-CMC 7050)"). MAME `src/devices/bus/neogeo/prot_pvc.cpp` L29–31: "PVC Protection — mslug5, svcchaos, kof2003". | The same **hardware/protection generation**. This says nothing about the game engine. Metal Slug 5 is on the same chip and is clearly not a fighting-game engine. |
| E3 | Release order: SVC first | **VERIFIED** | MAME `hash/neogeo.xml` L9450: svc `release` "20030724 (MVS), 20031113 (AES)". L9641: kof2003 `release` "20031212". Weblio (JA Wikipedia mirror) gives the same arcade date of July 24, 2003 (https://www.weblio.jp/content/SVC+CHAOS). | SVC shipped about 5 months **before** KOF 2003. A literal "SVC on the KOF 2003 engine" would need a shared in-development codebase. No public source documents one. |
| E4 | SVC's player-object field offsets match the KOF '96–2002 lineage; KOF 2003's documented layout does not | **VERIFIED** numbers. Lineage conclusion is **INFERENCE**. | fbneo-training-mode `games/svc/svc.lua` L14–24, `games/kof97/kof97.lua` L15–25 (and kof96/98/99/2000/2001/2002), `games/kof2003/kof2003.lua` L9–25, `hitboxes/svc-hitboxes.lua`, `hitboxes/kof2003-hitboxes.lua`, `hitboxes/kof-hitboxes.lua` L186–201. See the table in Q2. | **Moderate** evidence that SVC's fighter code derives from the KOF '96–2002 codebase. It also shows that KOF 2003's fighter representation diverged. This is the strongest *technical* evidence found, and it points **away from** "SVC = KOF 2003 engine". |
| E5 | SVC's graphics ROMs contain a large amount of leftover KOF 2002 graphics; leftover KOF '96/'97 sprites | **REPORTED** (secondary) | TCRF, https://tcrf.net/SvC_Chaos:_SNK_vs._Capcom_(Neo_Geo), sections "Unused Sprites" and "Leftover KOF 2002 Graphics" | Asset lineage from KOF 2002, not KOF 2003. |
| E6 | "The gameplay is based on the KOF series (particularly The King of Fighters 2002)" | **REPORTED**, uncited | English Wikipedia, https://en.wikipedia.org/wiki/SNK_vs._Capcom:_SVC_Chaos. The sentence has no footnote. | Gameplay similarity only. |
| E7 | JA Wikipedia: system/controls close to the KOF series; SNK-side sprites basically taken from KOF; sound effects newly made; Kyo's and Mr. Karate's move behaviour follows KOF2001 | **REPORTED** | https://ja.wikipedia.org/wiki/SNK_VS._CAPCOM_SVC_CHAOS | Lineage from KOF ≤2002 at design level. KOF 2003 is not named as the base. |
| E8 | KOF 2003 was originally planned for Atomiswave, then moved to MVS. Its multi-shift system replaced the Striker system. Falcoon had worked on SVC before. | **REPORTED** | English Wikipedia, https://en.wikipedia.org/wiki/The_King_of_Fighters_2003 (cites GameSpot "TGS 2003: King of Fighters update" and Arcadia "KOF 2003 Flame of Nova" p.131) | KOF 2003 was a substantial system rework. There is staff overlap with SVC (an artist). Nothing about shared code. |
| E9 | Same Z80 sound-driver RAM address for music (0xFD89) in garou, kof98–kof2003, lastbld2, samsho5, samsh5sp and svc | **VERIFIED** | fbneo-training-mode `addon/mute.lua` L55–57 | Weak. This is a family-wide SNK sound driver, not specific to SVC/KOF 2003. |
| E10 | Developer interview or credit saying which engine SVC used | **UNKNOWN** | Searches (EN/JA) found none. Both Wikipedias list SNK Playmore as developer. SVC producer: Eikichi Kawasaki. KOF 2003 producers: Eikichi Kawasaki, Kazuya Hirata. | — |

#### 1.2 Rating

- **"SVC Chaos is built on the KOF 2003 engine": weak / unsupported.** No primary source was found. The one cited source (SuperCombo) could not be read. The release order makes the literal claim unlikely. The best technical evidence (E4) shows SVC's player struct follows KOF '96–2002, not KOF 2003.
- **"SVC and KOF 2003 share a hardware platform and protection family": strong** (E2, emulator source).
- **"SVC's fighter code descends from the KOF '96–2002 codebase": moderate** (E4 plus E5–E7). This is *structural* evidence from two independently written community scripts. It is not code-level proof. One caveat: the SVC hitbox **box-ID colour table** was explicitly copied from the KOF script ("Table taken from the kof scripts could have some wrong data. Seems right mostly", `hitboxes/svc-hitboxes.lua` L15). However, the **struct offsets** in `games/svc/svc.lua` were found separately and still line up.
- **Implication for the Base/Donor decision:** the "Shared Characters reveal the engine" thesis must be **measured**, not assumed. The data suggests SVC's internal representation is closer to KOF 2002 than to KOF 2003.

### Q2. What the named projects document about memory, fighter struct, animation and hitboxes

#### 2.1 peon2/fbneo-training-mode (commit bf3541e, 2026-07-31)

Registration: `fbneo-training-mode.lua` L157 `kof2003 = {hitboxes = "kof2003-hitboxes", …}` and L198 `svc = {hitboxes = "svc-hitboxes", …}`. Game detection is at L365–372: a game matches if `ROM_NAME == key or PARENT_NAME == key`. Those come from `emu.romname()` / `emu.parentname()` in `resources/constants.lua` L3–4.

**SVC: `games/svc/svc.lua` (VERIFIED)**

| Item | P1 | P2 | Note |
|---|---|---|---|
| health (byte, value+1 shown) | 0x10A239 | 0x10A4B9 | max 0xE1 ("offset 1 for magic pixel") L8–15 |
| meter (word) | 0x10A1E8 | 0x10A468 | max 0x6400−0x80 L11–18 |
| facing (byte, 0 = facing left) | 0x10A131 | 0x10A3B1 | L20–21 |
| combo counter (byte; non-zero ⇒ opponent in hitstun) | 0x10A530 | 0x10A2B0 | L23–24 |
| round timer (word) | 0x10AC14 | — | L172 |
| Known issue | "Doesn't activate MAX properly" | | L3–6 |

**SVC: `hitboxes/svc-hitboxes.lua` (VERIFIED).** The author is unknown; peon2's header says "I think it's Mountainmanjed".
- Player base `0x10A100`, P2 = base + `0x280` (L90, L100). The script also scans 16 generic objects at `0x101000 + n*0x280` (L95–97).
- Per-object offsets: pos_x `+0x18` (word), pos_y `+0x20` (word), flip `+0x31` (byte), box-active mask `+0x261` (bits 0–3), 4 collision boxes at `+0x262 / +0x268 / +0x26E / +0x274`, push box `+0x27A` (L56–66, L102–126).
- Box record, read from `colbox`/`pushbox` (L29–53, L74–87): `+0` id, `+1` x (signed, ×2), `+2` y (signed, ×2), `+3` half-width, `+4` half-height. Records are 6 bytes apart.
- Commented-out fields: meter `+0xE8`, life `+0x138` (word), stun `+0x13E`, guard `+0x146` (L106–111). Balrog punch/kick "tap" counters are at `+0x1FA` / `+0x1FC` (L148–149).
- Camera: `0x10B4CE` (x), `0x10B4D6` (y). The draw gate is `rb(0x10B4B7) ~= 0` (L92–93, L165).
- Box-ID → type table is copied from the KOF scripts (L15–20). It is identical to the kof99/2000/2001/2002 table in `hitboxes/kof-hitboxes.lua` L154–175.

**KOF 2003: `games/kof2003/kof2003.lua` (VERIFIED)**

| Item | Address(es) | Note |
|---|---|---|
| active team-member index (0–2) | P1 0x107D1A, P2 0x107D1B | L9–10, used as an array index (L163–165) |
| health per member (byte) | P1 {0x2FE91D, 0x2FEA1D, 0x2FEB1D}, P2 {0x2FED1D, 0x2FEE1D, 0x2FEF1D} | L15–16. These are **inside NEO-PVC cart RAM** ($2FE000–$2FFFFF). max 0x71 |
| meter / stocks | P1 0x2FE800 (+0x4 = stocks), P2 0x2FEC00 | L18–19. Meter = byte + stocks×0x48 (L143–157). max 0x168 |
| facing per member | P1 {0x10108F, 0x10138F, 0x10168F}, P2 {0x101B0F, 0x101E0F, 0x10210F} | L21–22 |
| combo counter | P1 0x2FE80F, P2 0x2FEC0F | L24–25 (PVC RAM) |
| round timer (word) | 0x107D62 | L161 |

**KOF 2003: `hitboxes/kof2003-hitboxes.lua` (VERIFIED).** Original author unknown, per peon2's header.
- Object pointer list: 16 dwords from `0x107D1C` (L41–47). Only objects whose word at `+0x00` is 2 or 3 are drawn as player objects (L51).
- Per-object offsets: pos_x `+0x24`, pos_y `+0x28`, flip = bit 1 of `+0x0F`, box-active mask `+0x4F` (bits 0–3). 4 collision boxes at `+0xA0 / +0xA6 / +0xAC / +0xB2`, push box `+0xB8` (L53–68).
- Box record (L78–88): `+0` id, `+1` not read, `+2` x (signed, ×2), `+3` y (signed, ×2), `+4` width, `+5` height.
- Camera `0x1087BC` / `0x1087C0` (L39–40).
- Box-ID → type: its own 256-entry table (L15–34). It differs from the KOF '96–2002/SVC table: id 0 = push-like, 0x01–0x0E hurt, 0x0F–0x19 projectile, 0x1C–0x1E guard, 0x20+ attack. Comment: "60&61 are counter but appear as attack".
- Bug noted (VERIFIED by reading): L13 assigns `p = prjhcolor` and `c = throw`. Neither variable is defined (the defined one is `prjecolor`), so projectile/throw IDs get a nil colour. A later ticket should not trust projectile rendering in this script.

**KOF '94–2002 reference: `hitboxes/kof-hitboxes.lua`** (dammit, 2012, adapted by peon2; VERIFIED)
- Player base `0x108100`, spacing `0x200`, pos_x `+0x18`, pos_y `+0x26`, flip `+0x31`, status/active mask `+0x7C` (L186–195).
- Boxes at `+0x90/+0x95/+0x9A/+0x9F` (5-byte records: id, x, y, half-w, half-h) and push at `+0xA4` (L196–202, L355–364). Throwable box for kof96–2002 at `+0x18D` (L223).
- Game modules for kof96–kof2002 all use health `0x108239/0x108439`, meter `0x1081E8/0x1083E8`, facing `0x108131/0x108331` and combo `0x1084B0/0x1082B0` (e.g. `games/kof97/kof97.lua` L15–25, `games/kof2002/kof2002.lua` L9–22).

**Side-by-side (all numbers VERIFIED; the "same?" column is INFERENCE)**

| Field | KOF '96–2002 | SVC | KOF 2003 (as documented) | Same layout as SVC? |
|---|---|---|---|---|
| Player object base | 0x108100 (P2 +0x200) | 0x10A100 (P2 +0x280) | No fixed base. 16-entry pointer list at 0x107D1C. Per-member objects implied by facing addresses: P1 ≈0x101080/0x101380/0x101680, P2 ≈0x101B00/0x101E00/0x102100 (INFERENCE: facing − 0x0F) | KOF '96–02: same idea, relocated. KOF 2003: no |
| pos_x / pos_y | +0x18 / +0x26 | +0x18 / +0x20 | +0x24 / +0x28 | '96–02: x same. 2003: no |
| facing | +0x31 | +0x31 | +0x0F (bit 1) | '96–02: yes. 2003: no |
| health | +0x139 (byte) | +0x139 (byte; word +0x138) | PVC RAM 0x2FE91D + member×0x100 | '96–02: yes. 2003: no |
| meter | +0xE8 | +0xE8 | PVC RAM 0x2FE800 / 0x2FEC00 | '96–02: yes. 2003: no |
| combo counter | +0x1B0 | +0x1B0 | PVC RAM +0x0F of team block | '96–02: yes. 2003: no |
| box-active mask | +0x7C | +0x261 | +0x4F | concept same in all three |
| 4 boxes + push | +0x90…+0xA4, 5-byte records | +0x262…+0x27A, 6-byte spacing, fields id/x/y/w/h at +0..+4 | +0xA0…+0xB8, 6-byte records, fields at +0/+2/+3/+4/+5 | field order: SVC = '96–02. KOF 2003 has an extra byte at +1 |
| box-ID semantics | per-game tables | copied from KOF '99–2002 table | its own, different 256-entry table | 2003: no |

Not documented anywhere in this repo for either game: animation/frame pointer, sprite-frame tables, move/command scripts, state machine, character IDs, engine API (**UNKNOWN**).

#### 2.2 dev-dem/kof-training-mode-FBNeo (commit 132f382, 2021-02-21)

**VERIFIED:** supports only kof96 and kof97 (`README.md` "Supported Games"; `lib/profile.lua` L30 `name = {"kof96"}`, L131 `name = {"kof97"}`). Player base `0x108100` (`lib/profile.lua` L32, L133). It has **no** svc or kof2003 data. Hitbox code is credited to Jesuszilla's scripts (README).

#### 2.3 Jesuszilla/mame-rr-scripts (commit c35f354, 2019-01-25)

**VERIFIED:** `kof-hitboxes.lua` is dammit's "NeoGeo King of Fighters hitbox viewer, February 20, 2012" (L1–3). It covers kof94, kof95, kof96, kof97, kof98, kof99/kof2000, kof2001/kof2002 (7 profiles). Layout is the same as 2.1's reference (`g.address.player = 0x108100` L182; boxes L193–197). `fighting-OSD.lua` covers kof94–kof2002 (L618–802). Other scripts are CPS/garou/marvel/sf2/beat-'em-up. A grep for `svc|kof2003` in the repo finds nothing. It has **no** svc or kof2003 coverage.

#### 2.4 omegakatana92/The-King-of-Fighters-2003 (commit 196b3f8, 2026-10-27)

A native static recompilation of kof2003 on neogeorecomp v0.2.0 (`README.md` L1–10). It documents **hardware only**. All of the following is VERIFIED:
- Board NEO-MVS PROGBK3S (2003.10.1) + CHAFIO (2003.7.24) (`README.md` L62).
- 9 MB P program (p1/p2 32-bit-word-scrambled 4 MB each + p3 1 MB). Decrypted with a port of MAME `pvc_prot_device::kof2003_decrypt_68k()`, byte-exact against MAME 0.242 (`README.md` L64–83; `docs/COMPATIBILITY.md` L15–19, MD5 of the prepared program region given).
- PVC 8 KB RAM at `$2FE000–$2FFFFF`. Bank selector at `$2FFFF0/$2FFFF2` forms a 24-bit byte address, and the window base is address + `$100000`. Colour pack/unpack registers at PVC offsets `$1FE0/$1FE8` (`docs/COMPATIBILITY.md` L20–24; `README.md` L81–84).
- CMC 7050 GFX key `0x9d`, fix banking `NG_FIX_BANK_KOF2000`, CMC50 M1, PCM2 swap value 5 (`docs/COMPATIBILITY.md` L31–42).
- 18,439 recompiled entry points. 100% native coverage on a 9,000-frame session. `--verify` 0 mismatches (`README.md` L46–50).
- `src/game.c` holds only the ROM layout. The repo deliberately omits CMake files and generated C (`SOURCE-NOTES.md`). It has **no** fighter struct, animation or hitbox documentation. It has **nothing** on SVC.
- Useful INFERENCE: the KOF 2003 training-mode addresses (health/meter/combo at `0x2FE8xx–0x2FEFxx`) fall inside the PVC RAM this port models. A native port must therefore model PVC RAM as game-state memory, not only as a protection register file.

#### 2.5 sp00nznet/neogeorecomp (commit af96b2b, 2026-10-20)

**VERIFIED:** a generic MVS static-recompilation toolkit. Its compatibility list has only Metal Slug and Neo Drift Out (`README.md` "Compatibility"). `ROADMAP.md` L13 lists "Protected and encrypted sets (CMC, PVC, SMA)" under *Later*. The KOF 2003 repo says it needed "additional generic NEO-PVC, fixed-layer, audio and SDL changes" on top (`SOURCE-NOTES.md`). Its memory map documents work RAM `$100000–$1FFFFF` (64 KB, mirrored) (`docs/architecture.md` L32). It has **no** svc/kof2003 or fighter data.

#### 2.6 sunkpoet-lang/neogeo-recomp (commit 9f5e405, 2026-11-03)

**VERIFIED:** ports of kof97, kof98, kof2002 and kf2k2mp2 (`README.md` "What works"), built on tmcleroy's cps2recomp toolkit (`README.md` L3–4). Its only fighter-memory fact is kof97 health at `0x108239/0x108439`, explicitly taken from fbneo-training-mode (`games/kof97/src/kof97.cpp` L7, L15; `games/kof97/README.md` L40; credit in `README.md` L21). It has **no** svc or kof2003. It is relevant only as a working example of a recomp that reuses training-mode addresses.

#### 2.7 tmcleroy/cps2recomp (commit 59e25cb, 2026-11-10)

**VERIFIED:** CPS-2 only (a grep for `svc|kof2003|pvc` matches only third-party/audio and screenshot files). It has nothing on either game. It is relevant only as the upstream toolkit of 2.6.

#### 2.8 AlmazProud/metal-slug-5-recomp (commit 2b3626d, 2026-10-19)

**VERIFIED:** Metal Slug 5 is the third NEO-PVC title. The repo models the PVC as `NG_CART_PVC`, with `cart_ram[0x2000]` at `2FE000–2FFFFF` (`src/neogeo/neogeo.h` L39–41, L168) and bank writes at `0x2FFFF0` (`src/neogeo/bus.c` L12, L320–324). It notes that "No code runs from the NEO-PVC window" for mslug5 (`CLAUDE.md` L111, L156). It has no fighter data and no svc/kof2003. It is useful as a second, independently written PVC model to cross-check a future port.

#### 2.9 Other leads

- **Shigeshigeru/kof2003chaosPconv** (commit 5b9163d, 2026-11-11). VERIFIED: a P-ROM encrypt/decrypt tool, rewritten from MAME source (README, Japanese). It is based on IQ_132's original tools. Supported sets: kof2003 (9 MB), kof2003h, svc (8 MB), svcpcba ("same routine as svc"), mslug5, mslug5h (`new_version/README.txt` §1; `new_version/neo_pcrypt.py` L14–22, L35–111). This confirms that the three PVC games use per-game variants of one P-ROM scramble family. It has no fighter data. The repo also ships Windows `.exe` binaries (untrusted; not run).
- **city41/mameneogeodevplugin.** The clone failed (needs auth/inaccessible), and attaching the repo was not permitted in this session. REPORTED (ecosyste.ms listing): a MAME Lua plugin showing Neo Geo hardware internals (e.g. sprite bounding boxes). It documents no game-specific layouts. Last push 2024-09-06.
- **city41/neospriteviewer.** Repo not found or inaccessible. REPORTED (neogeodev wiki "Neo Sprite Viewer"): a C-ROM/S-ROM tile viewer with no game-specific animation data.
- **neogeodev wiki, NEO-PVC page** (REPORTED, secondary): used in SVC Chaos, Metal Slug 5 and KOF 2003. 8 KiB RAM, registers in `$2FE000–$2FFFFF`, bankswitch via `$2FFFF0/$2FFFF2`, colour pack/unpack at `$2FFFE0–$2FFFEC`, per-game P-ROM scramble. https://wiki.neogeodev.org/index.php/NEO-PVC

#### 2.10 MAME and FBNeo driver entries (VERIFIED)

MAME (commit 0205889, 2026-11-11):
- `src/mame/snk/neogeo.cpp`:
  - L9905–9912: svc board header (ID-0269, NGM-2690/NGH-2690, PROGBK3R 2003.9.2 / AEG PROGBK3R 2003.8.29, NEO-PCM2, NEO-PVC, CHAFIO + NEO-CMC 7050) and `ROM_START( svc )`. L9913: P region 0x800000 (8 MB).
  - L10057–10064: kof2003 header (ID-0271, NGM-2710/NGH-2710, PROGBK3S 2003.10.1 / AEG 2003.10.6, same chips) and `ROM_START( kof2003 )`. L10065: P region 0x900000 (9 MB, p3 at 0x800000).
  - L2681–2685 / L2723–2733: machine configs `svc` → cart `pvc_svc`, `kof2003` → `pvc_kf2k3`, `kof2003h` → `pvc_kf2k3h`. Bootlegs use `boot_*` carts (L2687–2709).
  - L12057–12061: GAME lines `svc` (Playmore / Capcom) plus clones svcboot, svcplus, svcplusa, svcsplus.
  - L12066–12071: `kof2003` (SNK Playmore, NGM-2710 Export) plus clones kof2003h, kf2k3bl, kf2k3bla, kf2k3pl, kf2k3upl.
- `src/mame/snk/neopcb.cpp` L563–566: JAMMA PCB sets `ms5pcb`, `svcpcb` (NEO-MVH MVO), `svcpcba` (MVOB), `kf2k3pcb` (Japan). These are separate parents, not clones of the cart sets.
- `src/devices/bus/neogeo/pvc.cpp` L82–98 (svc cart: `svc_px_decrypt`, PCM2 swap 3, CMC50 key `SVC_GFX_KEY`) and L102–119 (kof2003: `kof2003_decrypt_68k`, PCM2 swap 5, `KOF2003_GFX_KEY`). mslug5 is at L62–78 (swap 2).
- `src/devices/bus/neogeo/carts.cpp` L75–78: slot names `pvc_mslug5`, `pvc_svc`, `pvc_kf2k3`, `pvc_kf2k3h`.
- `src/devices/bus/neogeo/prot_cmc.h` L34–36: GFX keys MSLUG5 0x19, SVC 0x57, KOF2003 0x9d.
- `src/devices/bus/neogeo/prot_pvc.cpp` L29–31 (PVC games list) and L99 ("kf2k3pcb, kof2003, kof2003h, mslug5 and svc have updated P rom scramble").
- `hash/neogeo.xml` L9445–9450 (svc softlist, slot `pvc_svc`, release 2003-07-24 MVS / 2003-11-13 AES) and L9636–9646 (kof2003, slot `pvc_kf2k3`, release 2003-12-12). L9679+ has kof2003h (2004-03-18).

FBNeo (commit c549714, 2026-11-11), `src/burn/drv/neogeo/d_neogeo.cpp`:
- L10185 `BurnDrvSvcpcb`, L10216 `BurnDrvSvcpcba` (parent svcpcb), L10256 `BurnDrvSvc` (flags CMC50, ALTERNATE_TEXT, P32, ENCRYPTED_M1; init `svcpcbInit`, exit `NeoPVCExit`).
- Clones of svc: L10350 svcboot, L10437 svcplus, L10509 svcplusa, L10595 svcsplus, L22728 `svcfd` ("Fully Decrypted", plain `NeoInit`), plus `svcsplse` (2023 hack) near L22769.
- L10977 `BurnDrvKf2k3pcb` (flag `HARDWARE_SNK_KOF2K3`), L11076 `BurnDrvKof2003`, L11176 `BurnDrvKof2003h`.
- Clones of kof2003: kf2k3bl, kf2k3bla, kf2k3pl, kf2k3upl (L11260–11471), and FBNeo-only kof2k3fd, kof2003t, kf2k3ps2, kf2k3p2s, kof2k3br (L27220–27349).
- PVC emulation shared by both games: L2277–2390. `PVCRAM` is 0x2000 bytes mapped at `0x2fe000–0x2fffff` (L2357–2364). Bankswitch at L2305–2319, with the comment "for kof2003 (bank 0 is $100000)" at L2308. Colour pack/unpack is at L2281–2303.
- Init functions: `svcpcbInit` L10168, `kf2k3pcbInit` L10953, `kof2003Init` L11059, `kof2003hInit` L11159. P-ROM descramble callbacks: `svcCallback` L10130, `kf2k3pcbCallback` L10917, `kof2003Callback` L11018, `kof2003hCallback` L11118.

### Q3. Does fbneo-training-mode support svc (which set names)? Do the hitbox scripts cover svc and kof2003?

- **svc: yes (VERIFIED).** It has a module (`games/svc/svc.lua`) and hitboxes (`hitboxes/svc-hitboxes.lua`). The README lists "SNK vs. Capcom: SVC Chaos" and "SNK vs. Capcom: SVC Chaos Super Plus" (`README.md` L210–212). The changelog v0.22.09 has "Added support for SNK vs. Capcom: SVC Chaos (svc)", "(svcsplus)" and "svc: Added hitboxes". v0.22.10.28 fixed P2 meter, hitbox alignment and the toggle (`changelog` L459–463, L501–502, L523).
  - Set names accepted (VERIFIED mechanism, INFERENCE per set): any set whose name **or parent** is `svc`. In FBNeo that is `svc`, `svcboot`, `svcplus`, `svcplusa`, `svcsplus`, `svcfd`, `svcsplse`. Only `svc` and `svcsplus` are named as supported. The bootleg sets have modified programs, so addresses may differ (UNTESTED).
  - `svcpcb` / `svcpcba` are **not** recognised: their parent is `svcpcb`, not `svc`.
- **kof2003: yes (VERIFIED).** It has a module and hitboxes. The changelog says "Added support for The King of Fighters 2003 (kof2003)" (v0.22.04.08, L664–665) and "kof2003: Added hitboxes" (v0.22.09, L510). README L120.
  - Parent-matching covers `kof2003h`, `kf2k3bl`, `kf2k3bla`, `kf2k3pl`, `kf2k3upl` and the FBNeo-only clones (UNTESTED). `kf2k3pcb` is not recognised.
- **Hitbox coverage elsewhere:** dev-dem covers kof96/kof97 only. Jesuszilla/mame-rr-scripts covers kof94–kof2002 only. **Neither covers svc or kof2003 (VERIFIED).** The only public svc/kof2003 hitbox scripts found are the two in peon2's repo. Both have unknown original authors.

## Open questions

1. **Does the SuperCombo sentence exist, and what is its source?** The page was blocked for this agent. The owner can open it in a normal browser, or a later ticket can use a browser tool. If it cites nothing, treat it as folklore.
2. **Where are the animation and move-script fields?** No public source documents the animation pointer, current frame, frame timer or command/move-script pointer in either game. *Measurement:* in MAME or FBNeo, run a Lua script that dumps the SVC player object (0x10A100, 0x280 bytes) and the KOF 2003 active-member object (via the 0x107D1C pointer list) every frame. Then make a Shared Character do a known move (e.g. a standing light punch) in each game and find the fields that change in step with the animation.
3. **Is KOF 2003's "real" health/meter in PVC RAM, or is that a HUD copy?** *Measurement:* use write-watchpoints on `0x2FE91D` and on candidate work-RAM offsets in the member object. Also check whether SVC writes game state into PVC RAM at all (trace writes to `$2FE000–$2FEFFF` during a round).
4. **Do the SVC object pool (0x101000 + n×0x280) and the KOF 2003 member objects (≈0x101080 + n×0x300) share a header layout?** Compare words at +0x00 (KOF 2003 uses 2/3 = player type), and the coordinates and flip fields.
5. **Code-level kinship.** Is SVC's collision routine (4 boxes + active mask) the same routine as KOF 2002's, or KOF 2003's? *Measurement (local only, nothing published):* let the emulator decrypt the P-ROMs. Put breakpoints on the code that reads the box mask (SVC +0x261, KOF 2003 +0x4F, KOF 2002 +0x7C) and compare routine structure and size. Report only addresses and similarity scores, never code.
6. **Box-ID semantics for SVC** were copied from KOF 2002 and never verified. KOF 2003's table has a nil-colour bug for projectile/throw IDs. A hitbox ticket should check both against observed in-game behaviour.
7. **Bootleg/PCB set compatibility.** Do the svc addresses hold in `svcsplus`/`svcplus`, and do the kof2003 ones hold in `kof2003h`/`kf2k3pcb`? This is cheap to check with the same dump script.
8. **city41 tools** could not be accessed. They are reported to be generic hardware/tile viewers, so they are low priority.

## Sources

Primary (code, read at pinned commits):
- peon2/fbneo-training-mode @ bf3541e1d4f586f76f401617af4fa842447591de: https://github.com/peon2/fbneo-training-mode. Files: `fbneo-training-mode.lua`, `resources/constants.lua`, `games/svc/svc.lua`, `games/kof2003/kof2003.lua`, `games/kof96|kof97|kof98|kof99|kof2000|kof2001|kof2002/<name>.lua`, `hitboxes/svc-hitboxes.lua`, `hitboxes/kof2003-hitboxes.lua`, `hitboxes/kof-hitboxes.lua`, `addon/mute.lua`, `README.md`, `changelog`.
- dev-dem/kof-training-mode-FBNeo @ 132f382294eccf4edd23a00f4f27e0eb83030bc9: https://github.com/dev-dem/kof-training-mode-FBNeo (`README.md`, `lib/profile.lua`)
- Jesuszilla/mame-rr-scripts @ c35f3541b437fc4f1870ffd98e9d89f25e9ecc0e: https://github.com/Jesuszilla/mame-rr-scripts (`kof-hitboxes.lua`, `fighting-OSD.lua`)
- omegakatana92/The-King-of-Fighters-2003 @ 196b3f8ed2f25dfc34100c60835fee37ebcc69ad: https://github.com/omegakatana92/The-King-of-Fighters-2003 (`README.md`, `SOURCE-NOTES.md`, `docs/COMPATIBILITY.md`, `src/game.c`)
- sp00nznet/neogeorecomp @ af96b2b4b39b42b392b17bcaa6a74a5f27088202: https://github.com/sp00nznet/neogeorecomp (`README.md`, `ROADMAP.md`, `docs/architecture.md`)
- sunkpoet-lang/neogeo-recomp @ 9f5e4051d160043331f2b2ea9c9fd4e9136fc769: https://github.com/sunkpoet-lang/neogeo-recomp (`README.md`, `games/kof97/src/kof97.cpp`, `games/kof97/README.md`)
- tmcleroy/cps2recomp @ 59e25cb1019d3574554b15afb697f56eb1ea2c37: https://github.com/tmcleroy/cps2recomp
- AlmazProud/metal-slug-5-recomp @ 2b3626d28420eae2ce2ac6210a34a1f5a65bc234: https://github.com/AlmazProud/metal-slug-5-recomp (`CLAUDE.md`, `src/neogeo/neogeo.h`, `src/neogeo/bus.c`)
- Shigeshigeru/kof2003chaosPconv @ 5b9163d866ef7573a7275608f175c669de72a5c5: https://github.com/Shigeshigeru/kof2003chaosPconv (`README.md`, `new_version/README.txt`, `new_version/neo_pcrypt.py`)
- MAME @ 020588992f149e0f0176f4d499835135d2f8fbb6: https://github.com/mamedev/mame (`src/mame/snk/neogeo.cpp`, `src/mame/snk/neopcb.cpp`, `src/devices/bus/neogeo/pvc.cpp`, `prot_pvc.cpp`, `prot_cmc.h`, `carts.cpp`, `hash/neogeo.xml`)
- FinalBurn Neo @ c5497142ab928d34dbf4d8c395300c4892603fb9: https://github.com/finalburnneo/FBNeo (`src/burn/drv/neogeo/d_neogeo.cpp`)

Secondary (REPORTED):
- SuperCombo wiki, SvC Chaos (not readable, blocked): https://wiki.supercombo.gg/w/SvC_Chaos:_SNK_Vs_Capcom
- TCRF, SvC Chaos (Neo Geo): https://tcrf.net/SvC_Chaos:_SNK_vs._Capcom_(Neo_Geo)
- TCRF, KOF 2003 (Neo Geo): https://tcrf.net/The_King_of_Fighters_2003_(Neo_Geo)
- Wikipedia (EN), SNK vs. Capcom: SVC Chaos: https://en.wikipedia.org/wiki/SNK_vs._Capcom:_SVC_Chaos
- Wikipedia (EN), The King of Fighters 2003: https://en.wikipedia.org/wiki/The_King_of_Fighters_2003
- Wikipedia (JA), SNK VS. CAPCOM SVC CHAOS: https://ja.wikipedia.org/wiki/SNK_VS._CAPCOM_SVC_CHAOS
- Weblio (JA Wikipedia mirror), SVC CHAOS: https://www.weblio.jp/content/SVC+CHAOS
- Fighters Generation review: https://fightersgeneration.com/games/snk-vs-capcom-chaos.html
- StrategyWiki, SVC Chaos: https://strategywiki.org/wiki/SNK_vs._Capcom:_SVC_Chaos
- neogeodev wiki, NEO-PVC: https://wiki.neogeodev.org/index.php/NEO-PVC
- neogeodev wiki, Neo Sprite Viewer: https://wiki.neogeodev.org/index.php/Neo_Sprite_Viewer
- ecosyste.ms listing of city41/mameneogeodevplugin: https://awesome.ecosyste.ms/projects/github.com%2Fcity41%2Fmameneogeodevplugin
