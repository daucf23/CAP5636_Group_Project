# Team and Workflow

## Team

- Sahil Bhikha
- Thomas Belyakov
- David Almeida II

**Work lanes (unassigned):** A — Data, B — Train / infra, C — Eval / docs.  
Full split, week plan, and handoff contracts: [team-work-split.md](./team-work-split.md).

## Branching

- `main` — stable, submission-ready history
- `cursor/project-planning-3281` — temporary planning / organization branch
- Feature work: short-lived branches per lane when possible (e.g. `feat/data-split`, `feat/train-configs`, `feat/eval-prompts`)

## Pull requests

- Prefer small PRs with a clear purpose and a named lane (A/B/C) when known
- Planning docs can land via draft PRs for early feedback
- Implementation PRs should reference the relevant milestone or run ID (A-smoke / W-Wiki / G-General)

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
