---
title: "Read imported fighters' per-opponent rows through a proxy"
triage: ready-for-agent
---

# 16 Read imported fighters' per-opponent rows through a proxy

[Parent specification](../spec.md) · [Diagnosis](14-rehearsal-intro-and-command-normals.md) · [Rehearsal ticket](04-complete-first-imported-match.md)

## What to build

The readers at `$216AC` and `$21836` index 42-byte per-opponent rows by the
other fighter's ID, in tables of 37 rows. By the owner's decision, an imported
ID is read through a proxy: a 64-entry byte table maps each ID to the original
fighter whose rows are used (identity for `$00`–`$24`; `$1E` for the `$30`
rehearsal; Guile's proxy is chosen later). Replace the diagnostic patch with
this table and a checked tool step, and search for other readers that index
per-opponent data by ID.

## Acceptance criteria

- [ ] Search for every reader that indexes rows by the other fighter's ID
  (including multiples other than 42) and list them.
- [ ] A preparation step installs the proxy table and the reader changes with
  byte checks and tests on invented data; the proxy for `$30` is a parameter.
- [ ] In the differential loop, the grab and its aftermath equal original Kyo's
  with the clone attacking and being grabbed; the native build reports no new
  fallback after profiling.
- [ ] Original fighters facing originals are unchanged in a regression check
  beyond Kyo.

## Português (Brasil)

# 16 Ler as linhas por adversário dos importados por um proxy

_Os leitores em `$216AC` e `$21836` indexam linhas de 42 bytes por adversário
pelo ID do outro lutador, em tabelas de 37 linhas. Por decisão do dono, um ID
importado é lido por um proxy: uma tabela de 64 bytes associa cada ID ao lutador
original cujas linhas são usadas (identidade para `$00`–`$24`; `$1E` para o
ensaio no `$30`; o proxy do Guile será escolhido depois). Trocar o remendo de
diagnóstico por essa tabela e um passo de ferramenta verificado, e procurar
outros leitores que indexem dados por adversário pelo ID._

### Critérios de aceitação

- [ ] Procurar todo leitor que indexe linhas pelo ID do outro lutador
  (inclusive múltiplos diferentes de 42) e listá-los.
- [ ] Um passo de preparo instala a tabela de proxy e as mudanças nos leitores,
  com conferência de bytes e testes com dados inventados; o proxy do `$30` é um
  parâmetro.
- [ ] No ciclo diferencial, o agarrão e o que vem depois igualam os do Kyo
  original com o clone agarrando e sendo agarrado; o build nativo não mostra
  novo fallback após o perfil.
- [ ] Originais contra originais ficam inalterados numa conferência de regressão
  além do Kyo.

### 2026-11-19 — Evidence from ticket 13

The fight divergence with `$30` as the other player's fighter (4,789 px at frame
6,100 on the ticket 13 script) exists with the diagnostic proxy at `$52E00`
already installed, so another reader of per-opponent data may still index by the
raw ID; use that script as one of the loops for the reader search in the first
criterion. See [13](13-rehearsal-selection-presentation.md).

_PT-BR: a divergência de luta com o `$30` como lutador do outro jogador (4.789 px
no quadro 6.100 do roteiro do ticket 13) existe com o proxy de diagnóstico em
`$52E00` já instalado, então outra leitura de dados por adversário pode ainda
indexar pelo ID bruto; usar esse roteiro como um dos laços da busca de leitores
do primeiro critério. Ver [13](13-rehearsal-selection-presentation.md)._
