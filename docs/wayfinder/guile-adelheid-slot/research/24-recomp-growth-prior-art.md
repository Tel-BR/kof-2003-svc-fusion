# Ticket 24 - Prior art for growing a neogeorecomp-based port past 64 MB of C-ROM

Research date: 2026-11-16. Everything below is *unverified* in this project (nothing was tried here). Sources are public READMEs, source files, PRs and commit lists read through raw.githubusercontent.com and the GitHub API. No ROMs or game data were read.

## Summary (answer first)

1. `neogeorecomp` is the public repo **sp00nznet/neogeorecomp** (MIT, not a fork, created 2026-03-21, v0.2.0 released 2026-10-20). It is the generic Neo Geo MVS board model plus the `m68krecomp` 68000->C generator, with Musashi as fallback/oracle, `--verify`, and `--dump-misses`/`--entries`. Almost every public Neo Geo recomp (omegakatana92's ~25+ ports, danilopaulinodasilva/kof98recomp, tdstdx627/kof2002-recomp-mod) vendors it at v0.2.0 (upstream commit af96b2b4). The local KOF 2003 layout (`crom_size = 0x4000000`, four C pairs, 24 generated files, `profile` target) is identical to omegakatana92's KOF 2003 port.
2. **No public project was found that documents going past 64 MB.** Every `src/game.c` I read (KOF 2003, KOF 2002 mod, MS3, MS5, SamSho V Perfect, Garou, Rage of the Dragons) sets `crom_size = 0x4000000`. Upstream `romload.c` itself has no 64 MB cap (it just allocates `crom_size`), and the 64 MB figure comes from the per-game descriptor. So the local "fixed 64 MB" is a per-game constant, not an upstream limit (*unverified* for the local adapted copy).
3. Upstream decodes the whole C-ROM at load into 256 B/tile (2x the C-ROM size), so 64 MB -> 128 MiB RAM and 128 MiB -> 256 MiB RAM. This matches the local "tile cache 128 MiB" and the planned 256 MiB. The tile index mask is derived from tile count (power of two), so `0x80000` tiles wraps at `$7FFFF` and 128 MiB gives a full 20-bit mask. Hardware ceiling is 20 bits = 1,048,576 tiles = 128 MiB; more needs bankswitching (neogeodev wiki).
4. The only documented C-ROM change in the lineage is the Rage of the Dragons patch (omegakatana92): decoded buffer padded to a power of two (`pow2*256`, `calloc`) because non-power-of-two sets (KOF'97 at 40 MB) read past the heap. This is the main hazard if added C files make the total non-power-of-two.
5. Banked-P-ROM decode limits (the local "7 MB never becomes C") are listed on upstream's ROADMAP as unsupported; kof98recomp and Matrimelee added per-bank dispatch. I found no `--dump-misses` change beyond upstream.

## Lineage of neogeorecomp

| Project | URL | Author | Licence | Relation | Evidence |
|---|---|---|---|---|---|
| neogeorecomp (upstream) | https://github.com/sp00nznet/neogeorecomp | sp00nznet (commits by "Ned Heller"/"sp00nz") | MIT (API `license.spdx_id`=MIT) | Root of the lineage | API: `fork:false`; README credits Musashi (K. Stenerud, MIT), superzazu/z80, ymfm; layout follows sp00nznet lynxrecomp/snesrecomp. v0.2.0 = commit af96b2b (PR #8). Generic runtime introduced in 5000b3a (PR #1) |
| metalslug | https://github.com/sp00nznet/metalslug | sp00nznet | MIT | Reference game, submodule of the toolkit | README: "git submodule", clone `--recurse-submodules` |
| neodriftout | https://github.com/sp00nznet/neodriftout | sp00nznet | MIT | Second game, "no toolkit changes" | README v0.2.0; CHANGELOG 0.2.0 |
| danilopaulinodasilva/neogeorecomp | https://github.com/danilopaulinodasilva/neogeorecomp | Danilo P. da Silva | MIT (inherited) | Fork; author of YM2610 sound PR #3 (ce983d6, merged upstream); fork adds banked P-ROMs + AES mode (per PR #3 text) | API forks list; PR #3 body; fork head commits 57e9bb7, a47ee3f (2026-11-02) |
| kof98recomp | https://github.com/danilopaulinodasilva/kof98recomp | Danilo P. da Silva | MIT | Game repo, submodule = his fork (a47ee3f); began as a fork of `metalslug`; 5 MB P-ROM as four 1 MB banks, AES mode, widescreen (52 patched operands) | README; `.gitmodules` points to danilopaulinodasilva/neogeorecomp |
| tdstdx627/kof2002-recomp-mod | https://github.com/tdstdx627/kof2002-recomp-mod | tdstdx627 | MIT | Copies kof98recomp structure; toolkit "pinned to the version kof98recomp locks to"; adds `data/entries.txt` (1,275 entries), CLAUDE.md/AGENTS.md, `build.sh profile`; `crom_size=0x4000000`, 4 C pairs, `prom_size=0x500000` | PUBLIC_NOTES.md, README, game.c; has `LICENSE.kof98recomp` |
| omegakatana92 ports (KOF 96/97/98/2000/2002/2003, Garou, Matrimelee, RotD, MS3, MS5, SamSho, SamSho II, SamSho V Perfect, Last Blade 1/2, Blazing Star, Breakers, Ironclad, Ninja Master's, RBFF 1/2, Waku Waku 7, ...) | e.g. https://github.com/omegakatana92/The-King-of-Fighters-2003 , .../Rage-of-the-Dragons-Recomp , .../Metal-Slug-5-Recomp , .../-Power-Instinct-Matrimelee-Recomp | omegakatana92 ("OmegaKatanaXIII", 187 public repos) | Own code PolyForm Noncommercial 1.0.0; toolkit stays MIT (KOF2000 repo shows GPL-2.0 in API; unclear) | Vendor neogeorecomp v0.2.0 at af96b2b+ with generic patches | READMEs; SOURCE-NOTES.md (KOF 2003) names commit af96b2b4b39b42b392b17bcaa6a74a5f27088202; docs/TOOLKIT_PATCHES.md (RotD); docs/runtime-changes.md (Matrimelee). Repos created 2026-10-25..11-01; the author's other repos use other recomp toolkits (cps2recomp, psxrecomp) |
| Fork: matepore/neogeorecomp | https://github.com/matepore/neogeorecomp | Calcagno Mateo | MIT | Fork adding settings.cfg, pause/screenshot, graphics filters, volume (to 2026-11-09). No crom/tile commit seen in list | commit list |
| Fork: AuroraRAS (PR #9, open) | https://github.com/sp00nznet/neogeorecomp/pull/9 | AuroraRAS | MIT | Emscripten/WASM build; no size info read | PR list |
| Forks: LuizRafael79, q356782946, Vulto | https://github.com/Vulto/neogeorecomp etc. | various | MIT | Forks exist; LuizRafael79/q356782946 show no newer pushes; Vulto's recent commits (CI, LSP_1ST, "decomp") look like a separate line of work, relation *unclear* | forks API, Vulto commit list |
| NOT derived: AlmazProud/metal-slug-{x,3,4,5}-recomp | https://github.com/AlmazProud/metal-slug-5-recomp | AlmazProud | MIT | Own runtime (SDL3), "checked against MAME 0.289"; shares code only with sibling repos | README |
| NOT derived: sunkpoet-lang/neogeo-recomp | https://github.com/sunkpoet-lang/neogeo-recomp | sunkpoet-lang | GPL-3.0 | Built on CPS-2 Recomp (Tommy McLeroy); KOF97/98/2002/KOF2002MP2; runs in interpreter, C translation "next step" | README |

Likely path for the local repo (inference, *unverified*): upstream -> danilopaulinodasilva fork/kof98recomp -> tdstdx627-style mod (entries.txt + profile) and/or omegakatana92's KOF 2003 (same 24-file layout, 0x4000000 C-ROM, KOF2003 PVC).

## Projects that grew past 64 MB

**None found.** Evidence by absence (all *unverified* as to the local copy):

| Project | `crom_size` / pairs | Source |
|---|---|---|
| omegakatana92 KOF 2003 | 0x4000000, 4 pairs `271-c1c..c8c`, "64 MB after pairing"; P 0x900000 | https://raw.githubusercontent.com/omegakatana92/The-King-of-Fighters-2003/HEAD/src/game.c |
| omegakatana92 MS5 | 0x4000000, `268-c1c..c8c`; P 0x800000 | .../Metal-Slug-5-Recomp/HEAD/src/game.c |
| omegakatana92 MS3 | 0x4000000, `256-c1..c8`; P 0x900000 | .../Metal-Slug-3-Recomp/HEAD/src/game.c |
| omegakatana92 Garou | 0x4000000, `253-c1..c8` | .../Garou-Mark-of-the-Wolves-Recomp/HEAD/src/game.c |
| omegakatana92 SamSho V Perfect | 0x4000000, `273-c1d..c8d`; P 0x800000 | .../Samurai-Shodown-V-Perfect-Recomp-/HEAD/src/game.c |
| omegakatana92 Rage of the Dragons | 0x4000000, `264-c1..c8` | .../Rage-of-the-Dragons-Recomp/HEAD/src/game.c |
| tdstdx627 KOF2002 mod | 0x4000000, `kof2k2_c1..c8`; P 0x500000 | .../kof2002-recomp-mod/main/src/game.c |
| upstream metalslug / docs example | porting doc example uses crom_size 16 MB, two pairs | docs/porting-a-game.md |

No repo for SVC Chaos, KOF 2001/2003 hacks, 128 MB sets, Neo CD, or "cthulhu" was found. No issue or PR in sp00nznet/neogeorecomp (9 PRs, 0 issues) mentions crom size, 64/128 MB or tile cache.

### Related changes that did happen (what changed / what broke)

1. **Power-of-two padding of the decoded sprite buffer** (omegakatana92 RotD, `docs/TOOLKIT_PATCHES.md`, `src/video.c`). Changed: sprite codes masked to next power of two; buffer = `pow2 * 256` bytes via `calloc`. Broke before: non-power-of-two sets (KOF'97, 40 MB) read past the heap. RotD output unchanged (64 MB). README of RotD also says other sets still stop before sound init, fixes unconfirmed. *Unverified.*
2. **Upstream mask behaviour** (`src/video.c`, as read via a summariser; re-read the file before relying on it): tile count = C-ROM size / 128; mask = next pow2 minus 1; 20-bit tile code (16 bits + 4 attribute bits); out-of-ROM codes wrap rather than fail; decoded storage = tile count x 256 B; the buffer is NOT padded in upstream, so a non-power-of-two count can index past the end. *Unverified.*
3. **Loader** (`src/romload.c`, `ng_load_crom`): one `calloc(1, crom_size)`; per pair: both reads must succeed, sizes must be equal (`s0 != s1`), and `at + s0*2 <= crom_size`; byte interleave A->even, B->odd; returns NULL silently on failure; loops up to `NG_MAX_PARTS` (8). No cap constant. *Unverified.*
4. **P-ROM bank fixes**: MAME-style fallback to bank 0 when the 1 MB window starts past the P-ROM end (RotD patch); bank-aware native dispatch for the `$200000` window (Matrimelee `docs/runtime-changes.md`); four 1 MB banks each recompiled in its own context (kof98recomp). Upstream ROADMAP lists "multi-bank P ROMs (games over 2 MB)" as planned. *Unverified.*
5. **Generated-code layout**: upstream always emits 16 C functions/files; KOF 2003 changelog mentions a 24-file layout and a `profile` target. Matrimelee build produces ~180 MB of generated C. *Unverified.*
6. **Z80 counter / audio fixes** (MS5 README: modular Z80 cycle difference after 32-bit wrap) - a 32-bit overflow bug class, but in the Z80 timing, not the C-ROM address path.

## Comparison with this repo's generator

| Item | Status | Notes |
|---|---|---|
| Static recursive descent, vectors, header entries, jump tables, pointer scan, `--entries`, `--dump-misses`, `--verify`, `--no-pointer-scan` | Already has (same as upstream docs/recompiler.md) | Local lacks traces, same as upstream |
| Decode only 1 MB fixed + first bank + BIOS | Already has (= upstream: banked region is single, ROADMAP item) | Local gap (7 MB banked as interpreter) is the same upstream gap; kof98recomp/Matrimelee bank-aware dispatch is prior art to read |
| C-ROM pairs, equal-size check, overflow check vs `crom_size` | Already has (upstream identical) | Upstream struct allows 8 pairs (`NG_MAX_PARTS=8`); local descriptor uses 4. Adding pairs is probably only descriptor work *(unverified)* |
| `crom_size` 64 MB | Per-game constant, no upstream cap | Raise to 0x8000000 in descriptor; check local adapted romload for any added cap |
| Decoded tile storage 2x C-ROM | Already has (128 MiB at 64 MB) | 128 MiB C-ROM -> 256 MiB, as planned |
| Mask from tile count (wrap above $7FFFF) | Already has | Becomes 0xFFFFF at 128 MiB; this is where "first native draw of tile >= $80000" will show up; wrap vs real hardware ceiling is exactly 20 bits |
| Power-of-two padding of decoded buffer | LACKS (upstream also lacks it; RotD has it) | Needed if total C size is not a power of two (e.g. 64 MB + extra files that stop short of 128 MiB). Alternative: always size to 128 MiB |
| Size > 128 MiB | LACKS and impossible without bankswitching | Hardware tile number is 20 bits (wiki.neogeodev.org Sprites) |
| 32-bit overflow in `at`/index math | Unknown | 128 MiB and 256 MiB fit in 32-bit; verify the types in the local copy |
| Run-time checksums / matching C to ROM | Not found in any project | Local gap stands |
| Regeneration on ROM change | Same as upstream (entries/ROM dependent) | Graphics-only changes need no regeneration in any project read |
| RAM use of decode-at-load | Same as upstream | 256 MiB resident, no lazy cache in upstream; no project reports memory failures |

## Open points / not found

- No repo, issue or PR documenting a 128 MB `crom_size`, a bigger tile cache, or tile codes >= $80000 in this lineage. I am not claiming that none exists, only that I did not find one (GitHub code search is not available without auth; repo search results were truncated).
- The local "tile cache" may be local naming; upstream has a full decode, not a cache.
- tdstdx627's notes mention "C ROM expansion" as a route for imported graphics but give no sizes; read `AGENTS.md`/`docs/` there for the method.
- `video.c` and `romload.c` statements come from a summariser reading raw files; re-read the actual files (and the local adapted copy) before depending on them. Same for `docs/TOOLKIT_PATCHES.md`.
- omegakatana92's KOF 2000 repo shows GPL-2.0 in the API while README text for sibling repos says PolyForm Noncommercial; licences of the ports need checking before reuse of code.
- The 2026-10 commit dates of omegakatana92 repos are all within a week; many may be AI-generated and unreviewed. Treat their README claims as author claims.
- Real sets above 64 MB (and hardware at the 128 MiB edge) were not verified in MAME sources here.

## Sources

- https://github.com/sp00nznet/neogeorecomp (README, CHANGELOG, ROADMAP, docs/recompiler.md, docs/porting-a-game.md, src/romload.c, src/video.c, include/neogeorecomp/neogeo.h; API: repo, forks, issues/PRs #1-#9, commits af96b2b, 5000b3a, ce983d6)
- https://github.com/sp00nznet/neogeorecomp/pull/3 (sound; names kof98recomp and the fork)
- https://github.com/sp00nznet/metalslug , https://github.com/sp00nznet/neodriftout
- https://github.com/danilopaulinodasilva/neogeorecomp , https://github.com/danilopaulinodasilva/kof98recomp
- https://github.com/tdstdx627/kof2002-recomp-mod (README.md, PUBLIC_NOTES.md, AGENTS.md, docs/B_character_system.md, src/game.c)
- https://github.com/omegakatana92/The-King-of-Fighters-2003 (README, SOURCE-NOTES.md, docs/CHANGELOG.md, docs/COMPATIBILITY.md, src/game.c)
- https://github.com/omegakatana92/Rage-of-the-Dragons-Recomp (README, docs/TOOLKIT_PATCHES.md, src/game.c)
- https://github.com/omegakatana92/-Power-Instinct-Matrimelee-Recomp (README, docs/runtime-changes.md)
- https://github.com/omegakatana92/Metal-Slug-5-Recomp , .../Metal-Slug-3-Recomp , .../Garou-Mark-of-the-Wolves-Recomp , .../Samurai-Shodown-V-Perfect-Recomp- , .../The-King-of-Fighters-2002-Recomp
- https://github.com/matepore/neogeorecomp , https://github.com/Vulto/neogeorecomp (commit lists)
- https://github.com/AlmazProud/metal-slug-5-recomp , https://github.com/sunkpoet-lang/neogeo-recomp
- https://wiki.neogeodev.org/index.php?title=Sprites (20-bit tile number, 128 MiB)

---

## Resumo em português do Brasil

Tudo abaixo é *não verificado* (nada foi testado neste projeto).

1. `neogeorecomp` é o repositório público **sp00nznet/neogeorecomp** (MIT, não é fork, v0.2.0 em 2026-10-20, commit af96b2b). Quase todos os recomps públicos de Neo Geo usam esse toolkit: os ~25 portes do omegakatana92 (KOF 2003, KOF 2002, Garou, Matrimelee, MS3, MS5, SamSho V Perfect, RotD...), o kof98recomp do danilopaulinodasilva (que mantém um fork do toolkit com P-ROM em bancos e modo AES) e o kof2002-recomp-mod do tdstdx627 (entries.txt, `build.sh profile`). O layout local (`crom_size = 0x4000000`, 4 pares de C, 24 arquivos gerados, alvo `profile`) coincide com o KOF 2003 do omegakatana92. *Não verificado.*
2. **Não achei nenhum projeto público documentando crescimento acima de 64 MB.** Todos os `game.c` lidos usam `crom_size = 0x4000000`. O `romload.c` do upstream não tem teto de 64 MB: só faz `calloc(crom_size)`; o 64 MB é constante por jogo (no descritor). Não achei issues ou PRs sobre isso (9 PRs, 0 issues no upstream).
3. O upstream decodifica toda a C-ROM na carga (256 bytes por tile, 2x o tamanho): 64 MB vira 128 MiB de RAM, 128 MiB vira 256 MiB, igual ao plano do ticket 19. A máscara do índice de tile vem da contagem de tiles (potência de 2): o wrap acima de $7FFFF some sozinho ao subir para 128 MiB (máscara 0xFFFFF). Teto de hardware: 20 bits = 1.048.576 tiles = 128 MiB; acima disso só com bankswitching (wiki.neogeodev.org). *Não verificado.*
4. Única mudança documentada relacionada: no Rage of the Dragons (omegakatana92, `docs/TOOLKIT_PATCHES.md`) o buffer decodificado passou a ser preenchido até potência de 2 (`pow2*256`, `calloc`), porque conjuntos que não são potência de 2 (KOF'97, 40 MB) liam além do heap. Isso importa se o total de C ficar fora de potência de 2 (por exemplo 64 MB mais arquivos novos). O gerador local provavelmente NÃO tem isso (upstream também não). *Não verificado.*
5. Comparação: o gerador local JÁ tem (igual ao upstream) descoberta estática, `--verify`, `--dump-misses`, `--entries`, checagem de pares iguais e de estouro contra `crom_size`, decodificação 2x e máscara derivada da contagem; o limite de decodificar só 1 MB fixo + 1 banco é o mesmo do upstream (ROADMAP), e o kof98recomp e o Matrimelee têm despacho por banco como referência. FALTA: preenchimento em potência de 2, e acima de 128 MiB é impossível sem bankswitching. DESCONHECIDO: tipos de 32 bits no cálculo de `at`/índice (128 e 256 MiB cabem em 32 bits), e se a cópia local adaptada tem algum teto extra.
6. Lacunas: busca de código do GitHub indisponível; leituras de `video.c`/`romload.c` vieram de resumo automático (reler o arquivo real); licenças dos repos do omegakatana92 são inconsistentes (PolyForm Noncommercial no texto, GPL-2.0 no KOF2000 via API); os repos têm datas muito próximas e aparência de geração por IA, então são afirmações dos autores.
