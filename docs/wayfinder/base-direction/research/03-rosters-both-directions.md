# Research: Rosters in both directions

Ticket 03. Scope: Neo Geo MVS (arcade) releases of *The King of Fighters 2003* (NGM-271, 2003) and *SNK vs. Capcom: SVC Chaos* (NGM-269, 2003). Console releases are listed separately and not counted.

## Resumo (PT-BR)

- **KOF 2003 (MVS) tem 34 lutadores jogáveis.** São 30 lutadores em 10 times de 3, mais Kyo e Iori, que ficam fora dos times ("edit characters"), mais 2 secretos liberados por código na tela de seleção: **Kusanagi** (clone de Kyo e chefe do meio do jogo) e **Chizuru Kagura** (que também é chefe, junto com a irmã Maki).
  - Contagem ponderada (chefe vale 0,5): **33,0**. Se Chizuru contar como lutadora comum, fica 33,5.
  - Os chefes finais **Adelheid** e **Mukai** só podem ser jogados no PS2 e no Xbox. Não achei nenhuma trapaça documentada que os libere no fliperama, então ficaram fora da conta.
- **SVC Chaos tem 36 lutadores no total:** 24 normais (12 SNK e 12 Capcom) e 12 chefes ou subchefes.
  - **Num MVS comum dá para jogar com 32.** São os 24 normais mais 8 subchefes liberados por código: Geese, Goenitz, Mars People, Orochi Iori, Dan, Demitri, Zero e Violent Ken. Contagem ponderada: **28**.
  - **Shin Akuma e Serious Mr. Karate** só têm código no cartucho doméstico (AES). **Athena e Red Arremer** não têm código nenhum no fliperama nem no AES. No hardware de fliperama, esses 4 só ficam jogáveis com trapaça ou com um cartucho pirata modificado ("SVC Chaos Super Plus").
  - Contando tudo: **36 brutos / 30 ponderados**. Eles aparecem separados nas tabelas.
- **Personagens compartilhados (estão nos dois jogos): 6.** São Kyo, Iori, Terry, Ryo, Kim e Mai. O número é o mesmo nas duas direções.
  - **Atenção:** "compartilhado" quer dizer o mesmo personagem, não os mesmos arquivos. Os sprites, os golpes e o sistema de luta do SVC são outros. Mesmo um personagem compartilhado vai precisar de ajuste.
- **Direção A (Base = KOF 2003, Doador = SVC):** é preciso importar **30 exclusivos** (24 ponderados). São os 18 lutadores normais que faltam (todos os 12 da Capcom, mais Choi, Earthquake, Genjuro, Shiki, Kasumi e Mr. Karate) e os 12 chefes.
  - Se a conta ficar só no que o MVS comum libera: 26 exclusivos (22 ponderados).
- **Direção B (Base = SVC, Doador = KOF 2003):** é preciso importar **28 exclusivos** (27 ponderados). São 26 lutadores normais mais Kusanagi e Chizuru.
  - Se Adelheid e Mukai (só de console) também entrassem, seriam 30 (28 ponderados).
- **Mesmo nome, personagens diferentes:** a **Athena do SVC é a Princesa Athena original, do jogo *Athena* de 1986.** A Athena do KOF 2003 é a **Athena Asamiya**. Por isso as duas não contam como compartilhadas.
- **Versões alternativas:** Orochi Iori, Violent Ken, Shin Akuma e Serious Mr. Karate ocupam vaga própria e têm golpes próprios. Aqui eles contam como exclusivos.
  - Exemplo: se o dono preferir contar o Orochi Iori como "o mesmo Iori", a Direção A passa a ter 7 compartilhados e 29 exclusivos.
- **Diferença prática:** a Direção B (SVC como base) pede um pouco menos de importação em números brutos (28 contra 30). Mas a Direção A importa muitos chefes, que pesam menos. Na conta ponderada a Direção A fica mais leve: 24 contra 27.

## Findings

Status legend:
- **VERIFIED**: two independent sources agree, or a primary source confirms it.
- **REPORTED**: only one secondary source, or several sources that come from the same lineage (for example, MAME `history.dat` mirrors).
- **UNKNOWN**: not established.

Source keys refer to `## Sources`. All wiki and fan sites are secondary.

**Weighting rule used:** every fighter that serves as a sub-boss or boss in the MVS 1P mode gets weight 0.5, even if a code also makes it selectable. Everyone else gets 1.0.

### Table 1: KOF 2003 (MVS) roster

KOF 2003 has 3-on-3 free selection. Team names come from the extended-ending team list.

| # | Fighter | Team / side | How playable on MVS | Boss? (weight) | Status / source |
|---|---|---|---|---|---|
| 1 | Ash Crimson | Hero Team | Regular | No (1) | VERIFIED [W03][GDB03][FG03] |
| 2 | Duo Lon | Hero Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 3 | Shen Woo | Hero Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 4 | Terry Bogard | Fatal Fury Team | Regular | No (1) | VERIFIED [GDB03][FG03] |
| 5 | Joe Higashi | Fatal Fury Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 6 | Tizoc (JP: Griffon Mask) | Fatal Fury Team | Regular | No (1) | VERIFIED [GDB03][FAN03][EX03] |
| 7 | Ryo Sakazaki | Art of Fighting Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 8 | Robert Garcia | Art of Fighting Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 9 | Yuri Sakazaki | Art of Fighting Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 10 | Leona Heidern | Ikari Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 11 | Ralf Jones | Ikari Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 12 | Clark Still | Ikari Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 13 | Kim Kaphwan | Korea Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 14 | Chang Koehan | Korea Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 15 | Jhun Hoon | Korea Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 16 | King | Women Fighters Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 17 | Mai Shiranui | Women Fighters Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 18 | Blue Mary | Women Fighters Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 19 | Billy Kane | Outlaw Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 20 | Ryuji Yamazaki | Outlaw Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 21 | Gato | Outlaw Team | Regular | No (1) | VERIFIED [GDB03][FG03][FAN03] |
| 22 | Benimaru Nikaido | Japan (Benimaru) Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 23 | Shingo Yabuki | Japan (Benimaru) Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 24 | Goro Daimon | Japan (Benimaru) Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 25 | Athena Asamiya | High School Girls Team | Regular | No (1) | VERIFIED [W03][GDB03][FAN03] |
| 26 | Hinako Shijou | High School Girls Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 27 | Malin | High School Girls Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 28 | K' | K' Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 29 | Maxima | K' Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 30 | Whip | K' Team | Regular | No (1) | VERIFIED [W03][GDB03] |
| 31 | Kyo Kusanagi | "Edit" single entry; part of the Sacred Treasures extended-ending team | Regular (on the select screen, not in a team) | No (1) | VERIFIED [MOBY03][W03] |
| 32 | Iori Yagami | "Edit" single entry; part of the Sacred Treasures extended-ending team | Regular (on the select screen, not in a team) | No (1) | VERIFIED [MOBY03][W03] |
| 33 | Kusanagi ("Evil Kusanagi", Kyo clone) | Hidden | **Code** at character select: hold Down, rotate the stick clockwise to Up-Left, then counter-clockwise to Up-Right, then press any button | **Yes**: mid-boss whose KO method picks the final route (0.5) | Hidden-by-code: VERIFIED [TVT03][MOBY03][AH03]. Exact input: REPORTED (history.dat lineage: [AH03][GDB03][EX03]) |
| 34 | Chizuru Kagura | Hidden; Sacred Treasures team for extended ending | **Code** at character select: hold Up, rotate the stick counter-clockwise to Up-Right, then clockwise to Down-Left, then press any button. history.dat labels this "Chizuru and Maki" | **Yes**: on the DM route she is a boss alongside Maki's image, before Mukai (0.5; see Open questions) | Hidden-by-code: VERIFIED [TVT03][MOBY03][GB-CHIZ]. Exact input: REPORTED (history.dat lineage) |

**Fighters not playable on stock MVS (not counted, listed for completeness):**

| Fighter | Role on MVS | How playable anywhere | Status / source |
|---|---|---|---|
| Adelheid Bernstein | Final boss (you reach him by KOing Kusanagi without a DM) | PS2/Xbox only: beat him in Arcade, then hold R1 on Iori. TCRF notes he "isn't normally playable" on Neo Geo. No documented MVS cheat found | VERIFIED console-only [TVT03][SW03][CCC03][CH03][TCRF03] |
| Mukai | True final boss (DM-KO route, after Chizuru & Maki) | PS2/Xbox only: beat him, then hold R1 on Kyo. No documented MVS cheat found | VERIFIED console-only [TVT03][SW03][CCC03][CH03] |
| Maki Kagura | Appears only as Chizuru's mirror-image partner in the boss fight | Not separately playable on any version found | REPORTED [TVT03][FAN03] |
| Rose Bernstein | Ending cameo only (voice-credited) | Never playable | REPORTED [W03][GDB03] |

### Table 2: SVC Chaos (MVS) roster

Side follows the game's SNK/Capcom split. Giant Bomb gives 18 per side: 12 regular plus 6 hidden on each side.

| # | Fighter | Side | How playable on MVS | Boss? (weight) | Status / source |
|---|---|---|---|---|---|
| 1 | Kyo Kusanagi | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC][SNK24] |
| 2 | Iori Yagami | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC] |
| 3 | Terry Bogard | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC][SNK24] |
| 4 | Mai Shiranui | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC][SNK24] |
| 5 | Kim Kaphwan | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC][GS-SVC] |
| 6 | Choi Bounge | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC] |
| 7 | Ryo Sakazaki | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC][GS-SVC] |
| 8 | Kasumi Todoh | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC][GS-SVC] |
| 9 | Mr. Karate (Takuma Sakazaki) | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC] |
| 10 | Earthquake | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC] |
| 11 | Genjuro Kibagami | SNK | Regular | No (1) | VERIFIED [PIX][GDB-SVC] |
| 12 | Shiki | SNK | Regular | No (1) | VERIFIED [GDB-SVC][SW-SHIKI] |
| 13 | Ryu | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC][SNK24] |
| 14 | Ken Masters | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 15 | Chun-Li | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC][SNK24] |
| 16 | Guile | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 17 | Dhalsim | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 18 | M. Bison (JP: Vega) | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 19 | Balrog (JP: M. Bison) | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 20 | Vega (JP: Balrog) | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 21 | Sagat | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 22 | Akuma (JP: Gouki) | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 23 | Hugo | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 24 | Tessa (JP: Tabasa) | Capcom | Regular | No (1) | VERIFIED [PIX][FAN-SVC] |
| 25 | Geese Howard | SNK (hidden) | **Code**: hold Start, then L, L, L, D, L, U, R, U, then press A | **Yes**: Stage 4 mid-boss (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 26 | Goenitz | SNK (hidden) | **Code**: hold Start, then D, D, D, R, D, L, L, L, then A | **Yes**: Stage 4 mid-boss (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 27 | Mars People | SNK (hidden) | **Code**: hold Start, then U, D, R, R, R, U, D, L, L, D, then A | **Yes**: Stage 4 mid-boss (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 28 | Orochi Iori (Iori in "Riot of the Blood") | SNK (hidden) | **Code**: hold Start, then U, U, U, D, L, R, D, L, then A | **Yes**: Stage 7 mid-boss on the "fought Capcom in Stage 6" route (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 29 | Dan Hibiki | Capcom (hidden) | **Code**: hold Start, then D, L×7, then A | **Yes**: Stage 4 mid-boss (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 30 | Demitri Maximoff | Capcom (hidden) | **Code**: hold Start, then R, R, R, L, U, R, D, U, then A | **Yes**: Stage 4 mid-boss (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 31 | Zero (*Mega Man Zero* version) | Capcom (hidden) | **Code**: hold Start, then U, R, R, L, L, D, U, U, U, R, then A | **Yes**: Stage 4 mid-boss (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC][GOG] |
| 32 | Violent Ken (brainwashed Ken) | Capcom (hidden) | **Code**: hold Start, then U, U, D, L, L, R, L, U, then A | **Yes**: Stage 7 mid-boss on the "fought SNK in Stage 6" route (0.5) | VERIFIED [GS-SVC][GDB-SVC][SWSVC] |
| 33 | Serious Mr. Karate (Shin Mr. Karate) | SNK (hidden) | **Not selectable on stock MVS.** The code works only on the AES home cart, in a short window near the end of the select timer. On arcade hardware he needs a cheat or the "Super Plus" bootleg hack. **Marked: cheat/AES-only tier** | **Yes**: Stage 8 boss (0.5) | VERIFIED [SWSVC][GS-SVC][AH-SVCPLUS][GB-SVC] |
| 34 | Shin Akuma (Shin Gouki) | Capcom (hidden) | **Not selectable on stock MVS.** Same situation as Serious Mr. Karate (AES code, 5-second window). **Marked: cheat/AES-only tier** | **Yes**: Stage 8 boss (0.5) | VERIFIED [SWSVC][GS-SVC][AH-SVCPLUS][GB-SVC] |
| 35 | Athena (Princess Athena, from *Athena*, 1986) | SNK (secret) | **Not selectable on MVS or AES by any code.** Playable on arcade hardware only via cheat or the "Super Plus" bootleg hack. **Marked: cheat/hack-only tier** | **Yes**: Stage 9 secret final boss (no rounds lost in Stages 1-7, none won by chip damage) (0.5) | VERIFIED [WSVC][GB-SVC][AH-SVCPLUS][SNK24] |
| 36 | Red Arremer (Firebrand) | Capcom (secret) | **Not selectable on MVS or AES by any code.** Same situation as Athena. **Marked: cheat/hack-only tier** | **Yes**: Stage 9 secret final boss ("Hell" route) (0.5) | VERIFIED [WSVC][GB-SVC][AH-SVCPLUS][SNK24] |

**Notes on Table 2:**
- **Stage 4 mid-boss.** It depends on performance: Zero or Mars People for the best performance, then Geese or Demitri, otherwise Dan or Goenitz [GDB-SVC][SWSVC].
- **Code timing.** [SWSVC] says the AES-only codes must be entered "before the timer reaches 10". [GS-SVC] calls it a 5-second window.
- **Athena's surname.** [GDB-SVC] calls SVC's Athena "Athena Asamiya". That conflicts with [EX-SVC] ("the original Athena character design"), [PIX] (a celestial princess who turns into a mermaid) and [SNK24]. Treated as an error in [GDB-SVC].

### Table 3: Direction A (Base = KOF 2003, Donor = SVC Chaos)

Every SVC fighter is checked against the KOF 2003 MVS roster in Table 1.

**Classification rule:**
- **Shared**: the same character already has its own playable slot in KOF 2003.
- **Exclusive**: everything else. This includes "variant" fighters (Orochi Iori, Violent Ken, Shin Akuma, Serious Mr. Karate). Each one has its own select slot and moveset in SVC, so it would need its own import even when the base character is shared.

| SVC fighter | Shared / Exclusive | Notes on version differences |
|---|---|---|
| Kyo Kusanagi | **Shared** | SVC's SNK fighters are drawn from their *KOF '98* incarnations [GB-SVC]. KOF 2003 has a newer Kyo. The sprites, moves and system are SVC's own, so expect a rebuild even though the identity is shared. KOF 2003's "Kusanagi" is a **different character** (a clone). |
| Iori Yagami | **Shared** | *KOF '98*-based in SVC [GB-SVC] and the 2003 version in KOF 2003. Different sprites and moves. |
| Terry Bogard | **Shared** | *KOF '98*-based in SVC [GB-SVC]. KOF 2003 has its own version. The look and move details were not cross-checked here. |
| Ryo Sakazaki | **Shared** | Different version and sprite set. |
| Kim Kaphwan | **Shared** | Different version and sprite set. |
| Mai Shiranui | **Shared** | Different version and sprite set. |
| Choi Bounge | Exclusive | Not in KOF 2003. |
| Earthquake | Exclusive | Not in KOF 2003. |
| Genjuro Kibagami | Exclusive | *Samurai Shodown* character. |
| Shiki | Exclusive | *Samurai Shodown 64* character. |
| Kasumi Todoh | Exclusive | Not in KOF 2003. |
| Mr. Karate | Exclusive | This is Takuma Sakazaki in a mask. Takuma is not in KOF 2003 either. |
| Ryu | Exclusive | Capcom. |
| Ken Masters | Exclusive | Capcom. |
| Chun-Li | Exclusive | Capcom. |
| Guile | Exclusive | Capcom. |
| Dhalsim | Exclusive | Capcom. |
| M. Bison | Exclusive | Capcom. |
| Balrog | Exclusive | Capcom. |
| Vega | Exclusive | Capcom. |
| Sagat | Exclusive | Capcom. |
| Akuma | Exclusive | Capcom. |
| Hugo | Exclusive | Capcom. |
| Tessa | Exclusive | Capcom (*Red Earth*). |
| Geese Howard (boss) | Exclusive | Not in KOF 2003. |
| Goenitz (boss) | Exclusive | Not in KOF 2003. |
| Mars People (boss) | Exclusive | Not in KOF 2003. |
| Orochi Iori (boss) | Exclusive (**variant of Shared Iori**) | Same person as Iori, but a separate slot and moveset. Counts as Shared only under the lenient rule. |
| Serious Mr. Karate (boss) | Exclusive (variant of Exclusive Mr. Karate) | Based on Mr. Karate's original *Art of Fighting* appearance [WSVC]. |
| Athena (boss) | Exclusive: **different character, same name** | Princess Athena (1986) is not KOF 2003's Athena Asamiya [EX-SVC][PIX]. |
| Dan Hibiki (boss) | Exclusive | Capcom. |
| Demitri Maximoff (boss) | Exclusive | Capcom (*Darkstalkers*). |
| Zero (boss) | Exclusive | The *Mega Man Zero* (GBA) version [GOG]. |
| Violent Ken (boss) | Exclusive (variant of Exclusive Ken) | Original SVC variant [WSVC]. |
| Shin Akuma (boss) | Exclusive (variant of Exclusive Akuma) | |
| Red Arremer (boss) | Exclusive | *Ghosts 'n Goblins* character. |

### Table 4: Direction B (Base = SVC Chaos, Donor = KOF 2003)

| KOF 2003 fighter | Shared / Exclusive | Notes on version differences |
|---|---|---|
| Kyo Kusanagi | **Shared** | See Table 3. |
| Iori Yagami | **Shared** | SVC also has Orochi Iori as a separate boss slot. |
| Terry Bogard | **Shared** | Different versions. |
| Ryo Sakazaki | **Shared** | Different versions. |
| Kim Kaphwan | **Shared** | Different versions. |
| Mai Shiranui | **Shared** | Different versions. |
| Athena Asamiya | Exclusive: **different character, same name** | SVC's Athena is Princess Athena. |
| Kusanagi (boss) | Exclusive | A Kyo clone, not Kyo. |
| Chizuru Kagura (boss) | Exclusive | |
| Ash Crimson, Duo Lon, Shen Woo | Exclusive (3) | |
| Joe Higashi, Tizoc | Exclusive (2) | |
| Robert Garcia, Yuri Sakazaki | Exclusive (2) | Ryo's family and friends. Ryo and Mr. Karate/Takuma are in SVC, but Yuri and Robert are not. |
| Leona, Ralf, Clark | Exclusive (3) | |
| Chang Koehan, Jhun Hoon | Exclusive (2) | |
| King, Blue Mary | Exclusive (2) | |
| Billy Kane, Ryuji Yamazaki, Gato | Exclusive (3) | Geese is in SVC, but Billy is not. |
| Benimaru, Shingo, Daimon | Exclusive (3) | |
| Hinako Shijou, Malin | Exclusive (2) | |
| K', Maxima, Whip | Exclusive (3) | |
| *Adelheid, Mukai (not MVS-playable, not counted)* | *(Exclusive if ever counted)* | Console-only playable. |

That is 26 regular exclusives plus 2 boss exclusives (Kusanagi, Chizuru).

### Counts

Weights: regular = 1, boss or sub-boss = 0.5.

**Total playable per game**

| Measure | KOF 2003 (MVS) | SVC Chaos (MVS) |
|---|---|---|
| Stock MVS, including code-unlocked | **34 raw / 33.0 weighted** (32 regular + 2 boss) | **32 raw / 28.0 weighted** (24 regular + 8 mid-boss) |
| Plus the AES-code tier (same cart, home mode; cheat on MVS) | n/a | +2 (Shin Akuma, Serious Mr. Karate): 34 / 29.0 |
| Plus the cheat/hack-only tier | +0. Adelheid and Mukai have no documented MVS cheat. If added: 36 / 34.0 | +2 (Athena, Red Arremer): **36 raw / 30.0 weighted** |
| Owner's headline ("every fighter playable in some way") | **34 / 33.0** | **36 / 30.0** (4 of them only through the AES or cheat tiers) |

**Shared and Exclusive by direction**

| Measure | Direction A (Base KOF 2003, Donor SVC) | Direction B (Base SVC, Donor KOF 2003) |
|---|---|---|
| Shared Characters | **6** (6.0 weighted) | **6** (6.0 weighted) |
| Exclusive Characters to import, headline | **30 raw / 24.0 weighted** (18 regular + 12 boss) | **28 raw / 27.0 weighted** (26 regular + 2 boss) |
| Exclusive, stock-MVS donor only | 26 raw / 22.0 weighted (drops Shin Akuma, Serious Mr. Karate, Athena, Red Arremer) | 28 / 27.0 (no change) |
| Exclusive, lenient variant rule (Orochi Iori = Iori) | 29 raw / 23.5 weighted; Shared = 7 | 28 / 27.0 (no change) |
| Exclusive, if console-only Adelheid and Mukai were counted | n/a | 30 raw / 28.0 weighted |

**Alternative weight for Chizuru:** if the owner treats Chizuru as a normal fighter (weight 1), KOF 2003 becomes 33.5 weighted and Direction B Exclusive becomes 27.5 weighted.

## Console-only additions (not counted)

| Release | What changes for the roster | Status / source |
|---|---|---|
| KOF 2003, PS2 (JP 2004) and Xbox; also the *KOF 2002 & 2003* bundle (NA 2005) | Adelheid and Mukai become playable after you beat them: hold R1 on Iori (Adelheid) or on Kyo (Mukai). Kusanagi and Chizuru are available from the start. There is also a fighting mode without Tag Shift. No brand-new characters were found | VERIFIED [TVT03][CCC03][CH03][SW03][FAN03] |
| KOF 2003, PS2 Classics on PSN (JP 2015) | Re-release of the PS2 version | REPORTED [FG03] |
| SVC Chaos, Neo Geo AES home cart (NGH-269, Nov 2003) | Same 8 codes as MVS, plus AES-only codes (5-second window) for Shin Akuma and Serious Mr. Karate. Athena and Red Arremer are still inaccessible | VERIFIED [SWSVC][GS-SVC][WSVC] |
| SVC Chaos, PS2 (JP Dec 2003) and Xbox (only Xbox in NA) | 10 hidden fighters selectable by holding R/R1 on a stand-in fighter (for example Ryu → Zero, Kyo → Geese, Kasumi → Serious Mr. Karate, Balrog → Shin Akuma). Athena and Red Arremer unlock by beating them in Survival mode | VERIFIED [SWSVC][GS-SVC][WSVC][GB-SVC] |
| SVC Chaos, 2024 re-release (Steam, Switch, PS4, GOG; ported by Code Mystics) | All 36 fighters accessible from the start. The SNK page says Athena and Red Arremer, "hidden characters in the arcade version", can be used from the start. Hidden fighters sit under the inner select columns and are reached by holding L/LB. Rollback netcode and a gallery were added | VERIFIED [SNK24][WSVC][GOG][YB] |
| Bootlegs/hacks (not official, not counted) | "SVC Chaos Plus" adds the mid-bosses to the select screen. "SVC Chaos Super Plus" adds all hidden fighters, including the four final bosses, but Geese's and Zero's sounds are missing. KOF 2003 hacks "KOF 2004 Plus / Ultra Plus" exist; their roster effect is UNKNOWN | REPORTED [AH-SVCPLUS][GB-SVC][EX03] |

## Open questions

1. **What does the KOF 2003 Chizuru code give on MVS?** It could be the standard Chizuru, or the boss "Chizuru & Maki" build: history.dat labels the code "Chizuru and Maki". The answer affects whether her weight should be 0.5 or 1, and whether Maki needs separate assets. UNKNOWN. An in-game check or a primary MVS instruction card is needed.
2. **Can Adelheid and Mukai be played on MVS through a documented cheat?** Examples would be a MAME `cheat.xml` character-select cheat, or proof that the MVS ROM holds complete playable data for them. Nothing was found, so they are not counted. TCRF only speculates that Adelheid "was to be playable" [TCRF03].
3. **Are Athena and Red Arremer complete as playable fighters in the MVS ROM?** The "Super Plus" bootleg suggests yes. Some sources hint at incomplete data, for example sounds missing for some hidden fighters in that hack. Needs a direct check (MAME notes or cheat files) before weighting them like other bosses.
4. **Does the AES tier count as MVS?** Shin Akuma and Serious Mr. Karate are reachable on the same cart only in AES/home mode. This needs an owner decision. The headline counts them, flagged separately.
5. **Variant rule.** Should Orochi Iori (and, in principle, Violent Ken, Shin Akuma and Serious Mr. Karate) count as "the same character" for Shared purposes? This document treats them as Exclusive because each has its own slot and moveset. The lenient numbers are shown above.
6. **No independent check of exact KOF 2003 code inputs.** All found copies come from the MAME `history.dat` lineage. That hidden-by-code access exists is confirmed independently ([TVT03], [MOBY03]).
7. **Primary documents not retrieved.** No SNK MVS instruction cards, manuals or MAME driver/cheat files were read in this pass. The SuperCombo/SRK wiki pages were blocked by an anti-bot wall. Recommended follow-up: the SuperCombo pages for both games, and a MAME cheat file read as text only (no ROMs).
8. **Version details for the 6 Shared fighters** (moves, look) were not cross-checked. "Shared" means only that the identity matches. The engines and sprite sets differ completely between the two games.

## Sources

Every source below is secondary unless stated otherwise. Pages were accessed on 2026-11-11 through a summarizing fetch tool, so quotations are as relayed by that tool.

- [W03] Wikipedia, "The King of Fighters 2003": https://en.wikipedia.org/wiki/The_King_of_Fighters_2003
- [WSVC] Wikipedia, "SNK vs. Capcom: SVC Chaos": https://en.wikipedia.org/wiki/SNK_vs._Capcom:_SVC_Chaos
- [AH03] Arcade-History, KOF 2003 [NGM-271] (history.dat lineage): https://www.arcade-history.com/game/3264/
- [GDB03] GamesDatabase, MAME ROM `kof2003` (history.dat lineage): https://www.gamesdatabase.org/mame-rom/kof2003
- [EX03] Exotica, Lost In Translation / KOF 2003 (history.dat lineage): https://www.exotica.org.uk/wiki/Lost_In_Translation/King_of_Fighters_2003,_The
- [MOBY03] MobyGames, KOF 2003 (arcade): https://www.mobygames.com/game/arcade/king-of-fighters-2003
- [FG03] Fighters Generation, KOF 2003: https://www.FightersGeneration.com/games/kof2003.html
- [TVT03] TV Tropes, KOF 2003: https://www.tvtropes.org/pmwiki/pmwiki.php/VideoGame/TheKingOfFighters2003
- [FAN03] SNK Wiki (Fandom), KOF 2003: https://snk.fandom.com/wiki/The_King_of_Fighters_2003
- [SW03] StrategyWiki, KOF 2003: https://strategywiki.org/wiki/The_King_of_Fighters_2003
- [CCC03] CheatCC, KOF 2003 PS2 unlockables: https://www.cheatcc.com/articles/king-of-fighters-2003-cheats-codes-cheat-codes-walkthrough-guide-faq-unlockables-for-playstation-2-ps2-psx2/
- [CH03] Critical Hits (PT-BR), KOF 2003 cheats: https://criticalhits.com.br/dicas/the-king-of-fighters-2003-cheats-codigos-dicas-e-desbloqueaveis/
- [TCRF03] The Cutting Room Floor, KOF 2003 (Neo Geo): https://www.tcrf.net/The_King_of_Fighters_2003_(Neo_Geo)/en
- [GB-CHIZ] Giant Bomb, Chizuru Kagura: https://giantbomb.com/wiki/Characters/Chizuru_Kagura
- [SWSVC] StrategyWiki, SVC Chaos / Secrets: https://strategywiki.org/wiki/SVC_Chaos:_SNK_vs._Capcom/Secrets
- [GS-SVC] GameSpot, SVC Chaos cheats (user-submitted; arcade, Neo Geo, PS2 and Xbox sections): https://www.gamespot.com/games/svc-chaos-snk-vs-capcom/cheats/
- [GDB-SVC] GamesDatabase, MAME ROM `svc` (history.dat lineage): https://gamesdatabase.org/mame-rom/svc
- [EX-SVC] Exotica, Lost In Translation / SvC Chaos: https://www.exotica.org.uk/wiki/Lost_In_Translation/SvC_Chaos_-_SNK_Vs._Capcom
- [PIX] Pixiv Encyclopedia (JP), "SVC": https://dic.pixiv.net/a/SVC
- [GB-SVC] Giant Bomb, SVC Chaos: https://giantbomb.com/wiki/Games/SVC_Chaos_SNK_vs_Capcom
- [FAN-SVC] SNK Wiki (Fandom), SVC Chaos: https://snk.fandom.com/wiki/SNK_vs._Capcom:_SVC_Chaos
- [SNK24] SNK official, SVC CHAOS (2024) product page. **Primary, official**: https://snk-corp.co.jp/us/games/svc
- [AH-SVCPLUS] Arcade-History, "SVC Chaos Super Plus" (bootleg): https://www.arcade-history.com/game/4965/
- [TCRF-SVC] The Cutting Room Floor, SvC Chaos (Neo Geo): https://new.tcrf.net/SvC_Chaos:_SNK_vs._Capcom_(Neo_Geo)
- [SW-SHIKI] StrategyWiki, SVC Chaos / Shiki character page (seen in search results only, not fetched): https://strategywiki.org/wiki/SVC_Chaos:_SNK_vs._Capcom/Shiki
- [GOG] GOG forum, "Hidden characters" (2024 release): https://gog.com/forum/snk_vs_capcom_svc_chaos/hidden_characters
- [YB] Yardbarker, SVC Chaos hidden characters (2024 release): https://www.yardbarker.com/video_games/articles/all_svc_chaos_snk_vs_capcom_hidden_characters_and_how_to_unlock_them/s1_17144_40649109
- Attempted but blocked by an anti-bot wall: SuperCombo/SRK wiki pages for both games (https://wiki.supercombo.gg/w/SNK_vs._Capcom:_SVC_Chaos, https://srk.shib.live/w/SvC_Chaos:_SNK_Vs_Capcom/FAQ).
