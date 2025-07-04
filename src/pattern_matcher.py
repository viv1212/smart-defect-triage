import json

def load_defect_patterns(json_path="../data/defects.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_defects(logs, defect_patterns):
    """
    Detects defects in the structured logs.
    - logs: list of log dicts (from preprocess.py)
    - defect_patterns: dict loaded from defects.json
    Returns: list of matched defects
    """
    matched = []

    for defect_id, defect_info in defect_patterns.items():
        pattern = defect_info["pattern"]
        pattern_found = all(
            any(pat.lower() in log["message"].lower() for log in logs if "message" in log)
            for pat in pattern
        )

        if pattern_found:
            matched.append({
                "defect_id": defect_id,
                "description": defect_info["description"],
                "team": defect_info["team"],
                "pattern": pattern
            })

    return matched

if __name__ == "__main__":
    from preprocess import load_logs_structured

    logs = load_logs_structured("../data/sample_logs/log1.txt")
    defects = load_defect_patterns()
    matches = detect_defects(logs, defects)

    print(f"\n🔍 Found {len(matches)} defect(s):")
    for match in matches:
        print(f"➡️  {match['defect_id']}: {match['description']} (Team: {match['team']})")
