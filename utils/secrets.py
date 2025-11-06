import re

REGEXES = {
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "aws_secret": r"(?i)aws(.{0,20})?(secret|key).{0,60}[A-Za-z0-9/+=]{16,}",
    "pem_private_key": r"-----BEGIN (RSA )?PRIVATE KEY-----[\s\S]+?-----END (RSA )?PRIVATE KEY-----",
    "jwt_like": r"[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"(?:(?:\+?\d{1,3})?[-. ]?)?(?:\d{10,12})"
}

def find_secrets(text):
    hits = []
    for name, rx in REGEXES.items():
        for m in re.finditer(rx, text):
            snippet = text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
            hits.append({"type": name, "match": m.group(0)[:200], "snippet": snippet})
    return hits
