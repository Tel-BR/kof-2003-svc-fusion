---
id: 05
title: "1v1 fight in KOF 2003"
label: wayfinder:research
mode: AFK
status: closed
assignee: Tel-BR
blocked_by: []
research: research/05-kof2003-1v1-fight:docs/wayfinder/base-direction/research/05-kof2003-1v1-fight.md
---

## Question

Does any version of KOF 2003 have a 1v1 fight (hint: the console Team Play mode), or is there a 1v1 feature in the MVS code? If KOF 2003 is the Base Game, how much does it cost to have 1v1 for the tests?

_PT-BR: existe luta 1x1 em alguma versão do KOF 2003 (pista: Team Play do console) ou algum recurso no código MVS? Se a base for o KOF 2003, quanto custa ter 1x1 para os testes?_

## Resolution

**Arcade and home modes.** In the accepted `kof2003` Export set, the owner's MAME 0.289 check found no single-battle setting in the complete Europe MVS soft-DIP menu. The partial Japan menu check found none either. The reported MVS soft DIP therefore has no confirmation for this set. The owner saw a Single option in the cartridge's AES home mode through Universe BIOS 4.0. The AES fight itself, including team size, rounds, health and Leader super, remains unverified. PS2 reports describe the Single modes as 1v1 and Team Play as 3v3 without switching. The Xbox mode list was not independently confirmed.

**Cost for the first tests.** If KOF 2003 becomes the Base Game, the cartridge's AES mode is the lowest-effort candidate. Reusing it in the native runtime depends on that runtime supporting the cartridge's home-mode path. FBNeo's training script keeps three fighters per side. Draining two slots is an unvalidated workaround that can affect fight rules. A custom 1v1 with separate rounds and a defined win condition would need changes to game logic and validation in the port. The research does not establish a reliable effort estimate for that work.

**PT-BR**

**Modos arcade e console.** No conjunto Export `kof2003` aceito para o projeto, o dono conferiu no MAME 0.289 que o menu completo de soft DIPs do MVS com BIOS europeia não traz opção de luta individual. Na conferência parcial com BIOS japonesa também não apareceu. A opção de soft DIP relatada segue sem confirmação para esse conjunto. O dono viu uma opção Single no modo console AES do próprio cartucho via Universe BIOS 4.0. O comportamento da luta no AES ainda precisa ser conferido, incluindo tamanho do time, rounds, vida e golpe de Leader. Relatos sobre o PS2 descrevem os modos Single como 1x1 e o Team Play como 3x3 sem troca. A lista de modos do Xbox ficou sem confirmação independente.

**Custo para os primeiros testes.** Se o KOF 2003 for o jogo base, o modo AES do cartucho é o caminho de menor esforço a avaliar. Reaproveitá-lo no runtime nativo depende de o runtime conseguir iniciar o cartucho pelo modo console. O script de treino do FBNeo mantém três lutadores por lado. Zerar a vida de dois membros por lado é um recurso ainda sem validação e pode alterar as regras da luta. Um 1x1 próprio com rounds separados e condição de vitória definida exigiria mudanças na lógica do jogo e validação no port. A pesquisa não permite estimar com confiança o esforço desse trabalho.

Research / Pesquisa: `research/05-kof2003-1v1-fight:docs/wayfinder/base-direction/research/05-kof2003-1v1-fight.md` (commit `39f7974`).
