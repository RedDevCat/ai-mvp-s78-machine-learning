import os
import ast

SUSPICIOUS_KEYWORDS = [
    "eval(", "exec(", "subprocess", "os.system", "popen", "socket",
    "requests.post", "ftplib", "paramiko", "open("
]

def analyze_code(path, content=None):
    ext = os.path.splitext(path)[1].lower()
    res = {"language": None, "suspicious": [], "ast_hits": []}

    if ext == ".py":
        res["language"] = "python"
        source = content if content else open(path, "r", errors="ignore").read()
        for kw in SUSPICIOUS_KEYWORDS:
            if kw in source:
                res["suspicious"].append({"type": "keyword", "kw": kw, "count": source.count(kw)})
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    try:
                        name = ast.unparse(node.func)
                    except:
                        name = getattr(node.func, 'id', str(node.func))
                    if any(k.strip("()") in name for k in ["eval", "exec", "system", "Popen", "call"]):
                        res["ast_hits"].append({"lineno": getattr(node, 'lineno', None), "func": name})
        except Exception:
            pass
    else:
        res["language"] = "other"
        src = content if content else open(path, "r", errors="ignore").read()
        for kw in SUSPICIOUS_KEYWORDS:
            if kw in src:
                res["suspicious"].append({"type": "keyword", "kw": kw, "count": src.count(kw)})
    return res
