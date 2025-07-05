import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def train_model(csv_path="../data/labeled_logs.csv", save_path="../models/log_classifier.pkl"):
    df = pd.read_csv(csv_path)

    # Split data
    X = df["log"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(solver='liblinear'))
    ])

    # Train model
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("\n📊 Classification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(pipeline, save_path)
    print(f"\n✅ Model saved to: {save_path}")

def predict_log(message, model_path="../models/log_classifier.pkl"):
    pipeline = joblib.load(model_path)
    return pipeline.predict([message])[0]
if __name__ == "__main__":
    train_model()

    # Try prediction
    test_msg = "[ERROR] Bus load > 90% on CAN1"
    predicted = predict_log(test_msg)
    print(f"\n🔮 Predicted Label for: '{test_msg}' → {predicted}")
