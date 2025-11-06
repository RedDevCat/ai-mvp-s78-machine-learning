import streamlit as st
from utils.extractor import extract_text_from_file
from utils.embeddings import EmbeddingModel
from utils.faiss_index import FaissIndex
from utils.secrets import find_secrets
from utils.code_checks import analyze_code
from utils.features import extract_features
from utils.model_infer import RiskModel
from utils.db import save_report, list_reports, init_db
from utils.policy_rules import check_policy_rules
import os, uuid, json

DATA_DIR = "data/uploads"
CORPUS_DIR = "data/corpus"
INDEX_DIR = "index"
MODEL_PATH = "models/risk_model.txt"

def save_upload(file):
    os.makedirs(DATA_DIR, exist_ok=True)
    uid = str(uuid.uuid4())
    path = os.path.join(DATA_DIR, f"{uid}__{file.name}")
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    return path

@st.cache_resource
def get_embedding_model():
    return EmbeddingModel()

@st.cache_resource
def get_faiss():
    idx = FaissIndex(dim=get_embedding_model().dim)
    idx.load(index_path=os.path.join(INDEX_DIR, "faiss.index")) if os.path.exists(os.path.join(INDEX_DIR, "faiss.index")) else None
    return idx

@st.cache_resource
def get_risk_model():
    return RiskModel(MODEL_PATH)

def run_checks(file_path):
    text = extract_text_from_file(file_path)
    secrets = find_secrets(text)
    code_info = analyze_code(file_path, text)
    policy_flags = check_policy_rules(text)
    emb_model = get_embedding_model()
    q_vec = emb_model.embed(text)
    faiss_idx = get_faiss()
    if faiss_idx.is_ready():
        neighbors = faiss_idx.search(q_vec, k=5)
    else:
        neighbors = {"scores": [], "ids": []}
    try:
        import ssdeep
        from ssdeep import hash as ssdeep_hash
        with open(file_path,"rb") as f:
            b = f.read()
        fuzz = ssdeep_hash(b)
    except Exception:
        fuzz = None
    features = extract_features(text, secrets, code_info, neighbors)
    # Optionally, add policy tag counts as features
    features["num_policy_flags"] = len(policy_flags)
    risk_model = get_risk_model()
    risk_score = risk_model.predict(features)
    tag = "safe" if risk_score < 0.35 else ("moderate" if risk_score < 0.7 else "unsafe")
    report = {
        "file": os.path.basename(file_path),
        "path": file_path,
        "sha256": None,
        "plagiarism": {"neighbors": neighbors, "top_score": float(max(neighbors["scores"]) if neighbors["scores"] else 0.0)},
        "ssdeep": fuzz,
        "secrets": secrets,
        "code": code_info,
        "policy_flags": policy_flags,
        "features": features,
        "risk_score": float(risk_score),
        "risk_tag": tag
    }
    return report

def main():
    st.set_page_config(page_title="AI MVP", layout="wide")
    init_db()
    st.title("AI — Local File Safety & Risk Assessment")

    menu = st.sidebar.selectbox("Menu", ["Upload & Scan", "History", "Index Corpus", "Train Model"])

    emb_model = get_embedding_model()
    faiss_idx = get_faiss()

    if menu == "Upload & Scan":
        uploaded_files = st.file_uploader("Upload files (text/pdf/docx/code)", accept_multiple_files=True)
        if uploaded_files and st.button("Scan files"):
            for f in uploaded_files:
                path = save_upload(f)
                with st.spinner(f"Scanning {f.name}..."):
                    report = run_checks(path)
                    save_report(report)
                    st.success(f"Scanned {f.name} — risk: {report['risk_tag']} ({report['risk_score']:.2f})")
                    st.json(report)

    elif menu == "History":
        st.header("Previous reports")
        reports = list_reports()
        for r in reports:
            with st.expander(f"{r['file']} — {r['risk_tag']} ({r['risk_score']:.2f})"):
                st.write(f"Path: {r['path']}")
                st.write(f"Risk score: {r['risk_score']:.3f}")
                st.write("Plagiarism top score:", r.get("plagiarism",{}).get("top_score"))
                st.write("Secrets found:", len(r.get("secrets",[])))
                st.write("Policy flags:", [pf['tag'] for pf in r.get("policy_flags",[])])
                st.json(r)

    elif menu == "Index Corpus":
        st.header("Index local corpus for plagiarism searches")
        uploaded = st.file_uploader("Add docs to corpus", accept_multiple_files=True, key="corpus_u")
        if uploaded and st.button("Add to corpus"):
            os.makedirs(CORPUS_DIR, exist_ok=True)
            for f in uploaded:
                p = os.path.join(CORPUS_DIR, f.name)
                with open(p,"wb") as fh:
                    fh.write(f.getbuffer())
                st.write("Saved", f.name)
            st.info("Rebuilding FAISS index (may take time)...")
            texts, ids = [], []
            for fn in os.listdir(CORPUS_DIR):
                fp = os.path.join(CORPUS_DIR, fn)
                try:
                    t = open(fp, "rb").read().decode(errors="ignore")
                except Exception:
                    from utils.extractor import extract_text_from_file
                    t = extract_text_from_file(fp)
                v = emb_model.embed(t)
                texts.append(v)
                ids.append(fn)
            import numpy as np
            vecs = np.stack(texts).astype("float32")
            faiss_idx.reset()
            faiss_idx.add(vecs, ids)
            faiss_idx.save(os.path.join(INDEX_DIR, "faiss.index"))
            st.success("Index rebuilt with %d docs." % len(ids))

    elif menu == "Train Model":
        st.header("Train / Retrain Risk Model")
        csv_file = st.file_uploader("Upload labeled CSV dataset", type=["csv"])
        if csv_file and st.button("Train Model"):
            import pandas as pd
            df = pd.read_csv(csv_file)
            from utils.train_model import train
            # Save temp CSV
            tmp_path = "datasets/processed/temp_train.csv"
            df.to_csv(tmp_path, index=False)
            with st.spinner("Training model..."):
                train(tmp_path)
            st.success("Model trained and saved to models/risk_model.txt")


if __name__ == "__main__":
    main()
