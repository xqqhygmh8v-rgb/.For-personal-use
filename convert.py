import json
import requests
import os

RULES = {
    "Apple.arrs": "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Surge/Apple/Apple.list",
        "AI.arrs": "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Surge/OpenAI/OpenAI.list"
}

OUTPUT_DIR = "rules/common"

def convert_surge_to_arrs(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
    except Exception as e:
        print(f"Failed to fetch rules ({url}): {e}")
        return

    arrs_rules = []
    
    type_mapping = {
        "IP-CIDR": 0,
        "IP-CIDR6": 1,
        "DOMAIN-SUFFIX": 2,
        "DOMAIN-KEYWORD": 3,
        "DOMAIN": 2
    }

    for line in lines:
        line = line.strip()
        if not line or line.startswith(("#", "//", ";")):
            continue
        
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            rule_type = parts[0].upper()
            pattern = parts[1]
            policy = parts[2].lower() if len(parts) >= 3 else "proxy"

            if rule_type in type_mapping:
                arrs_rules.append({
                    "type": type_mapping[rule_type],
                    "pattern": pattern,
                    "policy": policy
                })

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_output_path = os.path.join(OUTPUT_DIR, output_path)

    with open(full_output_path, "w", encoding="utf-8") as f:
        json.dump(arrs_rules, f, indent=2, ensure_ascii=False)
    print(f"Successfully converted {len(arrs_rules)} rules to {full_output_path}")

if name == "main":
    for filename, url in RULES.items():
        convert_surge_to_arrs(url, filename)
