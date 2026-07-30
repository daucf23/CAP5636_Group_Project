"""Autoregressive decoding shared by training-time sampling and later eval (Lane C).

FIXED_EVAL_DECODING is the frozen decoding config the README requires to stay
the same across B0/B1/M2 when generating the final eval stories -- Lane C's
harness should import it rather than redefining its own settings.

Pass a seeded `torch.Generator` (or use `eval_sample_seed`) for reproducible
eval samples; training-time preview sampling may omit it.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import torch
import torch.nn.functional as F


@dataclass
class DecodingConfig:
    temperature: float = 1.0
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    greedy: bool = False
    max_new_tokens: int = 200


# max_new_tokens must exceed the gold story length (~200-260 tokens for the
# 120-180 word target in data/prompts/templates.json), otherwise M2 is cut off
# before it can emit <eos> and every system looks truncated.
FIXED_EVAL_DECODING = DecodingConfig(temperature=0.85, top_p=0.9, max_new_tokens=300)

# Default base seed for Lane C eval generation. Per-sample seeds are derived
# from (base, system_id, prompt_id) so regenerating one system does not change
# the others, and row order in the prompt pack does not matter.
FIXED_EVAL_SEED = 0


def eval_sample_seed(base_seed: int, system_id: str, prompt_id: str) -> int:
    """Stable 63-bit seed for one (system, prompt) generation."""
    payload = f"{base_seed}\0{system_id}\0{prompt_id}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big") % (2**63)


def make_generator(device: Union[str, torch.device], seed: int) -> torch.Generator:
    """Device-matched RNG for multinomial sampling."""
    dev = torch.device(device)
    # torch.multinomial requires the generator's device to match the probs
    # tensor's (a CPU generator on a cuda/mps tensor raises at sample time).
    g = torch.Generator(device=dev)
    g.manual_seed(int(seed))
    return g


@torch.no_grad()
def generate_ids(
    model,
    tokenizer,
    prompt: str,
    config: DecodingConfig,
    device,
    generator: Optional[torch.Generator] = None,
) -> Tuple[List[int], int]:
    """Sample a continuation; return (prompt_ids + new_ids, n_prompt_tokens).

    Callers that need the prompt/continuation boundary should use this rather
    than string-slicing `generate()`'s output: BPE decode(encode(x)) is not
    guaranteed to reproduce `x` byte-for-byte, and with a long rendered fact
    card a few characters of slippage would silently leak card text into the
    scored story (and into the perplexity mask).

    For comparable eval runs, pass a seeded `generator` (see `make_generator`
    / `eval_sample_seed`). Without one, sampling is non-deterministic.
    """
    was_training = model.training
    model.eval()
    eos_id = tokenizer.token_to_id("<eos>")
    prompt_ids = tokenizer.encode(prompt).ids
    ids = torch.tensor([prompt_ids], dtype=torch.long, device=device)

    for _ in range(config.max_new_tokens):
        ids_cond = ids[:, -model.config.block_size:]
        logits, _ = model(ids_cond)
        logits = logits[:, -1, :]

        if config.greedy:
            next_id = logits.argmax(dim=-1, keepdim=True)
        else:
            logits = logits / max(config.temperature, 1e-8)
            if config.top_k is not None:
                k = min(config.top_k, logits.size(-1))
                vals, _ = torch.topk(logits, k)
                logits[logits < vals[:, [-1]]] = float("-inf")
            if config.top_p is not None:
                sorted_logits, sorted_idx = torch.sort(logits, descending=True)
                cum_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                remove = cum_probs - F.softmax(sorted_logits, dim=-1) > config.top_p
                sorted_logits[remove] = float("-inf")
                logits = torch.zeros_like(logits).scatter(1, sorted_idx, sorted_logits)
            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1, generator=generator)

        ids = torch.cat([ids, next_id], dim=1)
        if next_id.item() == eos_id:
            break

    if was_training:
        model.train()
    return ids[0].tolist(), len(prompt_ids)


def generate(
    model,
    tokenizer,
    prompt: str,
    config: DecodingConfig,
    device,
    generator: Optional[torch.Generator] = None,
) -> str:
    """Full decoded sequence (prompt + continuation)."""
    all_ids, _ = generate_ids(model, tokenizer, prompt, config, device, generator=generator)
    return tokenizer.decode(all_ids)
