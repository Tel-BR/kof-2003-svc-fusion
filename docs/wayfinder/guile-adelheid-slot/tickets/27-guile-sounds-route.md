---
id: 27
title: "Choose how Guile's own sounds reach KOF 2003"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: [25, 26]
research:
---

## Question

With what [25](25-kof2003-sound-playback.md) and [26](26-svc-guile-sounds.md) found, how do Guile's own SVC sounds, voice and effects get into native KOF 2003, and at what cost? Which sounds are in this slice, which wait, and what is silent meanwhile? The answer is an import rule for every SVC fighter, like the animation rules.

_PT-BR: com o que os tickets 25 e 26 acharam, como os sons do próprio Guile no SVC, voz e efeitos, entram no KOF 2003 nativo, e a que custo? Quais sons entram nesta fatia, quais esperam e o que fica mudo enquanto isso? A resposta é uma regra de importação para todo lutador do SVC, como as regras de animação._

## Decision recorded

On 2026-11-16 the owner chose to use KOF 2003's reusable sounds for shared effects on Guile and every other Imported Character. SVC audio imports are limited to sounds specific to the Imported Character, including their voice. The choice of KOF 2003 equivalents and the route for adding character-specific samples are still open.

_PT-BR: em 16/11/2026, o dono escolheu usar os sons reaproveitáveis do KOF 2003 para os efeitos compartilhados do Guile e dos demais Personagens Importados. A importação de áudio do SVC fica restrita aos sons próprios de cada personagem, incluindo a voz. A escolha dos equivalentes no KOF 2003 e o caminho para acrescentar as amostras próprias seguem em aberto._

## Resolution

Owner decisions of 2026-11-16, valid for every Imported Character. The rule has seven parts.

1. **Scope of own sounds.** Only the two attack voices measured in [26](26-svc-guile-sounds.md) enter this slice: standing light punch and Guard Cancel attack, 3,840 bytes in total. Hurt, knockout and victory voices wait for a later ticket. The break-fall stays silent, as it is in SVC, where the M1 program disables that request.
2. **Shared effects.** Each action copies the sound code that KOF 2003 already plays in the action with the same job (walk, dash or run, jump takeoff and landing, guard, swing, light hit). The owner picks by hand only where SVC has a sound with no KOF counterpart, such as the immediate Guard Cancel contact.
3. **Voice trigger.** The voice plays every time the attack starts, through the sound word in the step script. SVC's conditional timing rule is not copied.
4. **Route for own samples.** The original KOF 2003 route: samples are placed in the free tail `[$FFC000,$1000000)` of the V region (16,384 bytes), a descriptor is added to the M1 program and the 68000 mapping is wired. Allocation is first come, first served, whole samples only, with a ledger that records offset and size of each sample. There is no fixed quota per fighter.
5. **Verification comes first.** The first step of the implementation is to prove that nothing else reads the tail, that the M1 program has room and valid indices for the new entries, and that the new sample plays in a scripted fight without changing the KOF audio. If the check fails or the tail fills up, work stops and returns to the owner with the options and their costs. The native separate audio path is not built automatically.
6. **Stand-in meanwhile.** Until an own voice plays, the fighter uses the KOF sound of the equivalent action (rule 2).
7. **Game data stays private.** SVC samples live under `private/` and are placed by a local tool from the user's own dumps. Only addresses, sizes, counts and hashes go to git.

Read-only check done in this session (no bytes copied, nothing changed), on the decrypted KOF 2003 M1 (SHA-256 `13e6ed399292eff412d5c7ddb2285111afda8342efb06ba6d2d865775abfadc6`) and V1+V2 (SHA-256 `44ee6c1f3c9f11d604df05cf54be7acde53cad556bf19ff9f46f5bb928a97fa2`):

- None of the 1,820 ADPCM-A rows and 28 ADPCM-B rows reaches the tail. The highest ADPCM-A page is `$EFFF` and the highest ADPCM-B page is `$FFBF`.
- The tail is 16,384 bytes of one repeated value, and so are the 512 bytes before it.
- In the first 128 KiB of M1, the only 16-bit words in `$FFC0`–`$FFFF` after a recognisable load instruction are Z80 RAM addresses (stack at `$FFFC` and variables). The scan cannot prove absence of reads, because the chip's page registers are written as separate bytes. Following the code that writes those registers stays in step 5.
- M1 room: a run of 6,250 zero bytes at `[$1E796,$20000)`, identical in the four 128 KiB regions but in the banked area, and runs of at most 395 bytes in the fixed 32 KiB window. Two new descriptors need 12 bytes. The packed validity map of the Z80 sound groups (directory at `$2E22`) is still unread and may be the real limit.

_PT-BR: decisões do dono em 16/11/2026, valendo para todo Personagem Importado. A regra tem sete partes._

1. _**Escopo dos sons próprios.** Só as duas vozes de ataque medidas no [26](26-svc-guile-sounds.md) entram nesta fatia: soco fraco em pé e ataque de Guard Cancel, 3.840 bytes no total. As vozes de dor, nocaute e vitória esperam outro ticket. A recuperação de queda fica muda, como no SVC, onde o programa M1 desativa esse pedido._
2. _**Efeitos compartilhados.** Cada ação copia o código de som que o KOF 2003 já toca na ação de mesma função (andar, dash ou corrida, saída e pouso de pulo, defesa, golpe, impacto leve). O dono escolhe à mão só onde o SVC tem um som sem par no KOF, como o contato imediato do Guard Cancel._
3. _**Gatilho da voz.** A voz toca toda vez que o ataque começa, pela palavra de som do script do passo. A regra condicional do SVC não é copiada._
4. _**Rota das amostras próprias.** A rota original do KOF 2003: as amostras vão para a faixa livre `[$FFC000,$1000000)` da região V (16.384 bytes), um descritor entra no programa M1 e o mapeamento do 68000 é ligado. A alocação é por ordem de chegada, só com amostras inteiras, e um livro-caixa registra deslocamento e tamanho de cada uma. Não há cota fixa por lutador._
5. _**Primeiro verificar.** A primeira etapa da implementação prova que nada mais lê a faixa, que o programa M1 tem espaço e índices válidos para as entradas novas e que a amostra nova toca numa luta automatizada sem alterar o áudio do KOF. Se a verificação falhar ou a faixa encher, o trabalho para e volta ao dono com as opções e seus custos. O caminho nativo separado não é construído automaticamente._
6. _**Reserva enquanto isso.** Até uma voz própria tocar, o lutador usa o som do KOF da ação equivalente (parte 2)._
7. _**Dados dos jogos ficam privados.** As amostras do SVC ficam em `private/` e são colocadas por uma ferramenta local a partir dos dumps do próprio usuário. Só endereços, tamanhos, contagens e hashes vão para o git._

_Conferência só de leitura feita nesta sessão (nenhum byte copiado, nada alterado), na M1 decifrada do KOF 2003 (SHA-256 `13e6ed399292eff412d5c7ddb2285111afda8342efb06ba6d2d865775abfadc6`) e em V1+V2 (SHA-256 `44ee6c1f3c9f11d604df05cf54be7acde53cad556bf19ff9f46f5bb928a97fa2`):_

- _Nenhuma das 1.820 entradas ADPCM-A e das 28 ADPCM-B chega à faixa livre. A maior página do ADPCM-A é `$EFFF` e a do ADPCM-B é `$FFBF`._
- _A faixa tem 16.384 bytes de um único valor repetido, e os 512 bytes antes dela também._
- _Nos primeiros 128 KiB da M1, as únicas palavras de 16 bits em `$FFC0`–`$FFFF` depois de uma instrução de carga reconhecível são endereços de RAM do Z80 (pilha em `$FFFC` e variáveis). A busca não prova que ninguém lê a faixa, porque os registradores de página do chip recebem bytes soltos. Acompanhar o código que escreve neles fica na etapa 5._
- _Espaço na M1: um trecho de 6.250 bytes zerados em `[$1E796,$20000)`, idêntico nas quatro regiões de 128 KiB, mas na área com troca de banco, e trechos de no máximo 395 bytes na janela fixa de 32 KiB. Duas entradas novas pedem 12 bytes. O mapa compactado de validade dos grupos de som do Z80 (diretório em `$2E22`) segue sem leitura e pode ser o limite real._

## Comments

- 2026-11-17 — The owner reconfirmed the three policy boundaries after a design review: the V tail remains a single first-come, first-served allocation with no per-fighter quota; a failed safety check stops the import and returns options and costs to the owner, without automatically building a separate audio route; and each action with no KOF 2003 counterpart keeps an explicit manual sound choice in its implementation ticket. / _O dono reconfirmou os três limites de política após a revisão de desenho: a cauda V continua uma alocação única por ordem de chegada, sem cota por lutador; uma verificação de segurança que falhe interrompe a importação e devolve opções e custos ao dono, sem construir automaticamente uma rota de áudio separada; e cada ação sem equivalente no KOF 2003 mantém uma escolha manual explícita de som no ticket de implementação._
