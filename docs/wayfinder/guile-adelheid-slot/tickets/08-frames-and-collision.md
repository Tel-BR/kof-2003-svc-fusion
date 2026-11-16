---
id: 08
title: "Choose how Guile's frames and collision become KOF 2003 data"
label: wayfinder:grilling
mode: HITL
status: open
assignee:
blocked_by: [01, 04, 05, 18, 20]
research:
---

## Question

[Animation format](../../base-direction/tickets/08-animation-format.md) ruled out copying SVC's frame and collision records directly. At what granularity is Guile translated: a converter that rewrites every SVC pose and box into KOF 2003 records, hand-authored records per action, or a mix? Where does the converter run and how is its output fed to the native build? Decide what is reusable for the next import and what stays manual.

_PT-BR: O [formato de animação](../../base-direction/tickets/08-animation-format.md) descartou copiar direto os registros de quadro e colisão do SVC. Em que granularidade o Guile é traduzido: um conversor que reescreve cada pose e caixa do SVC em registros do KOF 2003, registros escritos à mão por ação, ou uma mistura? Onde o conversor roda e como sua saída chega ao build nativo? Decidir o que se reaproveita na próxima importação e o que fica manual._

## Notes

- [How KOF 2003 turns a fighter ID into code, animations, graphics, palettes and sounds](01-fighter-id-to-data.md): collision is four 6-byte boxes inside each step of the per-fighter step scripts (file `$380000` directory), alongside velocity commands and sound codes; sprite frames sit in a separate per-fighter directory (file `$200000`) whose layout is not fully decoded, hence the blocker [How KOF 2003's sprite-frame records number their tiles](18-sprite-frame-tiles.md).
- [Inventory of Guile's SVC animations and assets for this slice](05-guile-svc-inventory.md): SVC records are three words (x offset, y offset, pose index) with no duration field; durations were measured.
- [How the native port's generator handles changed or added 68000 code and data](04-port-generator.md): data reads are live, but any change to the prepared `271-pd.bin` regenerates the C; rerunning `kof2003_decrypt` rewrites the prepared folder, so patching the prepared files and adding a step after preparation are both open.

_PT-BR: colisão são quatro caixas de 6 bytes dentro de cada passo dos scripts de passos do lutador, junto com velocidade e sons; os quadros de sprite ficam em outro diretório, de formato ainda não todo decodificado (daí o bloqueio pelo ticket 18). Os registros do SVC têm três palavras (x, y, índice de pose) e nenhuma duração. As leituras de dados são ao vivo, mas mudar o `271-pd.bin` preparado gera o C de novo; rodar o `kof2003_decrypt` outra vez reescreve a pasta preparada, então ficam em aberto modificar os arquivos preparados ou acrescentar um passo depois do preparo._
