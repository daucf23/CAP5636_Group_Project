# Team and Workflow

## Branching

- `main` — stable, submission-ready history
- `cursor/project-planning-3281` — temporary planning / organization branch
- Feature work: short-lived branches off `main` (or off planning until M1 is done), named clearly (e.g. `feat/...`, `docs/...`)

## Pull requests

- Prefer small PRs with a clear purpose
- Planning docs can land via draft PRs for early feedback
- Implementation PRs should reference the relevant milestone or issue

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
