import streamlit as st
from preprocess import load_logs_structured
from pattern_matcher import load_defect_patterns, detect_defects
from classifier import predict_log
from sequence_predictor import predict_sequence
from collections import Counter
from datetime import datetime
import csv
import os

st.set_page_config(page_title="Smart Defect Triage", layout="wide")
st.title("🚀 Smart Defect Triage System")

# ========= Upload Section =========
uploaded_file = st.file_uploader("📂 Upload a log file (.txt)", type=["txt"])

if uploaded_file:
    # Read and preprocess logs
    lines = uploaded_file.read().decode("utf-8").splitlines()
    structured_logs = [log for line in lines if (log := load_logs_structured.__globals__["parse_log_line"](line))]

    # ========= Rule-Based Detection =========
    st.subheader("🔍 Detected Defects (Rule-Based)")
    defect_patterns = load_defect_patterns()
    matched = detect_defects(structured_logs, defect_patterns)

    if matched:
        for d in matched:
            st.success(f"🛑 {d['defect_id']} - {d['description']} (Team: {d['team']})")
    else:
        st.info("No known defect patterns matched.")

    # ========= ML-Based Line Predictions =========
    st.subheader("🧠 ML-Based Predictions (Per Log Line)")
    predictions = []
    for log in structured_logs:
        if "message" in log:
            pred = predict_log(log["message"])
            predictions.append((pred, log["message"]))

    # Summary Table
    st.markdown("### 📊 Defect Prediction Summary")
    pred_count = Counter([p[0] for p in predictions])
    samples = {}
    for label, msg in predictions:
        if label not in samples:
            samples[label] = msg

    summary_data = []
    for label, count in pred_count.items():
        summary_data.append({
            "Predicted Defect": label,
            "Log Count": count,
            "Example Log": samples[label]
        })

    st.table(summary_data)

    # ========= Confirm and Assign UI =========
    st.markdown("### 🧩 Confirm & Assign Predicted Defects")

    def save_confirmation(label, count, sample, team, source_log):
        filepath = "../data/confirmed_defects.csv"
        file_exists = os.path.exists(filepath)
        with open(filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Defect Label", "Log Count", "Sample Message", "Assigned Team", "Timestamp", "Source Log File"])
            writer.writerow([
                label, count, sample, team,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                source_log
            ])

    for entry in summary_data:
        label = entry["Predicted Defect"]
        count = entry["Log Count"]
        sample = entry["Example Log"]

        st.write(f"🧠 **{label}** - {count} log(s)")
        st.code(sample, language="text")

        team = st.selectbox(
            f"Assign a team for {label}",
            options=["CAN Layer Team", "NavCore Team", "Diagnostics Team", "Unknown/Unassigned"],
            key=f"team_{label}"
        )

        if st.button(f"✅ Confirm {label}", key=f"confirm_{label}"):
            save_confirmation(label, count, sample, team, uploaded_file.name)
            st.success(f"{label} confirmed and assigned to **{team}** — saved to CSV ✅")

            summary_text = (
                f"🔍 Detected Defect: {label}\n"
                f"Assigned Team: {team}\n"
                f"Log Count: {count}\n"
                f"Example Log: {sample}\n"
                f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            st.code(summary_text)
            st.text_input("📋 Copy to clipboard:", value=summary_text)

    # ========= AI Prediction: Full Sequence =========
    st.subheader("🔮 Predict Defect from Entire Log File (AI-powered)")

    uploaded_file.seek(0)
    full_text = uploaded_file.read().decode("utf-8")
    predicted_defect = predict_sequence(full_text)

    st.success(f"🚨 Predicted Defect Type (Sequence): **{predicted_defect}**")

    st.code(full_text[:300] + "..." if len(full_text) > 300 else full_text, language="text")

    if st.button("✅ Confirm and Copy JIRA Summary"):
        jira_text = (
            f"🔍 Detected Defect: {predicted_defect}\n"
            f"Assigned By: ML Sequence Classifier\n"
            f"Source File: {uploaded_file.name}\n"
            f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        st.code(jira_text)
        st.text_input("📋 Copy to clipboard:", value=jira_text)

    # ========= Expand Full Line-by-Line Predictions =========
    with st.expander("📜 Full Line-by-Line Predictions"):
        for label, msg in predictions:
            st.write(f"🗒️ `{msg}` → **{label}**")
