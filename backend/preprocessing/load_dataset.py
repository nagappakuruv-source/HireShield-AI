
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "datasets" / "cleaned_job_posts.csv"


# Step 1: Load cleaned dataset
def load_job_data():
    df = pd.read_csv(DATASET_PATH)
    return df


# Step 2: Prepare text features and labels
def prepare_data():
    df = load_job_data()

    # Check dataset distribution
    print("\nDataset class distribution:")
    print(df["fraudulent"].value_counts())

    print("\nClass percentages:")
    print(df["fraudulent"].value_counts(normalize=True) * 100)

    text_columns = [
        "title",
        "description",
        "company_profile",
        "requirements",
        "benefits",
        "employment_type",
        "required_experience",
        "required_education",
        "industry",
        "function"
    ]

    X = df[text_columns].fillna("").astype(str).agg(" ".join, axis=1)
    y = df["fraudulent"].astype(int)

    return X.tolist(), y.tolist()
# Step 3: Split data for training and testing
def split_data():
    X, y = prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test

def split_data_three_way():

    X, y = prepare_data()

    # First split: 80% train + validation, 20% test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Second split: 60% train, 20% validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=0.25,
        random_state=42,
        stratify=y_train_val
    )

    return X_train, X_val, X_test, y_train, y_val, y_test
