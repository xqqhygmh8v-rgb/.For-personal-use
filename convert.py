import json
import requests
import os

# 定义规则源 (Surge 格式的原始链接)
RULES = {
    "Apple.arrs": "🔗 view-link.cx/sefRZ7XqTJS",
    "AI.arrs": "🔗 view-link.cx/8nocHbCBMUX"
}

# 输出文件夹，对应你在 Anywhere 里想要订阅的路径
OUTPUT_DIR = "rules/common"

def convert_surge_to_arrs(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
    except Exception as e:
        print(f"获取规则失败 ({url}): {e}")
        return

    arrs_rules = []
    
    # Anywhere 所需的数字映射 (0: IP-CIDR, 1: IP-CIDR6, 2: DOMAIN-SUFFIX, 3: DOMAIN-KEYWORD)
    type_mapping = {
        "IP-CIDR": 0,
        "IP-CIDR6": 1,
        "DOMAIN-SUFFIX": 2,
        "DOMAIN-KEYWORD": 3,
        "DOMAIN": 2  # 兼容普通 DOMAIN 映射为 DOMAIN-SUFFIX
    }

    for line in lines:
        line = line.strip()
        
        # 过滤掉注释和空行
        if not line or line.startswith(("#", "//", ";")):
            continue
        
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            rule_type = parts[0].upper()
            pattern = parts[1]
            
            # 策略：有指定就转小写，没有就默认 proxy
            policy = parts[2].lower() if len(parts) >= 3 else "proxy"

            if rule_type in type_mapping:
                arrs_rules.append({
                    "type": type_mapping[rule_type],
                    "pattern": pattern,
                    "policy": policy
                })

    # 确保文件夹存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_output_path = os.path.join(OUTPUT_DIR, output_path)

    with open(full_output_path, "w", encoding="utf-8") as f:
        json.dump(arrs_rules, f, indent=2, ensure_ascii=False)
    print(f"成功转换 {len(arrs_rules)} 条规则并保存至 {full_output_path}")

if __name__ == "__main__":
    for filename, url in RULES.items():
        convert_surge_to_arrs(url, filename)