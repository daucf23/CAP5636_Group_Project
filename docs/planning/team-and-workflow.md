# Team and Workflow

## Team

| Member | Lane (proposed) | Primary paths |
| --- | --- | --- |
| Sahil Bhikha | **A — Data** | `nanowiki/data/` |
| Thomas Belyakov | **B — Train / infra** | `third_party/nanochat/`, `nanowiki/configs/`, train `scripts/` |
| David Almeida II | **C — Eval / docs** | `nanowiki/eval/`, `nanowiki/prompts/`, `results/`, README |

Full split, week plan, and handoff contracts: [team-work-split.md](./team-work-split.md).

## Branching

- `main` — stable, submission-ready history
- `cursor/project-planning-3281` — temporary planning / organization branch
- Feature work: short-lived branches per lane when possible (e.g. `feat/data-split`, `feat/train-configs`, `feat/eval-prompts`)

## Pull requests

- Prefer small PRs with a clear purpose and a named lane owner
- Planning docs can land via draft PRs for early feedback
- Implementation PRs should reference the relevant milestone or run id (A / B / C-short)

## Documentation layout

```
docs/
  planning/                 # living planning notes
  superpowers/
    specs/                  # approved design specs
    plans/                  # implementation plans
```

## Conventions (draft)

- Keep the root README as the entry point for graders (setup, how to run, what to expect)
- Put design decisions in specs, not only in chat history
- Prefer reproducible commands in docs (exact install / run / evaluate steps)
- Respect lane handoff contracts in [team-work-split.md](./team-work-split.md)
