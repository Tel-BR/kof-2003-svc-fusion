# Imported-sound space verification

_Read-only result for [ticket 09](issues/09-verify-free-sound-space.md). This note records addresses, sizes, counts and a hash only; it contains no game bytes, disassembly, assets or traces._

## Evidence and reader boundary

The inspected decrypted KOF 2003 M1 has SHA-256 `13e6ed399292eff412d5c7ddb2285111afda8342efb06ba6d2d865775abfadc6`. The page-register writers reduce to these generic driver paths:

| Sample side | Page-register writer | Reaching paths | Data boundary |
| --- | --- | --- | --- |
| ADPCM-A | `$02E8` writes the four start/end page registers for the selected channel. | Initial descriptor lookup from `$01DD` (group 0) or `$0204` (groups 1–7), then `$0217`; the active-sample continuation at `$032C` reuses `$02E8`. | The six-byte descriptor selected through the group table supplies the pages. All 1,820 ADPCM-A descriptors were read; the highest page is `$EFFF`, ending before `$F00000`. |
| ADPCM-B | `$073E` writes the initial four start/end page registers; `$07E9` rewrites them for continuation. | `$0734` and `$08B6` enter `$073E`; `$0795` and `$07BC` enter `$07E9`. | The ADPCM-B record supplies the pages. All 28 records were read; the highest page is `$FFBF`, whose exclusive end is `$FFC000`. |

The port-write helpers themselves are `$26E8` for ADPCM-A and `$26CD` for ADPCM-B. No other call path reaches either side's sample page registers. Thus every original reader is bounded below the free V tail `[$FFC000,$1000000)`.

## Two M1 descriptors

Use sound group 1, indices 0 and 1. Its descriptor table starts at `$4410`, so the two six-byte descriptor slots are `$4410` and `$4416`. Both indices are currently invalid, and therefore unreachable through the original dispatcher. The group has 224 valid indices out of 256.

The packed validity-map directory points group 1 to `$3F04`. The dispatcher takes byte `floor(index / 8)` and masks it with `0x80 >> (index mod 8)`; a zero result rejects the request before descriptor lookup. Therefore the patched local M1 must set bit 7 for index 0 and bit 6 for index 1 in the byte at `$3F04`. This makes precisely the two new descriptor slots reachable. It does not need a new table or a move into banked M1 space.

## V-tail placement

| Voice | Placement | Size |
| --- | --- | ---: |
| Standing light punch | `[$FFC000,$FFC700)` | 1,792 bytes |
| Guard Cancel attack | `[$FFC700,$FFCF00)` | 2,048 bytes |
| Remaining tail | `[$FFCF00,$1000000)` | 12,544 bytes |

Both starts are page-aligned. The two voices consume 3,840 of 16,384 bytes, leaving 12,544 bytes for the first-come, first-served ledger.

## Decision

**Go.** The read-only safety gate passes: every original sample-page reader stops before the tail, and two unreachable descriptor slots plus their validity bits are available in the fixed M1 program. This result authorizes the later local build work in tickets 11 and 12; it does not import a sample, alter a dump, or replace their required scripted native playback and KOF-audio regression checks.

# Verificação de espaço para sons importados

_Resultados somente de leitura do [ticket 09](issues/09-verify-free-sound-space.md). Esta nota registra apenas endereços, tamanhos, contagens e um hash; não contém bytes dos jogos, desmontagem, recursos ou traces._

## Evidência e limite dos leitores

A M1 decriptada do KOF 2003 inspecionada tem SHA-256 `13e6ed399292eff412d5c7ddb2285111afda8342efb06ba6d2d865775abfadc6`. Os escritores dos registradores de página se reduzem aos seguintes caminhos genéricos do driver:

| Lado das amostras | Escritor dos registradores de página | Caminhos que chegam nele | Limite dos dados |
| --- | --- | --- | --- |
| ADPCM-A | `$02E8` escreve os quatro registradores de página de início/fim do canal escolhido. | A busca inicial de descritor parte de `$01DD` (grupo 0) ou `$0204` (grupos 1–7), passa por `$0217`; a continuação da amostra ativa em `$032C` reutiliza `$02E8`. | O descritor de seis bytes escolhido pela tabela do grupo fornece as páginas. Foram lidos os 1.820 descritores ADPCM-A; a maior página é `$EFFF`, terminando antes de `$F00000`. |
| ADPCM-B | `$073E` escreve os quatro registradores iniciais de página de início/fim; `$07E9` volta a escrevê-los na continuação. | `$0734` e `$08B6` entram em `$073E`; `$0795` e `$07BC` entram em `$07E9`. | O registro ADPCM-B fornece as páginas. Foram lidos os 28 registros; a maior página é `$FFBF`, cujo fim exclusivo é `$FFC000`. |

Os próprios auxiliares de escrita nas portas são `$26E8` para ADPCM-A e `$26CD` para ADPCM-B. Nenhum outro caminho de chamada chega aos registradores de página de amostras de qualquer lado. Assim, todo leitor original termina antes da cauda V livre `[$FFC000,$1000000)`.

## Dois descritores M1

Usar o grupo de som 1, índices 0 e 1. A tabela de descritores dele começa em `$4410`; os dois slots de descritor de seis bytes ficam em `$4410` e `$4416`. Ambos os índices são inválidos hoje e, por isso, não podem ser alcançados pelo despachante original. O grupo tem 224 índices válidos em 256.

O diretório do mapa compactado de validade aponta o grupo 1 para `$3F04`. O despachante pega o byte `floor(índice / 8)` e aplica a máscara `0x80 >> (índice mod 8)`; resultado zero rejeita o pedido antes da busca do descritor. Portanto, a M1 local corrigida deve ativar o bit 7 do índice 0 e o bit 6 do índice 1 no byte em `$3F04`. Isso torna alcançáveis exatamente os dois novos slots de descritor. Não é preciso criar tabela nova nem mover dados para a área bancária da M1.

## Colocação na cauda V

| Voz | Colocação | Tamanho |
| --- | --- | ---: |
| Soco fraco em pé | `[$FFC000,$FFC700)` | 1.792 bytes |
| Ataque de Guard Cancel | `[$FFC700,$FFCF00)` | 2.048 bytes |
| Cauda restante | `[$FFCF00,$1000000)` | 12.544 bytes |

Os dois inícios são alinhados em página. As duas vozes usam 3.840 dos 16.384 bytes, restando 12.544 bytes para o livro-caixa por ordem de chegada.

## Decisão

**Seguir.** A barreira de segurança somente de leitura passou: todo leitor original de página de amostra termina antes da cauda, e existem dois slots de descritor inacessíveis com seus bits de validade disponíveis no programa M1 fixo. O resultado autoriza o trabalho local posterior dos tickets 11 e 12; ele não importa amostras, não altera dumps e não substitui as verificações obrigatórias de reprodução nativa por script e de regressão do áudio do KOF.
