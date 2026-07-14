# Course Requirements (CAP 5636)

Recorded course requirements for the submitted abstract and final project deliverables.

## Milestone: Project Abstract

| Item | Requirement |
| --- | --- |
| Purpose | Structured proposal that locks problem, approach, and evaluation early; graded milestone; basis for instructor feedback |
| Length | **400–600 words**, single-spaced |
| Format | **PDF** via Webcourses by 11:59 pm on the due date |
| Team | **2–3 members**; one submission; list all members |
| Due date | **Already submitted** (team turned in the original NanoWiki abstract text) |
| Status | Complete — remaining work is execution (data, train, eval, final deliverables) |

### Required sections

1. **Title and team members** (1 line)
2. **Problem & Motivation** (~100 words)
3. **Approach** (~150 words) — specific architecture, training procedure, baselines (not “we will use a transformer”)
4. **Data** (~75 words) — source, size, license, preprocessing
5. **Evaluation Plan** (~75 words) — metrics, comparisons, what counts as success (quantitative + qualitative)
6. **References** (3–5)

### Rubric weights

| Component | Weight |
| --- | --- |
| Problem clarity & significance | 20% |
| Technical approach | 25% |
| Feasibility & scope | 20% |
| Evaluation plan | 15% |
| References & grounding | 10% |
| Writing quality | 10% |

### Failure modes to avoid (from assignment)

- Scope too large (e.g. full foundation-model build in seven weeks)
- Scope too small (tutorial reproduction with no extension)
- Vague approach
- No clear evaluation / baseline

### How our planning maps

| Abstract section | Planning source |
| --- | --- |
| Problem & Motivation | [project-overview.md](./project-overview.md) |
| Approach + feasibility | overview + [compute-budget.md](./compute-budget.md) |
| Data / Evaluation | overview |
| Draft for PDF export | [project-abstract-draft.md](./project-abstract-draft.md) |

## Final project

**Deadlines used by the team:** July 25 soft target; July 27 hard deadline.

### Acceptable project type

NanoWiki is positioned as an **empirical study**: systematically compare Wikipedia-only and general-text pretraining under controlled architecture and token budgets. The contribution is the measured domain-specialization trade-off, not reproduction of NanoChat itself.

The project must avoid the listed failure modes:

- Reproduction without a meaningful extension
- Weak or trivial baselines
- A working implementation without analysis
- Scope creep
- Writing only after experiments finish

### Final paper

- **Length:** 6–8 pages, references excluded
- **Format:** NeurIPS-style, single column, 10pt
- **Submission:** PDF through Webcourses
- **Required sections:**
  - Abstract (~150 words)
  - Introduction
  - Related Work
  - Methods, with enough detail to reproduce
  - Experiments, including setup, baselines, and ablations
  - Results & Discussion, including quantitative results, qualitative results, and error analysis
  - Conclusion & Future Work
  - References
- Identify each team member’s contributions.
- Add an **AI Tools** section describing which generative AI tools were used and for what purpose.

### Code repository

- Include the repository link in the paper.
- Root README must include project overview, dependencies, and commands to reproduce key results.
- Keep code organized and appropriately commented; remove dead files.
- Pin NanoChat, tokenizer/data provenance, configurations, and run metadata needed to reproduce the comparison.

### Presentation

- **15 minutes total:** 10-minute presentation + 5-minute discussion
- Approximately **10–12 slides**
- Cover motivation, approach, key results, and takeaways
- All team members must speak substantively
- Demo is optional

### Grading

Overall project:

| Component | Weight |
| --- | --- |
| Final paper | 60% |
| Code and reproducibility | 20% |
| Oral presentation | 20% |

Final paper:

| Component | Weight | NanoWiki implication |
| --- | --- | --- |
| Technical execution | 30% | Correct paired data/training/eval pipeline |
| Empirical rigor | 20% | Matched-token baseline, checkpoint ablation, cross-domain metrics, honest negative results |
| Originality | 15% | Controlled insight into domain-restricted small-model pretraining |
| Writing and structure | 20% | Clear claims, useful figures, limitations, and error analysis |
| Literature grounding | 15% | Position against corpus-quality, factuality, and small-LM pretraining work |

Presentation:

| Component | Weight |
| --- | --- |
| Content and clarity | 40% |
| Visual aids | 20% |
| Delivery | 20% |
| Discussion and Q&A | 20% |

### Design consequences

1. G-General must match W-Wiki’s model and token budget; an intentionally undertrained control is insufficient as the primary baseline.
2. Intermediate matched checkpoints provide the required ablation without separate training runs.
3. Both models must be evaluated on Wikipedia and general text to expose specialization trade-offs.
4. Claims about hallucination require a dedicated factuality evaluation; otherwise use domain-fit and generation-style language.
5. Methods, Related Work, README, and slides begin before final results are available.
