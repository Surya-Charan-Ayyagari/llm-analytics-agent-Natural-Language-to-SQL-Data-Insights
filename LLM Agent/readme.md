# ------------------------------
# LLM Analytics Agent – Postgres + GPT‑OSS‑20B (local) + Streamlit

This starter can run **OpenAI gpt‑oss‑20b** locally via **Transformers** (default), via **Ollama**, or via **OpenAI/OpenRouter/Fireworks** APIs. The UI is Streamlit; the DB is Postgres.

## 1) Choose an LLM backend

### A) Local (Transformers) – default
- Pros: private, free to run; fastest token latency on a good GPU/Apple Silicon.
- Install: `pip install -r requirements.txt` (ensures `transformers`, `accelerate`, `torch`).
- Model ID: `openai/gpt-oss-20b` (Hugging Face Hub).

> Notes: The model uses a **Harmony** chat template. Our code leverages Transformers’ chat template so you don’t have to implement it manually. See OpenAI’s repo/model card for details. citeturn0search1turn0search0

### B) Local (Ollama)
- Install Ollama, then pull the model: `ollama pull gpt-oss:20b` (or the exact tag in the Ollama library).
- Set `LLM_BACKEND=ollama` and `LLM_MODEL=gpt-oss:20b`.
- Good if you prefer a lightweight local server. citeturn0search7

### C) Cloud API
- If you’d rather call a hosted endpoint, set `LLM_BACKEND=openai` and `LLM_MODEL=gpt-oss-20b` (or use a compatible provider like OpenRouter/Fireworks). citeturn0search4turn0search2

## 2) Postgres setup
Use Neon/Supabase/local as before; load `schema.sql` to seed sample data.

## 3) Environment
Create `.env` with:
```
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname
# LLM selection
LLM_BACKEND=transformers   # or 'openai' or 'ollama'
LLM_MODEL=openai/gpt-oss-20b
# If BACKEND=openai, also set:
OPENAI_API_KEY=sk-...
```

## 4) Run
```
streamlit run app_streamlit.py
```

## 5) Tips
- **GPU recommended** for local inference. CPU will work but be slower. Some users report >10 tok/s with optimized builds; quantized variants are available through community repos and Ollama. citeturn0search13
- On Windows, ensure the correct **PyTorch** build for your CUDA/DirectML.
- If you see throughput issues, try a quantized checkpoint or use Ollama’s prebuilt MXFP4 quant. citeturn0search7

## 6) References
- OpenAI gpt‑oss announcement/model card & docs. citeturn0search3turn0search12turn0search4
- Hugging Face gpt‑oss overview. citeturn0search8
- OpenRouter model page. citeturn0search2
