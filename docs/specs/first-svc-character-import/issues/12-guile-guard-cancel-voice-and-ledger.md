---
title: "Guile's Guard Cancel attack voice and the sample ledger"
triage: ready-for-agent
---

# 12 Guile's Guard Cancel attack voice and the sample ledger

[Parent specification](../spec.md)

## What to build

Guile's Guard Cancel attack plays its own SVC voice (2,048 bytes) every time the attack starts, using the same route as the first voice. A ledger records every sample placed in the free tail (offset, size, hash, owning fighter, and the descriptor and sound word that use it) and the space that remains, and the placement process is written down as the import rule for the next SVC fighter, following [wayfinder ticket 27](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md).

## Blocked by

[11 Guile's standing-punch voice plays from SVC data](11-guile-standing-punch-voice.md) · Guile's Guard Cancel attack imported and working in the native match (no implementation ticket yet; it follows the review of ticket 04)

## Acceptance criteria

- [ ] A scripted native match shows the sound request and chip key-on for the second range at every Guard Cancel attack.
- [ ] The ledger lists both voices with their offsets, sizes (1,792 and 2,048 bytes) and hashes, and states the remaining tail space, which is 12,544 bytes if nothing else was placed.
- [ ] The written rule says how a new fighter's own samples are placed and recorded, when work stops and returns to the owner, and what the fighter plays meanwhile.
- [ ] Original fighters' sounds are unchanged and no game bytes enter git.

## Português (Brasil)

O ataque de Guard Cancel do Guile toca a voz própria do SVC (2.048 bytes) toda vez que o golpe começa, pela mesma rota da primeira voz. Um livro-caixa registra cada amostra colocada na faixa livre (deslocamento, tamanho, hash, lutador dono e o descritor e a palavra de som que a usam) e o espaço que resta, e o processo de colocação fica escrito como regra de importação para o próximo lutador do SVC, seguindo o [ticket 27 do wayfinder](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md).

### Bloqueios

[11 Guile's standing-punch voice plays from SVC data](11-guile-standing-punch-voice.md) · o ataque de Guard Cancel do Guile importado e funcionando na luta nativa (ainda sem ticket de implementação; vem depois da revisão do ticket 04)

### Critérios de aceitação

- [ ] Uma luta nativa por script mostra o pedido de som e o início da amostra no chip para a segunda faixa em todo ataque de Guard Cancel.
- [ ] O livro-caixa lista as duas vozes com deslocamentos, tamanhos (1.792 e 2.048 bytes) e hashes, e informa o espaço que resta na faixa, 12.544 bytes se nada mais foi colocado.
- [ ] A regra escrita diz como as amostras próprias de um lutador novo são colocadas e registradas, quando o trabalho para e volta ao dono e o que o lutador toca enquanto isso.
- [ ] Os sons dos lutadores originais não mudam e nenhum byte dos jogos entra no git.
