# Graphics-set growth tools

Tools for growing the native player's Graphics Set from 64 to 128 MiB with no visible change (spec `docs/specs/graphics-set-growth/`). Nothing here contains game data; captures, builds and logs stay under `private/work/graphics-growth/`.

| File | Purpose |
|---|---|
| `graphics_size.py` | Raises (`apply`), lowers (`undo`) or shows (`status`) the graphics size in the private cartridge descriptor (`private/work/kof2003-port/src/game.c`, the `.crom_size` value). Changes that one value only, is idempotent, keeps line endings, and prints the file's SHA-256 before and after. It copies none of the descriptor's code. |
| `added_space_tiles.py` | The synthetic tiles of build C: a made-up pattern, its palette words, the pair of graphics files, and the ROM folder for C (every file of the real one, hard-linked, plus the pair). No game data. |
| `added_space_proof.c` | Compiled into build C only. Plants one sprite pointing at tile `$80000`, with its palette, before each line is drawn. |
| `added_space_patch.py` | Turns the private descriptor and renderer into build C (`apply`), and back (`undo`): the 128 MiB size, the synthetic pair as the fifth pair, and the renderer's call to the planter under the `KOF2003_ADDED_SPACE_PROOF` macro. Both files are checked before either is written. |
| `verify_added_space.py` | Reads a capture and decides whether the synthetic tile is in the 16x16 box where `added_space_proof.c` puts it, pixel by pixel; with `--rom-path` it also hashes the Graphics Set's first tile for comparison. Reads PNGs with the standard library only. |
| `run_added_space.py` | Runs build C (against the ROM folder with the pair) and build B (against the real one) on one script, then checks every captured frame: the tile must be in C and in none of B. |

Builds: **A** is the reference, 64 MiB, kept read-only in `private/work/graphics-growth/build-a/`. **B** is 128 MiB with no test code and no extra file, kept in `build-b/`. Both are the same program; only the graphics size differs.

## Build B and compare it with A (Windows, PowerShell)

From `tools/kof2003`:

```
py -3 -m growth.graphics_size status          # 0x4000000 (64 MiB); note the hash
py -3 -m growth.graphics_size apply           # 0x8000000 (128 MiB)
cd ..\..\private\work\mvs-native-build
ninja kof2003_player                           # rebuilds the player
mkdir ..\graphics-growth\build-b
copy "KOF 2003.exe","SDL2.dll" ..\graphics-growth\build-b
cd ..\..\..\tools\kof2003
py -3 -m match.compare_builds                  # A vs B, both scripts; prints hashes and B's memory
py -3 -m growth.graphics_size undo             # back to 64 MiB; the hash must equal the first one
cd ..\..\private\work\mvs-native-build; ninja kof2003_player
```

## Build C and prove a tile of the Added Space is drawn (ticket 04)

Build C exists only for that proof: it is 128 MiB like B, and on top of that it loads a
temporary pair of graphics files with synthetic tiles from tile `$80000` and plants one
sprite that points at the first of them. The pair and the compile-time option are in
neither A nor B. From `tools/kof2003`:

```
py -3 -m growth.added_space_tiles              # writes the pair and the ROM folder for C
py -3 -m growth.added_space_patch apply        # 128 MiB, the fifth pair, the renderer's call
cmake -S ..\..\tools\kof2003 -B ..\..\private\work\mvs-native-build -DKOF2003_ADDED_SPACE_PROOF=ON
cd ..\..\private\work\mvs-native-build; ninja kof2003_player
mkdir ..\graphics-growth\build-c
copy "KOF 2003.exe","SDL2.dll" ..\graphics-growth\build-c
cd ..\..\..\tools\kof2003
py -3 -m growth.run_added_space                # C against B, frame by frame
py -3 -m growth.verify_added_space CAPTURE.png --rom-path ..\..\private\work\graphics-growth\rom-c
py -3 -m growth.added_space_patch undo         # back to the descriptor A and B share
cmake -S ..\..\tools\kof2003 -B ..\..\private\work\mvs-native-build -DKOF2003_ADDED_SPACE_PROOF=OFF
cd ..\..\private\work\mvs-native-build; ninja kof2003_player
```

The option is off by default, so a build that does not pass it is a B (or, with the
descriptor undone, an A). Leaving the option on without applying the patch builds a
player whose renderer never calls the planter, so nothing is drawn from the Added
Space; leaving the patch applied without the option builds a 128 MiB player that loads
the pair and draws nothing from it. Undo both when the proof is done.

`ninja` also runs the generator again, because it embeds the descriptor. Hash `generated/` before and after: every file must be identical, which proves the native code did not change. `compare_builds` exits with 1 on any difference, a missing build, or a `--verify` summary worse than A's. A rebuilt 64 MiB executable need not equal the saved `build-a` byte for byte (link-time stamps), so `build-a` is never rebuilt over.

## For whoever starts the Rehearsal

**Rule for graphics file pairs.** The loader lays the pairs of graphics files end to end, up to 8 pairs. The four original pairs fill exactly 64 MiB, so the Added Space starts at the fifth pair, and its first tile is tile number `$80000`. Four more pairs of 16 MiB complete 128 MiB. Whatever no file covers reads as zero. The decoded tile array is padded to a power of two by the loader, and 128 MiB already is one. A descriptor that does not list exactly four original pairs must not get a fifth added blindly (`added_space_patch.py` refuses it). Tile numbers at or above `$80000` no longer wrap to the low half.

**Measured memory of the grown player (build B).** Machine with 32,606 MiB installed. Peak working set 420 MiB (`coin-start`) and 419 MiB (`team-match`), peak commit 416 MiB in both, steady working set 300-310 MiB. The 256 MiB decoded tile cache and the load peak are acceptable. Details: `docs/specs/graphics-set-growth/issues/02-grow-and-match-reference.md`.

Tests: `py -3 -m pytest growth match` from `tools/kof2003`.

## Ferramentas da ampliação do Conjunto gráfico

Ferramentas para ampliar o Conjunto gráfico do player nativo de 64 para 128 MiB sem mudança visível (spec `docs/specs/graphics-set-growth/`). Nada aqui contém dados dos jogos; capturas, builds e logs ficam em `private/work/graphics-growth/`.

| Arquivo | Função |
|---|---|
| `graphics_size.py` | Sobe (`apply`), desce (`undo`) ou mostra (`status`) o tamanho gráfico no descritor privado do cartucho (`private/work/kof2003-port/src/game.c`, o valor `.crom_size`). Muda só esse valor, é idempotente, preserva as quebras de linha e imprime o SHA-256 do arquivo antes e depois. Não copia código do descritor. |
| `added_space_tiles.py` | Os tiles sintéticos do build C: um padrão inventado, as palavras de paleta, o par de arquivos gráficos e a pasta de ROMs do C (todos os arquivos da pasta real, por hard link, mais o par). Nenhum dado do jogo. |
| `added_space_proof.c` | Compilado só no build C. Planta um sprite apontando para o tile `$80000`, com a paleta dele, antes de cada linha ser desenhada. |
| `added_space_patch.py` | Transforma o descritor e o renderizador privados no build C (`apply`) e desfaz (`undo`): o tamanho de 128 MiB, o par sintético como quinto par e a chamada do plantador no renderizador sob a macro `KOF2003_ADDED_SPACE_PROOF`. Os dois arquivos são conferidos antes de qualquer um ser gravado. |
| `verify_added_space.py` | Lê uma captura e decide se o tile sintético está no quadrado de 16x16 onde o `added_space_proof.c` o põe, pixel por pixel; com `--rom-path` também calcula o hash do primeiro tile do Conjunto gráfico para comparação. Lê PNG só com a biblioteca padrão. |
| `run_added_space.py` | Roda o build C (contra a pasta de ROMs com o par) e o build B (contra a real) num roteiro e confere cada quadro capturado: o tile tem de estar no C e em nenhum do B. |

Builds: o **A** é a referência, 64 MiB, guardado em somente leitura em `private/work/graphics-growth/build-a/`. O **B** é 128 MiB sem código de teste nem arquivo extra, guardado em `build-b/`. Os dois são o mesmo programa; só o tamanho gráfico muda.

### Compilar o B e comparar com o A (Windows, PowerShell)

Os comandos são os do bloco em inglês acima, na mesma ordem. O `ninja` roda o gerador de novo porque ele embute o descritor; calcule o hash de `generated/` antes e depois, e todos os arquivos têm de ser idênticos, o que prova que o código nativo não mudou. O `compare_builds` sai com código 1 se houver diferença, build faltando ou resumo do `--verify` pior que o do A. Um executável de 64 MiB recompilado pode não ser igual byte a byte ao `build-a` guardado (carimbos de ligação), por isso o `build-a` nunca é recompilado por cima.

### Compilar o C e provar que um tile do Espaço acrescentado é desenhado (ticket 04)

Os comandos são os do bloco em inglês acima, na mesma ordem. O build C existe só para
essa prova: tem 128 MiB como o B e, além disso, carrega um par temporário de arquivos
gráficos com tiles sintéticos a partir do tile `$80000` e planta um sprite que aponta
para o primeiro deles. O par e a opção de compilação não existem no A nem no B. A opção
vem desligada por padrão, então um build que não a passe é um B (ou um A, com o
descritor desfeito). Deixar a opção ligada sem aplicar o patch compila um player cujo
renderizador nunca chama o plantador, e aplicar o patch sem a opção compila um player de
128 MiB que carrega o par e não desenha nada dele. Desfaça os dois quando a prova
terminar.

### Para quem começar o Ensaio

**Regra dos pares de arquivos gráficos.** O carregador dispõe os pares de arquivos gráficos um depois do outro, até 8 pares. Os quatro pares originais preenchem exatamente 64 MiB, então o Espaço acrescentado começa no quinto par, e seu primeiro tile é o número `$80000`. Mais quatro pares de 16 MiB completam 128 MiB. O que nenhum arquivo cobre lê como zero. O carregador preenche o vetor de tiles decodificados até potência de 2, e 128 MiB já é uma. Um descritor que não liste exatamente quatro pares originais não deve ganhar um quinto às cegas (o `added_space_patch.py` recusa). Números de tile iguais ou maiores que `$80000` não dão mais a volta para a metade baixa.

**Memória medida do player ampliado (build B).** Máquina com 32.606 MiB instalados. Pico de memória de trabalho de 420 MiB (`coin-start`) e 419 MiB (`team-match`), pico de commit de 416 MiB nos dois, memória de trabalho estável de 300-310 MiB. O cache de tiles decodificados de 256 MiB e o pico da carga são aceitáveis. Detalhes: `docs/specs/graphics-set-growth/issues/02-grow-and-match-reference.md`.

Testes: `py -3 -m pytest growth match` a partir de `tools/kof2003`.
