import lightgbm as lgb
import numpy as np
import os

class RiskModel:
    def __init__(self, model_path="models/risk_model.txt"):
        self.model = None
        if os.path.exists(model_path):
            self.model = lgb.Booster(model_file=model_path)

    def predict(self, features: dict):
        if self.model is None:
            score = 0.0
            score += min(1.0, features.get("num_secrets", 0) * 0.4)
            score += min(1.0, features.get("num_suspicious_keywords", 0) * 0.2)
            score += (features.get("plagiar_top", 0.0) * 0.5)
            score = max(0.0, min(1.0, score))
            return score
        fvec = [
            features.get("len_chars", 0),
            features.get("num_lines", 0),
            features.get("num_secrets", 0),
            features.get("num_suspicious_keywords", 0),
            features.get("plagiar_top", 0.0),
            features.get("num_policy_flags", 0)  # Included policy feature
        ]
        arr = np.array([fvec])
        return float(self.model.predict(arr)[0])
