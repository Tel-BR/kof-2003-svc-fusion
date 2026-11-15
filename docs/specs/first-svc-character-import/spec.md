---
title: "First SVC Chaos character import into KOF 2003"
triage: ready-for-agent
---

# First SVC Chaos character import into KOF 2003

## Problem Statement

We want to play a fighter exclusive to SVC Chaos in native KOF 2003 on PC and learn what it would take to import more fighters. The existing Windows port passed the native MVS verification run. Its AES Single path still needs validation. The Iori comparison showed that matching sprites and timing can coexist with different animation records and attack boxes, so visual similarity alone cannot establish that an import plays correctly. [Native KOF 2003 run](../../wayfinder/base-direction/tickets/09-run-kof2003-port.md) · [1v1 fight in KOF 2003](../../wayfinder/base-direction/tickets/05-kof2003-1v1-fight.md) · [Animation format](../../wayfinder/base-direction/tickets/08-animation-format.md)

## Solution

Make one SVC Exclusive Character selectable in native KOF 2003. Complete a reproducible MVS team match using recorded inputs and check the Imported Character with Multi-Shift. Use SVC Chaos as the reference for the fighter's identity and moves, and KOF 2003 as the reference for how those moves interact with the fight. Record the work that can carry over to another import and the work that required fighter-specific adaptation. [Decision record](../../adr/0001-kof-2003-base-for-first-import.md)

## User Stories

1. As a player, I want to select the Imported Character through the game's selection flow, so that I can use the fighter in a normal match.
2. As a player, I want to recognize the fighter's sprites, animations and moves from SVC Chaos, so that the import retains the fighter's identity.
3. As a player, I want the fighter to move, defend and perform the selected moveset from the expected inputs, so that I can control the fighter consistently.
4. As a player, I want attacks, blocks and misses to resolve according to KOF 2003's collision rules, so that the import behaves predictably against an original fighter.
5. As a player, I want damage, priority and juggle behavior to follow KOF 2003, so that the Imported Character participates in the same combat system.
6. As a player, I want the fighter's signature super available under KOF 2003's Leader Super rules, so that its use makes sense in the Base Game.
7. As a player, I want cancel sequences permitted by KOF 2003 to work, so that the Imported Character can use the Base Game's combo rules.
8. As a player, I want the team match to reach a normal match result, so that I can play the import from selection to the end of the match.
9. As a player, I want the Imported Character to enter, leave and return to the active slot in team play, so that I can use it with Multi-Shift.
10. As a player, I want original KOF 2003 fighters to remain playable, so that adding the import preserves the existing roster.
11. As a tester, I want to replay the same match inputs against the same starting state, so that I can reproduce a failure and verify a fix.
12. As a tester, I want to compare the original SVC moves with the import's observable behavior, so that I can distinguish intentional adaptations from bugs.
13. As a tester, I want native execution, state divergences, cycle differences and interpreter fallback reported, so that I can judge the quality of the native run.
14. As a contributor, I want to prepare the build with my own validated dumps, so that I can reproduce the result locally.
15. As a contributor, I want a repeatable import process with documented manual steps, so that I can assess how much effort a second fighter would take.
16. As the project owner, I want measured effort and estimates reported distinctly, so that I can compare the two conversion directions before committing to a larger roster.

## Implementation Decisions

- KOF 2003 is the Base Game. SVC Chaos is the Donor Game. The owner selected Guile from the approved SVC MVS roster of Exclusive Characters on 2026-11-15 ([ticket 03](issues/03-capture-svc-fighter-reference.md)). Use the recorded SVC execution to establish the selected fighter's reference moves and behavior. [Rosters in both directions](../../wayfinder/base-direction/tickets/03-rosters-both-directions.md)
- Establish a reproducible, modifiable KOF 2003 build and reproduce the native MVS control with the validated inputs. Use MVS team play for the first imported match and compare the original team match flow and Leader Super behavior against a working reference. AES Single is not a prerequisite for this milestone.
- Translate the fighter's animations, frame timing, collision data and move behavior into the representations used by KOF 2003. Integrate the fighter into selection and match flow. Follow the Base Game for damage, priority, juggle, meter, signature super activation and cancels. Record intended differences from SVC, including how the selected fighter's Exceed maps to Leader Super. Confirm the source activation conditions and the destination eligibility and cost from the reference runs. [Mechanics equivalence](../../wayfinder/base-direction/tickets/04-mechanics-equivalence.md)
- Exercise Multi-Shift in team play. Supply the selected fighter's required entry, exit and return behavior, including the entry attack where the Base Game expects it.
- Reuse the validated cartridge regions and user-supplied dumps. Keep ROMs, generated code, extracted assets, captures and traces with game data in the ignored `private/` area. Keep third-party source outside the tracked tree while the project license remains undecided.

## Testing Decisions

- **Primary test approved by the owner.** Use the native player's selection and match flow with a fixed input sequence and known initial state. Select the import, start a team match against original KOF 2003 fighters, exercise its controls and finish the match through the normal result screen. Reuse headless scripted input and observable game state, as in the KOF 2003 port verification. The test covers selection, conversion and combat together through the player's entry point.
- Observe the fighter's movement, animation timing, and at least one hit, block and miss. Check the selected fighter's signature super under the KOF activation and meter rules. Verify an allowed cancel and a donor-only sequence that KOF does not allow, using the references to define each expected result. Check collision through observable results such as contact, damage and reaction. [Animation and collision comparison](../../wayfinder/base-direction/tickets/08-animation-format.md) · [Mechanics equivalence](../../wayfinder/base-direction/tickets/04-mechanics-equivalence.md)
- Run the modified match segment with native verification against the same build's interpreter when supported by the chosen runtime. Record native blocks and coverage, interpreter fallback, state divergences and cycle differences. Require native execution of the Imported Character's exercised gameplay and resolve state divergences before accepting the native match. Use the original native MVS run as a regression control and keep its cycle counts separate from state comparisons. [Native verification precedent](../../wayfinder/base-direction/tickets/09-run-kof2003-port.md)
- Play a scripted team segment that switches the import in, out and back in. Check active slot, relevant health and meter state, entry behavior and continuation of the fight. Keep a reference fight with original KOF 2003 fighters to check existing play.
- Record the build and inputs, match result and evidence that another contributor can reproduce. For effort, log reusable tooling and per-fighter work separately, including manual steps and blockers. Record measured effort and a separate estimate of what a second fighter would reuse, with assumptions and remaining unknowns.

## Out of Scope

- A second Imported Character, full roster expansion and selectable alternate versions of Shared Characters.
- The reverse KOF 2003 → SVC conversion test, full native SVC support and the future Versus mode with both rulesets and both stage selections.
- New Arcade routes or endings, online play and physical MVS cartridge support.

## Further Notes

The next step is `/to-tickets`. The native MVS team baseline can be prepared independently of the owner selecting the fighter. Before any roster expansion, the ADR calls for a small reverse conversion test on a working SVC reference and a comparison of both directions. The [Versus fusion map](../../wayfinder/versus-fusion/map.md) tracks the longer-term goal.

# Primeira importação de um personagem do SVC Chaos para o KOF 2003

## Problema

Queremos jogar com um exclusivo do SVC Chaos no KOF 2003 nativo para PC e entender o esforço de importar mais lutadores. O port Windows passou na verificação nativa do MVS. O caminho para o modo Single do AES ainda precisa ser validado. A comparação do Iori mostrou que sprites e durações iguais podem coexistir com registros de animação e caixas de ataque diferentes. A semelhança visual, por si só, não confirma que a importação funciona em luta. [Execução nativa do KOF 2003](../../wayfinder/base-direction/tickets/09-run-kof2003-port.md) · [Luta 1x1 no KOF 2003](../../wayfinder/base-direction/tickets/05-kof2003-1v1-fight.md) · [Formato de animação](../../wayfinder/base-direction/tickets/08-animation-format.md)

## Solução

Tornar um personagem exclusivo do SVC selecionável no KOF 2003 nativo. Completar uma luta de equipes MVS reproduzível com entradas gravadas e conferir o personagem importado com Multi-Shift. Usar o SVC Chaos como referência para a identidade e os golpes do lutador e o KOF 2003 como referência para a interação desses golpes com a luta. Registrar o trabalho que pode ser reaproveitado e as adaptações próprias daquele lutador. [Registro da decisão](../../adr/0001-kof-2003-base-for-first-import.md)

## Histórias de usuário

1. Como jogador, quero escolher o personagem importado na seleção do jogo para usá-lo numa luta normal.
2. Como jogador, quero reconhecer os sprites, as animações e os golpes do SVC Chaos para identificar o lutador importado.
3. Como jogador, quero movimentar o lutador, defender e executar seus golpes com os comandos esperados para controlá-lo de forma consistente.
4. Como jogador, quero que acertos, defesas e golpes no vazio sigam as regras de colisão do KOF 2003 para que o importado se comporte de forma previsível contra um lutador original.
5. Como jogador, quero que dano, prioridade e juggle sigam o KOF 2003 para que o importado participe do mesmo sistema de combate.
6. Como jogador, quero usar o especial de assinatura sob as regras de Leader Super para que ele faça sentido no jogo base.
7. Como jogador, quero executar as sequências de cancelamento permitidas pelo KOF 2003 para usar as regras de combo do jogo base.
8. Como jogador, quero que a luta em equipes chegue ao resultado normal para jogar com o importado da seleção ao fim da partida.
9. Como jogador, quero que o importado entre, saia e volte à posição ativa em equipe para usá-lo com Multi-Shift.
10. Como jogador, quero continuar escolhendo os lutadores originais do KOF 2003 para preservar o elenco existente.
11. Como testador, quero repetir a luta com as mesmas entradas e o mesmo estado inicial para reproduzir falhas e conferir correções.
12. Como testador, quero comparar os golpes originais do SVC com o comportamento observável do importado para identificar adaptações intencionais e bugs.
13. Como testador, quero ver a execução nativa, as divergências de estado, as diferenças de ciclos e os retornos ao interpretador para avaliar a qualidade da execução.
14. Como colaborador, quero preparar o build com meus próprios dumps validados para reproduzir o resultado localmente.
15. Como colaborador, quero um processo de importação repetível, com as etapas manuais registradas, para avaliar o esforço de um segundo lutador.
16. Como dono do projeto, quero ver medições e estimativas registradas à parte para comparar os dois sentidos de conversão antes de investir num elenco maior.

## Decisões de implementação

- KOF 2003 é o jogo base. SVC Chaos é o jogo doador. Em 15/11/2026 o dono escolheu Guile da lista aprovada de exclusivos do SVC MVS ([ticket 03](issues/03-capture-svc-fighter-reference.md)). Usar uma execução do SVC como referência para os golpes e o comportamento do escolhido. [Elencos nos dois sentidos](../../wayfinder/base-direction/tickets/03-rosters-both-directions.md)
- Obter um build reproduzível e modificável do KOF 2003 e reproduzir o controle nativo de MVS com as entradas validadas. Usar o modo de equipes MVS na primeira luta com o importado e comparar o fluxo original da luta e o Leader Super com uma referência funcional. O Single do AES deixa de ser pré-requisito deste marco.
- Traduzir as animações, durações, dados de colisão e comportamento dos golpes para os formatos do KOF 2003. Integrar o lutador à seleção e ao fluxo da luta. Seguir o jogo base para dano, prioridade, juggle, barra, ativação do especial de assinatura e cancelamentos. Registrar diferenças intencionais em relação ao SVC, incluindo como o Exceed do lutador vira Leader Super. Confirmar nas execuções de referência as condições de ativação na origem e a disponibilidade e o custo no destino. [Equivalência de mecânicas](../../wayfinder/base-direction/tickets/04-mechanics-equivalence.md)
- Testar Multi-Shift em equipe. Fornecer o comportamento necessário de entrada, saída e retorno do lutador, incluindo o golpe de entrada onde o jogo base o espera.
- Reaproveitar as regiões validadas e os dumps fornecidos pelo usuário. Manter ROMs, código gerado, recursos extraídos, capturas e traces com dados dos jogos na área ignorada `private/`. Manter código de terceiros fora dos arquivos rastreados enquanto a licença do projeto estiver em aberto.

## Decisões de teste

- **Teste principal aprovado pelo dono.** Usar o fluxo de seleção e luta do port nativo com uma sequência fixa de entradas e estado inicial conhecido. Selecionar o importado, iniciar uma luta de equipes contra lutadores originais do KOF 2003, exercitar seus controles e terminar a luta na tela normal de resultado. Reaproveitar entradas por script sem janela e observação do estado do jogo, como na verificação do port. O teste cobre seleção, conversão e combate juntos pelo caminho que o jogador usa.
- Observar movimentação, duração das animações e pelo menos um acerto, uma defesa e um golpe no vazio. Conferir o especial de assinatura sob as regras de ativação e barra do KOF. Testar um cancelamento permitido e uma sequência exclusiva do doador que o KOF não permite, usando as referências para definir o resultado esperado. Conferir colisões por efeitos observáveis como contato, dano e reação. [Comparação de animação e colisão](../../wayfinder/base-direction/tickets/08-animation-format.md) · [Equivalência de mecânicas](../../wayfinder/base-direction/tickets/04-mechanics-equivalence.md)
- Rodar o trecho da luta modificada com verificação nativa contra o interpretador do mesmo build quando o runtime escolhido oferecer esse recurso. Registrar blocos e cobertura nativa, retornos ao interpretador, divergências de estado e diferenças de ciclos. Exigir execução nativa do comportamento exercitado do importado e resolver as divergências de estado antes de aceitar a luta nativa. Usar o teste nativo original de MVS como controle de regressão e tratar as contagens de ciclos à parte das comparações de estado. [Precedente de verificação nativa](../../wayfinder/base-direction/tickets/09-run-kof2003-port.md)
- Executar um trecho em equipe por script que ponha o importado na luta, o retire e o traga de volta. Conferir a posição ativa, o estado relevante de vida e barra, a entrada e a continuidade da luta. Usar uma luta de referência com personagens originais do KOF 2003 para conferir o comportamento existente.
- Registrar o build, as entradas, o resultado da luta e evidências que outro colaborador possa reproduzir. Para medir esforço, registrar à parte as ferramentas reutilizáveis e o trabalho por lutador, incluindo etapas manuais e bloqueios. Publicar o esforço medido e uma estimativa separada do que um segundo lutador reaproveitaria, com hipóteses e dúvidas em aberto.

## Fora do escopo

- Um segundo personagem importado, a ampliação do elenco e versões alternativas selecionáveis dos personagens compartilhados.
- O teste inverso de conversão KOF 2003 → SVC, o suporte nativo completo do SVC e o futuro Versus com os dois conjuntos de regras e as duas seleções de cenários.
- Novas rotas ou finais de Arcade, jogo online e suporte a cartuchos MVS físicos.

## Notas adicionais

O próximo passo é `/to-tickets`. A referência de equipe MVS pode ser preparada enquanto a escolha do lutador está em aberto. Antes de ampliar o elenco, a ADR prevê um teste pequeno no sentido inverso com uma referência funcional do SVC e a comparação dos dois sentidos. O [mapa da fusão no Versus](../../wayfinder/versus-fusion/map.md) acompanha a meta de longo prazo.
