import os
import pandas as pd
from utils.extractor import extract_text_from_file
from utils.secrets import find_secrets
from utils.code_checks import analyze_code
from utils.features import extract_features
from utils.policy_rules import check_policy_rules

def preprocess_dataset(raw_path, label_func, out_csv):
    """
    Scan files in raw_path folder, extract features and label them with label_func.
    Save processed CSV to out_csv.
    """
    records = []
    for fname in os.listdir(raw_path):
        fpath = os.path.join(raw_path, fname)
        text = extract_text_from_file(fpath)
        secrets = find_secrets(text)
        code_info = analyze_code(fpath, text)
        policy_flags = check_policy_rules(text)

        # Dummy neighbors zero for training, or you can build needed index
        neighbors = {"scores": [0.0]}
        features = extract_features(text, secrets, code_info, neighbors)
        features["num_policy_flags"] = len(policy_flags)
        features["label"] = label_func(text, fpath)
        records.append(features)

    df_out = pd.DataFrame(records)
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df_out.to_csv(out_csv, index=False)
    print(f"Saved preprocessed dataset to {out_csv}")
