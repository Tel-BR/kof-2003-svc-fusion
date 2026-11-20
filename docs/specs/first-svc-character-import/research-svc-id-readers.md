# What SVC Chaos reads by a fighter's ID (static inventory, wayfinder 28)

_Research note for [ticket 28](../../wayfinder/guile-adelheid-slot/tickets/28-guile-svc-reader-inventory.md),
started 2026-11-20. Addresses are offsets in the validated decrypted program file; only addresses,
sizes, counts and fighter IDs are recorded, and the listings stay in `private/work/svc-readers/`.
A Portuguese version follows. **Status: partial.** The readers of the fighter object's ID and the tables
the creation code copies by ID are inventoried; frames, sound, presentation by team slot and the
consumers of the copied rows are not yet._

## Method

MAME cannot see the game read work RAM (taps and `-debug` watchpoints: see the header of
`tools/kof2003/match/svc_id_readers.lua`), so the readers were found in the program instead:

```
py -3 -m pip install capstone
py -3 -m match.svc_id_static ..\..\private\work\decryption-mame\results\svc-learned-maincpu.bin ..\..\private\work\svc-readers\static
```

(from `tools/kof2003`; `--also 0x70` or `--also a5:0x2c34` follow more offsets, `--range` limits the report).
It sweeps the 68000 code, lists every instruction that touches the ID offsets of a fighter object, and
follows the loaded value forward to the tables it indexes. Three facts about the file that cost time:

- MAME's export stores every 16-bit word **byte-swapped** (the reset vector's stack pointer only reads as a
  work-RAM address after swapping); the tool puts it right. Offsets are unchanged.
- The code is **`$000000`–`$07FFFF`** (about 2,500 `rts`); `$080000` upward is data, and a sweep through
  it produces false readers.
- The word at **`+$70`** is every object's type or state (a menu counter, an effect's kind), so it is not
  an ID reader by itself; only code known to run on fighter objects tells it apart.

## 1. Identity

| Item | Where |
|---|---|
| Fighter objects | `$10A100` (P1) and `$10A380` (P2), `$280` apart; `a4` holds the current object in the fighter code |
| Team data (RAM base `a5` = `$108000`, so `$2C24(a5)`) | P1 `$10AC24`, P2 `$10AC48` (`$24` apart). Creation (`$17E44`–`$17E82`) reads the member index at `+$03` (only when `$10AC23` bit 0 is set, else 0), the colour byte at `+$08+index`, the **ID at `+$0C+index`** (three members, `$10AC30`–`$10AC32` for P1) and a byte at `+$11` clamped to 2 |
| ID in the object | **`+$71`** (byte; the word `+$70` is `$00`:ID), written once, by `$17E68`, from the team data. No code reads an ID back from `+$77` of a fighter object. The sites that touch `+$77` are on `a3`, an object not shown to be the fighter, and are input handling (they read `$1(a6)` and test bits 6 and 7, `$01DB20`–`$01DBD8`, `$051334`–`$051350`); the only other use is the 16-byte block `+$6F`–`+$8D` (odd bytes, so `+$71` and `+$77` both) saved to and restored from `$10D268` (`$10D278` for P2) by `$2697A`/`$269CE`. So the earlier "copy at `+$77`" is **unconfirmed**: nothing indexes by it |
| Mapped ID | **`+$1D6`**, set at `$17EBA` from the 38-byte table at **`$17ED6`** indexed by the word at `+$70`: 36 identity entries (`$00`–`$23`) plus two more (`$24`, `$FF`). Guile `$13` maps to itself. This is SVC's own presentation-map-like indirection: every identity test and most movement tables below read `+$1D6`, not `+$71` |
| Premultiplied IDs | `$17C60`–`$17C78` stores ID×2, ×4, ×8 and ×16 as words at **`+$180`, `+$182`, `+$184`, `+$186`** (the earlier "ID doubled at `+$181`" is the low byte of `+$180`). Tables read through them below |
| Roster size | **36 IDs, `$00`–`$23`**, in every table spaced by row size; Guile is `$13` (20th) |

## 2. Tables indexed by the ID

### 2.1 Copied into the fighter at creation (`$17CC0`–`$17E3C`, helper `$17EFC` copies `row size` bytes from `base + ID × row size`)

All have 36 rows. "Alt" is used for the second side (`+$171` bit 7 set). The destination is an offset in the
fighter's data block (`a2`). Guile's row is `base + $13 × row`.

| Base (alt) | Row | Table size | Block + | Guile row |
|---|---|---|---|---|
| `$0A695E` | 4 | 144 | `$000` | `$0A69AA` |
| `$0A69EE` | 8 | 288 | `$004` | `$0A6A86` |
| `$0A6B0E` | 2 | 72 | `$010` | `$0A6B34` |
| `$0A6B56` | 10 | 360 | `$012` | `$0A6C14` |
| `$0A6CBE` | 18 | 648 | `$01C` | `$0A6E14` |
| `$0A712A` (`$0A7A2A`) | 64 | 2,304 | `$0A2` | `$0A75EA` (alt `$0A7EEA`) |
| `$0A952A` (`$0A9E2A`) | 64 | 2,304 | `$0E2` | `$0A99EA` (alt `$0AA2EA`) |
| `$0A7066` | 2 | 72 | `$122` | `$0A708C` |
| `$0A6F46` (`$0A6FD6`) | 4 | 144 | `$124` | `$0A6F92` (alt `$0A7022`) |
| `$0A70F6` | 1 | 36 | `$128` | `$0A7109` |
| `$0A832A` (`$0A8C2A`) | 64 | 2,304 | `$138` | `$0A87EA` (alt `$0A90EA`) |
| `$0AA72A` (`$0AB02A`) | 64 | 2,304 | `$178` | `$0AABEA` (alt `$0AB4EA`) |
| `$0A70AE` | 2 | 72 | `$1B8` | `$0A70D4` |

Per-opponent rows: **`$0AB92A`**, `$A8` bytes per fighter (42 entries of 4 bytes), 36 rows, ends `$0AD0CA`; the copy
(`$17F0A`, at `$17CE6`) takes 4 bytes at `ID × $A8 + opponent ID × 4`, where the opponent's ID is the word at
`+$70` of the object at `+$B6`; destination block + `$00C`. Guile's row is `$0AC5A2`.

### 2.2 Read on every use

| Reader | What | Size / count |
|---|---|---|
| `$14C12` | Per-fighter dispatch: word offsets at **`$14C2E`** indexed by `+$1D6`×2, then `jmp` | 36 words (`$14C2E`–`$14C75`); **every entry points at the same routine, `$14C76`**, so there is no per-fighter code here |
| `$14D2A`, `$152B0`, `$1572C` | Flag byte table **`$0A65BA`** by `+$1D6` | 36 bytes; set for IDs `$09`, `$1A`, `$20` only (not Guile) |
| `$15B3E` (call `$1BBD2`) | Membership in the 64-bit set at **`$0A65DE`** by the opponent's `+$1D6` | 2 longs; 26 members; Guile is a member |
| `$158DE` | Pair matrix: `$232800` (alt `$833800`, the second ROM bank state) `+ {0, $1440, $2880}` (three variants chosen from the opponent's state) `+ ID × $90 + opponent ID × 4` | 3 × 36 × 36 entries of 4 bytes (distance bands: the code compares the horizontal distance with four bytes) |
| `$15D2E` | 4 KiB block per fighter: `$201000` (alt `$802000`) `+ ID × $1000 + …` | 36 × `$1000` bytes in the banked ROM; purpose not identified |
| `$0180B8` | 16 bytes per fighter at `$0180EA` (alt `$0180DA`) by `+$186`; reads 4 bytes into `+$27A` | 36 × 16 |
| `$019C6C` | Words at `$019CDE` by `+$186` and a state | 36 × 16 |
| `$017E96` | Pair of longs at `$0AD4BA`/`$0AD4BE` by `+$186` and a state | 36 × 16 |
| `$01B064` | Words at `$01B1F8` by `+$180` | 38 words (36 + 2 extra, the last is `$FFFF`) |
| `$01B130` | Longs at `$01B168` by `+$182` | 36 longs |
| `$026D46` | Words at `$026D72` by `+$180` | 38 words |
| `$02A82E` | Longs at `$02AB40` by `+$182` | 36 longs |
| `$01C81C`, `$0298CC`–`$0298E8` | `adda.w +$180` into pointers (tables not resolved) | open |

### 2.3 Identity tests (`+$1D6` compared with a literal ID)

31 comparisons in 15 places (`$014CA0`, `$0153DA`, `$015A48`–`$015C26`, `$0178FC`, `$01790E`) against IDs
`$01`, `$03`, `$09`, `$0A`, `$0D`, `$11`, `$12`, `$14`, `$15`, `$17`, `$1A`, `$1D`. Two more tests on the word at `+$70`
(`$01ADD0`–`$01AE94`, IDs `$09` and `$1A`). **Nothing in the program compares an ID with `$13`:
Guile has no ID-specific branch**, which is the SVC side of "is anything special-cased for him".

## 3. Mapping to the slot-anatomy kinds

| Slot-anatomy kind ([slot-anatomy.md](slot-anatomy.md) §2) | SVC counterpart found |
|---|---|
| ID tables copied or looked up (37-row tables) | the 13 creation tables of 2.1 (36 rows) and the per-use tables of 2.2 |
| Per-opponent rows | `$0AB92A` (4 bytes × 42 per fighter) and the `$232800` matrices |
| Per-fighter routine tables | `$14C2E` (36 words, one shared target) |
| Identity lists | `$0A65BA` (flags), `$0A65DE` (bit set), the 31 literal tests |
| Presentation map | `$17ED6` (identity map into `+$1D6`) |
| Command lists, command → action | not located; the 4 KiB blocks at `$201000`/`$802000` and the `$A2`/`$E2`/`$138`/`$178` row blocks are the candidates |
| Frames, palettes | not traced here (research 05: palette blocks `$577538`, `$577738`) |
| Sound | [research 26 and 30](../../wayfinder/guile-adelheid-slot/tickets/30-guile-svc-remaining-sounds.md): Guile's block of 80 rows at `$0A3BBC`; character voice tables around `$0AF3xx`–`$0AF4xx`; reader not re-derived here |
| Selection, intro, victory (read through the team data) | team-data users found at `$00D652`, `$00D698`, `$00DB9C`, `$00E362`, `$00E524` and the team area at `$011466`; not traced |

## 4. Open

- The consumers of the copied rows (what reads the fighter's data block at the offsets above) and the purpose of the
  `$15D2E` blocks.
- Frames, sound-by-ID and selection/intro/victory presentation, which read through other paths.
- Confirming a reader at run time: MAME cannot (see the Lua header); the SVC native player from `svc-port` could.

---

## Português (Brasil)

# O que o SVC Chaos lê pelo ID do lutador (inventário estático, wayfinder 28)

_Nota de pesquisa do [ticket 28](../../wayfinder/guile-adelheid-slot/tickets/28-guile-svc-reader-inventory.md),
iniciada em 2026-11-20. Os endereços são posições no arquivo de programa decifrado validado; só endereços, tamanhos,
contagens e IDs de lutador são registrados, e as listagens ficam em `private/work/svc-readers/`.
**Situação: parcial.** Estão inventariados os leitores do ID do objeto de lutador e as tabelas que a criação copia
por ID; quadros, som, apresentação pela vaga da equipe e os consumidores das linhas copiadas ainda não._

### Método

O MAME não vê o jogo ler a RAM (taps e watchpoints de `-debug`: veja o cabeçalho de `svc_id_readers.lua`), então os
leitores foram achados no próprio programa. A ferramenta `match.svc_id_static` (comando acima) varre o código 68000,
lista toda instrução que toca os deslocamentos de ID de um objeto de lutador e segue o valor carregado até as tabelas
que ele indexa. Três fatos sobre o arquivo que custaram tempo:

- A exportação do MAME guarda cada palavra de 16 bits **com os bytes trocados**; a ferramenta corrige. Os deslocamentos
  não mudam.
- O código ocupa **`$000000`–`$07FFFF`**; de `$080000` em diante é dado, e varrer isso produz leitores falsos.
- A palavra em **`+$70`** é o tipo ou estado de qualquer objeto (contador de menu, tipo de efeito), então ela sozinha
  não é leitura de ID; só o código que roda em objetos de lutador a distingue.

### 1. Identidade

- Objetos de lutador em `$10A100` (J1) e `$10A380` (J2), a cada `$280`. Dados da equipe (base de RAM `a5` = `$108000`, ou seja `$2C24(a5)`): J1 `$10AC24`, J2 `$10AC48`
  (`$24` de distância). A criação (`$17E44`–`$17E82`) lê o índice do membro em `+$03` (só se o bit 0 de `$10AC23` estiver
  ligado, senão 0), o byte de cor em `+$08+índice` e o **ID em `+$0C+índice`** (três membros, `$10AC30`–`$10AC32` no J1).
- O ID no objeto fica em **`+$71`** (byte; a word `+$70` é `$00`:ID), escrito uma vez em `$17E68` a partir da equipe.
  **Nenhum código lê o ID de volta em `+$77`** de um objeto de lutador: os pontos que tocam `+$77` usam `a3`, objeto que não se
  mostrou ser o lutador, e tratam entrada de controle (leem `$1(a6)`, testam bits 6 e 7); o outro uso é o bloco de 16 bytes
  `+$6F`–`+$8D` (bytes ímpares, logo `+$71` e `+$77`) salvo e restaurado em `$10D268` (`$10D278` no J2) por `$2697A`/`$269CE`.
  A "cópia em `+$77`" do ticket fica **não confirmada**: nada indexa por ela.
- **`+$1D6`** é preenchido em `$17EBA` pela tabela de 38 bytes em **`$17ED6`**, indexada pela word de `+$70`: 36 entradas
  de identidade (`$00`–`$23`) mais duas (`$24`, `$FF`). O Guile `$13` mapeia para ele mesmo. É um mapa de apresentação
  próprio do SVC: quase todo teste de identidade e tabela de movimento abaixo lê `+$1D6`, não `+$71`.
- `$17C60`–`$17C78` guarda ID×2, ×4, ×8 e ×16 como words em **`+$180`, `+$182`, `+$184`, `+$186`** (o "ID dobrado em
  `+$181`" do ticket é o byte baixo de `+$180`).
- O elenco tem **36 IDs, `$00`–`$23`**, em toda tabela medida pelo espaçamento; o Guile é `$13` (o 20º).

### 2. Tabelas indexadas pelo ID

**2.1 Copiadas para o lutador na criação** (`$17CC0`–`$17E3C`; a rotina `$17EFC` copia `tamanho da linha` bytes de
`base + ID × linha`): são as 13 tabelas da tabela em inglês acima, todas de 36 linhas; a "alt" vale para o segundo lado
(`+$171` bit 7). A linha do Guile é `base + $13 × linha` e está na última coluna. Linhas por adversário: **`$0AB92A`**, `$A8`
bytes por lutador (42 entradas de 4 bytes), 36 linhas, terminando em `$0AD0CA`; a cópia (`$17F0A`, em `$17CE6`) pega 4 bytes
em `ID × $A8 + ID do adversário × 4` (o adversário é o objeto em `+$B6`); a linha do Guile é `$0AC5A2`.

**2.2 Lidas a cada uso:** despacho por lutador (`$14C12`, palavras em `$14C2E`: 36 palavras, **todas apontam para a mesma
rotina `$14C76`**, então não há código por lutador ali); byte de marca `$0A65BA` (36 bytes, ligado só nos IDs `$09`, `$1A`
e `$20`, não no Guile); conjunto de bits `$0A65DE` (26 membros, o Guile é membro); matrizes de pares `$232800`
(alt `$833800`) `+ {0, $1440, $2880}` `+ ID × $90 + ID adversário × 4` (3 × 36 × 36 entradas de 4 bytes, faixas de distância);
blocos de 4 KiB por lutador em `$201000` (alt `$802000`), finalidade não identificada; e as tabelas por `+$180`…`+$186` da
tabela em inglês.

**2.3 Testes de identidade:** 31 comparações de `+$1D6` com um ID literal em 15 lugares, contra `$01`, `$03`, `$09`,
`$0A`, `$0D`, `$11`, `$12`, `$14`, `$15`, `$17`, `$1A`, `$1D`; mais dois testes na word `+$70` (`$09` e `$1A`).
**Nada no programa compara um ID com `$13`: o Guile não tem desvio específico por ID.**

### 3. Associação aos tipos da anatomia da vaga

Veja a tabela em inglês (§3). Resumo: tabelas por ID e linhas por adversário achadas; listas de identidade = `$0A65BA`,
`$0A65DE` e os testes literais; mapa de apresentação = `$17ED6`; **listas de comandos e comando → ação não localizadas**;
quadros e paletas não rastreados aqui; som nas pesquisas 26 e 30; seleção, intro e vitória leem pela equipe e não foram
rastreadas (usuários da equipe em `$00D652`, `$00D698`, `$00DB9C`, `$00E362`, `$00E524` e a área da equipe em `$011466`).

### 4. Em aberto

Os consumidores das linhas copiadas e a finalidade dos blocos de `$15D2E`; quadros, som por ID e a apresentação de
seleção, intro e vitória; e a confirmação em execução, que o MAME não faz (o player nativo do SVC a partir do `svc-port`
poderia).
