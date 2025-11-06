def extract_features(text, secrets, code_info, neighbors):
    features = {}
    features["len_chars"] = len(text)
    features["num_lines"] = text.count("\n")
    features["num_secrets"] = len(secrets)
    features["num_suspicious_keywords"] = sum(item.get("count", 1) for item in code_info.get("suspicious", []))
    features["plagiar_top"] = max(neighbors.get("scores", [0.0])) if neighbors else 0.0
    return features
