import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def train_sequence_model(csv_path="../data/log_sequences.csv", model_path="../models/log_sequence_model.pkl"):
    # Load dataset
    df = pd.read_csv(csv_path)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        df["log_text"], df["label"], test_size=0.2, random_state=42
    )

    # Pipeline: TF-IDF + Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("\n📊 Sequence-Level Classification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(pipeline, model_path)
    print(f"\n✅ Model saved to: {model_path}")

if __name__ == "__main__":
    train_sequence_model()
