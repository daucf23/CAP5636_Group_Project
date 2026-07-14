# Milestones

High-level phases for **NanoWiki** from July 13 to the July 25 soft deadline (July 27 hard deadline). The critical path is a controlled, matched-token Wikipedia-vs-general experiment plus the required paper, code, and presentation.

## M0 — Planning and organization (wrapping up)

- [x] Create temporary planning branch
- [x] Add planning document scaffold
- [x] Capture problem statement, approach, data, and eval plan
- [x] Lock v1 eval to simple metrics; draft compute tiers
- [x] Inventory hardware (Newton + 5090 + 3080 Ti) and draft resource forecast
- [x] Freeze the primary architecture at **depth 8**; cut depth 12 before submission
- [x] Replace the undertrained C-short baseline with a **matched-token G-General** run
- [x] Record init preference: **scratch first**, continue-pretrain/FT as realistic fallback
- [x] Default tokenizer: **reuse NanoChat as-is**
- [x] Val split: **hold out by article ID**
- [x] Capture abstract requirements; abstract **already submitted**
- [x] Choose repo/integration: **thin NanoChat wrapper**
- [x] Draft design spec with clear eval/data/train capture
- [x] Propose even 3-person work split as **unassigned lanes** (Data / Train / Eval-docs)
- [ ] Team review design spec
- [ ] Assign people to lanes when ready
- [x] Treat the RTX 5090 as the guaranteed compute path
- [x] Record final paper, repository, presentation, rubric, and AI disclosure requirements
- [ ] Confirm v1 non-goals

**Exit criteria (Jul 14):** design approved, names assigned to lanes, pinned NanoChat commit selected, and implementation plan accepted.

## M1 — Design

- [x] Write NanoWiki design spec under `docs/superpowers/specs/`
- [x] Cover: data pipeline, NanoChat integration, matched baseline, metrics, experiment matrix
- [ ] Team review and approve spec
- [x] Write implementation plan under `docs/superpowers/plans/`

**Exit criteria:** Approved spec + implementation plan committed.

## M2 — Paired data and training scaffold (Jul 14–15)

- [ ] Download / stream `wikimedia/wikipedia` (`20231101.en`) with license notes
- [ ] Preprocess text for NanoChat; build train / **article-ID** held-out Wikipedia splits
- [ ] Pin a general-text shard manifest and general validation holdout
- [ ] Expose a dataset-root override compatible with NanoChat’s Parquet/last-shard validation convention
- [ ] Freeze one tokenizer artifact and checksum for all runs
- [ ] Smoke-test both dataset roots: train, bpb, checkpoint reload, and generation
- [ ] Record 5090 throughput, peak VRAM, attention backend, and compile time

**Exit criteria (Jul 15):** reproducible paired data prep and green smoke runs that determine the equal full-run budget.

## M3 — Controlled experiments (Jul 16–21)

- [ ] Freeze equal token budget (target 0.5B each; deadline-safe floor ~0.25B)
- [ ] Run W-Wiki and save matched token-position checkpoints
- [ ] Run G-General with identical non-data settings and token budget
- [ ] Quantitative eval: both models/checkpoints on Wiki and general bpb
- [ ] Qualitative eval: fixed prompts, identical decoding, anonymized outputs
- [ ] At least two team members independently score samples before identities are revealed
- [ ] Record failures, null results, throughput, wall time, and limitations

**Exit criteria (Jul 21):** experiment freeze with a controlled cross-domain table, learning curves, and blinded qualitative results.

## M4 — Report and submission (draft continuously; finalize Jul 22–25)

- [ ] Draft Methods and Related Work while runs execute
- [ ] Complete 6–8 page NeurIPS-style paper with all required sections
- [ ] Include baselines, checkpoint ablation, error analysis, limitations, and individual contributions
- [ ] Add an “AI Tools” section documenting tool use and purpose
- [ ] Publish reproducible README: dependencies, data prep, smoke, train, and eval commands
- [ ] Remove dead files and verify a clean setup/smoke path
- [ ] Prepare ~10–12 slides for a 10-minute talk; assign substantive speaking sections to all members
- [ ] Freeze experiments after Jul 21 and target submission on Jul 25

**Exit criteria:** PDF, repository link, slides, contribution statement, and AI disclosure are submission-ready; Jul 26–27 are correction-only buffer.
