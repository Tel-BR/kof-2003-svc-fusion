# Guile in SVC Chaos: moves and system research

Reference research for [ticket 03](issues/03-capture-svc-fighter-reference.md). Button names follow the Neo Geo layout: A light punch, B light kick, C strong punch, D strong kick. `[←]` means hold back to charge.

## Moves

| Type | Move | Input |
|---|---|---|
| Command normal | Knee Bazooka | ← or → + B |
| Command normal | Rolling Sobat | ← or → + D |
| Command normal | Slide Kick | ↘ + B |
| Command normal | Spin Back Knuckle | → + C |
| Special | Sonic Boom | [←] → + punch |
| Special | Somersault Kick (Flash Kick) | [↓] ↑ + kick |
| Super | Somersault Slash | [↙] ↘ ↙ ↗ + punch |
| Super | Somersault Strike | [↙] ↘ ↙ ↗ + kick |
| Super | Total Wipeout | [←] → ← → + kick |
| Exceed | Sonic Hurricane | [←] → ← → + two punches |

The SVC list comes from StrategyWiki's move list for the arcade game. The "delta" motion for the Somersault supers is read from StrategyWiki's stick icons (charge down-back, then down-forward, down-back, up-forward), following the same notation in Street Fighter Alpha 3. [StrategyWiki: Guile](https://strategywiki.org/wiki/SVC_Chaos:_SNK_vs._Capcom/Guile) · [SuperCombo: Guile (SFA3)](https://srk.shib.live/w/Guile_(SFA3)) · [Critical Hits: SVC special moves](https://criticalhits.com.br/dicas/svc-chaos-snk-vs-capcom-todos-os-golpes-especiais/)

## Charge input

- SuperCombo describes SVC charge moves as needing 30 frames of charge, and calls Guile the only full-charge character that adapts well to SVC. [SuperCombo: Guile](https://srk.shib.live/w/SvC_Chaos:_SNK_Vs_Capcom/Guile)
- SVC requires the stick to pass through neutral on the way from a down charge to up. The PS2 and Xbox releases offer an option for SNK's usual input instead. [Weblio (Japanese Wikipedia)](https://www.weblio.jp/content/SVC+CHAOS)
- A character can start charging again only after returning to neutral. Supers can be charged while dashing, special moves cannot. [SuperCombo: Mechanics](https://srk.shib.live/w/SvC_Chaos:_SNK_Vs_Capcom/Mechanics)
- **Owner's test, 2026-11-20, supersedes the web claims above for the import.** Guile does not charge from a neutral position; in his special moves he plays like Ash. His charge supers are distinctive and still undescribed. See [35](../../wayfinder/guile-adelheid-slot/tickets/35-guile-charge-rule.md).
- Holding down-back charges both Sonic Boom and Flash Kick. A review of the 2024 re-release reports that the stick must first go to down or back before down-back charges both. [SuperCombo: FAQ](https://wiki.supercombo.gg/w/SvC_Chaos:_SNK_Vs_Capcom/FAQ) · [Final Weapon review](https://finalweapon.net/2024/08/03/snk-vs-capcom-svc-chaos-review-its-m-u-g-e-n-but-you-have-to-pay-for-it)

## Power Gauge, MAX and Exceed

- SVC's Power Gauge has three levels: LVL.1, LVL.2 and MAXIMUM. Supers, Guard Cancel Attack and Guard Cancel Front Step are available from LVL.1. MAXIMUM adds Cancel Anywhere. [SNK official system page](https://game.snk-corp.co.jp/official/svc/english/system/system_top.html)
- Reaching MAXIMUM starts MAX Activation automatically. The gauge becomes a draining timer and drops back to LVL.2 when it runs out. Each super uses one gauge level. [Wikipedia](https://en.wikipedia.org/wiki/SNK_vs._Capcom:_SVC_Chaos) · [Giant Bomb](https://www.giantbomb.com/-/3030-8521/)
- The gauge fills on taking damage, using special moves, landing attacks and being taunted. Every character starts the match at level 1. A missed throw costs a quarter of a level. [SuperCombo: Mechanics](https://srk.shib.live/w/SvC_Chaos:_SNK_Vs_Capcom/Mechanics) · [Giant Bomb](https://www.giantbomb.com/-/3030-8521/)
- Guard Cancel Front Step costs part of a level. Guard Cancel Attack (C+D while blocking) costs one level and does no damage. [SNK official system page](https://game.snk-corp.co.jp/official/svc/english/system/system_top.html) · [SuperCombo: Mechanics](https://srk.shib.live/w/SvC_Chaos:_SNK_Vs_Capcom/Mechanics)
- Exceed: one per character, usable once per match when health is at half or less, according to the Japanese Wikipedia text. The official page also mentions a Power Gauge condition. Read through a summarizing tool, it gave "less than half", which conflicts with the health condition and needs checking. Guile's Exceed summons a large Sonic Boom in front of him. [Weblio (Japanese Wikipedia)](https://www.weblio.jp/content/SVC+CHAOS) · [SNK official system page](https://game.snk-corp.co.jp/official/svc/english/system/system_top.html) · [SuperCombo: Guile](https://srk.shib.live/w/SvC_Chaos:_SNK_Vs_Capcom/Guile)

## Owner's check

On 2026-11-15 the owner checked the Exceed in the MVS game. It needs no Power Gauge. The only condition is health at half or less, and it can be used once per fight.

The owner also confirmed in the game that C+D while blocking performs the Guard Cancel Attack and costs one gauge level.

The owner also reports that every SVC super costs one gauge level. Measurements in MAME are in [ticket 03](issues/03-capture-svc-fighter-reference.md#2026-11-15--measured-in-mame).

## Open points for the owner's recorded reference

- Which cancels work outside MAX: normal into special, and special into super.
- How fast the gauge refills.

## Differences that affect the import

**Throws (owner's report, 2026-11-15).** Both games have two close-range throws, but the systems differ:

| | SVC Chaos | KOF 2003 |
|---|---|---|
| Throw input | A+B or C+D near the opponent | Back or forward + C or D near the opponent |
| Throw that misses | The fighter performs a throw whiff animation | No throw animation |
| A+B | Throw | Evasive roll |
| C+D | Throw, or Guard Cancel Attack while blocking | Change of team member, or Guard Cancel Attack while blocking |

**Air throws (owner's report).** Both games have air throws that behave the same way. SVC uses A+B or C+D in the air. An air throw that misses has no throw whiff animation and no gauge cost: the fighter performs the normal jumping attack of the buttons pressed. KOF 2003 uses C or D in the air. Imported fighters use KOF 2003's air throw input as well.

Giant Bomb's description that a missed throw costs a quarter of a gauge level in SVC fits the whiff animation. Imported fighters must use KOF 2003's throw input, because A+B and C+D are already system actions in KOF 2003. Guile's throws will need their KOF trigger and no whiff animation. [Giant Bomb](https://www.giantbomb.com/-/3030-8521/)

**Shared system mechanics (owner's report, 2026-11-15).** Two mechanics work the same way in both games and need no adaptation:

- Guard Cancel Attack: C+D while blocking, costing one gauge level in SVC and one stock in KOF 2003.
- Knockdown recovery: pressing A+B before landing from a knockdown makes the fighter recover with a roll.

SVC has no evasive roll. Imported fighters get KOF 2003's rolls built from their recovery roll: [ADR 0002](../../adr/0002-evasive-rolls-from-recovery-animation.md).


KOF 2003 uses whole stocks, with a limit from 3 to 5 and a Leader Super. SVC uses three gauge levels with an automatic MAX mode and an Exceed. Guile's supers map naturally to one KOF stock each. KOF 2003 has no Exceed; the owner decided on 2026-11-20 that Sonic Hurricane becomes a Leader Super, so it comes out only when Guile leads the team ([34](../../wayfinder/guile-adelheid-slot/tickets/34-exceed-super-in-kof.md)). On the charge rule the owner tested the game and corrected this note: Guile does **not** charge from a neutral position, and in his special moves he plays like Ash, so the specials follow KOF 2003's usual charge rule with no adaptation. His **charge supers** are the distinctive part and are not described anywhere yet ([35](../../wayfinder/guile-adelheid-slot/tickets/35-guile-charge-rule.md)).

---

# Guile no SVC Chaos: pesquisa de golpes e sistema

Pesquisa de referência para o [ticket 03](issues/03-capture-svc-fighter-reference.md). Os botões seguem o padrão Neo Geo: A soco fraco, B chute fraco, C soco forte, D chute forte. `[←]` significa segurar para trás para carregar.

## Golpes

| Tipo | Golpe | Comando |
|---|---|---|
| Golpe de comando | Knee Bazooka | ← ou → + B |
| Golpe de comando | Rolling Sobat | ← ou → + D |
| Golpe de comando | Slide Kick | ↘ + B |
| Golpe de comando | Spin Back Knuckle | → + C |
| Especial | Sonic Boom | [←] → + soco |
| Especial | Somersault Kick (Flash Kick) | [↓] ↑ + chute |
| Super | Somersault Slash | [↙] ↘ ↙ ↗ + soco |
| Super | Somersault Strike | [↙] ↘ ↙ ↗ + chute |
| Super | Total Wipeout | [←] → ← → + chute |
| Exceed | Sonic Hurricane | [←] → ← → + dois socos |

A lista do SVC vem do StrategyWiki para a versão arcade. O movimento em "delta" dos supers Somersault foi lido dos ícones do StrategyWiki (carregar baixo-trás e então baixo-frente, baixo-trás, cima-frente), com a mesma notação do Street Fighter Alpha 3. Fontes na versão em inglês acima.

## Comandos de carga

- O SuperCombo descreve 30 quadros de carga para golpes de carga no SVC e considera o Guile o único personagem de carga completa bem adaptado ao jogo.
- O SVC exige que a alavanca passe pela posição neutra entre a carga para baixo e o comando para cima. As versões de PS2 e Xbox têm opção para o comando usual da SNK.
- Só é possível carregar de novo depois de voltar à posição neutra. Supers podem ser carregados durante a corrida, especiais não.
- **Teste do dono, 20/11/2026, vale mais que as afirmações da web acima para a importação.** O Guile não carrega em posição neutra; nos golpes especiais ele joga como o Ash. Os supers de carga dele é que são bem exclusivos, e seguem sem descrição. Ver o [35](../../wayfinder/guile-adelheid-slot/tickets/35-guile-charge-rule.md).
- Segurar baixo-trás carrega Sonic Boom e Flash Kick juntos. Uma análise do relançamento de 2024 relata que é preciso ir primeiro para baixo ou para trás antes de baixo-trás carregar os dois.

## Barra de poder, MAX e Exceed

- A barra do SVC tem três níveis: LVL.1, LVL.2 e MAXIMUM. Supers, Guard Cancel Attack e Guard Cancel Front Step ficam disponíveis a partir do LVL.1. O MAXIMUM acrescenta o Cancel Anywhere.
- Ao chegar ao MAXIMUM, a MAX Activation começa automaticamente. A barra vira um cronômetro que se esvazia e volta ao LVL.2 quando acaba. Cada super gasta um nível.
- A barra enche ao receber dano, usar especiais, acertar golpes e ser provocado. Todos começam a partida no nível 1. Errar um arremesso custa um quarto de nível.
- Guard Cancel Front Step custa parte de um nível. Guard Cancel Attack (C+D defendendo) custa um nível e não causa dano.
- Exceed: um por personagem, utilizável uma vez por partida com a vida pela metade ou menos, segundo o texto da Wikipédia japonesa. A página oficial também menciona uma condição de barra. Lida por uma ferramenta de resumo, ela indicou "menos da metade", o que conflita com a condição de vida e precisa ser conferido. O Exceed do Guile cria um Sonic Boom grande à frente dele.

## Conferência do dono

Em 15/11/2026 o dono conferiu o Exceed no jogo MVS. Ele não precisa de barra de poder. A única condição é estar com metade da vida ou menos, e ele pode ser usado uma vez por luta.

O dono também confirmou no jogo que C+D durante a defesa executa o Guard Cancel Attack e consome um nível da barra.

O dono também informa que todo super do SVC custa um nível da barra. As medições no MAME estão no [ticket 03](issues/03-capture-svc-fighter-reference.md#2026-11-15--measured-in-mame).

## Pontos em aberto para a referência gravada pelo dono

- Quais cancelamentos funcionam fora do MAX: normal em especial e especial em super.
- Com que rapidez a barra enche.

## Diferenças que afetam a importação

**Arremessos (relato do dono, 15/11/2026).** Os dois jogos têm dois arremessos de curta distância, mas os sistemas diferem:

| | SVC Chaos | KOF 2003 |
|---|---|---|
| Comando do arremesso | A+B ou C+D perto do adversário | Trás ou frente + C ou D perto do adversário |
| Arremesso que não pega | O personagem faz uma animação de agarrão no vazio | Não há animação de agarrão |
| A+B | Arremesso | Esquiva |
| C+D | Arremesso, ou Guard Cancel Attack ao defender | Troca de membro da equipe, ou Guard Cancel Attack ao defender |

**Arremessos aéreos (relato do dono).** Os dois jogos têm arremesso aéreo com o mesmo comportamento. O SVC usa A+B ou C+D no ar. Um arremesso aéreo que não pega não tem animação de agarrão no vazio nem custo de barra: o personagem executa o golpe normal no ar dos botões apertados. O KOF 2003 usa C ou D no ar. Os importados também usam o comando de arremesso aéreo do KOF 2003.

A descrição do Giant Bomb de que errar um arremesso no SVC custa um quarto de nível da barra é coerente com essa animação. Os personagens importados precisam usar o comando de arremesso do KOF 2003, porque A+B e C+D já são ações do sistema no KOF 2003. Os arremessos do Guile vão precisar do acionamento do KOF e não terão animação no vazio.

**Mecânicas de sistema compartilhadas (relato do dono, 15/11/2026).** Duas mecânicas funcionam igual nos dois jogos e não precisam de adaptação:

- Guard Cancel Attack: C+D durante a defesa, consumindo um nível da barra no SVC e um estoque no KOF 2003.
- Recuperação de queda: apertar A+B antes de tocar o chão após uma queda faz o personagem se recuperar com uma cambalhota.

O SVC não tem esquiva. Os importados recebem as esquivas do KOF 2003 feitas a partir da cambalhota de recuperação: [ADR 0002](../../adr/0002-evasive-rolls-from-recovery-animation.md).


O KOF 2003 usa estoques inteiros, com limite de 3 a 5 e Leader Super. O SVC usa três níveis de barra, com modo MAX automático e Exceed. Os supers do Guile se encaixam naturalmente em um estoque do KOF cada. O KOF 2003 não tem Exceed; o dono decidiu em 20/11/2026 que o Sonic Hurricane vira Leader Super, então ele só sai quando o Guile for líder da equipe ([34](../../wayfinder/guile-adelheid-slot/tickets/34-exceed-super-in-kof.md)). Sobre a carga, o dono testou o jogo e corrigiu esta nota: o Guile **não** carrega em posição neutra e, nos golpes especiais, joga como o Ash, então os especiais seguem a regra de carga usual do KOF 2003 sem adaptação. Os **supers de carga** dele é que são bem exclusivos e ainda não estão descritos em lugar nenhum ([35](../../wayfinder/guile-adelheid-slot/tickets/35-guile-charge-rule.md)).
