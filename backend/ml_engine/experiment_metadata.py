
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from backend.preprocessing.load_dataset import load_job_data


def experiment_metadata():

    df = load_job_data()

    text_columns = [
        "title", "description", "company_profile", "requirements",
        "benefits", "employment_type", "required_experience",
        "required_education", "industry", "function"
    ]

    df["combined_text"] = (
        df[text_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    metadata_columns = [
        "telecommuting",
        "has_company_logo",
        "has_questions"
    ]

    df[metadata_columns] = (
        df[metadata_columns]
        .fillna("Unknown")
        .astype(str)
    )

    X = df[["combined_text"] + metadata_columns]
    y = df["fraudulent"].astype(int)

    # First separate the final test dataset (20%)
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Split remaining data into training (60%) and validation (20%)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val,
        test_size=0.25,
        random_state=42,
        stratify=y_train_val
    )

    preprocessor = ColumnTransformer([
        (
            "text",
            TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                max_features=100000,
                min_df=2,
                sublinear_tf=True
            ),
            "combined_text"
        ),
        (
            "metadata",
            OneHotEncoder(handle_unknown="ignore"),
            metadata_columns
        )
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                class_weight="balanced",
                max_iter=1000
            )
        )
    ])

    model.fit(X_train, y_train)

    # Get fraud probabilities on validation data
    fraud_index = list(model.classes_).index(1)
    probabilities = model.predict_proba(X_val)[:, fraud_index]

    print("\n===== THRESHOLD TUNING RESULTS =====")
    print("Threshold | Precision | Recall | F1-score | FP | FN")

    for threshold in [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]:

        predictions = (probabilities >= threshold).astype(int)

        precision = precision_score(
            y_val, predictions, zero_division=0
        )
        recall = recall_score(
            y_val, predictions, zero_division=0
        )
        f1 = f1_score(
            y_val, predictions, zero_division=0
        )

        tn, fp, fn, tp = confusion_matrix(
            y_val, predictions, labels=[0, 1]
        ).ravel()

        print(
            f"{threshold:.2f}      | "
            f"{precision:.3f}     | "
            f"{recall:.3f}  | "
            f"{f1:.3f}   | "
            f"{fp} | {fn}"
        )


if __name__ == "__main__":
    experiment_metadata()
