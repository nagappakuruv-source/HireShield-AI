
from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

from backend.preprocessing.load_dataset import split_data_three_way


def train_validate_model():

    # Step 1: Load three datasets
    X_train, X_val, X_test, y_train, y_val, y_test = split_data_three_way()

    # Step 2: Create Logistic Regression pipeline
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=100000,
            min_df=2,
            sublinear_tf=True
        )),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            max_iter=1000
        ))
    ])

    # Step 3: Train using training data only
    print("Training Logistic Regression...")
    model.fit(X_train, y_train)

    print("Model training completed!")

    # Step 4: Get fraud probabilities on validation data
    val_probabilities = model.predict_proba(X_val)[:, 1]

    # Step 5: Compare different thresholds
    for threshold in [0.50, 0.40, 0.35, 0.30, 0.25]:

        val_predictions = (val_probabilities >= threshold).astype(int)

        print(f"\n===== VALIDATION THRESHOLD: {threshold} =====")

        print(classification_report(
            y_val,
            val_predictions,
            target_names=["Genuine", "Fraudulent"]
        ))

        print("Confusion Matrix:")
        print(confusion_matrix(y_val, val_predictions))

    # Step 6: Final evaluation on untouched test data
    test_probabilities = model.predict_proba(X_test)[:, 1]

    selected_threshold = 0.50

    test_predictions = (
        test_probabilities >= selected_threshold
    ).astype(int)

    print("\n===== FINAL TEST SET RESULTS =====")

    print(classification_report(
        y_test,
        test_predictions,
        target_names=["Genuine", "Fraudulent"]
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, test_predictions))

    # Step 7: Save the validated model
    project_root = Path(__file__).resolve().parents[2]

    model_path = (
        project_root / "trained_models" / "hire_shield_model.joblib"
    )

    model_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)

    print("\nValidated model saved successfully!")
    print("Model path:", model_path)

    return model, X_val, y_val, X_test, y_test


if __name__ == "__main__":
    train_validate_model()
