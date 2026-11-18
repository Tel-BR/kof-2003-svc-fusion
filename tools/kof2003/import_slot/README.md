# First imported character: workspace preparation

`prepare_workspace.py` copies an already prepared ROM directory into a new
directory under `private/`. It uses independent files, so later edits to the
experimental program do not change the original control. It refuses an existing
destination and sources containing symbolic links. Both paths must be in
`private/`. This prepares inputs only: it does not make a build or add a fighter.

```powershell
python tools/kof2003/import_slot/prepare_workspace.py `
  private/work/mvs-control-v0.1.0/roms private/work/first-import/roms
```

If copying fails, inspect any partially created destination before removing it
and retrying. Never stage its contents in git.

## Preparação para o primeiro personagem importado

O `prepare_workspace.py` copia uma pasta de ROMs já preparada para uma pasta
nova dentro de `private/`. Os arquivos são independentes, então alterações
posteriores no programa experimental não mudam o controle original. O comando
recusa um destino existente e origens com links simbólicos. Os dois caminhos
devem ficar em `private/`. Ele apenas prepara os arquivos: não compila o jogo
nem acrescenta um lutador.

Use o comando acima no PowerShell. Se a cópia falhar, inspecione qualquer pasta
parcial antes de removê-la e tentar novamente. Nunca adicione seu conteúdo ao git.
