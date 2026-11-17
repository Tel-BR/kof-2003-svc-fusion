---
id: 25
title: "How KOF 2003 plays a fighter's sounds and whether it can take new ones"
label: wayfinder:research
mode: AFK
status: open
assignee:
blocked_by: []
research:
---

## Question

Guile will use his own SVC sounds, voice and effects ([13](13-adelheid-sounds.md), superseded). How does KOF 2003 play a fighter's sound: how does a sound code in a step script or in the 16 per-fighter situation tables at `$6CF1E` reach the sound driver, what does the driver do with it (command word, Z80 sound program, ADPCM samples), and where do the samples live? How much room do the sound program and the sample ROMs have free, can the sample set grow the way the Graphics Set did, and what limits the number of distinct codes? Read the program, the sound ROM and the driver; do not copy bytes into the repository.

_PT-BR: o Guile vai usar os sons dele no SVC, voz e efeitos ([13](13-adelheid-sounds.md), substituído). Como o KOF 2003 toca o som de um lutador: como um código de som num script de passos ou nas 16 tabelas de situação por lutador em `$6CF1E` chega ao driver de som, o que o driver faz com ele (palavra de comando, programa Z80, amostras ADPCM) e onde ficam as amostras? Quanto espaço livre têm o programa de som e as ROMs de amostras, o conjunto de amostras pode crescer como o Conjunto gráfico cresceu, e o que limita o número de códigos distintos? Ler o programa, a ROM de som e o driver; não copiar bytes para o repositório._

## Notes

- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): sound codes sit in the per-fighter step scripts (a code word after a flag bit) and in 16 per-fighter situation tables at `$6CF1E`.
- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.

_PT-BR: os códigos de som ficam nos scripts de passos de cada lutador e em 16 tabelas de situação por lutador em `$6CF1E`. Regra obrigatória do `AGENTS.md`: só endereços, tamanhos, contagens e hashes nas notas._
