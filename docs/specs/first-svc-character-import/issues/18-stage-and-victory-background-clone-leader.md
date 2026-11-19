---
title: "Diagnose the fight stage and victory background when the clone leads the team"
triage: ready-for-agent
---

# 18 Diagnose the fight stage and victory background when the clone leads the team

[Parent specification](../spec.md) · [Rehearsal ticket](04-complete-first-imported-match.md) · [Victory screen ticket](17-victory-screen-native-and-clone.md) · [Slot anatomy](../slot-anatomy.md)

Run with `/diagnosing-bugs`, following the method and checklist of
[slot anatomy](../slot-anatomy.md) (§4 item 7 for the route, item 6 for finding a
lookup). Build the feedback loop first.

## What to build

Find and fix the one defect [ticket 17](17-victory-screen-native-and-clone.md)
left open. When a team is led by the clone (`$30`, which stands in for Kyo
Kusanagi), the fight is played in front of, and the victory screen is shown in
front of, the **default** background (the red pagoda) instead of the background
the same team gets with original Kyo leading. With the clone not leading (team
positions 2 and 3) the background is right. Ticket 17 already made the winner
sprite, animation, win quote and name plates of the clone equal to Kyo's; this
background is the only component that still differs, and it is why that ticket's
acceptance line "clone wins at each team position and on the other player side;
each component equals the same screen with original Kyo" is still unchecked.

There are two surfaces and it is not known yet whether they share one lookup:
**(a)** the fight stage, and **(b)** the victory-screen background. Slot anatomy
§2 lists 64-entry tables with a shared default above `$24` that were found by
scan and not yet exercised (`$0641E8`, `$06D32A`, `$06D374`, `$06E9D0`); they are
candidates to check, not conclusions.

## Facts the next session starts from (not written elsewhere in the repository)

All under `private/work/first-import/diag-t17/`, never committed.

- **Deterministic route.** `make_versus.py OUT.txt --pos {0,1,2,3} [--p2side]
  [--end N]` writes the two-player input script (P1 and P2 join, P1 attacks, P2
  stays idle). `--pos 0` is an original team, `--pos 1/2/3` puts the clone at that
  team position, `--p2side` gives the clone team to player 2. `wide.py TAG ROM END
  LO HI STEP [--p2side]` runs the player headless on that script and saves
  screenshots at frames `LO`..`HI` every `STEP` (at most 64), into `wide-TAG/`
  with `run.log`; it reads `POS`, `EXE` and `INTERP` from the environment.
- **Current candidate.** ROM set `roms-v` with the player `build-final\KOF 2003.exe`
  (the one `nat.ps1` and `Jogar-Ensaio-t17.ps1` use). Reference ROM set: `roms-ref`
  (differs only in the selection cell, so the team shows original Kyo).
- **Frames that matter.** In `nat.ps1`, the clone-leading route (`POS=1`) takes its
  captures at 7950–8400 step 30, and the original-team route (`POS=0`) at
  9150–9650 step 25. The fight itself is on screen between roughly frame 5400 and
  those windows; pick fixed frames from a first scan, do not guess.
- **ROM-read tracker.** `runtime-trace/` is a private clone of the runtime with a
  temporary tracer (tag `[DEBUG-t17b]`, in `src/exec.c`, `src/neogeo.c`); the
  player built from it is `build-trace\KOF 2003.exe`. It works only with `--interp`.
  Set `KOF_T17R=LOFRAME-HIFRAME` and it prints to stderr, once per distinct
  (program counter, address, size), every program-ROM or banked-ROM read below
  `$300000` in that frame window, with data registers D0–D7 (low 16 bits). `trace2.ps1`
  runs it for clone and reference; `t17diff2.py` groups by program counter the reads
  made at different addresses by the two runs. A read whose register holds the ID
  times the entry size (`$30` × 2, 4, 8, 16) in the clone run and `$1E` times it in
  the reference run names an ID-indexed table (slot anatomy §4 item 6).
- **`victory_check.py` is for defect A, not for this.** It judges a flat dark
  sprite. This ticket needs a new verdict: the background region of the clone-led
  capture against the same frame of the reference run.

## Blocked by

None.

## Acceptance criteria

- [ ] A scripted, deterministic run reaches the fight and the victory screen with
  the clone leading (`--pos 1`, and `--pos 1 --p2side`), takes screenshots at fixed
  frames, and compares the background region against the reference run; it goes red
  on the symptom (default background), is green for the clone not leading and for an
  original team. Record its command and output; keep captures and logs in `private/`.
  Show the first red run before any code change.
- [ ] Every lookup that picks the fight stage and the victory background from the
  leader's ID is found and listed with its address, entry size and default entry
  (they may be one table or two); the ID path is named (team byte copied where, read
  where).
- [ ] Hypotheses are ranked and falsifiable before any probe, and the winning one is
  recorded with the evidence that separated it from the others.
- [ ] `$30` reads Kyo's entries through the presentation map (`$53100`) or a new
  table; the original entries are unchanged. A tool step with byte checks and tests
  on invented data carries any code change; test with `--interp` first, then rebuild.
- [ ] The clone leading shows the same fight stage and the same victory background
  as original Kyo leading, at team position 1 and on the other player side; the clone
  not leading is unchanged.
- [ ] Original teams are unchanged (byte-identical frames before and after, as in
  ticket 17's regression check), including a team led by Kyo himself.
- [ ] Ticket 17's last acceptance line is checked once this one holds, and its "Left
  open" paragraph gets a pointer to this ticket's resolution.
- [ ] Slot anatomy gets the stage and background lookups (§2 table, "Left open"
  paragraph removed, §5 checklist line for `map_victory_screen.py` or its successor);
  the Rehearsal shortcut points at the new candidate (see `AGENTS.md`).

## Decisions that belong to the owner

- The clone borrows Kyo's stage because it stands in for Kyo. For a real imported
  fighter (Guile and the next ones) the stage a team led by that fighter gets is a
  choice, not a fact: whether it reuses an original stage, uses the source game's
  stage, or stays on the default. This ticket maps `$30` only; record the mechanism
  so the choice for other IDs is a table entry.

## Português (Brasil)

# 18 Diagnosticar o cenário da luta e o fundo da vitória quando o clone lidera a equipe

Rodar com `/diagnosing-bugs`, seguindo o método e o checklist da
[anatomia da vaga](../slot-anatomy.md) (§4 item 7 para a rota, item 6 para achar
uma busca). Primeiro construir o laço de feedback.

### O que construir

Achar e corrigir o único defeito que o [ticket 17](17-victory-screen-native-and-clone.md)
deixou em aberto. Quando a equipe é liderada pelo clone (`$30`, que faz o papel do
Kyo Kusanagi), a luta acontece diante do fundo **padrão** (o pagode vermelho), e a
tela de vitória também, em vez do fundo que a mesma equipe recebe com o Kyo original
na liderança. Com o clone fora da liderança (posições 2 e 3) o fundo está certo. O
ticket 17 já igualou ao do Kyo o sprite do vencedor, a animação, a frase de vitória e
as placas de nome; este fundo é o único componente que ainda difere, e por isso a
linha de aceitação daquele ticket "o clone vence em cada posição e do outro lado do
jogador; cada componente é igual ao da mesma tela com o Kyo original" segue sem marca.

São duas superfícies e ainda não se sabe se dividem a mesma busca: **(a)** o cenário
da luta e **(b)** o fundo da tela de vitória. A anatomia da vaga (§2) lista tabelas de
64 entradas com padrão comum acima de `$24`, achadas por varredura e ainda não
exercitadas (`$0641E8`, `$06D32A`, `$06D374`, `$06E9D0`); são candidatas a conferir,
não conclusões.

### Fatos de partida da próxima sessão (não escritos em outro lugar do repositório)

Tudo em `private/work/first-import/diag-t17/`, nunca vai para o git.

- **Rota determinística.** `make_versus.py OUT.txt --pos {0,1,2,3} [--p2side]
  [--end N]` escreve o roteiro de dois jogadores (P1 e P2 entram, P1 ataca, P2 fica
  parado). `--pos 0` é equipe original, `--pos 1/2/3` põe o clone nessa posição,
  `--p2side` dá a equipe do clone ao jogador 2. `wide.py TAG ROM END LO HI STEP
  [--p2side]` roda o player sem janela nesse roteiro e salva capturas dos quadros
  `LO`..`HI` de `STEP` em `STEP` (até 64) em `wide-TAG/`, com `run.log`; lê `POS`,
  `EXE` e `INTERP` do ambiente.
- **Candidato atual.** Conjunto de ROMs `roms-v` com o player `build-final\KOF 2003.exe`
  (o que `nat.ps1` e `Jogar-Ensaio-t17.ps1` usam). Conjunto de referência: `roms-ref`
  (difere só na célula da seleção, então a equipe mostra o Kyo original).
- **Quadros que importam.** No `nat.ps1`, a rota com o clone na liderança (`POS=1`)
  captura em 7950–8400 de 30 em 30, e a de equipe original (`POS=0`) em 9150–9650 de
  25 em 25. A luta está na tela mais ou menos entre o quadro 5400 e essas janelas;
  escolher quadros fixos a partir de uma primeira varredura, sem chutar.
- **Rastreador de leituras da ROM.** `runtime-trace/` é um clone privado do runtime
  com um rastreador temporário (marca `[DEBUG-t17b]`, em `src/exec.c` e
  `src/neogeo.c`); o player compilado dele é `build-trace\KOF 2003.exe`. Só funciona
  com `--interp`. Com `KOF_T17R=QUADROINI-QUADROFIM` ele imprime no stderr, uma vez
  por (contador de programa, endereço, tamanho) distinto, toda leitura da ROM de
  programa ou de banco abaixo de `$300000` naquela janela, com os registradores de
  dados D0–D7 (16 bits baixos). O `trace2.ps1` roda para clone e referência; o
  `t17diff2.py` agrupa por contador de programa as leituras que as duas execuções
  fazem em endereços diferentes. Uma leitura cujo registrador vale o ID vezes o
  tamanho da entrada (`$30` × 2, 4, 8, 16) na execução do clone e `$1E` vezes isso na
  de referência nomeia uma tabela indexada por ID (anatomia §4 item 6).
- **O `victory_check.py` é do defeito A, não deste.** Ele julga um sprite escuro
  chapado. Este ticket precisa de um veredito novo: a região de fundo da captura com
  o clone na liderança contra o mesmo quadro da execução de referência.

### Bloqueios

Nenhum.

### Critérios de aceitação

- [ ] Um roteiro determinístico chega à luta e à tela de vitória com o clone na
  liderança (`--pos 1` e `--pos 1 --p2side`), tira capturas em quadros fixos e compara
  a região de fundo com a execução de referência; fica vermelho no sintoma (fundo
  padrão) e verde com o clone fora da liderança e com equipe original. Registrar o
  comando e a saída; capturas e logs em `private/`. Mostrar a primeira execução
  vermelha antes de qualquer mudança de código.
- [ ] Toda busca que escolhe o cenário da luta e o fundo da vitória pelo ID do líder
  é achada e listada com endereço, tamanho de entrada e entrada padrão (podem ser uma
  tabela ou duas); o caminho do ID é nomeado (byte da equipe copiado onde, lido onde).
- [ ] As hipóteses são ranqueadas e falsificáveis antes de qualquer sonda, e a
  vencedora é registrada com a evidência que a separou das outras.
- [ ] O `$30` lê as entradas do Kyo pelo mapa de apresentação (`$53100`) ou por uma
  tabela nova; as entradas originais não mudam. Uma etapa de ferramenta com
  conferência de bytes e testes em dados inventados carrega qualquer mudança de
  código; testar primeiro com `--interp`, depois recompilar.
- [ ] O clone na liderança mostra o mesmo cenário de luta e o mesmo fundo de vitória
  que o Kyo original na liderança, na posição 1 e do outro lado do jogador; o clone
  fora da liderança fica inalterado.
- [ ] Equipes originais ficam inalteradas (quadros idênticos byte a byte antes e
  depois, como na regressão do ticket 17), inclusive uma equipe liderada pelo próprio
  Kyo.
- [ ] A última linha de aceitação do ticket 17 é marcada quando este valer, e o
  parágrafo "Em aberto" dele ganha um ponteiro para a resolução deste.
- [ ] A anatomia da vaga recebe as buscas de cenário e fundo (tabela da §2, parágrafo
  "Em aberto" removido, linha do checklist da §5 para o `map_victory_screen.py` ou
  seu sucessor); o atalho do Ensaio aponta para o novo candidato (ver `AGENTS.md`).

### Decisões que são do dono

- O clone toma emprestado o cenário do Kyo porque faz o papel dele. Para um lutador
  importado de verdade (Guile e os próximos), o cenário de uma equipe liderada por ele
  é uma escolha, não um fato: reaproveitar um cenário original, usar o do jogo de
  origem ou ficar no padrão. Este ticket mapeia só o `$30`; registrar o mecanismo para
  que a escolha dos outros IDs seja uma entrada de tabela.
