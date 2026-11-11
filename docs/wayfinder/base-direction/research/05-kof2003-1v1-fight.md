# Research: 1v1 fight in KOF 2003

Ticket 05. Question: does any version of KOF 2003 have a 1v1 fight, or is there a 1v1 feature in the MVS code? If KOF 2003 is the Base Game, how much does it cost to get 1v1 for the first tests?

Labels used below: **VERIFIED** = read directly in a primary or first-hand file (repo, cheat file, official page). **REPORTED** = stated by a secondary source (wiki, review, forum), not checked in the game. **UNKNOWN** = no source found. **GUESS** = our own reasoning, not sourced.

## Resumo (PT-BR)

- **Sim, existe 1v1 no KOF 2003, em dois lugares diferentes.**
  1. **Nas versões de PS2/Xbox (2004/2005)** há os modos "Single Play", "Single VS" e "Single Survival", descritos como o 1 contra 1 tradicional. Esses modos são **código novo da versão de console** (o PS2 é outro programa, com gráficos e cenários 3D novos). Não estão nos dados do MVS. (REPORTED)
  2. **No próprio MVS (fliperama)**, uma wiki japonesa diz que dá para ligar uma **"luta single" mudando uma configuração da placa** (as "soft DIPs", o menu de configurações do fliperama). Nesse modo cada lado tem **um só lutador**, com **3 barras de vida** (como um chefe), e a luta é de **um round só**. A exceção é a dupla Chizuru e Maki, que continua trocando. (REPORTED por uma única fonte; ainda não confirmado por nós.)
- **Se isso for confirmado, o 1v1 para os testes custa praticamente zero:** é só um valor de configuração. Num port nativo isso vira mudar um número numa tabela de configurações, sem programar nada.
- **Como confirmar (minutos, sem programar):** abrir o menu de configurações do jogo (o menu de soft DIPs da BIOS do MVS) num emulador ou na versão ACA NeoGeo da Hamster, que usa a ROM do MVS. Só vale com uma cópia legal do jogo, e ninguém da equipe deve baixar ROM.
- **Plano B, também barato:** os cheats do FBNeo para kof2003 já têm "Drain All Character (A/B/C) Energy Now!", que zera a vida de 2 dos 3 lutadores de cada time. Isso imita um 1v1, mas é gambiarra. O jogo dá barra de especial extra ao time que perde membros e pode reagir de forma estranha. (VERIFIED que o cheat existe; o efeito real é GUESS.)
- **O modo de treino do fbneo-training-mode para kof2003 não faz 1v1.** Ele dá tempo infinito, vida e barra recarregando, e mostra hitboxes, mas mantém os 3 lutadores e a troca. Serve para testar golpes, não para testar a regra do 1v1. (VERIFIED)
- **Não existe chave de debug conhecida que force 1 lutador por time.** As listas de debug DIPs conhecidas trazem hitboxes, invencibilidade e medidores, mas nada de tamanho de time. (REPORTED, e as listas estão incompletas.)
- **Opções caras:** copiar a lógica do modo Single do PS2 é a pior opção, porque seria engenharia reversa de outro programa, para outro processador. Escrever nosso próprio patch (time de 1 + regra de vitória + troca desligada) é viável, mas é GUESS de **dias a poucas semanas** depois que o port estiver rodando. Isso fica para depois dos testes, se o modo single do MVS não servir.
- **Caminho mais barato recomendado:** (1) confirmar a soft DIP "single" do MVS; (2) se não existir ou não servir, usar os cheats de "drenar vida" só para os testes; (3) só depois decidir se vale escrever um modo 1v1 próprio.

## Findings

### 1. Console versions and collections

**PS2 (JP 28 Oct 2004; NA Feb 2005 as part of the 2002/2003 bundle; PAL 2006) and Xbox (JP 25 Aug 2005; NA 2005)**
- Release dates: [Wikipedia](https://en.wikipedia.org/wiki/The_King_of_Fighters_2003). Wikipedia's own NA dates are inconsistent (infobox says Feb 2005, body says 2006), so treat the NA date as approximate.
- **Mode list (REPORTED).** A Japanese PS2 review lists 11 menu items: Arcade Play, Arcade VS, Team Play, Team VS, **Single Play, Single VS**, Team Survival, **Single Survival**, Practice, Gallery, Options. It states: "シングルは従来通りの1vs1。サバイバルも同様。" ("Single is the traditional 1vs1. Survival likewise.") [crymson.x0.com review](https://crymson.x0.com/nandemo/game/kof2003.html)
- A 2005 English review of the NA PS2 bundle corroborates this: "Arcade mode, Single mode, and Arcade and Single Vs. modes are all here… Team and Single Survival modes are here." [1Emulation review](https://www.1emulation.com/forums/topic/11857-021205-king-of-fighters-2002-and-2003-ps2/). A 2008 Yahoo! Chiebukuro question names "シングルサバイバルモード" on PS2. [Yahoo! Chiebukuro](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1421412434)
- **How the modes treat switch and Leader (REPORTED):**
  - *Arcade Play / Arcade VS*: same Multi-Shift and Leader rules as the MVS. The first character picked is the Leader. [crymson](https://crymson.x0.com/nandemo/game/kof2003.html)
  - *Team Play / Team VS*: classic round-based 3-on-3 with **no switching** ("交代行動と交代攻撃は使用できない"). **All three members can use the Leader super.** Sources: [crymson](https://crymson.x0.com/nandemo/game/kof2003.html), [atwiki gcmatome](https://w.atwiki.jp/gcmatome/pages/2393.html), [namu.moe](https://namu.moe/w/KOF2003)
  - *Single Play / Single VS / Single Survival*: 1 fighter per side, "traditional 1vs1". **No source says explicitly** whether the Leader super is usable there. Switching is implicitly absent because there is no partner. Leader super availability in Single modes: **UNKNOWN**.
  - *Practice*: on PS2 it is 3-on-3. Its "LeaderMax" gauge option lets all 3 act as leaders. [1Emulation](https://www.1emulation.com/forums/topic/11857-021205-king-of-fighters-2002-and-2003-ps2/)
- **Which modes put exactly one fighter per side in a round?** On PS2/Xbox, the Single modes do (REPORTED). Team Play keeps 3 per team but only one is on screen at a time, so each round is effectively 1v1, but the next member comes in after a KO (classic KOF elimination).
- **Is this console code or MVS data?** It is **console code (REPORTED / strong GUESS)**. The PS2/Xbox versions were rebuilt with "new high-quality graphics and 3D stages" [StrategyWiki](https://strategywiki.org/wiki/The_King_of_Fighters_2003), added an "arrange"/Normal mode with balance changes, and removed the arcade timer [atwiki](https://w.atwiki.jp/gcmatome/pages/2393.html), [namu.moe](https://namu.moe/w/KOF2003). They are not emulations of the MVS ROM, so the Single-mode logic lives in the PS2/Xbox executable. The Xbox version is grouped with PS2 by the atwiki, and it added colour edit and online play. Its exact mode list was not checked separately (**UNKNOWN** in detail).
- Re-releases of the PS2 build: PS2 "SNK Best Collection" (2006) and PS3 "Game Archives" (2015). [atwiki](https://w.atwiki.jp/gcmatome/pages/2393.html)

**ACA NeoGeo (Hamster; Switch / PS4 / Xbox One / Windows, from 21 Feb 2019)**
- **VERIFIED (official page):** "This title is based on the MVS (NEOGEO arcade) version". The page mentions only Multi-Shift 3-on-3, plus difficulty and "other settings" being changeable. No Single mode is advertised. [Hamster product page](https://hamster.co.jp/american_hamster/arcadearchives/switch/kof2003.htm)
- So ACA = MVS ROM + Hamster emulator. If the MVS "single battle" soft DIP exists (see §2), ACA's settings menu *may* expose it. That is **UNKNOWN**; the Hamster page doesn't list the settings.
- Amazon Prime Gaming / GOG PC release: a Japanese emulation blogger reports it is derived from the one-board PCB (MV-0) program, not AES. [shigeshige blog](https://sigeshigeru.hateblo.jp/entry/2023/11/18/211153) (REPORTED). No 1v1 mode is advertised (UNKNOWN).

### 2. MVS / AES code: settings, debug, cheats, training mode

**2a. MVS board setting ("soft DIP") for single battles — the key finding (REPORTED, single source)**
- The Japanese Game Catalog wiki states: "今作も基板の設定変更によりシングル戦が行えるが、やはりラウンド制ではなく、ボスのように1人で3本分の体力ゲージを持った1回勝負となっている。" This means: "As in previous entries, single battles can be enabled by changing the board settings. It is still not round-based: it is a one-bout match where one character has three health bars' worth of life, like a boss." It adds that the Chizuru & Maki pair still appears as a tag team that switches, even in single battles. [atwiki gcmatome — KOF2003](https://w.atwiki.jp/gcmatome/pages/2393.html)
- Mechanism (VERIFIED, from documentation of the hardware): MVS "software DIPs" are defined in the game's program header and edited in the MVS BIOS menu. They are saved in backup RAM and copied at boot to `BIOS_GAME_DIP` at **$10FD84–$10FD93**. **The AES does not offer them; it always uses the game's default values.** [NeoGeoDev: Software DIPs](https://wiki.neogeodev.org/index.php/Software_DIPs), [NeoGeoDev: BIOS RAM locations](https://wiki.neogeodev.org/index.php/BIOS_RAM_locations)
- Weak corroboration that a "single mode" exists inside the 2003 program: HBMAME lists fan hacks of the KOF 2003 code base titled "Kof2004 Hero (Single Mode Power Cauge)" and "Kof2004 EX Ultra Plus (Single Mode Power Cauge)". [HBMAME kof2003.cpp](https://github.com/Robbbert/hbmame/blob/master/src/hbmame/drivers/kof2003.cpp) (VERIFIED that the hack titles exist; what they change is UNKNOWN.)
- **Not yet verified by us:** the exact name of the setting, its position in the menu, whether the Leader super works in that mode, and how the win screen behaves. We found no English source listing KOF 2003's soft DIP menu, and the NEOGEO mini option menu for KOF 2003 is described as "very simple" with no list in text. [3KA blog](https://kikyou9drt.hatenablog.com/entry/2020/01/06/120045)
- **Consequence for the project:** if confirmed, the MVS program already contains code for "one fighter per side". In a native port that runs the original game logic, turning it on is a configuration value, not new code. It is **not** identical to SVC Chaos: it is one bout with triple health, while SVC uses round-based 1v1. For first tests that is probably fine.

**2b. Debug DIPs (REPORTED / partially VERIFIED)**
- Neo Geo debug DIPs are 2 bytes of game RAM used for developer options (job meters, hitboxes, invincibility). Only a debug BIOS, UniBIOS or emulators can set them. [NeoGeoDev: Debug DIPs](https://wiki.neogeodev.org/index.php/Debug_DIPs), [TCRF: Neo Geo](https://tcrf.net/Neo_Geo)
- Community list for KOF 2003 (incomplete): 1-4 hitboxes; 1-6 both invincible; 1-7 human invincible; 2-1 and 2-3 data meter; 2-4 hex edit; the rest "?". **Nothing about team size, single battle or disabling the switch.** [1Emulation thread](https://www.1emulation.com/forums/topic/25082-dip-switches-in-kawaks-for-king-of-fighters-2001-and-on/). The neo-geo.com debug-dip catalogue stops at KOF 2000. [neo-geo.com KOF dip codes](https://neo-geo.com/snk/dipcodes/kof.html)
- The FBNeo cheat "DIP= 1-6 Infinite Energy" writes a bit at **$107800**, which suggests KOF 2003's debug-DIP bytes live around $107800–$107801 (GUESS, inferred from the cheat).

**2c. Cheat databases (VERIFIED — FBNeo cheat file read directly)**
File: `cheats/kof2003.ini` in [FBNeo-cheats](https://github.com/finalburnneo/FBNeo-cheats) (cloned 2026-11-11). Relevant entries (names and RAM addresses only):
- "Drain All Character (A/B/C) Energy Now! PL1/PL2": sets each team slot's health to 0. P1 slots $2FE91D / $2FEA1D / $2FEB1D; P2 slots $2FED1D / $2FEE1D / $2FEF1D.
- "Infinite Character (A/B/C) Energy", "Infinite Battle Time" ($107D62), "Finish this Round Now!".
- "Select Character (A/B/C) PL1/PL2": slot character IDs around $107D0C onward.
- "Set Leader change Now!" (P1 $107D18, P2 $107D19; values High/Middle/Low = slot 0/1/2).
- "Always Possible Change" (P1 $2FE806–$2FE807, P2 $2FEC06–$2FEC07), "Never Faint", "Always have Maximum POW".
- "Select Cartridge/NeoGeo Type": Arcade (MVS) / Home (NEOGEO), via $10FD82, which is the documented BIOS_MVS_FLAG. [NeoGeoDev](https://wiki.neogeodev.org/index.php/BIOS_RAM_locations)
- "DIP(DEBUG)= Boss Code" (writes at $10FE80, which NeoGeoDev documents as BIOS_DEVMODE, so the label is the cheat author's).
- **There is no cheat that sets team size to 1 or disables switching.** The closest is draining slots B and C at the start of the fight (a pseudo-1v1). What the game does then is a **GUESS**: probably it treats those members as defeated. That would also trigger the documented handicap: "when a team loses a member, their gauge capacity increases by one" ([Wikipedia](https://en.wikipedia.org/wiki/The_King_of_Fighters_2003)), so both sides would play with 2 extra gauge stocks.
- MAME/Pugsy XML cheat file for kof2003: it exists ("made by Pugsy", per the cheat credits file in [libretro/mame2010-libretro](https://github.com/libretro/mame2010-libretro)), but we could not download the current XML (the mamecheat.co.uk links go through mega.nz and the site refused fetch). Its contents are **UNKNOWN**. The legacy MAME 0.78 cheat.dat has no kof2003 entry.
- HBMAME hacks of interest: "Always Change Ok", "Enable Kagura-Twins, Adel or Mukai To Be a Team Leader", "Unlock Leader Special Move". None is a 1v1 hack. [HBMAME kof2003.cpp](https://github.com/Robbbert/hbmame/blob/master/src/hbmame/drivers/kof2003.cpp)

**2d. AES (home) mode of the same ROM**
- Same program; the BIOS flag at $10FD82 selects AES or MVS behaviour (VERIFIED: flag documented; cheat exposes it). On AES, soft DIPs are not editable, and the defaults are used. [NeoGeoDev](https://wiki.neogeodev.org/index.php/Software_DIPs) So the MVS "single battle" setting is **not reachable from the AES menu** unless the defaults already enable it (GUESS: they don't).
- The AES mode adds a Practice mode, described as the worst in the series: you cannot exit without a reset, and the dummy's health does not refill. [namu.moe](https://namu.moe/w/KOF2003) (REPORTED). A Single VS mode on AES is **UNKNOWN** (no source found).

**2e. fbneo-training-mode (VERIFIED — repo read)**
- `games/kof2003/kof2003.lua` in [peon2/fbneo-training-mode](https://github.com/peon2/fbneo-training-mode) supports kof2003 with: health and meter refill per player, infinite time (writes $107D62), facing and hitstun detection, combo counter, and hitboxes (changelog: "kof2003: Added hitboxes").
- It **keeps the 3-member team**. It reads which slot is on point each frame (P1 $107D1A, P2 $107D1B) and indexes the 3-entry health arrays. It **does not** change team size, disable the switch or change the win condition.
- **Verdict:** it gives "endless practice, one fighter at a time on screen" inside the FBNeo emulator. It is good for checking moves and hitboxes, not a 1v1 rule. It runs only inside FBNeo (Lua), so it does not carry over to a native port.

### 3. Cost if KOF 2003 is the Base Game

See the table below. In short: the MVS single-battle soft DIP (if confirmed) is close to free. Cheats are a free test hack. A real SVC-style 1v1 (round-based, no switch, no team) needs our own change to the game rules, and copying the PS2 mode is not worth it.

## Cost options

| Option | What it gives | Effort | Risk | Evidence |
|---|---|---|---|---|
| **(a1) MVS soft DIP "single battle"** | 1 fighter per side, 1 bout, triple health; Chizuru & Maki still tag. Original game code, no patch. In a native port: set a config byte (in the $10FD84 block) or a menu option. | Verify: ~1 hour with a legal copy (emulator BIOS menu or ACA settings). Use: ≈ zero. | Medium: single secondary source; exact setting name and Leader behaviour unknown; not round-based like SVC. | REPORTED: [atwiki](https://w.atwiki.jp/gcmatome/pages/2393.html); mechanism VERIFIED: [NeoGeoDev](https://wiki.neogeodev.org/index.php/Software_DIPs) |
| **(a2) Existing cheats (drain slots B and C at fight start)** | Pseudo-1v1: only slot A left per side. Can add "Infinite Battle Time" and "Select Character". | ≈ zero (FBNeo cheat menu, or poke the same RAM addresses in the port). | Medium-high: side effects GUESSED (gauge handicap +2 stocks, KO/win-screen glitches); 3 health bars still shown; not a real mode. | VERIFIED cheat entries: [FBNeo-cheats kof2003.ini](https://github.com/finalburnneo/FBNeo-cheats) |
| **(a3) Debug DIPs** | Hitboxes, invincibility, meters. **No 1v1.** | ≈ zero | n/a for 1v1 | REPORTED, incomplete: [1Emulation](https://www.1emulation.com/forums/topic/25082-dip-switches-in-kawaks-for-king-of-fighters-2001-and-on/) |
| **(b) fbneo-training-mode** | Infinite time, refill, hitboxes, one fighter on screen at a time; team of 3 and switching remain. | ≈ zero (emulator only) | Low, but does not answer "1v1 rules" and is not part of a native port. | VERIFIED: [repo](https://github.com/peon2/fbneo-training-mode) |
| **(c) Port PS2 "Single Play" logic** | True round-based 1v1 as SNK designed it for console. | High: reverse-engineering a different program (PS2 MIPS executable, different engine build), then translating to the MVS logic. Weeks to months (GUESS). | High: technical (two different code bases) and legal/IP (a second commercial program). | Modes REPORTED: [crymson](https://crymson.x0.com/nandemo/game/kof2003.html), [1Emulation](https://www.1emulation.com/forums/topic/11857-021205-king-of-fighters-2002-and-2003-ps2/) |
| **(d) Own patch in the port (team size 1 + win condition + switch off)** | Exactly what we want (e.g. SVC-like rounds), under our control. | Medium: GUESS of days to a few weeks once the port runs. The known RAM map (slots, health, leader, change flags, active slot) is a head start; the round/win flow must still be found. | Medium: side effects on gauge handicap, Leader super, win poses, endings, CPU AI and the Chizuru & Maki boss. | RAM addresses VERIFIED from cheat/training files; effort GUESS |

**Plain-language consequences (for the owner):**
- If (a1) is confirmed, choosing KOF 2003 as Base does **not** block 1v1 tests. The 1v1 already exists in the arcade program; we just switch it on. The look will be "one fighter with triple health, one bout", not SVC's rounds.
- (a2) and (b) are fine for quick experiments in an emulator but are tricks, not features. Results from them (balance, gauge) can mislead.
- (c) is the most expensive and least useful path. Skip it.
- (d) is what we would do eventually if we want a clean SVC-style 1v1 inside a KOF-based port. It is real programming work, best done after the port runs and only if (a1) isn't good enough.

## Open questions

1. **Confirm the MVS soft DIP**: its exact name and options, its behaviour (rounds, triple health, Leader super, switch disabled?), and whether CPU opponents in arcade mode also become single. Method: open the MVS BIOS "game settings" for kof2003 in an emulator, or check the ACA settings menu, using a legal copy (no ROM downloads).
2. Is that setting exposed in ACA NeoGeo's settings menu (Hamster says "difficulty and other settings")?
3. Does the AES mode have any Single VS? (No source found.)
4. Exact behaviour of the "drain B/C" cheat at round start: auto-KO, gauge handicap, win screen.
5. In PS2/Xbox Single modes, is the Leader super available? Rounds per match?
6. Contents of Pugsy's current MAME XML cheat for kof2003 (could not obtain): does it have a "1 character per team" or "single mode" cheat?
7. What do the HBMAME "Single Mode Power Gauge" hacks change? This would confirm that a single mode exists in the 2003 code base and how the gauge behaves in it.

## Sources

- Wikipedia, The King of Fighters 2003 — https://en.wikipedia.org/wiki/The_King_of_Fighters_2003
- StrategyWiki, The King of Fighters 2003 — https://strategywiki.org/wiki/The_King_of_Fighters_2003
- Game Catalog @Wiki (atwiki gcmatome), THE KING OF FIGHTERS 2003 — https://w.atwiki.jp/gcmatome/pages/2393.html
- crymson.x0.com, KOF2003 (PS2) review — https://crymson.x0.com/nandemo/game/kof2003.html
- 1Emulation, KOF 2002 & 2003 PS2 review (2005) — https://www.1emulation.com/forums/topic/11857-021205-king-of-fighters-2002-and-2003-ps2/
- Yahoo! Chiebukuro, PS2 KOF2003 Single Survival question — https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1421412434
- namu.moe (Namuwiki mirror), KOF2003 — https://namu.moe/w/KOF2003
- GameSpot reviews (PS2 and Xbox bundles) — https://www.gamespot.com/reviews/the-king-of-fighters-2002-and-2003-review/1900-6118481/ ; https://www.gamespot.com/reviews/the-king-of-fighters-02-03-review/1900-6132643/
- Hamster, ACA NEOGEO THE KING OF FIGHTERS 2003 (Switch) — https://hamster.co.jp/american_hamster/arcadearchives/switch/kof2003.htm
- shigeshige blog (Prime Gaming / ACA set notes) — https://sigeshigeru.hateblo.jp/entry/2023/11/18/211153
- 3KA blog, NEOGEO mini option menus — https://kikyou9drt.hatenablog.com/entry/2020/01/06/120045
- NeoGeoDev Wiki: Software DIPs — https://wiki.neogeodev.org/index.php/Software_DIPs ; BIOS RAM locations — https://wiki.neogeodev.org/index.php/BIOS_RAM_locations ; Debug DIPs — https://wiki.neogeodev.org/index.php/Debug_DIPs
- TCRF, Neo Geo — https://tcrf.net/Neo_Geo
- 1Emulation, debug DIPs for KOF 2001–2003 — https://www.1emulation.com/forums/topic/25082-dip-switches-in-kawaks-for-king-of-fighters-2001-and-on/
- neo-geo.com debug DIP codes, KOF — https://neo-geo.com/snk/dipcodes/kof.html
- FBNeo cheats repo (`cheats/kof2003.ini`, `cheats/kof2003h.ini`) — https://github.com/finalburnneo/FBNeo-cheats
- fbneo-training-mode (`games/kof2003/kof2003.lua`, `changelog`) — https://github.com/peon2/fbneo-training-mode
- HBMAME kof2003 driver (hack list) — https://github.com/Robbbert/hbmame/blob/master/src/hbmame/drivers/kof2003.cpp
- libretro mame2010 cheat credits (Pugsy kof2003 entry) — https://github.com/libretro/mame2010-libretro

## Addendum: owner's checks (2026-11-11)

Checked by the owner on his own cartridge set (MAME `kof2003`, NGM-2710 Export, verified good by MAME 0.289), running in MAME 0.289 and Fightcade FBNeo.

- **MVS soft DIPs, Europe BIOS:** 10 items: PLAY TIME, DEMO SOUND, HOW TO PLAY, DIFFICULTY, VERSUS LIMIT, CONT. SERVICE, CREDIT/LEVEL, BLOOD/FLASH, LANGUAGE, COUNTRY. **No single-battle item.** (VERIFIED)
- **MVS soft DIPs, Japan BIOS (`-bios japan`):** the same items in Japanese (プレイタイム, デモサウンド, 遊び方説明, 難易度, たいせんせいげん, コンティニュー/サービス, クレジット/レベル, しゅっけつ/フラッシュ, …). **No single-battle item** among those seen; the bottom of the list was not captured. (VERIFIED, partial)
- **Console (AES) mode via Universe BIOS 4.0:** the owner saw a **single** option in the game's menu. How it plays (one fighter per side, rounds or one bout, health) is **not yet confirmed**. (VERIFIED that the option exists; behaviour UNKNOWN)
- **Consequence:** the claim that the MVS game settings have a single battle is **not supported** for the Export set; the 1v1 path is the cartridge's own console (AES) mode. Confirming its behaviour is the remaining step when this ticket is reviewed.

_PT-BR: conferido pelo dono com o próprio romset (kof2003 Export, MAME 0.289 diz que está bom). Nas configurações do fliperama (BIOS europeia e japonesa) não há luta single. No modo console (AES), via Universe BIOS, o dono viu uma opção single no menu; falta confirmar como ela funciona (um lutador por lado, rounds ou luta única, vida). O caminho para o 1x1 é o modo console do próprio cartucho._
