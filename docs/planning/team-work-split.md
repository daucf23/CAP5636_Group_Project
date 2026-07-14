# Team Work Split (3 people)

**Goal:** Even ownership across three lanes for a 3-person team.  
**Rule:** Each person owns one **lane** end-to-end (design → code → smoke proof → handoff). Shared integration happens at week boundaries. **Do not assign names yet** — pick lanes when the team is ready.

## Lanes (equal weight)

| Lane | Owns | Does *not* own |
| --- | --- | --- |
| **A — Data** | Wiki/general download, article-ID Wiki split, both validation sets, Parquet export, manifests/checksums, smoke fixtures | Training hyperparameters, prompt scoring |
| **B — Train / infra** | Pinned NanoChat, dataset-root adapter, tokenizer artifact, configs/launchers, paired smoke, W-Wiki/G-General jobs and checkpoints | Wikipedia cleaning policy, final prose ownership |
| **C — Eval / paper** | Cross-domain bpb, anonymized prompts/scoring, results/figures, root README, paper integration, slides | Data shard internals, training launcher internals |

**Shared (all three):** design review, interpreting W-Wiki vs G-General results, final PDF/report polish, and presentation.

## Why this is even

| Week | Lane A (Data) | Lane B (Train) | Lane C (Eval/Docs) |
| --- | --- | --- | --- |
| **Jul 13–15** | Freeze both tiny roots and Wiki article-ID split | Pin/adapt NanoChat; paired smoke; benchmark 5090 | Freeze prompt/rating sheet; paper/README skeleton |
| **Jul 16–20** | Freeze full manifests and checksums; support reruns | Launch matched W-Wiki/G-General and save checkpoints | Wire cross-domain eval; draft Methods/Related Work |
| **Jul 21–25** | Data appendix and reproduction verification | Package configs/run cards; help reproduce smoke | Freeze results; integrate paper, README, and slides |

Each lane has a **week-1 deliverable**, a **week-2 critical path item**, and a **week-3 packaging item**.

## Handoff contracts (keep interfaces clear)

1. **Data → Train:** Lane A publishes frozen paths:
   - separate Wiki/general dataset roots with train shards and final validation shard
   - `data/processed/wiki_val_article_ids.json` (or equivalent)
   - source manifests, token estimates, checksums, licenses, and rebuild instructions
2. **Train → Eval:** Lane B publishes under `results/<run_id>/`:
   - checkpoint path
   - run card (depth, tokens, init, tokenizer, dataset manifest, hardware, throughput, wall time)
3. **Eval → Report:** Lane C publishes:
   - `results/summary.md` (W-Wiki/G-General cross-domain bpb and checkpoint curves)
   - `results/<run_id>/samples.md`
   - README “How to reproduce”

## Integration checkpoints (all three present)

- **Jul 15:** both smoke roots train/evaluate/reload; throughput fixes the matched budget; prompt sheet exists.
- **Jul 20:** W-Wiki and G-General are finished or the decision gate has been invoked.
- **Jul 21:** experiments freeze; Lane C has the first complete results narrative.
- **Jul 25:** paper, repository, and slides are submission-ready.

## Load-balancing knobs

If one lane finishes early:

- Lane A can help B with run manifests or general-text data.
- Lane B can help C automate sample generation.
- Lane C can help A with license/README data docs.

If one lane slips:

- Cut optional factuality evaluation first; reduce both token budgets equally if compute slips. Never weaken only the baseline.

## Open

- Assign people to lanes A / B / C when the team decides.
- Assign names immediately; unassigned lanes are a schedule blocker.
