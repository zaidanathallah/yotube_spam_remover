
import re

def is_judol_comment(comment):
    patterns = [
        r"🚩.*🚩",
        r"([A-Z0-9]\s*){5,}",
        r"(\w+)\1{2,}",
        r"x\s*[0-9]+",
        r"weton|togel|slot|bo"
    ]
    return any(re.search(p, comment, re.IGNORECASE) for p in patterns)
