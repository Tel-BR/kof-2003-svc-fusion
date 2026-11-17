---
id: 25
title: "How KOF 2003 plays a fighter's sounds and whether it can take new ones"
label: wayfinder:research
mode: AFK
status: closed
assignee: codex-research
blocked_by: []
research: research/25-kof2003-sound-playback:docs/wayfinder/guile-adelheid-slot/research/25-kof2003-sound-playback.md
---

## Question

Guile will use his own SVC sounds, voice and effects ([13](13-adelheid-sounds.md), superseded). How does KOF 2003 play a fighter's sound: how does a sound code in a step script or in the 16 per-fighter situation tables at `$6CF1E` reach the sound driver, what does the driver do with it (command word, Z80 sound program, ADPCM samples), and where do the samples live? How much room do the sound program and the sample ROMs have free, can the sample set grow the way the Graphics Set did, and what limits the number of distinct codes? Read the program, the sound ROM and the driver; do not copy bytes into the repository.

_PT-BR: o Guile vai usar os sons dele no SVC, voz e efeitos ([13](13-adelheid-sounds.md), substituído). Como o KOF 2003 toca o som de um lutador: como um código de som num script de passos ou nas 16 tabelas de situação por lutador em `$6CF1E` chega ao driver de som, o que o driver faz com ele (palavra de comando, programa Z80, amostras ADPCM) e onde ficam as amostras? Quanto espaço livre têm o programa de som e as ROMs de amostras, o conjunto de amostras pode crescer como o Conjunto gráfico cresceu, e o que limita o número de códigos distintos? Ler o programa, a ROM de som e o driver; não copiar bytes para o repositório._

## Notes

- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): sound codes sit in the per-fighter step scripts (a code word after a flag bit) and in 16 per-fighter situation tables at `$6CF1E`.
- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.

_PT-BR: os códigos de som ficam nos scripts de passos de cada lutador e em 16 tabelas de situação por lutador em `$6CF1E`. Regra obrigatória do `AGENTS.md`: só endereços, tamanhos, contagens e hashes nas notas._

## Resolution

Both 68000 entry paths feed a sound request that strips the flags and translates the index. A replay followed a step request through the 68000 queue and sound latch to the Z80 dispatcher, then to the YM2610 key-on. The ordinary request index has 12 bits. Z80 sound groups impose their own tables and eligibility checks, so the field width alone does not give a count of playable sounds or reusable slots.

The two decrypted sample files fill the 16 MiB range that the YM2610 can address directly. The native loader accepts additional files. In a synthetic test of the playback adapter, encoding a start address just above that range wrapped to zero. The recovered ADPCM-A and ADPCM-B tables leave a uniform 16,384-byte tail at `[$FFC000,$1000000)` outside their references. It fits the voice payload measured in [26](26-svc-guile-sounds.md), pending a check for direct references and a native playback and regression test. Repeated blocks and padding in the Z80 program also give candidates, with no proven safe M1 allocation yet.

_PT-BR: os dois caminhos do 68000 chegam à rotina que trata os bits de controle e traduz o índice de som. Um replay acompanhou um pedido do script de passos pela fila e pelo registrador de comunicação do 68000, pelo despacho do Z80 e até o início da reprodução no YM2610. O índice comum tem 12 bits. Os grupos do Z80 têm tabelas e verificações próprias, então a largura do índice sozinha não dá a quantidade de sons disponíveis nem de entradas reaproveitáveis._

_Os dois arquivos de amostras decifrados ocupam os 16 MiB que o YM2610 endereça diretamente. O carregador nativo aceita outros arquivos. Num teste sintético do adaptador de reprodução, codificar um endereço inicial logo acima da faixa fez o endereço voltar a zero. A faixa uniforme de 16.384 bytes em `[$FFC000,$1000000)` fica fora das referências das tabelas ADPCM-A e ADPCM-B recuperadas. As vozes medidas no [26](26-svc-guile-sounds.md) cabem nessa faixa, que ainda precisa de uma busca por referências diretas e de teste de reprodução e regressão no runtime nativo. O programa do Z80 tem blocos repetidos e preenchimento, ainda sem espaço de M1 comprovado para a implantação._
