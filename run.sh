#!/bin/bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "from utils.db import init_db; init_db()"
mkdir -p data/uploads data/corpus index models/embeddings_cache datasets/processed
streamlit run app.py