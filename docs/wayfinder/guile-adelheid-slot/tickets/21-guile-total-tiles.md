---
id: 21
title: "How many tiles Guile's complete SVC frame data uses"
label: wayfinder:research
mode: AFK
status: open
assignee:
blocked_by: []
research:
---

## Question

[How KOF 2003's sprite-frame records number their tiles](18-sprite-frame-tiles.md) found that Adelheid's graphics are one solid block of 7,211 tiles and that the recorded SVC sessions show 2,145 distinct Guile body tiles, a floor that leaves out his normals, specials and supers. His block in SVC's graphics spans about 9,100 tile numbers (`$42B6F`–`$44EF8`), and nothing yet says whether all of it is his.

Walking SVC's own frame data for Guile, as research 18 did for KOF 2003, how many distinct tiles do all of his frames reference, and what is their range? Where do his neighbours' tiles begin and end? Do his projectiles and effects use tiles outside that range? The answer sizes the graphics space each imported fighter needs and says whether all of Guile would fit in Adelheid's 7,211 tiles; it blocks no decision on this map. Start from the pose pointer at object `+$28` and the 6-byte pose records of [Animation format](../../base-direction/tickets/08-animation-format.md) and from the tools in `private/work/svc-guile/` and `private/work/guile-adelheid-slot/05-guile-svc-inventory/`. Record addresses, sizes and counts only.

_PT-BR: a pesquisa 18 mostrou que os gráficos da Adelheid são um bloco único de 7.211 tiles e que as sessões gravadas do SVC mostram 2.145 tiles distintos do corpo do Guile, um mínimo que deixa de fora os golpes normais, especiais e supers. O bloco dele nos gráficos do SVC cobre cerca de 9.100 números de tile (`$42B6F`–`$44EF8`), e ainda não se sabe se é todo dele. Percorrendo os dados de quadro do próprio SVC, como a pesquisa 18 fez no KOF 2003, quantos tiles distintos todos os quadros do Guile usam, e em que faixa? Onde começam e terminam os tiles dos vizinhos? Os projéteis e efeitos dele usam tiles fora dessa faixa? A resposta dimensiona o espaço gráfico que cada personagem importado precisa e diz se o Guile inteiro caberia nos 7.211 tiles da Adelheid; não bloqueia nenhuma decisão deste mapa. Partir do ponteiro de pose em `+$28` do objeto e dos registros de pose de 6 bytes do ticket 08 do mapa anterior, e das ferramentas em `private/work/svc-guile/` e `private/work/guile-adelheid-slot/05-guile-svc-inventory/`. Registrar só endereços, tamanhos e contagens._
