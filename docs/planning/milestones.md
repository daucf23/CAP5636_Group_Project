# Milestones

High-level phases for **NanoWiki**. Dates and owners TBD once syllabus deadlines and roles are set.

## M0 — Planning and organization (current)

- [x] Create temporary planning branch
- [x] Add planning document scaffold
- [x] Capture problem statement, approach, data, and eval plan
- [x] Lock v1 eval to simple metrics; draft compute tiers
- [x] Inventory hardware (Newton + 5090 + 3080 Ti) and draft resource forecast
- [ ] Confirm Newton access / queue plan and cloud contingency cap
- [ ] Pick first main run shape (d12@1B vs d8@0.5B)
- [ ] Confirm course deliverables and deadlines
- [ ] Lock baseline definition and v1 non-goals
- [ ] Assign roles / ownership

**Exit criteria:** Overview + open questions resolved enough to write a design spec.

## M1 — Design

- [ ] Write NanoWiki design spec under `docs/superpowers/specs/`
- [ ] Cover: data pipeline, NanoChat integration, baseline(s), metrics, experiment matrix
- [ ] Team review and approve spec
- [ ] Write implementation plan under `docs/superpowers/plans/`

**Exit criteria:** Approved spec + implementation plan committed.

## M2 — Data and training scaffold

- [ ] Download / stream `wikimedia/wikipedia` (`20231101.en`) with license notes
- [ ] Preprocess text for NanoChat; build train / held-out article splits
- [ ] Wire NanoChat training config for a small Wikipedia run
- [ ] Smoke-test: short train + val loss logging

**Exit criteria:** Reproducible data prep + a short training run that logs loss.

## M3 — Experiments

- [ ] Run Wikipedia-adapted training to the agreed token/step budget
- [ ] Run baseline comparison (matched budget where possible)
- [ ] Optional ablations: data size and/or training duration
- [ ] Quantitative eval: val loss / perplexity
- [ ] Qualitative eval: fixed encyclopedic prompt sheet + sample generations

**Exit criteria:** Tables + sample outputs comparing baseline vs Wikipedia model.

## M4 — Report and submission

- [ ] Document results, limitations, and reproduction steps in README / report
- [ ] Prepare presentation materials
- [ ] Freeze release for grading and submit per course instructions

**Exit criteria:** Course submission package ready.
