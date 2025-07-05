import joblib

# Load the trained sequence-level model once
_model = joblib.load("../models/log_sequence_model.pkl")

def predict_sequence(log_text: str) -> str:
    return _model.predict([log_text])[0]
