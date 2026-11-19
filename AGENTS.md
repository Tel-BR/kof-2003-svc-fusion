# KOF 2003 × SVC Chaos Recomp

A planned native PC port that unites the rosters of The King of Fighters 2003 and SNK vs. Capcom: SVC Chaos (Neo Geo MVS) in one game.

_Port nativo para PC, ainda em planejamento, que une os elencos de The King of Fighters 2003 e SNK vs. Capcom: SVC Chaos (Neo Geo MVS) num só jogo. A versão em português de cada seção vem logo depois da versão em inglês._

## Hard rule: no game data in git

This repository must never contain anything from the games or derived from them:
ROMs, BIOS, C code generated from the ROMs, extracted tiles or sprites, RAM dumps,
traces carrying game data, or save states. Users supply their own dumps (bring your
own ROM). All of that lives in `private/`, which is git-ignored. Never `git add -f`
anything under `private/`, and never paste game data into tickets, research notes,
docs or commit messages. Hashes, addresses, sizes and counts are fine; bytes,
disassembly listings and images are not.

### Regra obrigatória: nada dos jogos no git

Este repositório nunca pode conter nada dos jogos nem derivado deles: ROMs, BIOS,
C gerado a partir das ROMs, tiles ou sprites extraídos, dumps de RAM, traces com
dados do jogo ou save states. Cada usuário fornece os próprios dumps. Tudo isso fica
em `private/`, que o git ignora. Nunca use `git add -f` em nada dentro de `private/`
e nunca cole dados dos jogos em tickets, notas de pesquisa, documentação ou mensagens
de commit. Hashes, endereços, tamanhos e contagens podem; bytes, listagens de
disassembly e imagens não.

## Third-party code

The project licence is not decided yet. Reading and studying third-party code
(MAME, FBNeo, the recomp projects) is fine; copying it into this repository is not,
until the licence is decided. Third-party projects that need to be run locally are
cloned outside the repository or under `private/`.

### Código de terceiros

A licença do projeto ainda não foi decidida. Ler e estudar código de terceiros (MAME,
FBNeo, os projetos de recomp) é livre; copiar para este repositório não, até a licença
ser decidida. Projetos de terceiros que precisem rodar localmente são clonados fora
do repositório ou dentro de `private/`.

## Facts vs decisions

Agents establish facts themselves (tools, reading, subagents). Decisions belong to
the owner: ask. The owner is not a systems programmer, so every option comes with
its causes and consequences in plain language, and questions use the interactive
question tool. Talk to the owner in Brazilian Portuguese.

### Fatos e decisões

Os agentes levantam os fatos sozinhos (ferramentas, leitura, subagentes). As decisões
são do dono do repositório: pergunte. Ele não é programador de sistemas, então cada
opção vem com causas e consequências em linguagem simples, e as perguntas usam a
ferramenta interativa. Fale com ele em português do Brasil.

## Language convention

Human-facing docs (README, `docs/` outside `docs/agents/`, ADRs, glossary, tickets)
are bilingual when possible: English first, then Brazilian Portuguese. Ticket titles
are in English. Agent-operational files in `docs/agents/` are English-only so the
two versions cannot drift apart.

### Convenção de idioma

A documentação para pessoas (README, `docs/` fora de `docs/agents/`, ADRs, glossário,
tickets) é bilíngue sempre que possível: inglês primeiro, depois português do Brasil.
Títulos de tickets em inglês. Os arquivos operacionais para agentes em `docs/agents/`
ficam só em inglês, para que as duas versões não se desencontrem.

## Workflow

The repo follows the mattpocock/skills flow: `/wayfinder` maps until the way is
clear, then `/to-spec` → `/to-tickets` → `/implement` (with `/tdd` and `/code-review`).
Do not skip `/to-spec`. When working through a map, resolve one ticket per session
(research tickets excepted), claim it before starting, record the resolution in the
ticket and add a pointer to the map's "Decisions so far".

### Fluxo de trabalho

O repositório segue o fluxo do mattpocock/skills: `/wayfinder` até o caminho ficar
claro, depois `/to-spec` → `/to-tickets` → `/implement` (com `/tdd` e `/code-review`).
Não pule o `/to-spec`. Ao percorrer um mapa, resolva um ticket por sessão (exceto
pesquisa), faça o claim antes de começar, registre a resolução no ticket e um ponteiro
em "Decisions so far" no mapa.

## Ticket references

When a user refers to a ticket only by its number, first search every ticket and issue
location. Report every match with its path, title and state (status or triage), then
ask which one they mean unless the surrounding request names exactly one path or title.
Never silently choose a match from its number alone.

### Referências a tickets

Quando o usuário mencionar um ticket só pelo número, primeiro pesquise todos os locais
de tickets e issues. Informe cada correspondência com caminho, título e estado (status
ou triage), depois pergunte qual delas ele quer, a menos que o pedido ao redor nomeie
exatamente um caminho ou título. Nunca escolha uma correspondência em silêncio apenas
pelo número.

## Agent skills

### Issue tracker

Local Markdown: wayfinder maps and tickets live under `docs/wayfinder/`, specs and implementation tickets under `docs/specs/`. Moves to GitHub Issues once there is something the community can try. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Rehearsal shortcut

The owner tests the Rehearsal with the git-ignored shortcut `Jogar-Ensaio.cmd` at the repository root. Whenever the Rehearsal candidate changes (its ROM image, any patched code, or the native player built for it), rebuild what is needed and repoint the shortcut's launcher at the new candidate before reporting completion, check that it starts, and say in the report which candidate it opens and how the owner should test it. Keep the launcher and builds under `private/`; never commit them.

### Atalho do Ensaio

O dono testa o Ensaio pelo atalho `Jogar-Ensaio.cmd` na raiz do repositório, ignorado pelo git. Sempre que o candidato do Ensaio mudar (a imagem de ROM, qualquer código remendado ou o player nativo compilado para ele), recompile o que for preciso e aponte o lançador do atalho para o novo candidato antes de relatar a conclusão, confira que ele abre e diga no relatório qual candidato ele abre e como o dono deve testar. Mantenha o lançador e os builds em `private/`; nunca os versione.

## Task completion

When a task changes tracked files, commit its intended changes on the current branch before reporting completion. Inspect the working tree, stage only files changed for that task, and review the staged diff. Keep pre-existing unrelated work out of the commit and never include anything under `private/`. Do not create an empty commit when there are no task-owned tracked changes; do not push unless the owner asks.

After each completed task, report the natural next steps. If there are none, say so. Include one ready-to-copy prompt for the next conversation that continues the most natural next step.

Keep that prompt a pointer: the skill to run, the ticket or doc path, and only the decisions or facts not yet written in the repository. The ticket, spec and docs carry the rest, so record anything the next session needs there first. Add one line on the session boundary: `/clear` when the repository carries the context, continue when the next step needs this conversation as its primary source.

### Conclusão de tarefas

Quando uma tarefa alterar arquivos rastreados, faça commit das mudanças pretendidas da tarefa na branch atual antes de informar a conclusão. Confira a árvore de trabalho, adicione ao stage somente os arquivos alterados por essa tarefa e revise o diff staged. Deixe mudanças preexistentes e sem relação fora do commit e nunca inclua nada de `private/`. Não crie commit vazio se não houver alteração rastreada da tarefa; não faça push sem pedido do dono.

Ao concluir cada tarefa, informe os próximos passos naturais. Se não houver, diga isso. Inclua um prompt pronto para copiar na próxima conversa, dando continuidade ao próximo passo mais natural.

Esse prompt é um ponteiro: a skill a rodar, o caminho do ticket ou documento e só as decisões ou fatos ainda não escritos no repositório. O ticket, a spec e os documentos levam o resto, então registre neles antes o que a próxima sessão precisar. Acrescente uma linha sobre a passagem de sessão: `/clear` quando o repositório já carrega o contexto, continuar quando o próximo passo precisa desta conversa como fonte primária.
