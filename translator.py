"""
অনুবাদ ইঞ্জিন — NLLB + mBART + RAG সংশোধন।
Flask অ্যাপ এটা import করে ব্যবহার করবে।
"""
import os
import torch
import openpyxl
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util

BASE = r"C:\Users\SAMSUNG GALAXY\Desktop\dialect_project"
MAX_LEN = 64
RAG_THRESHOLD = 0.85  # এর বেশি মিল হলে RAG সংশোধন করবে

DIALECTS = ["sylheti", "chittagonian", "mymensingh", "noakhali"]

# ---- গ্লোবাল (একবার লোড হবে) ----
_nllb_tok = _nllb_model = None
_mbart_tok = _mbart_model = None
_embedder = None
_pairs = None
_std_emb = _dl_emb = None


def load_all():
    """সব মডেল + RAG index একবার লোড করে।"""
    global _nllb_tok, _nllb_model, _mbart_tok, _mbart_model
    global _embedder, _pairs, _std_emb, _dl_emb

    print("NLLB লোড হচ্ছে...")
    p = os.path.join(BASE, "mate_2models (1)", "model_nllb200")
    _nllb_tok = AutoTokenizer.from_pretrained(p)
    _nllb_model = AutoModelForSeq2SeqLM.from_pretrained(p).eval()

    print("mBART লোড হচ্ছে...")
    p = os.path.join(BASE, "shobuz_3models", "model_mbart50")
    _mbart_tok = AutoTokenizer.from_pretrained(p)
    _mbart_model = AutoModelForSeq2SeqLM.from_pretrained(p).eval()

    print("RAG index বানাচ্ছি...")
    wb = openpyxl.load_workbook(os.path.join(BASE, "shobuz_cse445.xlsx"), read_only=True)
    ws = wb["Dialect_Dataset"]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(h).strip() for h in rows[0]]
    col = {n: i for i, n in enumerate(header)}
    _pairs = []
    for r in rows[1:]:
        if r is None or len(r) < 3:
            continue
        sb = str(r[col.get("Standard_Bangla", 1)] or "").strip()
        dl = str(r[col.get("Local_Dialect", 2)] or "").strip()
        if sb and dl:
            _pairs.append({"standard": sb, "dialect": dl})

    _embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    _std_emb = _embedder.encode([x["standard"] for x in _pairs], convert_to_tensor=True)
    _dl_emb = _embedder.encode([x["dialect"] for x in _pairs], convert_to_tensor=True)
    print("✅ সব রেডি!")


def translate(text, direction="dialect", dialect="sylheti", model_choice="nllb"):
    """
    মূল অনুবাদ ফাংশন — মডেল + RAG সংশোধন।
    direction: 'dialect' (std->dialect) বা 'standard' (dialect->std)
    """
    if direction == "dialect":
        inp = f"<{dialect}> translate to dialect: {text}"
    else:
        inp = f"<{dialect}> translate to standard: {text}"

    if model_choice == "nllb":
        tok, model = _nllb_tok, _nllb_model
    else:
        tok, model = _mbart_tok, _mbart_model

    ids = tok(inp, return_tensors="pt", truncation=True, max_length=MAX_LEN)
    with torch.no_grad():
        out = model.generate(**ids, max_length=MAX_LEN, num_beams=4)
    model_out = tok.decode(out[0], skip_special_tokens=True)

    # RAG সংশোধন
    q = _embedder.encode(text, convert_to_tensor=True)
    emb = _std_emb if direction == "dialect" else _dl_emb
    hits = util.cos_sim(q, emb)[0]
    idx = int(hits.argmax())
    score = float(hits[idx])
    ref = _pairs[idx]["dialect"] if direction == "dialect" else _pairs[idx]["standard"]
    used_rag = score >= RAG_THRESHOLD
    final = ref if used_rag else model_out

    return {
        "model_output": model_out,
        "final": final,
        "rag_used": used_rag,
        "score": round(score, 3),
    }