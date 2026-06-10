import json
import requests

这里以 Apple 规则为例，你可以换成任意 Surge 规则链接
SURGE_RULE_URL = "🔗 view-link.cx/wXp9HZw3bCm"
OUTPUT_FILE = "Apple.arrs"

def convert_surge_to_arrs(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
    except Exception as e:
        print(f"获取规则失败: {e}")
        return

    arrs_rules = []
    supported_types = {"DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6"}

    for line in lines:
        line = line.strip()
过滤掉注释和空行
        if not line or line.startswith(("#", "//", ";")):
            continue
        
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            rule_type = parts[0].upper()
            pattern = parts[1]
            policy = parts[2].lower() # 转换为 Anywhere 所需的小写

            if rule_type in supported_types:
                arrs_rules.append({
                    "type": rule_type,
                    "pattern": pattern,
                    "policy": policy
                })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(arrs_rules, f, indent=2, ensure_ascii=False)
    print(f"成功转换 {len(arrs_rules)} 条规则并保存至 {output_path}")

if name == "main":
    convert_surge_to_arrs(SURGE_RULE_URL, OUTPUT_FILE)