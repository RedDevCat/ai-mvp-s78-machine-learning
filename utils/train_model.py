import pandas as pd
import lightgbm as lgb
import os

def train(csv_path, out_model="models/risk_model.txt"):
    df = pd.read_csv(csv_path)
    features = ["len_chars", "num_lines", "num_secrets", "num_suspicious_keywords", "plagiar_top", "num_policy_flags"]
    X = df[features].fillna(0)
    y = df["label"]
    train_data = lgb.Dataset(X, y)
    params = {"objective": "regression", "metric": "rmse", "verbosity": -1}
    model = lgb.train(params, train_data, num_boost_round=200)
    os.makedirs(os.path.dirname(out_model), exist_ok=True)
    model.save_model(out_model)
    print("Saved model to", out_model)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python train_model.py path_to_dataset.csv")
    else:
        train(sys.argv[1])
