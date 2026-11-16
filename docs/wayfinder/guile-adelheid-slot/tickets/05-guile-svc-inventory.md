---
id: 05
title: "Inventory of Guile's SVC animations and assets for this slice"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/05-guile-svc-inventory:docs/wayfinder/guile-adelheid-slot/research/05-guile-svc-inventory.md
---

## Question

In SVC Chaos, which animations and assets does Guile have for walking, his forward dash and backdash, each jump type SVC offers, the knockdown recovery roll, standing and crouching guard, the Guard Cancel attack and front step, the selection portrait, the HUD icon and his palettes? For each: frame count, durations, where its records sit (addresses, strides), tile counts, and how close it is to the KOF 2003 action it might stand in for. Reuse [ticket 03](../../../specs/first-svc-character-import/issues/03-capture-svc-fighter-reference.md), [the Guile research](../../../specs/first-svc-character-import/research-guile-svc.md) and the tools in `private/work/svc-guile/`.

_PT-BR: No SVC Chaos, que animações e recursos o Guile tem para andar, dash para frente e para trás, cada tipo de pulo do SVC, cambalhota de recuperação de queda, defesa em pé e agachado, golpe e passo de Guard Cancel, retrato da seleção, ícone do placar e paletas? Para cada um: número de quadros, durações, onde ficam os registros (endereços, espaçamentos), contagem de tiles e quão próximo está da ação do KOF 2003 que poderia substituir. Reaproveitar o ticket 03, a pesquisa do Guile e as ferramentas em `private/work/svc-guile/`._

## Resolution

**Movement.** SVC Guile walks forward in a 30-frame, 6-pose loop (about 3.1 px per frame) and back in a 36-frame loop. His front step lasts 19 frames and covers 72 px; holding forward afterwards returns to the walk, so **SVC has no run**. His back step is a 25-frame, 86 px hop of height 16. He has **one jump arc** (height 90, 33 frames in the air, 44 frames of animation) in neutral, forward and back versions. Taps of 1–3 frames give the same jump, and the Big Jump only lengthens forward travel (144 px, or 173 px out of a front step).

**Guard and Guard Cancel.** Standing guard uses 4 poses, crouching guard 2. The Guard Cancel attack (C+D) has 15 poses over 42 frames, does no damage and pushes the opponent back 176 px. The Guard Cancel front step plays the front step's poses and durations from its own 7 records and travels 54 px.

**Break-fall.** A+B on landing after a sweep and after an uppercut gave a 7-frame slide in the jump's landing-crouch poses, **not a roll**. This contradicts the recovery roll that ADR 0002 relies on. Other knockdowns and timings were not tested.

**Select screen, HUD and palettes.** SVC gives Guile a 4-tile (32×32 px) grid icon, a full-body figure drawn with his fighter sprites, and an animated 80×96 px pre-fight dialogue face (75 tiles). It has **no dedicated select portrait and no HUD icon** for him; the HUD shows only his name. He has **2 colour sets** on MVS (A = C, B = D) of 8 palette slots each, in blocks at `0x577538` and `0x577738` of the decrypted P region.

**Left open.** KOF 2003's own run, jump, roll and blowback durations and heights were not measured.

**PT-BR**

**Movimento.** O Guile do SVC anda para frente num ciclo de 30 quadros e 6 poses (cerca de 3,1 px por quadro) e para trás num ciclo de 36 quadros. O dash para frente dura 19 quadros e anda 72 px; segurar frente depois volta a andar, então **o SVC não tem corrida**. O passo para trás é um saltinho de 25 quadros, 86 px e altura 16. Ele tem **um único arco de pulo** (altura 90, 33 quadros no ar, 44 quadros de animação), nas versões neutra, para frente e para trás. Toques de 1 a 3 quadros dão o mesmo pulo, e o Big Jump só aumenta a distância para frente (144 px, ou 173 px saindo do dash).

**Defesa e Guard Cancel.** A defesa em pé usa 4 poses e a agachada 2. O golpe de Guard Cancel (C+D) tem 15 poses em 42 quadros, não causa dano e empurra o adversário 176 px. O passo de Guard Cancel toca as poses e durações do dash a partir de 7 registros próprios e anda 54 px.

**Recuperação de queda.** A+B ao tocar o chão depois de rasteira e de gancho deu um deslize de 7 quadros nas poses agachadas do pouso do pulo, **não uma cambalhota**. Isso contradiz a cambalhota de recuperação em que a ADR 0002 se apoia. Outras quedas e outros tempos não foram testados.

**Seleção, placar e paletas.** O SVC dá ao Guile um ícone de grade de 4 tiles (32×32 px), uma figura de corpo inteiro feita com os sprites de luta e um rosto animado de 80×96 px no diálogo antes da luta (75 tiles). **Não há retrato próprio de seleção nem ícone de placar**; o placar mostra só o nome. Ele tem **2 conjuntos de cores** no MVS (A = C, B = D), de 8 slots de paleta cada, em blocos em `0x577538` e `0x577738` da região P decriptada.

**Em aberto.** As durações e alturas do próprio KOF 2003 para corrida, pulos, esquivas e golpe CD não foram medidas.

Research / Pesquisa: `research/05-guile-svc-inventory:docs/wayfinder/guile-adelheid-slot/research/05-guile-svc-inventory.md` (commit `2156b20`).
