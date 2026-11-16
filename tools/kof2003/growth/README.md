# Graphics-set growth tools

Tools for growing the native player's Graphics Set from 64 to 128 MiB with no visible change (spec `docs/specs/graphics-set-growth/`). Nothing here contains game data; captures, builds and logs stay under `private/work/graphics-growth/`.

| File | Purpose |
|---|---|
| `graphics_size.py` | Raises (`apply`), lowers (`undo`) or shows (`status`) the graphics size in the private cartridge descriptor (`private/work/kof2003-port/src/game.c`, the `.crom_size` value). Changes that one value only, is idempotent, keeps line endings, and prints the file's SHA-256 before and after. It copies none of the descriptor's code. |

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

`ninja` also runs the generator again, because it embeds the descriptor. Hash `generated/` before and after: every file must be identical, which proves the native code did not change. `compare_builds` exits with 1 on any difference, a missing build, or a `--verify` summary worse than A's. A rebuilt 64 MiB executable need not equal the saved `build-a` byte for byte (link-time stamps), so `build-a` is never rebuilt over.

Tests: `py -3 -m pytest growth match` from `tools/kof2003`.

## Ferramentas da ampliação do Conjunto gráfico

Ferramentas para ampliar o Conjunto gráfico do player nativo de 64 para 128 MiB sem mudança visível (spec `docs/specs/graphics-set-growth/`). Nada aqui contém dados dos jogos; capturas, builds e logs ficam em `private/work/graphics-growth/`.

| Arquivo | Função |
|---|---|
| `graphics_size.py` | Sobe (`apply`), desce (`undo`) ou mostra (`status`) o tamanho gráfico no descritor privado do cartucho (`private/work/kof2003-port/src/game.c`, o valor `.crom_size`). Muda só esse valor, é idempotente, preserva as quebras de linha e imprime o SHA-256 do arquivo antes e depois. Não copia código do descritor. |

Builds: o **A** é a referência, 64 MiB, guardado em somente leitura em `private/work/graphics-growth/build-a/`. O **B** é 128 MiB sem código de teste nem arquivo extra, guardado em `build-b/`. Os dois são o mesmo programa; só o tamanho gráfico muda.

### Compilar o B e comparar com o A (Windows, PowerShell)

Os comandos são os do bloco em inglês acima, na mesma ordem. O `ninja` roda o gerador de novo porque ele embute o descritor; calcule o hash de `generated/` antes e depois, e todos os arquivos têm de ser idênticos, o que prova que o código nativo não mudou. O `compare_builds` sai com código 1 se houver diferença, build faltando ou resumo do `--verify` pior que o do A. Um executável de 64 MiB recompilado pode não ser igual byte a byte ao `build-a` guardado (carimbos de ligação), por isso o `build-a` nunca é recompilado por cima.

Testes: `py -3 -m pytest growth match` a partir de `tools/kof2003`.
