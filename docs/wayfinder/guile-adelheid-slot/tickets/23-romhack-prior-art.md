---
id: 23
title: "What documented ROM hacks learned about adding fighters and growing graphics"
label: wayfinder:research
mode: AFK
status: closed
assignee: owner
blocked_by: []
research: research/23-romhack-prior-art:docs/wayfinder/guile-adelheid-slot/research/23-romhack-prior-art.md
---

## Question

Documented ROM hacks of KOF 2002 added fighters that come from other platforms (the owner names King and Geese, which exist only on the PS2), and hacks of KOF 2003 and SVC Chaos released or added fighters. What did they document about free fighter IDs and slots, the selection screen, palettes, sounds, and how they fit more graphics than the original graphics ROM held? Which of those facts hold for KOF 2003 and which only for KOF 2002?

Read only published documentation, tables and write-ups; do not download modified ROMs. List only facts that change an open ticket on this map (06, 07, 08, 22) or the graphics growth already chosen in [19](19-guile-tile-placement.md), and mark each one *unverified* with its source. A fact is verified only when measured in MAME or in the port. The hacks patch the original ROM, while this project's limit is the port generator, so say where a hack's solution cannot be copied.

_PT-BR: hacks documentados do KOF 2002 adicionaram lutadores vindos de outras plataformas (o dono cita King e Geese, só do PS2), e hacks do KOF 2003 e do SVC Chaos liberaram ou adicionaram lutadores. O que documentaram sobre IDs e vagas livres, tela de seleção, paletas, sons e sobre como couberam mais gráficos do que a ROM gráfica original tinha? O que vale para o KOF 2003 e o que só para o KOF 2002? Ler só documentação, tabelas e textos publicados; não baixar ROMs modificadas. Listar só fatos que mudam um ticket aberto do mapa (06, 07, 08, 22) ou o crescimento gráfico já escolhido no 19, cada um marcado como *não verificado* com a fonte. Um fato só é verificado quando medido no MAME ou no port. Os hacks alteram a ROM original e o limite deste projeto é o gerador do port; dizer onde a solução de um hack não pode ser copiada._

## Resolution

**Almost nothing documented by hack authors exists; four facts are worth carrying, all *unverified* (web sources, nothing measured in MAME or in the port).** Findings: `research/23-romhack-prior-art:docs/wayfinder/guile-adelheid-slot/research/23-romhack-prior-art.md` (read with `git show`).

What was not found: any readme, forum thread or wiki by a hack author on free fighter IDs, table sizes, `$24`-style guards, selection-cell counts, palettes, sounds or frame and collision formats, for KOF 2002 (King and Geese), KOF 2003 or SVC Chaos. No KOF 2003 or SVC hack adds a fighter as a new ID. What exists is ROM file lists in the FBNeo and MAME drivers, Neo Geo Dev Wiki pages and catalog pages, so everything else is inference from file sizes. Nothing here changes tickets 08 or 22 firmly.

Facts that bear on the map:

- **[Choose where Guile's tiles go in the graphics files](19-guile-tile-placement.md):** (1) 128 MiB is the ceiling of the game's own 20-bit tile number; going past it needs bankswitching the game code does not have. The added 64 MiB holds about 57 Guile-sized blocks, against about 236,600 tiles for all 26 Exclusive Characters (approximate; ticket 21 sizes Guile). (2) Hack sets above 64 MiB exist only on sister engines (KOF 2002 and 2001 at 80 to 112 MiB, KOF '98 and '99 at 80 to 96 MiB) and only in emulator; no KOF 2003 or SVC set passes 64 MiB, so KOF 2003 would be first, which agrees with [How Neo Geo recompilation projects grew past a 64 MB graphics set](24-recomp-growth-prior-art.md). (3) Their extra chips follow the original eight, so new tiles start at `$80000`, the range 19 already plans. (4) The FBNeo and MAME loaders pad the set to the next power of two and treat the tail as transparent: if the new total is not a power of two, pad the decoded buffer or size the set to exactly 128 MiB.
- **[Choose how fighter slots are found for the SVC Exclusive Characters](06-slot-strategy.md):** hacks give no help choosing between relocating tables, renumbering objects or widening the ID. Expect gaps in boss sound and quote data when counting which of the 26 can be imported (an SVC unlock hack reports Geese's and Zero's sounds missing); check per fighter, as ticket 05 did for Guile. A KOF 2002 hack lists some characters more than once, but whether those are separate IDs or data swaps is not documented.
- **[How KOF 2003's selection screen maps cells and codes to fighter IDs](02-selection-screen.md) / ticket 07:** a KOF 2003 hack makes the hidden fighters selectable on MVS with the original program and graphics sizes, so releasing existing hidden IDs needs no growth; how it did so is not documented, and nothing shows a cell for a new ID above `$24`. The only redrawn selection grid is a KOF 2002 hack's.
- **Lead only, not acted on (ticket 22 is closed):** a catalog page says the KOF 2003 final boss depends on how mid-boss Kusanagi is beaten, which hints that one of the unmeasured bytes `$107D64`/`$107D66` carries a "how the mid-boss ended" branch.

Cannot be copied: hacks patch the original ROM on emulator loaders; here new code must live in the fixed 1 MB or the first banked MB ([How the native port's generator handles changed or added 68000 code and data](04-port-generator.md)), graphics growth is the fixed `crom_size` plus C-file pairs, not chips added to a set, and real-board limits (64 MiB decryption window, 96 MB PCB) do not apply to the port.

**PT-BR**

**Não há quase nada documentado pelos autores de hacks; quatro fatos valem ser levados, todos *não verificados* (fontes da web, nada medido no MAME nem no port).** Achados: `research/23-romhack-prior-art:docs/wayfinder/guile-adelheid-slot/research/23-romhack-prior-art.md` (ler com `git show`).

Não achei nenhum readme, tópico de fórum ou wiki de autor de hack sobre IDs livres, tamanho de tabelas, verificações de `$24`, número de células de seleção, paletas, sons ou formato de quadros e colisão, nem para o KOF 2002 (King e Geese), nem para o KOF 2003, nem para o SVC Chaos. Nenhum hack do KOF 2003 ou do SVC adiciona lutador como ID novo. O que existe são listas de arquivos nos drivers do FBNeo e do MAME, páginas do Neo Geo Dev Wiki e de catálogo, então o resto é inferência a partir de tamanhos. Nada aqui muda de forma firme os tickets 08 e 22.

Fatos que pesam no mapa:

- **Ticket 19:** (1) 128 MiB é o teto do número de tile de 20 bits do jogo; passar disso exige troca de banco que o código do jogo não tem. Os 64 MiB acrescentados comportam cerca de 57 blocos do tamanho do Guile, contra cerca de 236.600 tiles dos 26 exclusivos (conta aproximada; o ticket 21 mede o Guile). (2) Hacks acima de 64 MiB só existem em motores irmãos (KOF 2002 e 2001 com 80 a 112 MiB, KOF 98 e 99 com 80 a 96 MiB) e só em emulador; nenhum conjunto do KOF 2003 ou do SVC passa de 64 MiB, então o KOF 2003 seria o primeiro, o que concorda com o ticket 24. (3) Os chips extras vêm depois dos oito originais, então os tiles novos começam em `$80000`, a faixa que o 19 já prevê. (4) Os carregadores do FBNeo e do MAME completam o conjunto até a próxima potência de 2 e tratam o resto como transparente: se o total novo não for potência de 2, completar o buffer decodificado ou dimensionar o conjunto em exatamente 128 MiB.
- **Ticket 06:** os hacks não ajudam a escolher entre mover tabelas, renumerar objetos ou alargar o ID. Esperar lacunas em sons e falas de chefes ao contar quais dos 26 podem ser importados (um hack do SVC que libera chefes reporta sons do Geese e do Zero ausentes); checar lutador a lutador, como o ticket 05 fez com o Guile. Um hack do KOF 2002 lista alguns personagens mais de uma vez, mas não se sabe se são IDs separados ou troca de dados.
- **Ticket 07 / pesquisa 02:** um hack do KOF 2003 deixa os lutadores ocultos selecionáveis no MVS com programa e gráficos do tamanho original, então liberar os IDs ocultos existentes não exige crescimento; como ele fez não está documentado, e nada mostra uma célula para ID novo acima de `$24`. A única grade de seleção redesenhada é de um hack do KOF 2002.
- **Só uma pista, sem ação (o ticket 22 está fechado):** uma página de catálogo diz que o chefe final do KOF 2003 depende de como o Kusanagi é derrotado, o que sugere que um dos bytes não medidos `$107D64`/`$107D66` guarda um ramo "como o chefe do meio terminou".

Não dá para copiar: hacks alteram a ROM original em carregadores de emulador; aqui o código novo precisa ficar no 1 MB fixo ou no primeiro MB com banco (pesquisa 04), o crescimento gráfico é o `crom_size` fixo mais pares de arquivos C, não chips acrescentados a um conjunto, e os limites da placa real (janela de 64 MiB da decriptação, PCB de 96 MB) não valem para o port.
