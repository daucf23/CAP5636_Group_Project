# Milestones

High-level phases for **NanoWiki**. Guidance target: **~3 weeks** to v1 (d8 Wikipedia + C-short + draft results). These milestones organize work and compute/time expectations; adjust as hardware and course dates firm up.

## M0 — Planning and organization (wrapping up)

- [x] Create temporary planning branch
- [x] Add planning document scaffold
- [x] Capture problem statement, approach, data, and eval plan
- [x] Lock v1 eval to simple metrics; draft compute tiers
- [x] Inventory hardware (Newton + 5090 + 3080 Ti) and draft resource forecast
- [x] Pick first main run shape: **depth 8 @ ~0.5B**, then maybe depth 12
- [x] Lock v1 baseline to **C-short** (~5–25M tokens; 3-week path)
- [x] Record init preference: **scratch first**, continue-pretrain/FT as realistic fallback
- [x] Default tokenizer: **reuse NanoChat as-is**
- [x] Val split: **hold out by article ID**
- [x] Capture abstract requirements; abstract **already submitted**
- [x] Choose repo/integration: **thin NanoChat wrapper**
- [ ] Confirm Newton access / queue plan and cloud contingency cap
- [ ] Confirm later course deliverables (report / presentation)
- [ ] Confirm v1 non-goals
- [ ] Assign roles / ownership
- [ ] Approve implementation design → write spec/plan

**Exit criteria:** Design approved; ready to implement.

## M1 — Design

- [ ] Write NanoWiki design spec under `docs/superpowers/specs/`
- [ ] Cover: data pipeline, NanoChat integration, baseline(s), metrics, experiment matrix
- [ ] Team review and approve spec
- [ ] Write implementation plan under `docs/superpowers/plans/`

**Exit criteria:** Approved spec + implementation plan committed.

## M2 — Data and training scaffold

- [ ] Download / stream `wikimedia/wikipedia` (`20231101.en`) with license notes
- [ ] Preprocess text for NanoChat; build train / **article-ID** held-out splits
- [ ] Wire NanoChat training config for a small Wikipedia run
- [ ] Smoke-test: short train + val loss logging

**Exit criteria:** Reproducible data prep + a short training run that logs loss.

## M3 — Experiments (3-week critical path)

- [ ] Run B: Wikipedia d8 @ ~0.5B tokens
- [ ] Run C-short: ~5–25M tokens control (same arch / tokenizer / Wiki eval)
- [ ] Quantitative eval: val loss / perplexity (bpb)
- [ ] Qualitative eval: fixed encyclopedic prompt sheet + sample generations
- [ ] Optional (only if ahead): C-full general-text matched run and/or d12 scale-up

**Exit criteria:** Tables + sample outputs comparing C-short vs Wikipedia-trained d8 model.

## M4 — Report and submission

- [ ] Document results, limitations, and reproduction steps in README / report
- [ ] Prepare presentation materials
- [ ] Freeze release for grading and submit per course instructions

**Exit criteria:** Course submission package ready.
