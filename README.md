# AI-MVP: Security Risk and Plagiarism Detection using Machine Learning

## Overview

AI-MVP is a Python-based Streamlit web application designed to analyze source code for security vulnerabilities, plagiarism risks, and code quality issues.  
It leverages machine learning models, static code analysis, and code similarity indexing to provide real-time risk assessments of uploaded files.

## Features

- **Static Security Analysis**: Detect known patterns and risky code using rule-based and ML-enhanced heuristics.
- **ML-based Risk Scoring**: Trains a LightGBM model on curated datasets to provide risk scores for uploaded code.
- **Plagiarism Detection**: Embedded code similarity search with FAISS, enabling detection of copied code fragments.
- **Document Parsing**: Supports PDFs, DOCX files along with plain code files.
- **Interactive Web Interface**: Streamlit-powered UI for easy file upload, real-time scanning, model training, and corpus indexing.

## How It Works
```mermaid
flowchart TD
UploadFile[User uploads file] --> Parse[Parse and extract code]
Parse --> Features[Extract Features: syntax, security, secrets, embeddings]
Features --> RiskModel[Run LightGBM Risk Model]
RiskModel --> RiskScore[Output Risk Score and Flags]
Features --> SimilaritySearch[FAISS Embedding Search]
SimilaritySearch --> PlagiarismReport[Find similar code/plagiarism]
RiskScore --> Report[Generate Combined Report]
PlagiarismReport --> Report
Report --> UI[Display report in Streamlit UI]
```


## How To Run

1. Activate Python virtual environment.
2. Preprocess datasets (`utils/train_process.py`) and train risk models (`utils/train_model.py`).
3. Launch the Streamlit app (`streamlit run app.py`).
4. Upload files to scan for risks and plagiarism.

## Explanation for Teachers

This project combines **traditional static code analysis** (syntax and rule-based checks) with **machine learning risk assessment** leveraging LightGBM trained on large labeled security code datasets.  
Plagiarism detection uses **state-of-the-art embedding similarity** techniques with FAISS indexes to identify copied code.  

The modular architecture allows preprocessing of multiple real-world datasets, feature extraction, ML model training, and an interactive web interface for easy usage.  
This work demonstrates practical applications of ML for software security and plagiarism detection in real-world codebases.

## Technologies Used

- Python 3.10
- Streamlit  
- LightGBM, scikit-learn  
- Pandas, NumPy  
- FAISS, sentence-transformers  
- ssdeep for fuzzy hashing  
- python-magic, pypdf, python-docx  

---
