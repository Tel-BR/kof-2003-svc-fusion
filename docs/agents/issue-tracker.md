# Issue tracker: Local Markdown

_PT-BR: por enquanto as issues deste repositório são arquivos Markdown locais; viram GitHub Issues quando houver algo que a comunidade possa experimentar. Arquivo operacional para agentes, só em inglês._

Issues, specs and wayfinder maps for this repo live as Markdown files in the repository. This is the owner's choice until there is something the community can try; then everything moves to GitHub Issues (see **Moving to GitHub later**).

Never paste game data (ROM bytes, extracted assets, disassembly of copyrighted code) into any ticket, spec or research note. Hashes, addresses, sizes and counts are fine. See the hard rule in `AGENTS.md`.

## Conventions (specs and implementation tickets)

- One feature per directory: `docs/specs/<feature-slug>/`
- The spec is `docs/specs/<feature-slug>/spec.md`
- Implementation tickets are one file per ticket at `docs/specs/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- Triage state is recorded as a `triage:` field in each ticket's frontmatter (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `docs/specs/<feature-slug>/` (creating the directory if needed). Wayfinder maps and tickets go under `docs/wayfinder/` instead (below).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the ticket number directly.

## Wayfinding operations

Used by `/wayfinder`. Each map lives in `docs/wayfinder/<map-slug>/`:

- **Map**: `map.md`, with frontmatter `label: wayfinder:map`, `title`, `status`. Body sections: Destination, Notes, Decisions so far, Not yet specified, Out of scope.
- **Child ticket**: `tickets/NN-slug.md`, one per ticket, numbered from `01`. Frontmatter: `id`, `title`, `label` (`wayfinder:research` / `wayfinder:prototype` / `wayfinder:grilling` / `wayfinder:task`), `mode` (`HITL` / `AFK`), `status` (`open` / `closed`), `assignee`, `blocked_by` (list of ticket ids), `research` (pointer to findings, optional). Body starts with `## Question`.
- **Blocking**: the `blocked_by` list. A ticket is unblocked when every id it lists points to a ticket with `status: closed`.
- **Frontier query**: tickets with `status: open`, empty `assignee`, and every `blocked_by` id closed. Lowest id wins.
- **Claim**: set `assignee` to the driving dev and save, before any other work.
- **Resolve**: append a `## Resolution` section with the answer, set `status: closed`, then add one line to the map's "Decisions so far": `- [<title>](tickets/NN-slug.md): <one-line gist>`.
- **Out of scope**: close the ticket and add one line to the map's "Out of scope" linking it.

### Research findings

Research tickets are resolved by a background agent that writes one Markdown file of cited findings.

- The findings file is `docs/wayfinder/<map-slug>/research/<NN>-<slug>.md`.
- It is committed on a throwaway local branch `research/<NN>-<slug>`, created from `main`, never merged.
- On `main`, the ticket's `research` field points at it: `research/<NN>-<slug>:docs/wayfinder/<map-slug>/research/<NN>-<slug>.md`. Read it with `git show <that pointer>`.
- When a session resolves the research ticket, it summarises the findings in the ticket's `## Resolution` with the branch pointer; the branch stays as the record.
- Owner-supplied leads that are not research output (e.g. `research/00-starting-leads.md`) live on `main`.

## Moving to GitHub later

Create one issue per file, keeping a table that maps local ids to issue numbers; label the map `wayfinder:map` and each ticket with its `wayfinder:<type>`; wire native sub-issues and native issue dependencies (`gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`); push the `research/*` branches and link them from their tickets. Then replace this file with the GitHub variant.
