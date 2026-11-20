---
title: "Guile plays the KOF 2003 sounds of his shared actions"
triage: ready-for-agent
---

# 10 Guile plays the KOF 2003 sounds of his shared actions

[Parent specification](../spec.md)

## What to build

In the native match, Guile's actions that have the same job in KOF 2003 (walk, dash or run, jump takeoff and landing, guard, swing, light hit) play the sound that KOF 2003 already plays for that action, copied by a mechanical rule that works for any Imported Character ([wayfinder ticket 27](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md)). Where SVC has a sound with no KOF 2003 counterpart, such as the immediate Guard Cancel contact, the owner picks the sound by hand. The two moments that will later carry an own voice (standing light punch and Guard Cancel attack) play the KOF 2003 sound of the equivalent action in the meantime. The break-fall stays silent.

## Blocked by

[04 Complete the first Imported Character match](04-complete-first-imported-match.md)

## Acceptance criteria

- [ ] A table pairs each of Guile's shared actions with the KOF 2003 action it copies its sound from, and lists the cases that needed a manual pick with the owner's choice.
- [ ] A scripted native match shows a sound request for each paired action at the expected frame, and none for the break-fall.
- [ ] Original fighters' sounds in the same scripted match are unchanged.
- [ ] No game bytes enter git.

## Português (Brasil)

Na luta nativa, as ações do Guile que têm a mesma função no KOF 2003 (andar, dash ou corrida, saída e pouso de pulo, defesa, golpe, impacto leve) tocam o som que o KOF 2003 já toca nessa ação, copiado por uma regra mecânica que vale para qualquer Personagem Importado ([ticket 27 do wayfinder](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md)). Onde o SVC tem um som sem par no KOF 2003, como o contato imediato do Guard Cancel, o dono escolhe o som à mão. Os dois momentos que depois levarão uma voz própria (soco fraco em pé e ataque de Guard Cancel) tocam, enquanto isso, o som do KOF 2003 da ação equivalente. A recuperação de queda continua muda.

### Bloqueios

[04 Complete the first Imported Character match](04-complete-first-imported-match.md)

### Critérios de aceitação

- [ ] Uma tabela liga cada ação compartilhada do Guile à ação do KOF 2003 de onde o som é copiado e lista os casos de escolha manual com a escolha do dono.
- [ ] Uma luta nativa por script mostra um pedido de som para cada ação ligada, no quadro esperado, e nenhum na recuperação de queda.
- [ ] Os sons dos lutadores originais na mesma luta por script não mudam.
- [ ] Nenhum byte dos jogos entra no git.
