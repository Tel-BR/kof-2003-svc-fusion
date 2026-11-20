# Voice roles of Guile in SVC Chaos: MAME checklist (ticket 33)

_Versão em português do Brasil logo depois da versão em inglês._

## English

Goal: confirm in MAME which situation plays each of Guile's 38 enabled sound slots (rows 2496 to 2575, slots +0 to +79 in [research 30](../../../docs/wayfinder/guile-adelheid-slot/tickets/30-guile-svc-remaining-sounds.md)). The roles in that research are inferred; this run confirms or corrects them. You play; the script only listens. The log holds frame numbers, row numbers, sample address ranges and situation names, and stays under `private/`.

### Run

1. Open PowerShell in `tools\kof2003` of the repository.
2. Run `py -3 -m match.svc_voice_roles_report run`. MAME opens in a window with sound, SVC Chaos, Europe MVS BIOS, the same keys as the manual MVS runs ([`manual-p1.cfg`](../manual-p1.cfg)). If MAME is not at `%USERPROFILE%\MAME\mame.exe`, set `KOF2003_MAME` to its full path first.
3. Keys: `5` coin, `1` Start (also the taunt), `A` `S` `D` `Space` = left, down, right, up; numeric keypad `4` `5` `1` `2` = buttons A, B, C, D. In the table, ← is back (Guile facing right), → forward.
4. Play 1 player against the CPU with Guile. Nothing about a practice mode, a test menu or a DIP option is verified, so none is used.
5. Marker: numeric keypad `0` = next situation, numeric keypad `.` (Del) = go back. The screen shows `[n/46] name`. Press it before you start doing the situation; the last marker pressed owns every sound until the next press. The order of the table follows a fight, but you may jump (press `0` or `.` several times) and redo any item in any round. Keep NumLock on. If the keypad keys do nothing, before the command set `$env:VOICE_KEY_NEXT='KEYCODE_PGUP'` and `$env:VOICE_KEY_BACK='KEYCODE_PGDN'` (not tested).
6. Hook check, 1 minute: at item 5 do 10 light punches, then in a second PowerShell window run `py -3 -m match.svc_voice_roles_report report private\work\mame-runs\voice-roles-YYYYMMDD-HHMMSS` (the folder is printed when MAME opens). Slot `+0` must show `req` above 0. If it says WARNING (no request), close MAME and send `mame.log` and the `.tsv`: the hook is not working.
7. Suggested plan: round 1, items 1 to 37 as far as the CPU allows; lose it on purpose (38, 39). Round 2: items 40 to 44. Repeat in the next fights whatever the CPU did not allow. Do not press F3 (soft reset); to start over close MAME and run the command again (it makes a new folder).
8. The eight voices with no static trigger (+3, +4, +10, +11, +12, +28, +29, +30) may be select, intro, stun, win or time lines; the places to catch them are items 1 to 3, 35, 37, 39 and 43 to 46. Anything that plays there shows as a Guile slot in the report.

### Situations

"Expect" is only research 30's inference; the log decides. `[unexpected +N]` in the report marks a slot you did not expect, which is useful news.

| n | id | Do | Expect |
|---|---|---|---|
| 1 | `select-guile` | Coin (5), Start (1), cursor on Guile, confirm. | none known; a Guile slot here is a select voice |
| 2 | `pre-fight-dialogue` | The face dialogue before the fight; let it play. | none known |
| 3 | `round-start` | Round intro until FIGHT shows. | none known |
| 4 | `movement-only` | Walk, front step, jump, crouch for 15 s; no attacks (control). | nothing |
| 5 | `sanity-light-punch` | Standing A, 10 times (air is fine). | +0 (hook check) |
| 6 | `sanity-light-kick` | Standing B, 10 times. | +0 |
| 7 | `strong-standing` | Standing C 10 times, then D 10 times. | +0 or +2 (third tier) |
| 8 | `crouch-normals` | Crouching A, B, C, D, 5 each. | +0 or +2 |
| 9 | `jump-normals` | Jumping A, B, C, D, 5 each. | +0 or +2 |
| 10 | `knee-bazooka` | → + B and ← + B, 5 each. | +0, +2 or a special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 11 | `rolling-sobat` | → + D and ← + D, 5 each. | +0, +2 or a special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 12 | `slide-kick` | ↘ + B, 5 times. | +0, +2 or a special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 13 | `spin-back-knuckle` | → + C, 5 times. | +0, +2 or a special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 14 | `sonic-boom-a` | Hold ← 1 s, then → + A. 5 times. | special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 15 | `sonic-boom-c` | Hold ← 1 s, then → + C. 5 times. | special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 16 | `somersault-kick-b` | Hold ↓ 1 s, then ↑ + B. 5 times. | special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 17 | `somersault-kick-d` | Hold ↓ 1 s, then ↑ + D. 5 times. | special voice +15, +16, +25 or +26 (effects +48, +49, +51) |
| 18 | `throw-ground` | Next to the CPU: C or D (add → or ←). 5 throws. | +5 |
| 19 | `throw-air` | Jump next to the CPU, press C or D. Skip if nothing happens. | +5 |
| 20 | `taunt` | Start (1), 5 times, when safe. If nothing happens, note it. | +14 (maybe twice per taunt) |
| 21 | `super-somersault-slash` | Needs 1 gauge level. Hold ↙, then ↘ ↙ ↗ + punch (A or C). | super voice +17 to +24 or +27 (effects +50, +54) |
| 22 | `super-somersault-strike` | Hold ↙, then ↘ ↙ ↗ + kick (B or D). | super voice +17 to +24 or +27 (effects +50, +54) |
| 23 | `super-total-wipeout` | Hold ←, then → ← → + kick (B or D). | super voice +17 to +24 or +27 (effects +50, +54) |
| 24 | `guard-cancel-attack` | Block a CPU attack (hold ←), then C+D. 5 times. Costs 1 gauge level. | +1 (hook check) |
| 25 | `hurt-light` | Let the CPU hit you with weak moves (jab, short kick): 10 hits. Half the hits are silent. | +7 |
| 26 | `hurt-medium` | Same with medium hits: 10 hits. | +6 |
| 27 | `hurt-heavy` | Same with heavy hits (strong punch or kick): 10 hits. | +8 |
| 28 | `hurt-launch` | Get hit and flung into the air or far back. | +31 or +8 |
| 29 | `hurt-knockdown` | Get hit and fall to the floor (round goes on). | +9, +8 or +31 |
| 30 | `hurt-crouch` | Get hit while crouching. | a hurt voice: +6, +7, +8 or +31 |
| 31 | `hurt-air` | Get hit while jumping. | a hurt voice: +6, +7, +8 or +31 |
| 32 | `hurt-projectile` | Get hit by a projectile. | a hurt voice: +6, +7, +8 or +31 |
| 33 | `hurt-super` | Get hit by a CPU super. | a hurt voice: +6, +7, +8 or +31 or +9 |
| 34 | `thrown` | Stand next to the CPU without blocking until it throws you. | a hurt voice: +6, +7, +8 or +31 |
| 35 | `guard-crush` | Keep blocking until the guard breaks and Guile is stunned. | none known |
| 36 | `exceed` | Health at half or less (name flashing), once per fight: ← held, then → ← → + two punches (A+C). | special voice +15, +16, +25 or +26 (effects +48, +49, +51) or super voice +17 to +24 or +27 (effects +50, +54) |
| 37 | `max-mode` | Fill the gauge to MAX (it starts by itself). | none known |
| 38 | `ko-guile` | Let the CPU land the last hit of the round on you. | +9 |
| 39 | `lose-pose` | From the KO until the next round starts. | none known |
| 40 | `round-start-2` | Next round intro until FIGHT. | none known |
| 41 | `ko-opponent` | Knock out the CPU with a normal move. | none known (the victim voice is the CPU's) |
| 42 | `ko-opponent-special` | Knock out the CPU with a special or a super. | special voice +15, +16, +25 or +26 (effects +48, +49, +51) or super voice +17 to +24 or +27 (effects +50, +54) |
| 43 | `win-round` | Round win pose, until the next round. | none known |
| 44 | `win-match` | Win the match: pose and final line, until the next screen. | none known |
| 45 | `time-over` | Optional: run from the CPU until the clock hits 0. | none known |
| 46 | `continue-screen` | If you lose the match: the continue countdown (press 1 to go on). | none known |

### Stop and send back

- Close MAME (Esc). The report prints by itself and is saved as `report.txt` next to `voice_roles.tsv` in `private\work\mame-runs\voice-roles-<time>\`.
- To print it again: `py -3 -m match.svc_voice_roles_report report private\work\mame-runs\voice-roles-<time>`.
- Send back: the `voice_roles.tsv` and the `report.txt` of that folder (no screenshots needed). Both stay under `private/`; never commit them.

## Português (Brasil)

Objetivo: confirmar no MAME em que situação toca cada um dos 38 slots de som ativos do Guile (linhas 2496 a 2575, slots +0 a +79 da [pesquisa 30](../../../docs/wayfinder/guile-adelheid-slot/tickets/30-guile-svc-remaining-sounds.md)). Os papéis da pesquisa são inferidos; esta rodada confirma ou corrige. Você joga; o script só escuta. O log guarda só número de quadro, número de linha, faixa de endereços da amostra e nome da situação, e fica em `private/`.

### Rodar

1. Abra o PowerShell em `tools\kof2003` do repositório.
2. Rode `py -3 -m match.svc_voice_roles_report run`. O MAME abre em janela, com som, SVC Chaos, BIOS MVS Europa e as mesmas teclas das rodadas manuais ([`manual-p1.cfg`](../manual-p1.cfg)). Se o MAME não estiver em `%USERPROFILE%\MAME\mame.exe`, defina antes `KOF2003_MAME` com o caminho completo.
3. Teclas: `5` moeda, `1` Start (também é a provocação), `A` `S` `D` `Espaço` = esquerda, baixo, direita, cima; teclado numérico `4` `5` `1` `2` = botões A, B, C, D. Na tabela, ← é para trás (Guile virado para a direita) e → para frente.
4. Jogue 1 jogador contra o CPU com o Guile. Nada de modo treino, menu de teste ou DIP foi verificado, então nenhum é usado.
5. Marcador: teclado numérico `0` = próxima situação, teclado numérico `.` (Del) = voltar. A tela mostra `[n/46] nome`. Aperte antes de começar a situação; o último marcador apertado vale para todo som até o próximo aperto. A ordem da tabela segue uma luta, mas você pode pular (aperte `0` ou `.` várias vezes) e refazer qualquer item em qualquer round. Deixe o NumLock ligado. Se as teclas do teclado numérico não responderem, antes do comando defina `$env:VOICE_KEY_NEXT='KEYCODE_PGUP'` e `$env:VOICE_KEY_BACK='KEYCODE_PGDN'` (não testado).
6. Teste do gancho, 1 minuto: no item 5 faça 10 socos leves e, num segundo PowerShell, rode `py -3 -m match.svc_voice_roles_report report private\work\mame-runs\voice-roles-AAAAMMDD-HHMMSS` (a pasta aparece quando o MAME abre). O slot `+0` deve mostrar `req` maior que 0. Se aparecer WARNING (nenhum pedido), feche o MAME e mande o `mame.log` e o `.tsv`: o gancho não funciona.
7. Plano sugerido: round 1, itens 1 a 37 até onde o CPU deixar; perca de propósito (38, 39). Round 2: itens 40 a 44. Repita nas lutas seguintes o que o CPU não deixou fazer. Não aperte F3 (reset); para recomeçar feche o MAME e rode o comando de novo (cria pasta nova).
8. As oito vozes sem gatilho estático (+3, +4, +10, +11, +12, +28, +29, +30) podem ser falas de seleção, introdução, atordoamento, vitória ou tempo esgotado; os lugares para pegá-las são os itens 1 a 3, 35, 37, 39 e 43 a 46. O que tocar ali aparece como slot do Guile no relatório.

### Situações

"Esperado" é só a inferência da pesquisa 30; o log decide. `[unexpected +N]` no relatório marca um slot que ninguém esperava, o que é notícia útil.

| n | id | Fazer | Esperado |
|---|---|---|---|
| 1 | `select-guile` | Moeda (5), Start (1), cursor no Guile, confirmar. | nenhum conhecido; slot do Guile aqui é voz de seleção |
| 2 | `pre-fight-dialogue` | O diálogo com o rosto antes da luta; deixar tocar. | nenhum conhecido |
| 3 | `round-start` | Intro do round até aparecer FIGHT. | nenhum conhecido |
| 4 | `movement-only` | Andar, dash, pular e abaixar por 15 s, sem golpes (controle). | nada |
| 5 | `sanity-light-punch` | A em pé, 10 vezes (no ar vale). | +0 (teste do gancho) |
| 6 | `sanity-light-kick` | B em pé, 10 vezes. | +0 |
| 7 | `strong-standing` | C em pé 10 vezes, depois D 10 vezes. | +0 ou +2 (terceiro nível) |
| 8 | `crouch-normals` | Agachado: A, B, C, D, 5 de cada. | +0 ou +2 |
| 9 | `jump-normals` | No pulo: A, B, C, D, 5 de cada. | +0 ou +2 |
| 10 | `knee-bazooka` | → + B e ← + B, 5 de cada. | +0, +2 ou voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 11 | `rolling-sobat` | → + D e ← + D, 5 de cada. | +0, +2 ou voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 12 | `slide-kick` | ↘ + B, 5 vezes. | +0, +2 ou voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 13 | `spin-back-knuckle` | → + C, 5 vezes. | +0, +2 ou voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 14 | `sonic-boom-a` | Segurar ← 1 s, depois → + A. 5 vezes. | voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 15 | `sonic-boom-c` | Segurar ← 1 s, depois → + C. 5 vezes. | voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 16 | `somersault-kick-b` | Segurar ↓ 1 s, depois ↑ + B. 5 vezes. | voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 17 | `somersault-kick-d` | Segurar ↓ 1 s, depois ↑ + D. 5 vezes. | voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) |
| 18 | `throw-ground` | Colado no CPU: C ou D (com → ou ←). 5 arremessos. | +5 |
| 19 | `throw-air` | Pular colado no CPU e apertar C ou D. Pular se nada acontecer. | +5 |
| 20 | `taunt` | Start (1), 5 vezes, em hora segura. Se nada acontecer, anote. | +14 (talvez 2 vezes por provocação) |
| 21 | `super-somersault-slash` | Precisa de 1 nível de barra. Segurar ↙, depois ↘ ↙ ↗ + soco (A ou C). | voz de super +17 a +24 ou +27 (efeitos +50, +54) |
| 22 | `super-somersault-strike` | Segurar ↙, depois ↘ ↙ ↗ + chute (B ou D). | voz de super +17 a +24 ou +27 (efeitos +50, +54) |
| 23 | `super-total-wipeout` | Segurar ←, depois → ← → + chute (B ou D). | voz de super +17 a +24 ou +27 (efeitos +50, +54) |
| 24 | `guard-cancel-attack` | Defender um golpe do CPU (segurar ←) e apertar C+D. 5 vezes. Gasta 1 nível de barra. | +1 (teste do gancho) |
| 25 | `hurt-light` | Deixar o CPU acertar golpes leves (soco ou chute curto): 10 acertos. Metade dos acertos é muda. | +7 |
| 26 | `hurt-medium` | O mesmo com golpes médios: 10 acertos. | +6 |
| 27 | `hurt-heavy` | O mesmo com golpes fortes (soco ou chute forte): 10 acertos. | +8 |
| 28 | `hurt-launch` | Ser acertado e jogado para o alto ou para longe. | +31 ou +8 |
| 29 | `hurt-knockdown` | Ser acertado e cair no chão (o round continua). | +9, +8 ou +31 |
| 30 | `hurt-crouch` | Ser acertado agachado. | voz de dor: +6, +7, +8 ou +31 |
| 31 | `hurt-air` | Ser acertado no pulo. | voz de dor: +6, +7, +8 ou +31 |
| 32 | `hurt-projectile` | Ser acertado por projétil. | voz de dor: +6, +7, +8 ou +31 |
| 33 | `hurt-super` | Ser acertado por um super do CPU. | voz de dor: +6, +7, +8 ou +31 ou +9 |
| 34 | `thrown` | Ficar colado no CPU, sem defender, até ele arremessar. | voz de dor: +6, +7, +8 ou +31 |
| 35 | `guard-crush` | Defender sem parar até a guarda quebrar e o Guile ficar atordoado. | nenhum conhecido |
| 36 | `exceed` | Com a vida na metade ou menos (nome piscando), uma vez por luta: ← segurado, depois → ← → + dois socos (A+C). | voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) ou voz de super +17 a +24 ou +27 (efeitos +50, +54) |
| 37 | `max-mode` | Encher a barra até o MAX (começa sozinho). | nenhum conhecido |
| 38 | `ko-guile` | Deixar o CPU dar o último golpe do round em você. | +9 |
| 39 | `lose-pose` | Do KO até o próximo round começar. | nenhum conhecido |
| 40 | `round-start-2` | Intro do round seguinte até o FIGHT. | nenhum conhecido |
| 41 | `ko-opponent` | Nocautear o CPU com golpe comum. | nenhum conhecido (a voz da vítima é do CPU) |
| 42 | `ko-opponent-special` | Nocautear o CPU com especial ou super. | voz de especial +15, +16, +25 ou +26 (efeitos +48, +49, +51) ou voz de super +17 a +24 ou +27 (efeitos +50, +54) |
| 43 | `win-round` | Pose de vitória do round, até o próximo round. | nenhum conhecido |
| 44 | `win-match` | Vencer a luta: pose e fala final, até a próxima tela. | nenhum conhecido |
| 45 | `time-over` | Opcional: fugir do CPU até o relógio zerar. | nenhum conhecido |
| 46 | `continue-screen` | Se perder a luta: contagem do continue (apertar 1 para seguir). | nenhum conhecido |

### Parar e enviar

- Feche o MAME (Esc). O relatório sai sozinho e fica salvo como `report.txt` ao lado do `voice_roles.tsv`, em `private\work\mame-runs\voice-roles-<hora>\`.
- Para imprimir de novo: `py -3 -m match.svc_voice_roles_report report private\work\mame-runs\voice-roles-<hora>`.
- Mande de volta: o `voice_roles.tsv` e o `report.txt` dessa pasta (não precisa de captura de tela). Os dois ficam em `private/`; nunca faça commit deles.
