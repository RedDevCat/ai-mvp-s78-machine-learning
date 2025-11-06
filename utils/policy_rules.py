import re

POLICY_RULES = {
    "forbidden_license": [r"GPL", r"Proprietary License", r"Unlicensed"],
    "forbidden_keywords": [r"rootkit", r"backdoor", r"cryptominer"],
    "sensitive_topics": [r"sexual", r"extremist", r"drug"]
}

def check_policy_rules(text):
    hits = []
    for tag, patterns in POLICY_RULES.items():
        for pattern in patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                snippet = text[max(m.start() - 30, 0) : m.end() + 30]
                hits.append({"tag": tag, "match": m.group(), "snippet": snippet})
    return hits
