from sklearn.metrics import classification_report
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from backend.ml_engine.train_model import train_model


def evaluate_model():

    # Step 1: Train the model and get test data
    model, X_test, y_test = train_model()

    # Step 2: Predict results
    predictions = model.predict(X_test)

    # Step 3: Calculate evaluation metrics
    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test, predictions, zero_division=0
    )

    recall = recall_score(
        y_test, predictions, zero_division=0
    )

    f1 = f1_score(
        y_test, predictions, zero_division=0
    )

    # Step 4: Calculate confusion matrix
    cm = confusion_matrix(y_test, predictions)

    # Step 5: Display results
    print("===== HireShield AI Model Evaluation =====")

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)

    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_test, predictions,target_names=["Genuine Job", "Fraudulent Job"],
        zero_division=0))

    # Step 6: Display individual outcomes
    tn, fp, fn, tp = cm.ravel()

    print("\n===== Confusion Matrix Results =====")
    print("True Negative (TN):", tn)
    print("False Positive (FP):", fp)
    print("False Negative (FN):", fn)
    print("True Positive (TP):", tp)


if __name__ == "__main__":
    evaluate_model()
