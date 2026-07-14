# NanoWiki Deadline-Driven Execution Plan

**Window:** July 13–25, 2026 (soft target); July 27 hard deadline  
**Guaranteed compute:** one RTX 5090  
**Primary experiment:** matched-token W-Wiki vs G-General at depth 8  
**Rule:** corpus is the intended independent variable; all feasible non-data settings remain matched.

## Definition of done

The project is complete when the repository contains:

1. Pinned NanoChat source and tokenizer provenance.
2. Reproducible Wiki/general data preparation with frozen manifests and validation sets.
3. Green paired smoke runs.
4. W-Wiki and G-General runs with equal consumed tokens and matched checkpoints.
5. Cross-domain bpb results, learning curves, and blinded fixed-prompt analysis.
6. A reproducible root README and organized result artifacts/run cards.
7. A 6–8 page final paper, 10–12 presentation slides, individual contributions, and AI Tools disclosure.

## Non-negotiable controls

- Same NanoChat commit, depth, tokenizer, seed/init recipe, context length, attention pattern, optimizer recipe, batch-token schedule, and consumed-token budget.
- Different training corpus: Wikipedia versus pinned general text.
- Both models evaluated on the same frozen Wikipedia and general-text holdouts.
- Any budget reduction applies equally to both runs.
- bpb and Wikipedia-like style are not described as factuality or hallucination metrics.

## Lane assignments

Assign one name to each lane before implementation starts:

- **Lane A — Data:** Wiki/general manifests, splitting, Parquet export, overlap checks, licenses/checksums.
- **Lane B — Train/infra:** NanoChat pin/adapter, tokenizer artifact, configs, smoke, full runs, run cards.
- **Lane C — Eval/paper:** cross-domain eval, prompts/blinding, results/figures, README, paper/slides integration.

All members review the design, interpret results, write their contribution sections, score anonymized samples, and speak in the presentation.

## Jul 13–14 — Freeze interfaces and begin writing

### Lane A

- Confirm `wikimedia/wikipedia`, configuration `20231101.en`, fields, streaming behavior, and license attribution.
- Define deterministic article-ID train/validation assignment.
- Define Wiki/general dataset-root layout and the “last Parquet is validation” invariant.
- Select and record the pinned general-text source/shard manifest.

### Lane B

- Pin an exact NanoChat commit.
- Verify the current `uv` GPU environment on the RTX 5090.
- Add the smallest maintainable dataset-root override/adapter.
- Freeze one tokenizer artifact; record source and checksum.
- Create smoke configurations with expensive CORE evaluation disabled.

### Lane C

- Create the paper skeleton with every required section.
- Draft Methods and Related Work from frozen design decisions.
- Freeze the prompt sheet, decoding settings, anonymized scoring form, and result schema.
- Create the README skeleton and run-card template.

### Integration checkpoint

- Owners, NanoChat commit, tokenizer, corpus sources, directory interfaces, and research question are written down.

## Jul 15 — Paired end-to-end smoke

Run a tiny Wiki root and tiny general root through:

1. Data load
2. Short train
3. bpb evaluation
4. Checkpoint save/reload
5. Fixed-prompt generation

Record:

- `train/tok_per_sec`
- Peak VRAM
- Compile/setup time
- Attention backend and window pattern
- Device batch size and gradient accumulation
- Eval/checkpoint overhead

If SDPA plus sliding-window attention is slow, benchmark full-context `--window-pattern=L`; freeze one choice for both primary runs.

### Gate 1

- **Green by end of Jul 15:** estimate 0.5B run time and freeze equal budget.
- **Not green:** simplify the adapter/configuration and target 0.25–0.3B each. Do not add optional evaluation.

## Jul 16–17 — Freeze full data and launch readiness

### Lane A

- Stream/export enough Wikipedia source tokens for the selected consumed-token budget plus packing loss.
- Freeze Wiki train manifest and validation article IDs.
- Export pinned general train and validation data.
- Assert no Wiki article-ID overlap.
- Record counts, source tokens/bytes, checksums, and licenses.

### Lane B

- Convert frozen token budget to explicit iterations.
- Create W-Wiki and G-General configurations differing only in dataset root and run/output identity.
- Configure checkpoints near 10%, 30%, 60%, and 100% of tokens.
- Perform one-step config validation on both full roots.

### Lane C

- Verify eval can target both validation roots for any checkpoint.
- Finalize anonymized generation export.
- Continue Methods, Related Work, and reproducibility instructions.

### Gate 2

- **Both roots ready by Jul 17:** launch primary runs.
- **Not ready:** document a formal pivot to a Wikipedia learning-curve pilot. Do not present an unmatched model as a controlled corpus baseline.

## Jul 18–20 — Primary runs

1. Run W-Wiki.
2. Inspect only operational health: loss is finite, throughput stable, checkpoints valid.
3. Run G-General with matched settings and token budget.
4. Re-run only for correctness failures, not because results are undesirable.
5. Write a run card immediately after each run.

Lane C evaluates completed checkpoints while the other run trains. Lane A verifies manifests/checksums and helps with reruns.

### Gate 3

- **Comparable pair complete by Jul 20:** proceed to final evaluation.
- **One run failed:** use Jul 21 retry buffer, reducing both budgets only if neither completed budget would remain comparable.
- **No comparable pair:** stop expanding experiments and write an honest pilot/negative-results report.

## Jul 21 — Experiment freeze and analysis

- Evaluate every matched checkpoint on Wiki and general holdouts.
- Plot bpb versus consumed tokens for both model/domain combinations.
- Generate fixed prompts with identical decoding and anonymized labels.
- Have at least two team members independently score samples.
- Reveal identities only after scores are frozen.
- Select representative successes, failures, repetitions, contradictions, and evaluator disagreements.
- Record threats to validity: possible corpus overlap, tokenizer-domain bias, small scale, limited seeds, and bpb/factuality distinction.

No new model scale, tokenizer, corpus, or training objective after this date.

## Jul 22–24 — Deliverables

### Paper

- Abstract: state the controlled question and actual result.
- Introduction: motivation, narrow contribution, and explicit non-claim about hallucination.
- Related Work: small-LM pretraining, corpus quality/domain specialization, Wikipedia/factuality work.
- Methods: architecture, tokenizer, data manifests, split, controls, token budget, hardware.
- Experiments: paired baseline, checkpoint ablation, cross-domain metrics, prompt protocol.
- Results & Discussion: quantitative, qualitative, negative/null findings, error analysis.
- Conclusion & Future Work: factuality evaluation and larger matched runs as future work.
- Add individual contributions and AI Tools disclosure.

### Repository

- Re-run README setup and smoke commands in a clean environment where practical.
- Confirm every result links to a config, manifest, checkpoint/run card, and eval command.
- Remove dead files and redact machine-specific paths or secrets.

### Presentation

- Build ~10–12 slides emphasizing the controlled comparison and main figure.
- Give each member a substantive speaking segment.
- Prepare answers for baseline fairness, factuality claims, data leakage, compute limits, and reproducibility.

## Jul 25–27 — Submission control

- **Jul 25:** target complete submission package.
- **Jul 26–27:** formatting, citation, reproducibility, and correctness fixes only.
- Do not start new experiments unless a required result is invalid and the rerun can finish without threatening submission.

## Optional work, in priority order

Only after the matched pair, cross-domain evaluation, paper draft, and README are secure:

1. Small external factuality-prompt subset with clearly defined metric.
2. Additional blinded raters.
3. More decoding settings.

Depth 12, alternative tokenizers, additional corpora, RAG, SFT/RL, and a web UI are out of scope.
