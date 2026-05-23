from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "iris_model.joblib"


def train_and_save_model():
    # 1. Load dataset
    iris = load_iris()

    X = iris.data
    y = iris.target

    # 2. Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 3. Create ML model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    # 4. Train model
    model.fit(X_train, y_train)

    # 5. Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # 6. Save model + metadata
    model_bundle = {
        "model": model,
        "accuracy": accuracy,
        "feature_names": list(iris.feature_names),
        "class_names": list(iris.target_names),
    }

    joblib.dump(model_bundle, MODEL_PATH)

    print("Model trained successfully.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
