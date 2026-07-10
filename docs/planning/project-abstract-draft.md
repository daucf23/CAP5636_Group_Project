# Project Abstract Draft (for Webcourses PDF)

**Status:** Draft for team review — export to single-spaced PDF after edits.  
**Target length:** 400–600 words (body).  
**Course:** CAP 5636  

---

**NanoWiki: Pretraining a Small Decoder-Only Transformer from Scratch on Curated Wikipedia Data** — Sahil Bhikha, Thomas Belyakov, David Almeida II

**Problem & Motivation.** Small language models are attractive because they can be trained and served with modest compute, but they often hallucinate and contradict known facts. Many pretraining mixtures span heterogeneous web text, which may encourage fluent but loosely grounded generation. Wikipedia offers a large, structured, and relatively neutral encyclopedic corpus. This project asks whether restricting (or strongly emphasizing) pretraining on Wikipedia improves a small decoder-only model’s fit to encyclopedic text and the style of its completions, relative to an undertrained control with the same architecture. We treat lower held-out Wikipedia perplexity and more coherent, Wikipedia-like generations as proximate success criteria, while noting that perplexity alone is not a full factuality benchmark.

**Approach.** We will use NanoChat, Karpathy’s minimal GPT-style decoder-only transformer for autoregressive language modeling, as our training harness. The primary experiment trains a depth-8 NanoChat model from scratch on a curated English Wikipedia subset for about 0.5B tokens, reusing NanoChat’s tokenizer. If from-scratch quality is too weak within our timeline, we fall back to continued pretraining or light fine-tuning from a small NanoChat checkpoint with the same token budget and document that choice. The v1 baseline is a C-short control: the same architecture, tokenizer, and initialization recipe, trained for only about 5–25M tokens so the comparison stays cheap and schedule-friendly. We defer a full matched-token general-text pretrain and a depth-12 scale-up unless the depth-8 run finishes early. Compute guidance targets UCF’s Newton GPU cluster (prefer a single H100), with student RTX 5090 / 3080 Ti machines as backup and a small cloud contingency if needed.

**Data.** We use the public Hugging Face `wikimedia/wikipedia` dataset, English split `20231101.en` (~11.6 GB of text derived from Wikipedia dumps; original content under CC BY-SA 3.0 and GFDL). We will not require the full dump for the first experiment: we subset to approximately the 0.5B-token training budget, clean and shard text for NanoChat’s dataloader, and hold out validation by article ID so evaluation measures generalization to unseen pages rather than random chunks from trained articles.

**Evaluation Plan.** Quantitatively, we report validation loss and perplexity (or NanoChat bits-per-byte) on the held-out Wikipedia articles and compare the Wikipedia-trained depth-8 model to the C-short control under the same tokenizer and eval set. Qualitatively, we generate completions from a fixed sheet of encyclopedic prompts and compare coherence, repetition, neutral tone, and Wikipedia-like structure. A positive result is lower held-out Wikipedia loss/perplexity and visibly more encyclopedic, less degenerate samples than the control, with limitations (especially perplexity versus hallucination) stated explicitly in the write-up.

**References.**
[1] A. Karpathy, “nanochat,” GitHub repository, https://github.com/karpathy/nanochat  
[2] Wikimedia Foundation, “wikimedia/wikipedia,” Hugging Face Datasets, https://huggingface.co/datasets/wikimedia/wikipedia  
[3] A. Vaswani et al., “Attention Is All You Need,” NeurIPS, 2017. https://arxiv.org/abs/1706.03762  
[4] S. Gunasekar et al., “Textbooks Are All You Need,” 2023. https://arxiv.org/abs/2306.11644  
[5] J. Li et al., “DataComp-LM: In search of the next generation of training sets for language models,” 2024. https://arxiv.org/abs/2406.11794  

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
