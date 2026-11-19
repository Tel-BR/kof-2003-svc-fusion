---
id: 33
title: "Confirm in MAME the roles of Guile's inferred voices"
label: wayfinder:task
mode: HITL
status: closed
assignee: tel
blocked_by: [31]
research:
---

## Question

[30](30-guile-svc-remaining-sounds.md) inferred the roles of Guile's remaining voices by static reading: hurt tiers, launch hurt, taunt, third attack tier, throw, knockout, which move records are specials and which are supers, and whether the eight voices with no static trigger ever play. None was confirmed in a MAME run. Run SVC Chaos in MAME on the owner's machine with Guile and record, for each candidate sample, the situation in which it plays (or that it never plays), as sample range and situation only. The answer feeds the per-fighter register of [31](31-guile-remaining-voices-choice.md), part 3, and blocks only the mapping of the hooks.

_PT-BR: o [30](30-guile-svc-remaining-sounds.md) inferiu por leitura estática os papéis das vozes restantes do Guile: níveis de dor, dor de lançamento, provocação, terceiro nível de ataque, arremesso, nocaute, quais registros de golpe são especiais e quais são supers, e se as oito vozes sem gatilho estático chegam a tocar. Nenhum foi confirmado numa execução do MAME. Rodar o SVC Chaos no MAME na máquina do dono com o Guile e anotar, para cada amostra candidata, a situação em que ela toca (ou que nunca toca), só como faixa da amostra e situação. A resposta alimenta o registro por lutador da parte 3 do [31](31-guile-remaining-voices-choice.md) e bloqueia só o mapeamento dos ganchos._

## Notes

- Task type: the work is a manual run, so the agent hands the owner a precise checklist when this ticket is taken.
- Hard rule of `AGENTS.md`: no game data in the notes; sample ranges and situations only.

## Resolution

Owner's manual MAME run of 2026-11-19, from the hook log under `private/work/mame-runs/voice-roles-20261119-145124/` (46 of 46 situations, about 65,700 frames; the earlier attempt `voice-roles-20261119-115727` stopped at the selection screen and is not used). The hook logged every request to Guile's block of the sound table and every chip start of his V ranges. The owner pressed the markers by hand, lost rounds on purpose to move on, and filled the gauge with ordinary special moves (never other supers), so each sound is read by its frame and the life bars around it, not by the marker alone. Move names below are the owner's names for the situations, not SNK's. Counts are chip starts across the whole run; sizes are the whole sample.

Confirmed by the log:

| Slot | V range | Bytes | Role | Evidence |
|---|---|---|---|---|
| +0 | `0x722900`–`0x722FFF` | 1,792 | attack voice, A and B | 59 starts |
| +1 | `0x724A00`–`0x7251FF` | 2,048 | Guard Cancel attack voice | 1 start |
| +2 | `0x635B00`–`0x636BFF` | 4,352 | strong attack voice (C and D, crouching, and the start of several specials and supers) | 147 starts |
| +3 | `0x633700`–`0x6347FF` | 4,352 | throw voice | 6 starts (3 ground, 3 air) |
| +5 | `0x725200`–`0x725BFF` | 2,560 | throw voice, second one | 1 start |
| +7 | `0x723000`–`0x7236FF` | 1,792 | light hurt | 6 starts; life lost 3 to 7 |
| +6 | `0x723700`–`0x7241FF` | 2,816 | medium hurt | 8 starts; life lost 5 to 23 |
| +8 | `0x5AD900`–`0x5AF1FF` | 6,400 | heavy or general hurt | 21 starts of 61 requests; life lost 0 to 31 |
| +9 | `0x334400`–`0x337AFF` | 14,080 | knockout voice | 5 starts, each in the frames of one of Guile's 7 knockouts |
| +10 | `0x52C900`–`0x52E5FF` | 7,424 | round-start voice | 7 starts, always at the start of a round |
| +12 | `0x5A3B00`–`0x5A55FF` | 6,912 | round-win voice | 3 starts, each 140 to 200 frames after the opponent's knockout (3 of 9 round wins) |
| +14 | `0x52AD00`–`0x52C8FF` | 7,168 | taunt | 5 starts of 9 requests |
| +15 | `0x4AE000`–`0x4B00FF` | 8,448 | Sonic Boom voice (with Guile-only effect +48, 14,336) | 57 starts |
| +16 | `0x5A5600`–`0x5A6FFF` | 6,656 | Somersault Kick voice (with shared effect +49) | 23 starts |
| +17 to +20 | see 30 | 3,072 / 2,816 / 3,584 / 6,912 | Somersault Strike voices (super) | 2 / 2 / 2 / 1 starts |
| +21 to +24 | see 30 | 6,656 / 2,816 / 2,560 / 4,864 | Total Wipeout voices (super) | 3 / 2 / 2 / 3 starts |
| +27 | `0x3A9500`–`0x3AC2FF` | 11,776 | Somersault Slash voice (super) | 2 starts |
| +25, +26 | `0x5AA500`–`0x5ABDFF`, `0x5ABE00`–`0x5AD8FF` | 6,400 / 6,912 | Exceed voices (with Guile-only effect +51, 16,896) | 2 / 2 starts; +51 2 starts |

So the move record that [30](30-guile-svc-remaining-sounds.md) left unresolved (`0x04FB1C`) is the Exceed.

Not settled:

- +11 (11,776 bytes): 3 starts, one about 160 frames after an opponent knockout, the other two during a throw and a super. Role unclear (possibly a second round-win line).
- +4 (2,560 bytes): 1 start, at the owner's Spin Back Knuckle marker. Role unclear.
- Never started in the whole run: +28 (2,048), +29 (2,560), +30 (2,048) and +31 (10,240), the inferred launch hurt: 16,896 bytes in all.
- Not observed: launch, knockdown and thrown-by-the-CPU hurt (the owner could not make the CPU deliver them: hurt voices are random), a won match (the run ended on the continue screen) and time over. The owner saw the round-win pose.
- Owner and log disagree on one point: the owner heard silence when Guile fell (item 38), while the log shows +9 requested and started in 5 of his 7 knockouts. No Guile knockout falls inside the item-38 window (the knockout there is the opponent's), so the two do not necessarily clash; +9 is confirmed by the log, not by ear.

Consequences: roles above go into the per-fighter register of [31](31-guile-remaining-voices-choice.md), part 3, with status confirmed; the unsettled and not-observed ones keep status inferred or unknown, and the ticket does not block the attack voices. No decision is taken here about which voices enter the tail.

_PT-BR: execução manual do dono no MAME em 19/11/2026, a partir do log do gancho em `private/work/mame-runs/voice-roles-20261119-145124/` (46 de 46 situações, cerca de 65.700 quadros; a tentativa anterior `voice-roles-20261119-115727` parou na seleção e não é usada). O gancho registrou todo pedido ao bloco do Guile na tabela de sons e todo início de reprodução de faixas V dele. O dono apertou os marcadores à mão, perdeu rounds de propósito para avançar e encheu a barra com especiais comuns (nunca outros supers), então cada som é lido pelo quadro e pelas barras de vida em volta, não só pelo marcador. Os nomes dos golpes são os nomes do dono para as situações, não da SNK. As contagens são inícios no chip em toda a rodada; os tamanhos são da amostra inteira._

_Confirmado pelo log: a tabela acima. O registro de golpe que o [30](30-guile-svc-remaining-sounds.md) deixou sem classe (`0x04FB1C`) é o Exceed._

_Não resolvido: +11 (11.776 bytes), 3 inícios, um uns 160 quadros depois de um nocaute do adversário e os outros dois durante um arremesso e um super, papel incerto (talvez uma segunda fala de vitória do round); +4 (2.560 bytes), 1 início, no marcador do Spin Back Knuckle, papel incerto. Nunca tocaram em toda a rodada: +28 (2.048), +29 (2.560), +30 (2.048) e +31 (10.240), a dor de lançamento inferida: 16.896 bytes. Não observados: dor de lançamento, de derrubada e de arremesso do CPU (o dono não conseguiu fazer o CPU aplicá-los: a voz de dor é aleatória), luta vencida (a rodada terminou na tela de continue) e tempo esgotado. O dono viu a pose de vitória do round. Dono e log divergem em um ponto: o dono ouviu silêncio quando o Guile caiu (item 38), enquanto o log mostra +9 pedido e iniciado em 5 dos 7 nocautes dele. Nenhum nocaute do Guile cai dentro da janela do item 38 (o nocaute ali é o do adversário), então os dois não necessariamente se contradizem; o +9 está confirmado pelo log, não de ouvido._

_Consequências: os papéis acima entram no registro por lutador do [31](31-guile-remaining-voices-choice.md), parte 3, com estado confirmado; os não resolvidos e não observados ficam como inferido ou desconhecido, e o ticket não bloqueia as vozes de ataque. Nenhuma decisão sobre quais vozes entram na faixa é tomada aqui._
