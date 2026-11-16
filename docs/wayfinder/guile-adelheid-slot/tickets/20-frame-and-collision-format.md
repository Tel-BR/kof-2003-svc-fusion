---
id: 20
title: "KOF 2003's sprite frame and collision record format"
label: wayfinder:research
mode: AFK
status: closed
assignee: claude-research
blocked_by: []
research: research/20-frame-and-collision-format:docs/wayfinder/guile-adelheid-slot/research/20-frame-and-collision-format.md
---

## Question

[How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md) found that a step in a fighter's step script names a sprite frame and can carry up to four 6-byte collision boxes, copied to object `+$A0`, `+$A6`, `+$AC` and `+$B2`, and [Animation format](../../base-direction/tickets/08-animation-format.md) measured that geometry starts at record offset `+2`. Neither says what the bytes mean. [How KOF 2003's sprite-frame records number their tiles](18-sprite-frame-tiles.md) settles how a frame record numbers its tiles.

What is the byte-level layout of a step record and of its collision boxes: which fields are fixed, which are optional and what switches them on, what each of the four box slots is used for, and how the six bytes of a box encode its kind, position and size, including facing? Together with the sprite-frame record, is that enough to write a fighter's frames and boxes as KOF 2003 data without new 68000 code? Use Adelheid's idle, walk and guard as the worked example. Record addresses, strides, sizes and counts only.

_PT-BR: a pesquisa 01 mostrou que um passo do script de passos do lutador indica um quadro de sprite e pode trazer até quatro caixas de colisão de 6 bytes, copiadas para `+$A0`, `+$A6`, `+$AC` e `+$B2` do objeto, e o ticket 08 do mapa anterior mediu que a geometria começa no deslocamento `+2` do registro. Nenhum dos dois diz o que os bytes significam. O [ticket 18](18-sprite-frame-tiles.md) fecha como um registro de quadro numera os tiles. Qual é o formato, byte a byte, de um registro de passo e das suas caixas de colisão: quais campos são fixos, quais são opcionais e o que os liga, para que serve cada uma das quatro posições de caixa e como os seis bytes de uma caixa guardam tipo, posição e tamanho, inclusive o lado para onde o lutador olha? Junto com o registro de quadro de sprite, isso basta para escrever os quadros e as caixas de um lutador como dados do KOF 2003 sem código 68000 novo? Usar a espera, o andar e a defesa da Adelheid como exemplo. Registrar só endereços, espaçamentos, tamanhos e contagens._

## Resolution

**Step record.** A step has a 10-byte fixed part: duration in frames, active-box mask, four flag bytes, the frame word (frame number in bits 0–9, flips in bits 12–13, "another layer follows" in bit 11) and two signed position bytes in 2-pixel units. Then come up to two more layers, two control bytes, up to four 6-byte boxes, an optional sound word and the operands of one command. The control bytes give the size of every part. Walking all 37 fighters this way covers 166,830 steps in 25,684 sequences, and every sequence ends on the byte where the next one starts.

**Box.** Six bytes: kind, attack index, X offset, Y offset, half-width, half-height. Offsets are signed, in 2-pixel units from the object's position, and X mirrors with facing; half-sizes are in pixels. The four slots are treated alike. The kind sets the role: body (`$01`–`$0E`, in four classes an attack can be told to ignore), guard (`$1C`–`$1F`), attack (the kinds marked in the fighter's own 128-bit map at `$6C62E`) or projectile class (`$0F`–`$1B`). The attack index picks the row of the attacker's 64-entry tables, which is the way to an attack's hit properties.

**Push box.** It is not in the steps. It comes from the four boxes of the fighter's action `$3FF`, read once at creation and chosen each frame by posture flags.

**Enough for data-only frames and boxes: yes.** Frames, timing, position, boxes, velocity (command `$06`) and sound calls are data in the two banked directories. For idle, walk and guard nothing needs new 68000 code. Not fully read: the flag bytes `+$50`–`+$53`, the upper nibble of the mask byte, frame-word bits 14–15, the meaning of each kind beyond its class, and the roles of most commands (their sizes are known). For idle, walk and guard a converter can copy those values from Adelheid's matching action.

**PT-BR**

**Registro de passo.** Um passo tem 10 bytes fixos: duração em quadros, máscara de caixas ativas, quatro bytes de indicadores, a palavra do quadro (número do quadro nos bits 0–9, espelhamentos nos bits 12–13, "há outra camada" no bit 11) e dois bytes de posição com sinal, em unidades de 2 pixels. Depois vêm até duas camadas extras, dois bytes de controle, até quatro caixas de 6 bytes, uma palavra de som opcional e os operandos de um comando. Os bytes de controle dão o tamanho de cada parte. Percorrendo os 37 lutadores assim são 166.830 passos em 25.684 sequências, e toda sequência termina no byte em que a próxima começa.

**Caixa.** Seis bytes: tipo, índice do golpe, deslocamento X, deslocamento Y, meia largura e meia altura. Os deslocamentos têm sinal, valem 2 pixels por unidade a partir da posição do lutador, e o X espelha conforme o lado para onde ele olha; as meias medidas são em pixels. As quatro posições são tratadas da mesma forma. O tipo define a função: corpo (`$01`–`$0E`, em quatro classes que um golpe pode ignorar), defesa (`$1C`–`$1F`), golpe (os tipos marcados no mapa de 128 bits do próprio lutador, em `$6C62E`) ou classe de projétil (`$0F`–`$1B`). O índice do golpe escolhe a linha das tabelas de 64 entradas de quem ataca, e é por ali que se chega às propriedades do golpe.

**Caixa de empurrão.** Não vem nos passos. Sai das quatro caixas da ação `$3FF` do lutador, lidas uma vez na criação e escolhidas a cada quadro conforme a postura.

**Dá para escrever quadros e caixas só com dados: sim.** Quadros, tempos, posição, caixas, velocidade (comando `$06`) e sons são dados nos dois diretórios com banco. Para a espera, o andar e a defesa não é preciso código 68000 novo. Ficaram sem leitura completa os indicadores `+$50`–`+$53`, a metade alta da máscara, os bits 14–15 da palavra do quadro, o significado de cada tipo além da classe e o papel da maioria dos comandos (os tamanhos são conhecidos). Para a espera, o andar e a defesa o conversor pode copiar esses valores da ação correspondente da Adelheid.

Research / Pesquisa: `research/20-frame-and-collision-format:docs/wayfinder/guile-adelheid-slot/research/20-frame-and-collision-format.md` (commit `fd3947d`).
