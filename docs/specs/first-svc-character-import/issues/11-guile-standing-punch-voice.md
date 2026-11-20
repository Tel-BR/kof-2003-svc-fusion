---
title: "Guile's standing-punch voice plays from SVC data"
triage: ready-for-agent
---

# 11 Guile's standing-punch voice plays from SVC data

[Parent specification](../spec.md)

## What to build

The first sample imported from SVC plays end to end in native KOF 2003: Guile's standing light punch voice (1,792 bytes), every time the attack starts. A local tool reads the sample from the user's own SVC dump and places it in the free tail of the sample region, whole and page-aligned, following the placement approved in [09](09-verify-free-sound-space.md). The M1 descriptor, the 68000 mapping and the sound word at the start of the attack step connect it. The rule is the one decided in [wayfinder ticket 27](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md).

## Blocked by

[09 Verify the free V tail and the M1 room for imported sounds](09-verify-free-sound-space.md) · [10 Guile plays the KOF 2003 sounds of his shared actions](10-guile-reuses-kof-sounds.md)

## Acceptance criteria

- [ ] A scripted native match shows the sound request and the chip key-on for the new range at every standing light punch, hit, block or whiff.
- [ ] The sounds of original fighters in the same scripted match are unchanged, and the music keeps playing.
- [ ] The owner listens to the result and confirms the voice sounds right.
- [ ] The tool works from the user's own dumps. The sample, the changed sound program and any dump stay under `private/`, and git holds only addresses, sizes, counts and hashes.

## Português (Brasil)

A primeira amostra importada do SVC toca de ponta a ponta no KOF 2003 nativo: a voz do soco fraco em pé do Guile (1.792 bytes), toda vez que o golpe começa. Uma ferramenta local lê a amostra do dump do SVC do próprio usuário e a coloca inteira, alinhada em páginas, na faixa livre da região de amostras, seguindo a colocação aprovada no [09](09-verify-free-sound-space.md). O descritor na M1, o mapeamento do 68000 e a palavra de som no início do passo do golpe ligam tudo. A regra é a decidida no [ticket 27 do wayfinder](../../../wayfinder/guile-adelheid-slot/tickets/27-guile-sounds-route.md).

### Bloqueios

[09 Verify the free V tail and the M1 room for imported sounds](09-verify-free-sound-space.md) · [10 Guile plays the KOF 2003 sounds of his shared actions](10-guile-reuses-kof-sounds.md)

### Critérios de aceitação

- [ ] Uma luta nativa por script mostra o pedido de som e o início da amostra no chip para a faixa nova em todo soco fraco em pé, seja acerto, defesa ou golpe no vazio.
- [ ] Os sons dos lutadores originais na mesma luta por script não mudam, e a música continua tocando.
- [ ] O dono ouve o resultado e confirma que a voz soa certa.
- [ ] A ferramenta trabalha a partir dos dumps do próprio usuário. A amostra, o programa de som alterado e qualquer dump ficam em `private/`, e o git guarda só endereços, tamanhos, contagens e hashes.
