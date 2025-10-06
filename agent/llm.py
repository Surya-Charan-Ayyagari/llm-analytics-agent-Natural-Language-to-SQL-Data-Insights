import json, os
from typing import Literal
from .prompts import SYSTEM_PROMPT, INSIGHT_PROMPT

# Backends: 'openai', 'transformers', 'ollama'
BACKEND: Literal['openai','transformers','ollama'] = os.getenv('LLM_BACKEND','openai')  # default to local
MODEL_ID = os.getenv('LLM_MODEL', 'gpt-4o-mini-2024-07-18')

# -------- OpenAI (cloud) --------
_openai_client = None

def _get_openai():
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI
        if not os.getenv('OPENAI_API_KEY'):
            raise RuntimeError('OPENAI_API_KEY not set for OpenAI backend')
        _openai_client = OpenAI()
    return _openai_client

# -------- Transformers (local) --------
_hf_pipe = None

def _get_hf_pipe():
    """Load gpt-oss-20b locally with Transformers pipeline.
    Uses chat template so Harmony format is applied automatically (per model card).
    """
    global _hf_pipe
    if _hf_pipe is None:
        from transformers import pipeline
        import torch
        device = 0 if torch.cuda.is_available() else -1
        _hf_pipe = pipeline(
            'text-generation',
            model=MODEL_ID,
            torch_dtype='auto',
            device=device,
            trust_remote_code=True,
        )
    return _hf_pipe

# -------- Ollama (local server) --------
_ollama_client = None

def _get_ollama():
    global _ollama_client
    if _ollama_client is None:
        import ollama
        _ollama_client = ollama
    return _ollama_client

# ---------- Public API ----------

def nlsql(question: str, schema: dict, model: str | None = None) -> str:
    schema_json = json.dumps(schema)
    user_content = (
        f"SCHEMA (JSON):{schema_json} QUESTION:{question} Return ONLY SQL (no prose). Use CTEs and a final SELECT."
    )

    if BACKEND == 'openai':
        client = _get_openai()
        msgs = [
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_content}
        ]
        resp = client.chat.completions.create(model=model, messages=msgs, temperature=0)
        return resp.choices[0].message.content.strip()

    if BACKEND == 'transformers':
        pipe = _get_hf_pipe()
        messages = [
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_content},
        ]
        # Use chat template automatically
        out = pipe(messages, max_new_tokens=600, do_sample=False)
        text = out[0]["generated_text"][-1]["content"] if isinstance(out[0], dict) else out[0]["generated_text"]
        return text.strip()

    if BACKEND == 'ollama':
        client = _get_ollama()
        resp = client.chat(model=model, messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_content},
        ])
        return resp["message"]["content"].strip()

    raise ValueError(f"Unknown backend: {BACKEND}")


def summarize_df(df, model: str | None = None) -> str:
    preview = df.head(20).to_markdown(index=False)
    user_content = f"{INSIGHT_PROMPT}COLUMNS: {', '.join(df.columns)}PREVIEW:{preview}"
    if BACKEND == 'openai':
        client = _get_openai()
        msgs = [
            {"role":"system","content":"Be a precise data analyst."},
            {"role":"user","content":user_content}
        ]
        resp = client.chat.completions.create(model=model, messages=msgs, temperature=0)
        return resp.choices[0].message.content.strip()

    if BACKEND == 'transformers':
        pipe = _get_hf_pipe()
        messages = [
            {"role":"system","content":"Be a precise data analyst."},
            {"role":"user","content":user_content},
        ]
        out = pipe(messages, max_new_tokens=400, do_sample=False)
        text = out[0]["generated_text"][-1]["content"] if isinstance(out[0], dict) else out[0]["generated_text"]
        return text.strip()

    if BACKEND == 'ollama':
        client = _get_ollama()
        resp = client.chat(model=model, messages=[
            {"role":"system","content":"Be a precise data analyst."},
            {"role":"user","content":user_content},
        ])
        return resp["message"]["content"].strip()

    raise ValueError(f"Unknown backend: {BACKEND}")
