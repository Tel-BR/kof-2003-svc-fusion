# KOF 2003 Single and replay research

## Primary sources

- SNK's official KOF 2003 system page describes the arcade leader selection, the Leader's special move and one-fall team fights. Its description concerns 3-on-3 team play and does not establish the AES Single flow or Iori's move commands and costs. [SNK KOF 2003 system](https://www.snk-corp.co.jp/official/kof2003/english/system/index.html)
- MAME documents `-record` and `-playback` for input sessions. It cautions that playback is not reliable for every system and that differing configuration, NVRAM or memory card contents may cause desynchronization. A recording and a matching initial state are candidates for a reproducible reference, subject to a successful replay. Keep recordings and state under `private/`. [MAME command-line options](https://docs.mamedev.org/commandline/commandline-all.html)

## Owner's reported test

The owner reports that the first AES Single opponent can vary, mentioning Maxima and Whip. The owner corrected the earlier Saika observation, stating that the Ya Otome follow-up is available in KOF 2003 and consumes an additional stock. The owner reports that a special move such as Oniyaki can be canceled into a super or Leader Super at an additional stock cost, whereas the reported normal and chain-combo transitions into supers had no additional cancel cost. These reports are documented in the ticket and have not been independently reproduced in this research. [Ticket 02](issues/02-complete-native-single-match.md)

## Open points

No primary KOF 2003 source located in this search establishes Iori's exact Saika input, cancel windows, or the extra stock costs. Avoid substituting move lists from another KOF title. Determine the exact commands and conditions from an official KOF 2003 source or a reproducible game reference.

The opponent matters when comparing the same scripted fight, because a different opponent changes what the fixed inputs encounter. It is not established whether the existing native runtime can reproduce the same opponent, clock and initial state as MAME. Test this rather than assuming MAME's recording format is accepted by the native player.

# Pesquisa sobre o Single do KOF 2003 e reprodução

## Fontes primárias

- A página oficial de sistema do KOF 2003 da SNK descreve a escolha do líder no arcade, seu golpe especial e lutas de equipe em um único round. A descrição trata do 3 contra 3 e não estabelece o fluxo do Single do AES nem os comandos e custos de Iori. [Sistema do KOF 2003 pela SNK](https://www.snk-corp.co.jp/official/kof2003/english/system/index.html)
- O MAME documenta `-record` e `-playback` para sessões de entrada. A documentação avisa que a reprodução não é confiável em todos os sistemas e que diferenças de configuração, NVRAM ou cartão de memória podem causar dessincronização. Uma gravação com o estado inicial correspondente é candidata a uma referência reproduzível, sujeita à confirmação por uma repetição bem-sucedida. Mantenha gravações e estados em `private/`. [Opções de linha de comando do MAME](https://docs.mamedev.org/commandline/commandline-all.html)

## Teste relatado pelo dono

O dono relata que o primeiro adversário do Single AES pode variar, citando Maxima e Whip. Corrigiu a observação anterior sobre Saika e informou que a extensão de Ya Otome está disponível no KOF 2003 e consome uma barra adicional. Relata que um movimento especial como Oniyaki pode ser cancelado em super ou Leader Super ao custo de uma barra adicional, enquanto as transições de golpes normais e chain combos em super que descreveu não tiveram custo adicional de cancelamento. Os relatos estão no ticket e não foram reproduzidos de forma independente nesta pesquisa. [Ticket 02](issues/02-complete-native-single-match.md)

## Pontos em aberto

Nenhuma fonte primária de KOF 2003 encontrada nesta busca estabelece o comando exato de Saika, as janelas de cancelamento ou os custos adicionais. Confirme os comandos e as condições em uma fonte oficial do KOF 2003 ou numa referência reproduzível do jogo.

O adversário importa para comparar a mesma luta por script, pois um adversário diferente muda o que a sequência fixa de comandos encontra. Ainda não foi estabelecido se o runtime nativo consegue reproduzir o mesmo adversário, relógio e estado inicial do MAME. É preciso testar essa correspondência e a compatibilidade dos formatos de gravação.
