---
id: 26
title: "How SVC Chaos stores Guile's sounds and voice"
label: wayfinder:research
mode: AFK
status: closed
assignee: codex-research
blocked_by: []
research: research/26-svc-guile-sounds:docs/wayfinder/guile-adelheid-slot/research/26-svc-guile-sounds.md
---

## Question

For the actions in this slice (walking, guarding, one basic attack, run, backstep, four jumps, evasive rolls, both Guard Cancels, and his break-fall recovery), which sounds and voice lines does SVC play for Guile, which code in his step data starts each, and where are the samples (sound ROM, format, length)? How many distinct samples and how many bytes do they add up to, and which are shared with other SVC fighters or with the system? Read the program and the sound ROM; do not copy bytes into the repository.

_PT-BR: para as ações desta fatia (andar, defender, um golpe básico, corrida, passo para trás, quatro pulos, esquivas, os dois Guard Cancels e a recuperação de queda), que sons e falas o SVC toca para o Guile, que código nos dados de passos dele inicia cada um, e onde estão as amostras (ROM de som, formato, duração)? Quantas amostras distintas e quantos bytes elas somam, e quais são compartilhadas com outros lutadores do SVC ou com o sistema? Ler o programa e a ROM de som; não copiar bytes para o repositório._

## Notes

- [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md) covers animations, portrait and palettes; sounds were not inventoried.
- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.

_PT-BR: o inventário do ticket 05 cobre animações, retrato e paletas; os sons não foram inventariados. Regra obrigatória do `AGENTS.md`: só endereços, tamanhos, contagens e hashes nas notas._

## Resolution

Movement, attack startup, guard and immediate contact in the measured SVC slice use 17 distinct ADPCM-A samples covering 59,392 bytes, including stage and impact variants. The attack voice tables assign two conditional cues to Guile, for his standing light punch and Guard Cancel attack, occupying 3,840 bytes. The other 15 samples cover 55,552 bytes of shared effects. The catalog links action handlers and sound-table entries to the decrypted V ranges. Guile's successful break-fall issues a request whose entry the M1 program disables. [27](27-guile-sounds-route.md) records the rule to use KOF 2003's reusable sounds for shared effects.

_PT-BR: movimento, início de ataque, defesa e contato imediato da fatia medida no SVC usam 17 amostras distintas em ADPCM-A, somando 59.392 bytes com as variantes de cenário e impacto. As tabelas de voz de ataque atribuem duas vocalizações condicionais ao Guile, uma para o soco fraco em pé e outra para o ataque de Guard Cancel, somando 3.840 bytes. As outras 15 amostras somam 55.552 bytes de efeitos compartilhados. O catálogo liga as rotinas de ação e as entradas de som às faixas V decriptadas. Quando o Guile se recupera da queda, o jogo envia um pedido cuja entrada o programa M1 desativa. O [27](27-guile-sounds-route.md) registra a regra de usar sons reaproveitáveis do KOF 2003 nos efeitos compartilhados._
