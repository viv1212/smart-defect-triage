import re

def parse_log_line(line):
    """
    Parses a log line into a structured dictionary.
    Format expected:
    1970-01-01 00:00:01.123 [ECU1] [NAV] [ERROR] message content...
    """
    pattern = r'^([\d\-:.\s]+) \[(.*?)\] \[(.*?)\] \[(.*?)\] (.*)$'
    match = re.match(pattern, line)
    if match:
        return {
            "timestamp": match.group(1).strip(),
            "ecu": match.group(2).strip(),
            "context": match.group(3).strip(),
            "severity": match.group(4).strip(),
            "message": match.group(5).strip()
        }
    else:
        return {
            "raw": line.strip()
        }

def load_logs_structured(file_path):
    """
    Loads and parses logs into a list of structured dicts.
    """
    structured_logs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            cleaned = line.strip()
            if cleaned:
                parsed = parse_log_line(cleaned)
                structured_logs.append(parsed)
    return structured_logs


if __name__ == "__main__":
    import os
    import json

    sample_dir = "../data/sample_logs"
    for filename in os.listdir(sample_dir):
        if filename.endswith(".txt"):
            print(f"\n🗂️  Reading: {filename}")
            logs = load_logs_structured(os.path.join(sample_dir, filename))
            print(f"🔹 Parsed {len(logs)} lines")
            print("🔸 First structured log:")
            print(json.dumps(logs[0], indent=2))
