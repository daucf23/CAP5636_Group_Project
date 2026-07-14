# Submitted Project Proposal (Archive)

**Status:** **Submitted** — this file preserves the original submitted proposal. The [design spec](../superpowers/specs/2026-07-10-nanowiki-design.md) selects and strengthens the proposal’s general-text baseline for final execution.
**Target length:** 400–600 words (body).  
**Course:** CAP 5636  

---

**NanoWiki: Pretraining a Small Decoder-Only Transformer from Scratch on Curated Wikipedia Data**

**Team members:** Sahil Bhikha, Thomas Belyakov, David Almeida II

**Problem & Motivation.** Small language models are computationally accessible but they often struggle with hallucinations and factual inconsistency. Usually the datasets they are trained on are massive and ranging over a wide variety of writing styles. Wikipedia provides a large, structured, neutral set of information that could be ideal for testing whether a mode could be trained on structured, encyclopedic data to help with factual accuracy and consistency. This project is studying whether restricting pretraining on Wikipedia data can help improve upon a small model's tendency to hallucinate or have factual inconsistencies.

**Approach.** We plan to use NanoChat, a minimal implementation of a GPT-style decoder-only transformer for autoregressive language modeling, to train a small model on the Wikipedia dataset. We will compare the Wikipedia adapted model against the baseline trained on general text or simply the untuned NanoGPT model. We may also compare multiple data sizes or durations of training to further analyze our findings and improvements.

**Data.** We will use the publicly available Hugging Face `wikimedia/wikipedia` dataset (`20231101.en` split), which is derived from Wikipedia dumps. The original textual content is licensed under the Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) and GNU Free Documentation License (GFDL). The English split from 2023 contains about 11.6 GB of text information. We will need to preprocess the data in order to prepare it for model pretraining. A held-out validation set will be created for unseen articles.

**Evaluation Plan.** We will evaluate the model quantitatively using validation loss and perplexity on a held-out Wikipedia test set. We will compare the Wikipedia-adapted model against a baseline model that has not been trained on the Wikipedia subset, or against models trained for different numbers of steps/tokens. Qualitatively, we will generate completions from fixed encyclopedic prompts and compare outputs for coherence, repetition, neutral tone, and Wikipedia-like structure. The result we are looking for would be lower perplexity on held-out Wikipedia text and visibly more encyclopedic completions without excessive repetition or degeneration.

**References.**
[1] https://github.com/karpathy/nanochat
[2] https://huggingface.co/datasets/wikimedia/wikipedia
[3] https://arxiv.org/pdf/1706.03762 — Attention Is All You Need
[4] https://arxiv.org/pdf/2306.11644 — Textbooks Are All You Need
[5] https://arxiv.org/pdf/2406.11794 — DataComp-LM: In search of the next generation of training sets for language models

---

## Word count check

Run after edits:

```bash
# Count words in the abstract body (from title line through Evaluation Plan; exclude this checklist)
python3 - <<'PY'
from pathlib import Path
text = Path("docs/planning/project-abstract-draft.md").read_text()
start = text.index("**NanoWiki:")
end = text.index("**References.**")
body = text[start:end]
# include references in official submission; count body sections only for ~400-600 guidance
print("words through Evaluation Plan:", len(body.split()))
refs = text[end:text.index("---", end)]
print("words including References block:", len((body + refs).split()))
PY
```

## Export notes

- Paste the abstract block (title through references) into a doc, single-space, export PDF
- One team submission on Webcourses; confirm due date on the course site
