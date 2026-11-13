---
id: 08
title: "Animation format"
label: wayfinder:task
mode: AFK
status: closed
assignee: codex
blocked_by: [07]
research:
---

## Question

Starting from the anchors, are the frame, animation, hitbox and move-script formats of the two games equivalent? Test the shared-engine hypothesis. What changes, and which conversion direction is simpler?

_PT-BR: partindo das âncoras, os formatos de frame, animação, hitbox e scripts de golpe dos dois jogos são equivalentes? Testar a hipótese de motor compartilhado. O que muda, e qual direção de conversão é mais simples?_

## Resolution

### Iori's idle and standing light punch / Espera e soco fraco em pé do Iori

**English.** The smallest comparison used the paired Iori anchors from [Shared art](07-shared-art.md), tile `0x60b16` in KOF 2003 and `0x0d405` in SVC Chaos. Their nonblank tile hashes match. With player one standing still, the anchor appeared in every sampled idle frame. The nine poses repeat every **49 emulator frames** in both games. Aligning the loops by phase gave **60 of 60** identical sprite compositions. The SVC idle sample comes from the round announcement, when the fighter is already playing that loop. The comparison uses exact nonblank tile hashes, column positions relative to the head of the sprite chain, row indices and flip flags. Absolute position, palette and zoom are outside that comparison.

**Português (Brasil).** A comparação mínima usou as âncoras pareadas do Iori de [Shared art](07-shared-art.md), tile `0x60b16` no KOF 2003 e `0x0d405` no SVC Chaos. Os hashes dos tiles não zerados coincidem. Com o jogador 1 parado, a âncora apareceu em todos os quadros de espera amostrados. As nove poses se repetem a cada **49 quadros do emulador** nos dois jogos. O alinhamento pela fase do ciclo deu **60 de 60** composições de sprite idênticas. A amostra de espera do SVC vem do anúncio do round, quando o lutador já executa esse ciclo. A comparação usa os hashes exatos dos tiles não zerados, a posição das colunas em relação ao início da cadeia de sprites, os índices das linhas e os indicadores de espelhamento. Posição absoluta, paleta e zoom ficam fora dessa comparação.

**English.** In the live round, a neutral-direction A press produced a standing light punch that missed. Against a no-input control, all **13** action frames differed from idle in each game. Aligning by the first changed sprite composition, all **13 of 13** compositions matched across the games, including the five consecutive pose spans of **2, 3, 2, 3 and 3** frames. Both returned to idle. The opponent's health stayed constant. A box classified as attack was active for three frames in each game, in the same part of the action. KOF 2003 exposed three active collision records during that interval and SVC exposed two, excluding the push box. The decoded attack box geometry also differed. The box classifications come from the training viewers and the observed appearance and disappearance during the punch. [KOF 2003 viewer](https://github.com/peon2/fbneo-training-mode/blob/bf3541e1d4f586f76f401617af4fa842447591de/hitboxes/kof2003-hitboxes.lua) · [SVC viewer](https://github.com/peon2/fbneo-training-mode/blob/bf3541e1d4f586f76f401617af4fa842447591de/hitboxes/svc-hitboxes.lua)

**Português (Brasil).** Com o round em andamento, apertar A sem direção produziu um soco fraco em pé que não acertou o adversário. Em relação à execução de controle sem apertar A, os **13** quadros do golpe diferiram da espera em cada jogo. Alinhando pela primeira mudança na composição do sprite, as **13 de 13** composições coincidiram entre os jogos, inclusive os cinco trechos consecutivos de **2, 3, 2, 3 e 3** quadros. Ambos voltaram à espera. A vida do adversário permaneceu constante. Uma caixa classificada como ataque ficou ativa por três quadros em cada jogo, na mesma parte do golpe. O KOF 2003 expôs três registros de colisão ativos nesse intervalo e o SVC expôs dois, excluída a caixa de empurrão. A geometria decodificada da caixa de ataque também diferiu. A classificação das caixas vem dos visualizadores de treino e da observação de quando a caixa apareceu e sumiu durante o soco. [Visualizador do KOF 2003](https://github.com/peon2/fbneo-training-mode/blob/bf3541e1d4f586f76f401617af4fa842447591de/hitboxes/kof2003-hitboxes.lua) · [Visualizador do SVC](https://github.com/peon2/fbneo-training-mode/blob/bf3541e1d4f586f76f401617af4fa842447591de/hitboxes/svc-hitboxes.lua)

### Observed formats / Formatos observados

Addresses are in the 68000 CPU address space. `+` offsets are relative to the fighter object or, where indicated, to the pointed-to ROM data. The pointer-to-pose comparison pairs each RAM sample with the sprite output one emulator frame later. / _Os endereços estão no espaço da CPU 68000. Os deslocamentos com `+` são relativos ao objeto do lutador ou, quando indicado, aos dados apontados na ROM. A comparação entre ponteiro e pose associa cada amostra de RAM à saída de sprites um quadro do emulador depois._

| Observation / Observação | KOF 2003 | SVC Chaos |
| --- | --- | --- |
| Iori's P1 object and pose-related ROM pointer / Objeto do Iori no P1 e ponteiro de ROM associado à pose | `0x101080`, `+0x60` | `0x10A100`, `+0x28` |
| Nine idle addresses / Nove endereços da espera | `0x299A80`–`0x299BA4`, adjacent addresses separated by 14–42 bytes / intervalos de 14 a 42 bytes entre endereços adjacentes | `0x202C8E`–`0x202CBE`, eight consecutive 6-byte gaps / oito intervalos consecutivos de 6 bytes |
| CPU read offsets from those ROM pointers / Deslocamentos de leitura da CPU a partir desses ponteiros de ROM | `+0`, `+2`, `+4`, `+6`, `+8`, `+10`, `+12` | `+0`, `+2`, `+4` |
| Jab pose spans and pointed-to addresses / Trechos de pose do soco e endereços apontados | 5 spans, 4 addresses. Spans 2 and 5 reuse `0x29A27A`. / 5 trechos, 4 endereços. Os trechos 2 e 5 reutilizam `0x29A27A`. | 5 spans, 5 addresses at 6-byte intervals from `0x2030C6` to `0x2030DE`. / 5 trechos, 5 endereços de 6 em 6 bytes de `0x2030C6` a `0x2030DE`. |
| Collision mask and first record / Máscara de colisão e primeiro registro | `+0x4F`, `+0xA0`. Records are 6 bytes apart, geometry begins at record offset `+2`. / Registros espaçados de 6 bytes, geometria a partir de `+2` no registro. | `+0x261`, `+0x262`. Records are 6 bytes apart, geometry begins at record offset `+1`. / Registros espaçados de 6 bytes, geometria a partir de `+1` no registro. |

**English.** The measured frame references, action steps and collision records rule out copying those structures directly. The common sprite compositions and timing show content reuse in these two actions. Engine lineage and the complete move-script grammar, including command dispatch and branches, remain unverified. In this sample, SVC's fixed-stride records are easier to enumerate on the source side. KOF 2003 references the same frame again on recovery, and the two games apply different collision records and geometry. Both import directions need to translate the sequence and author or map the target game's collision behavior. The two actions provide no ranking of end-to-end conversion cost.

**Português (Brasil).** As referências de quadro, os passos do golpe e os registros de colisão medidos descartam a cópia direta dessas estruturas. As composições de sprite e as durações em comum mostram reaproveitamento de conteúdo nessas duas ações. O parentesco entre os motores e a gramática completa dos scripts de golpe, incluindo o despacho de comandos e as ramificações, seguem sem verificação. Na amostra, o espaçamento fixo dos registros do SVC facilita enumerá-los na origem. O KOF 2003 volta a referenciar o mesmo quadro durante a recuperação, e os dois jogos aplicam registros e geometrias de colisão diferentes. Nos dois sentidos de importação, é preciso traduzir a sequência e definir ou mapear o comportamento de colisão do jogo de destino. As duas ações ainda não permitem comparar o custo total da conversão.

### Reproduction / Reprodução

**English.** Run from the repository root with Python 3.11.9, MAME 0.289, the `euro` BIOS, the `kof2003` Export and `svc` sets, and the validated C regions and Iori samples from [Shared art](07-shared-art.md). The idle comparison aligns KOF 2003 frames 2140–2199 with SVC frames 2182–2241. The punch starts visually at frames 2160 and 2486. The attack box appears in object RAM on frames 2166–2168 and 2492–2494. The capture helpers and raw outputs stay in `private/work/decryption-mame/animation/`. [MAME Lua memory API](https://docs.mamedev.org/luascript/ref-mem.html)

**Português (Brasil).** Execute na raiz do repositório com Python 3.11.9, MAME 0.289, o BIOS `euro`, os conjuntos `kof2003` Export e `svc`, e as regiões C validadas e amostras do Iori de [Shared art](07-shared-art.md). A comparação da espera alinha os quadros 2140–2199 do KOF 2003 com 2182–2241 do SVC. O soco começa a aparecer nos quadros 2160 e 2486. A caixa de ataque aparece na RAM do objeto nos quadros 2166–2168 e 2492–2494. Os auxiliares de captura e as saídas brutas ficam em `private/work/decryption-mame/animation/`. [API de memória Lua do MAME](https://docs.mamedev.org/luascript/ref-mem.html)

```powershell
python private/work/decryption-mame/animation/run.py idle --trace
python private/work/decryption-mame/animation/verify.py idle
python private/work/decryption-mame/animation/run.py jab --trace
python private/work/decryption-mame/animation/run.py control
python private/work/decryption-mame/animation/verify.py jab
python private/work/decryption-mame/animation/action.py
```
