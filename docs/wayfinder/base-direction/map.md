---
label: wayfinder:map
title: "Map: choosing the Base Game / Direção da base"
status: closed
---

# Map: choosing the Base Game

_Mapa: direção da base. Cada seção traz o inglês primeiro e o português logo depois._

Tickets live in [`tickets/`](./tickets/), one file per ticket; research findings live on `research/*` branches (see each ticket's `research` field), and the owner's starting leads in [`research/00-starting-leads.md`](./research/00-starting-leads.md). See "Wayfinding operations" in `docs/agents/issue-tracker.md` for how to query the frontier, claim, and resolve.

## Destination

Decide which game is the **Base Game** (KOF 2003 or SVC Chaos), with the reasoning recorded. Criterion: which direction makes the first milestone cheaper to reach. The milestone is, in order, the Base Game running natively on PC, then the Base Game with one **Imported Character**.

_PT-BR: decidir qual jogo é o **jogo base** (KOF 2003 ou SVC Chaos), com a justificativa registrada. Critério: qual direção torna mais barato chegar ao primeiro marco. O marco é, nessa ordem, o jogo base nativo no PC e depois o jogo base com um **personagem importado**._

## Notes

- **Domain:** a native PC port that unites the rosters of KOF 2003 and SVC Chaos (MVS). Use the vocabulary in [`GLOSSARY.md`](../../../GLOSSARY.md).
- **Central thesis:** the **Shared Characters** work as a Rosetta Stone. Correlating them reveals how each engine represents animation, hitboxes, move scripts and engine API, which is what makes a converter possible.
- **Inspiration:** tmcleroy/soulcalibur2-recomp unites the exclusives of three versions in one game, with rollback. Key difference: that was one game on three platforms; here there are two distinct games, so importing a fighter means understanding and translating data and code between engines.
- **Decider:** the repo owner answers every HITL ticket; collaborators comment. Facts are gathered by agents; decisions are the owner's. Every option comes with causes and consequences in plain language, and questions use the interactive question tool.
- **Skills:** `grilling` + `domain-modeling` for grilling tickets; `research` for research tickets; `prototype` if the conversion prototype becomes necessary; `wizard` for steps only the owner can do.
- **Evidence:** research + measurement. A conversion prototype in both directions only if the measurement is inconclusive.
- **Runtime premise:** the neogeorecomp foundation, where KOF 2003 already runs natively, is the yardstick for both games. If it costs little, both games run natively in the same runtime.
- **First tests in a 1v1 fight**, whatever the Base Game. Afterwards the format follows the Base Game.
- **Shared Characters:** at first only the Base Game's version.
- **Rules:** Imported Characters follow the Base Game's rules (juggle, priority, damage), with values derived from the correlation with the Shared Characters.
- **Roster count:** see the official MVS selection and boss weighting in [Rosters in both directions](tickets/03-rosters-both-directions.md).
- **Distribution:** open source, PC only (Windows, Linux, macOS).
- **Hard rule:** no game data in the repository, tickets or research notes (see `AGENTS.md`). Hashes, addresses, sizes and counts are fine.
- **Tracker:** local Markdown; moves to GitHub Issues once there is something the community can try.
- **Language:** ticket titles in English; bodies bilingual (English, then Brazilian Portuguese).
- **Planning only:** this map produces decisions, not code. Architecture and implementation belong to the next map.

_PT-BR:_
- _**Domínio:** port nativo para PC unindo os elencos de KOF 2003 e SVC Chaos (MVS). Ver o glossário._
- _**Tese central:** os **personagens compartilhados** funcionam como pedra de Roseta. Correlacioná-los revela como cada motor representa animação, hitbox, scripts de golpe e API do motor, o que permite construir um conversor._
- _**Inspiração:** tmcleroy/soulcalibur2-recomp une os exclusivos de três versões num só jogo, com rollback. Diferença crucial: lá era o mesmo jogo em três plataformas; aqui são dois jogos distintos, então importar um personagem exige entender e traduzir dados e código entre motores._
- _**Quem decide:** o dono do repositório responde todos os tickets HITL; colaboradores comentam. Fatos os agentes levantam; decisões são do dono. Cada opção vem com causas e consequências em linguagem simples, e as perguntas usam a ferramenta interativa._
- _**Skills:** `grilling` + `domain-modeling` para tickets de conversa; `research` para pesquisa; `prototype` se o protótipo de conversão for necessário; `wizard` para passos que só o dono pode fazer._
- _**Evidência:** pesquisa + medição. Protótipo de conversão nos dois sentidos só se a medição for inconclusiva._
- _**Premissa de runtime:** a fundação neogeorecomp, onde o KOF 2003 já roda nativo, serve de régua para os dois jogos. Se custar pouco, os dois rodam nativos no mesmo runtime._
- _**Testes iniciais em luta 1x1**, qualquer que seja o jogo base. Depois o formato segue o jogo base._
- _**Personagens compartilhados:** primeiro só a versão do jogo base._
- _**Regras:** personagens importados seguem as regras do jogo base (juggle, prioridade, dano), com valores derivados da correlação com os personagens compartilhados._
- _**Contagem de elenco:** ver seleção oficial do MVS e peso dos chefes em [Rosters in both directions](tickets/03-rosters-both-directions.md)._
- _**Distribuição:** código aberto, só PC (Windows, Linux, macOS)._
- _**Regra obrigatória:** nenhum dado dos jogos no repositório, nos tickets ou nas notas de pesquisa. Hashes, endereços, tamanhos e contagens podem._
- _**Tracker:** markdown local; vira GitHub Issues quando houver algo experimentável._
- _**Idioma:** títulos dos tickets em inglês; corpo bilíngue._
- _**Só planejamento:** este mapa produz decisões, não código. Arquitetura e implementação ficam para o mapa seguinte._

## Decisions so far

<!-- one line per closed ticket: [title](tickets/NN-slug.md): one-line gist -->

- [Dump the cartridges](tickets/01-cartridge-dumps.md): the owner's original carts are covered by the MAME-verified `kof2003` (Export), `svc` and `neogeo` zips in `private/`, accepted as the working dumps; per-chip hashes recorded. / _os zips verificados pelo MAME são os dumps de trabalho; hashes por chip registrados._
- [Existing documentation of both engines](tickets/02-existing-documentation.md): FBNeo has training and hitbox modules for both games. Shared hardware is documented and engine lineage remains unverified. / _O FBNeo tem módulos de treino e hitbox para os dois jogos. O hardware compartilhado está documentado e o parentesco dos motores segue sem comprovação._
- [Rosters in both directions](tickets/03-rosters-both-directions.md): official MVS selection yields 6 Shared Characters, 26 SVC exclusives (weighted 22) and 28 KOF 2003 exclusives (weighted 27). / _A seleção oficial do MVS dá 6 compartilhados, 26 exclusivos do SVC (peso 22) e 28 do KOF 2003 (peso 27)._
- [1v1 fight in KOF 2003](tickets/05-kof2003-1v1-fight.md): the Export cart shows an AES Single option and the checked MVS settings showed no equivalent. AES fight behavior and native runtime support remain to be verified. / _O cartucho Export mostra a opção Single no AES. Os menus MVS conferidos não mostraram opção equivalente. Falta verificar a luta no AES e o suporte no runtime nativo._
- [Mechanics equivalence](tickets/04-mechanics-equivalence.md): signature supers and cancels follow the Base Game, with Multi-Shift in KOF 2003 team play after the 1v1 test. / _Supers de assinatura e cancelamentos seguem o jogo base, com Multi-Shift nas lutas em equipe do KOF 2003 após o teste 1x1._
- [Run the KOF 2003 port with my dumps](tickets/09-run-kof2003-port.md): MVS ran natively on Windows with zero state divergences. Single mode validation remains pending. / _O MVS rodou em modo nativo no Windows com zero divergências de estado. A validação do modo Single segue pendente._
- [Decryption with existing tools](tickets/06-decryption-existing-tools.md): the existing KOF 2003 decryptor and the local SVC adaptations matched MAME 0.289 byte for byte in all five cartridge regions tested per game. / _O descriptografador existente do KOF 2003 e as adaptações locais para SVC bateram byte a byte com o MAME 0.289 nas cinco regiões de cartucho testadas de cada jogo._
- [Shared art](tickets/07-shared-art.md): 59,291 distinct nonzero 16×16 tile hashes match. Five Shared Characters have paired anchors, and Kyo uses separate anchors in each game. / _Há 59.291 hashes distintos de tiles 16×16 não zerados em comum. Cinco personagens compartilhados têm âncoras pareadas, e Kyo usa âncoras próprias em cada jogo._
- [Animation format](tickets/08-animation-format.md) — Iori's idle and standing light punch match in sampled sprite composition and timing. Frame references and collision layouts differ, and conversion cost by direction remains open. / _A espera e o soco fraco em pé do Iori coincidem na composição dos sprites e nas durações amostradas. As referências de quadro e os formatos de colisão diferem, e o custo por sentido de conversão segue em aberto._

- [Cost of making SVC native](tickets/10-svc-native-cost.md) — SVC reached the first round in the KOF 2003 runtime's interpreter after a loader workaround. Rendering was incomplete and native execution remains unverified. / _O SVC chegou ao primeiro round no interpretador do runtime do KOF 2003 após contornar a limitação do carregador. A renderização ficou incompleta e a execução nativa segue sem verificação._
- [Direction decision](tickets/11-direction-decision.md) — KOF 2003 is the Base Game for the first SVC exclusive. Compare conversion effort in both directions before expanding the roster. / _KOF 2003 é o jogo base para o primeiro exclusivo do SVC. Comparar o esforço de conversão nos dois sentidos antes de ampliar o elenco._

## Not yet specified

The first-import spec will define the fighter, acceptance criteria and how to measure the conversion work. The [Versus fusion map](../versus-fusion/map.md) carries the remaining questions about Shared Character versions and both rulesets.

_PT-BR: a especificação da primeira importação vai definir o lutador, os critérios de aceitação e como medir o trabalho de conversão. As questões sobre as versões dos personagens compartilhados e os dois conjuntos de regras seguem no [mapa da fusão no Versus](../versus-fusion/map.md)._

## Out of scope

Ruled beyond this map's destination; each may become its own future map. / _Fora do destino deste mapa; cada item pode virar um mapa futuro._

- **Foundation and licence** (first subject of the next map). Options: fork/use of the PolyForm Noncommercial KOF 2003 port, neogeorecomp (MIT, C), neogeo-recomp/cps2recomp (GPL-3, C++, with rollback and training mode in the lineage) or a foundation of our own. The language belongs here too (Rust is wanted; the existing ecosystem is C/C++). Note: PolyForm NC and GPL do not mix. / _**Fundação e licença** (primeiro assunto do próximo mapa). Opções: fork/uso do port PolyForm NC do KOF 2003, neogeorecomp (MIT, C), neogeo-recomp/cps2recomp (GPL-3, C++, com rollback e treino na linhagem) ou fundação própria. A linguagem também entra aqui (Rust desejado; o ecossistema existente é C/C++). Atenção: PolyForm NC e GPL não se misturam._
- **Rollback netplay:** next map. State isolation and determinism become requirements there. / _Netplay com rollback: próximo mapa. O isolamento de estado e o determinismo entram como requisito._
- **Console modes** (single vs, team vs, etc.) beyond the 1v1 used for tests. / _Modos de console além do 1x1 para testes._
- **Combined roster and stages under either game's rules**, including both versions of Shared Characters. Planned in [KOF 2003 and SVC Chaos Versus fusion](../versus-fusion/map.md). / _Elenco e cenários combinados sob as regras de qualquer um dos jogos, incluindo as duas versões dos personagens compartilhados. Planejado em [KOF 2003 and SVC Chaos Versus fusion](../versus-fusion/map.md)._
- **Running on real MVS hardware.** / _Rodar no MVS real._
