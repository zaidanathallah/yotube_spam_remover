import re

def is_judol_comment(comment):
    patterns = [
        r"🚩.*🚩",                      # Emoji bendera
        r"([A-Z0-9]\s*){5,}",          # Huruf kapital berlebihan
        r"(\w+)\1{2,}",                # Kata berulang
        r"x\s*[0-9]+",                 # Format x 500
        r"weton|togel|slot|bo"        # Kata kunci spam
    ]
    return any(re.search(p, comment, re.IGNORECASE) for p in patterns)
