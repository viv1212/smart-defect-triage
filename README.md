# Smart Defect Triage System

This project uses machine learning to analyze log files (e.g., DLT logs) and identify known defect patterns, classify log content, and flag anomalies. Useful for teams handling log triage or defect detection.

## Structure

- `data/`: Contains sample log files and defect patterns
- `src/`: Code for preprocessing, pattern matching, classification, and the app
- `models/`: Trained models will be stored here

## Setup

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run src/app.py
```