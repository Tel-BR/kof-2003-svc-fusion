# Triage Labels

_PT-BR: rótulos de triagem padrão do mattpocock/skills. Arquivo operacional para agentes, só em inglês._

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker. In the local Markdown tracker the label goes in the ticket's `triage:` frontmatter field.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Wayfinder maps and tickets never carry triage labels, only `wayfinder:<type>`.

Edit the "Label in our tracker" column to match whatever vocabulary you actually use.
