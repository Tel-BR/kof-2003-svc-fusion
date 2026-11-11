# Starting leads (November 2026)

_PT-BR: pistas iniciais trazidas pelo dono do repositório de uma conversa anterior. Não são achados verificados: confirme cada item antes de depender dele._

These are the owner's leads from an earlier conversation, not verified research output. Confirm each item against its primary source before depending on it.

## Recompilation projects / Projetos de recompilação

- **omegakatana92/The-King-of-Fighters-2003**: https://github.com/omegakatana92/The-King-of-Fighters-2003
  - KOF 2003 statically recompiled on top of neogeorecomp v0.2.0.
  - Decrypts NEO-PVC, CMC and PCM2 identically to MAME 0.242.
  - Has a `--verify` mode; runs 100% native in the sessions tested.
  - Licence of the original code: **PolyForm Noncommercial 1.0.0**, which is not open source.
- **sp00nznet/neogeorecomp** (MIT): https://github.com/sp00nznet/neogeorecomp
  - Neo Geo recomp runtime and toolkit in C.
  - Used for the KOF '96, Samurai Shodown V Perfect and Neo Drift Out ports.
- **Vulto/neogeorecomp**: https://github.com/Vulto/neogeorecomp (relationship to sp00nznet's repo unknown; check whether it is a fork).
- **sunkpoet-lang/neogeo-recomp** (GPL-3, C++, cps2recomp lineage): https://github.com/sunkpoet-lang/neogeo-recomp
  - Runs KOF '97 in the interpreter, deterministically, with a per-frame state hash.
  - Plans a training mode and rollback with GekkoNet.
  - Uses fbneo-training-mode as its source of memory addresses.
  - Organises changes with OpenSpec.
- **tmcleroy/cps2recomp** (GPL-3): https://github.com/tmcleroy/cps2recomp
  - Recomp with training mode, rollback online and a launcher.
  - Issue #139 asks for Neo Geo support: https://github.com/tmcleroy/cps2recomp/issues/139
- **AlmazProud/metal-slug-5-recomp**: https://github.com/AlmazProud/metal-slug-5-recomp — same protection as our games (NEO-PVC, CMC50, PCM2), with clean-room decryption.

## Engines and data / Motores e dados

- **Strong hypothesis (SuperCombo Wiki):** SVC Chaos was built on the KOF 2003 engine. If true, correlating the games should be much more direct. https://wiki.supercombo.gg/w/SvC_Chaos:_SNK_Vs_Capcom
- **peon2/fbneo-training-mode**: memory addresses and training mode. Supports kof2003; check svc. https://github.com/peon2/fbneo-training-mode
- **Hitbox scripts:**
  - dev-dem/kof-training-mode-FBNeo: https://github.com/dev-dem/kof-training-mode-FBNeo
  - Jesuszilla/mame-rr-scripts: source for understanding the hitbox format.

## Tools / Ferramentas

- **GekkoNet** (BSD-2): C/C++ P2P rollback SDK. https://github.com/HeatXD/GekkoNet
- **city41/mameneogeodevplugin**: Lua MAME plugin exposing Neo Geo internals.
- **city41/neospriteviewer**: tile viewer.
- **Shigeshigeru/kof2003chaosPconv**: P-ROM encryption for KOF 2003 and SVC. https://github.com/Shigeshigeru
- **Icedomega13/StrikeHDCollection** (wiki): https://github.com/Icedomega13/StrikeHDCollection/wiki (relevance to be checked).
- **Hardware reference:** MAME's neogeo driver (GPL). Study, do not copy, until the licence is decided.

## Other sources of the games / Outras fontes dos jogos

- **SVC Chaos by Code Mystics (2024, Steam/GOG):** official port with rollback. Check whether the PC release ships the MVS data and could serve as an alternative to dumps, the way Metal Slug ports use the GOG releases.

## Hint for the 1v1 ticket / Pista para o ticket 1x1

- Console versions of KOF 2003 have a mode without the switch (Team Play).
