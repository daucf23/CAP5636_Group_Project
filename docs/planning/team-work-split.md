# Team Work Split (3 people)

**Goal:** Even ownership across Sahil Bhikha, Thomas Belyakov, and David Almeida II.  
**Rule:** Each person owns a **lane** end-to-end (design → code → smoke proof → handoff). Shared integration happens at week boundaries. Names below are a starting assignment — swap freely if someone prefers another lane.

## Lanes (equal weight)

| Lane | Owner (proposed) | Owns | Does *not* own |
| --- | --- | --- | --- |
| **A — Data** | Sahil Bhikha | `nanowiki/data/`, download/clean/article-ID split/export, train/val manifests, smoke shard | Training hyperparameters, prompt sheet |
| **B — Train / infra** | Thomas Belyakov | `third_party/nanochat/`, `nanowiki/configs/`, `scripts/` train launchers, Newton/5090 run recipes, Run A/B/C-short jobs | Wikipedia cleaning logic, final write-up prose |
| **C — Eval / docs** | David Almeida II | `nanowiki/eval/`, `nanowiki/prompts/`, `results/` tables & samples, root `README` repro steps, report/figures draft | Data shard format internals, Slurm scripts (unless helping B) |

**Shared (all three):** design review, interpreting B vs C-short results, final PDF/report polish, presentation if required.

## Why this is even

| Week | Sahil (Data) | Thomas (Train) | David (Eval/Docs) |
| --- | --- | --- | --- |
| **1** | Download + clean + article-ID split; tiny smoke export | Pin NanoChat; smoke config; prove train on smoke shard | Draft prompt sheet; stub metrics/results layout; README skeleton |
| **2** | Freeze 0.5B subset + val ID list; document C-short tiny corpus choice | Run A done; launch Run B (d8@0.5B); launch C-short | Wire eval on checkpoints; collect bpb + samples into `results/` |
| **3** | Help re-export / checksums if runs need reruns; data appendix for report | Optional B-FT / B2 only if ahead; package checkpoints | Comparison table, qualitative notes, write-up, repro README |

Each lane has a **week-1 deliverable**, a **week-2 critical path item**, and a **week-3 packaging item**.

## Handoff contracts (keep interfaces clear)

1. **Data → Train:** Sahil publishes frozen paths:
   - `data/processed/train/` shards
   - `data/processed/val/` shards
   - `data/processed/val_article_ids.json` (or equivalent)
   - short note: token estimate, license, how to rebuild
2. **Train → Eval:** Thomas publishes under `results/<run_id>/`:
   - checkpoint path
   - run card (depth, tokens, init, hardware, wall time)
3. **Eval → Report:** David publishes:
   - `results/summary.md` (B vs C-short bpb table)
   - `results/<run_id>/samples.md`
   - README “How to reproduce”

## Integration checkpoints (all three present)

- End of week 1: smoke train reads Sahil’s shard and logs one val metric; David’s prompt file exists.
- End of week 2: Run B and C-short finished (or clearly in queue); David has first comparison draft.
- End of week 3: summary table + samples + README repro frozen for submission package.

## Load-balancing knobs

If one lane finishes early:

- Sahil can help Thomas with Newton job scripts or C-short data.
- Thomas can help David automate sample generation.
- David can help Sahil with license/README data docs.

If one lane slips:

- Cut stretch (B2 / C-full) first — never cut another person’s critical path without agreeing.

## Open

Confirm or swap the proposed owner names. Exact final-report format still TBD from the course.
