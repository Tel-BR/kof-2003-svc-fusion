---
id: 21
title: "How many tiles Guile's complete SVC frame data uses"
label: wayfinder:research
mode: AFK
status: closed
assignee:
blocked_by: []
research: research/21-guile-total-tiles:docs/wayfinder/guile-adelheid-slot/research/21-guile-total-tiles.md
---

## Question

[How KOF 2003's sprite-frame records number their tiles](18-sprite-frame-tiles.md) found that Adelheid's graphics are one solid block of 7,211 tiles and that the recorded SVC sessions show 2,145 distinct Guile body tiles, a floor that leaves out his normals, specials and supers. His block in SVC's graphics spans about 9,100 tile numbers (`$42B6F`–`$44EF8`), and nothing yet says whether all of it is his.

Walking SVC's own frame data for Guile, as research 18 did for KOF 2003, how many distinct tiles do all of his frames reference, and what is their range? Where do his neighbours' tiles begin and end? Do his projectiles and effects use tiles outside that range? The answer sizes the graphics space each imported fighter needs and says whether all of Guile would fit in Adelheid's 7,211 tiles; it blocks no decision on this map. Start from the pose pointer at object `+$28` and the 6-byte pose records of [Animation format](../../base-direction/tickets/08-animation-format.md) and from the tools in `private/work/svc-guile/` and `private/work/guile-adelheid-slot/05-guile-svc-inventory/`. Record addresses, sizes and counts only.

_PT-BR: a pesquisa 18 mostrou que os gráficos da Adelheid são um bloco único de 7.211 tiles e que as sessões gravadas do SVC mostram 2.145 tiles distintos do corpo do Guile, um mínimo que deixa de fora os golpes normais, especiais e supers. O bloco dele nos gráficos do SVC cobre cerca de 9.100 números de tile (`$42B6F`–`$44EF8`), e ainda não se sabe se é todo dele. Percorrendo os dados de quadro do próprio SVC, como a pesquisa 18 fez no KOF 2003, quantos tiles distintos todos os quadros do Guile usam, e em que faixa? Onde começam e terminam os tiles dos vizinhos? Os projéteis e efeitos dele usam tiles fora dessa faixa? A resposta dimensiona o espaço gráfico que cada personagem importado precisa e diz se o Guile inteiro caberia nos 7.211 tiles da Adelheid; não bloqueia nenhuma decisão deste mapa. Partir do ponteiro de pose em `+$28` do objeto e dos registros de pose de 6 bytes do ticket 08 do mapa anterior, e das ferramentas em `private/work/svc-guile/` e `private/work/guile-adelheid-slot/05-guile-svc-inventory/`. Registrar só endereços, tamanhos e contagens._

## Resolution

Findings: `research/21-guile-total-tiles:docs/wayfinder/guile-adelheid-slot/research/21-guile-total-tiles.md` (commit `481bc5c`, local throwaway branch). Resolved by a research subagent; the owner can spot-check the total by hand.

**Total.** Guile's complete SVC frame data is 444 frames and 9,690 distinct tiles, one solid block `$42B6F`-`$45148` with no gaps (`$45148 - $42B6F + 1 = 9,690`). It is table 19 of 42 pose tables in the SVC graphics set; his neighbours end at `$42B6E` and start at `$45149`, and no other table uses his tiles. The 2,145 tiles seen in earlier sessions are all inside this set; the "about 9,100" of research 03 was only the highest tile one session showed.

**Fit.** He does not fit in Adelheid's block of 7,211 tiles (2,479 short). He would fit in Mukai's 10,481 and in 16 other KOF 2003 blocks (17 of 37), which does not change [Choose where Guile's tiles go in the graphics files](19-guile-tile-placement.md): his tiles go into the added 128 MiB space, and the 9,690 is the size to plan for.

**Left open.** (1) Whether his Sonic Boom frames live in his own table or in the shared effect tables 36-41 (`$64589`-`$6CCEF`, outside his block) was not traced. (2) SVC's move scripts were not walked, so which of the 444 poses his moves actually reach is unknown. (3) The `+$100000` address mapping comes from the clean decoding, not from tracing the PVC chip **[I]**.

**PT-BR**

Achados: `research/21-guile-total-tiles:docs/wayfinder/guile-adelheid-slot/research/21-guile-total-tiles.md` (commit `481bc5c`, branch local descartável). Resolvido por um subagente de pesquisa; o dono pode conferir o total à mão.

**Total.** Os dados de quadros completos do Guile no SVC são 444 quadros e 9.690 tiles distintos, um bloco sólido `$42B6F`-`$45148` sem buracos (`$45148 - $42B6F + 1 = 9.690`). É a tabela 19 de 42 tabelas de poses dos gráficos do SVC; as vizinhas terminam em `$42B6E` e começam em `$45149`, e nenhuma outra tabela usa os tiles dele. Os 2.145 tiles vistos nas sessões anteriores estão todos dentro desse conjunto; os "cerca de 9.100" da pesquisa 03 eram só o maior tile que uma sessão mostrou.

**Cabe.** Ele não cabe no bloco da Adelheid, de 7.211 tiles (faltam 2.479). Caberia no do Mukai (10.481) e em outros 16 blocos do KOF 2003 (17 de 37), o que não muda o [ticket 19](19-guile-tile-placement.md): os tiles dele vão para o espaço acrescentado de 128 MiB, e o tamanho a planejar é 9.690.

**Em aberto.** (1) Não se rastreou se os quadros do Sonic Boom ficam na tabela dele ou nas tabelas de efeitos compartilhadas 36-41 (`$64589`-`$6CCEF`, fora do bloco). (2) Os scripts de golpe do SVC não foram percorridos, então não se sabe quais das 444 poses os golpes dele realmente alcançam. (3) O mapeamento de endereços `+$100000` vem da decodificação limpa, não de rastrear o chip PVC **[I]**.
