import os
import pandas as pd
from utils.extractor import extract_text_from_file
from utils.secrets import find_secrets
from utils.code_checks import analyze_code
from utils.features import extract_features
from utils.policy_rules import check_policy_rules

def default_label_func(row, src_path):
    """
    Example label function: returns 1.0 if vulnerable, else 0.0.
    Customize this logic based on your dataset columns.
    """
    # You may need to adapt to your actual dataset, for example:
    # return 1.0 if row.get('vulnerability', False) else 0.0
    # Or for plagiarism datasets, use row['is_plagiarized'] or similar
    return 1.0 if 'vuln' in str(row).lower() else 0.0

def preprocess_all_csvs_in_folder(folder_path, label_func=default_label_func, out_csv='datasets/processed/merged.csv'):
    """
    Processes all CSVs in folder_path:
      - Optionally extracts code text, features, policy flags for each row
      - Applies label_func for labeling
      - Outputs single merged processed CSV at out_csv
    """
    dfs_processed = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.csv'):
            fpath = os.path.join(folder_path, filename)
            print(f"Processing {fpath} ...")
            df = pd.read_csv(fpath)
            new_records = []

            # Try to infer code column: most security/plagiarism datasets have 'code', 'source', or similar
            code_columns = [c for c in df.columns if c.lower() in ['code', 'source', 'text', 'snippet', 'function']]
            code_col = code_columns[0] if code_columns else None

            for _, row in df.iterrows():
                if code_col:
                    code = row[code_col]
                else:
                    # fallback: try to reconstruct code from all columns (if needed)
                    code = str(row)
                # Feature extraction pipeline
                secrets = find_secrets(str(code))
                code_info = analyze_code(fpath, str(code))
                policy_flags = check_policy_rules(str(code))
                neighbors = {"scores": [0.0]}  # You can add this to FAISS later if needed

                features = extract_features(str(code), secrets, code_info, neighbors)
                features["num_policy_flags"] = len(policy_flags)
                features["label"] = label_func(row, fpath)
                new_records.append(features)
            dfs_processed.append(pd.DataFrame(new_records))

    if dfs_processed:
        merged_df = pd.concat(dfs_processed, ignore_index=True)
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        merged_df.to_csv(out_csv, index=False)
        print(f"All processed CSVs merged and saved to {out_csv}")
    else:
        print("No CSV files found or processed in folder.")

# Usage:
# python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/devign', out_csv='datasets/processed/devign_train.csv')"
# You can also pass a custom label_func if your dataset schema is different.
