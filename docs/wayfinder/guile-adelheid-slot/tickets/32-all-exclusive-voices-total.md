---
id: 32
title: "How many bytes of own sound all SVC Exclusive Characters need, and the routes to a larger sound space"
label: wayfinder:research
mode: AFK
status: open
assignee:
blocked_by: [31]
research:
---

## Question

[31](31-guile-remaining-voices-choice.md) leaves Guile's extra voices out for lack of space and states the owner's goal: bring every voice of every Exclusive Character later, through a more aggressive expansion of the sound space. How many bytes of character-specific sound (voices and Guile-only-style effects, deduplicated, in 256-byte pages) do all SVC Exclusive Characters need together, per fighter and in total, in the same classification as [30](30-guile-svc-remaining-sounds.md)? And which routes exist to give KOF 2003 that much room: what the address space of the chip, the V region and the M1 program allow, what a larger V region would need in the native port, and what each route costs? Read the SVC and KOF 2003 sound data statically or with MAME as the reading instrument; the output is sizes, counts and costs, not a decision to build.

_PT-BR: o [31](31-guile-remaining-voices-choice.md) deixa as vozes extras do Guile de fora por falta de espaço e registra o objetivo do dono: trazer todas as vozes de todos os exclusivos depois, por uma expansão mais agressiva do espaço de som. Quantos bytes de som próprio (vozes e efeitos só do personagem, sem repetição, em páginas de 256 bytes) todos os Personagens Exclusivos do SVC pedem juntos, por lutador e no total, na mesma classificação do [30](30-guile-svc-remaining-sounds.md)? E que rotas existem para dar esse espaço ao KOF 2003: o que o espaço de endereços do chip, a região V e o programa M1 permitem, o que uma região V maior exigiria no port nativo e quanto cada rota custa? Ler os dados de som do SVC e do KOF 2003 de forma estática ou com o MAME como instrumento de leitura; a saída são tamanhos, contagens e custos, não decisão de construir._

## Notes

- Scope: sizing and routes only. Building the expansion is out of scope for this map.
- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.
