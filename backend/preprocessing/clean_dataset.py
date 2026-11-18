
import pandas as pd
from pathlib import Path
import re
import html

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATASET_PATH = PROJECT_ROOT / "datasets" / "dataset.csv"

CLEANED_DATASET_PATH = PROJECT_ROOT / "datasets" / "cleaned_job_posts.csv"


def load_raw_dataset():
    df = pd.read_csv(RAW_DATASET_PATH)

    print("Original dataset loaded successfully!")
    print("Total records:", len(df))

    return df


def remove_duplicates(df):
    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print("Duplicate records removed:", before - after)

    return df


def remove_empty_descriptions(df):
    before = len(df)

    df = df.dropna(subset=["description"])
    df = df[df["description"].str.strip() != ""]

    after = len(df)

    print("Empty descriptions removed:", before - after)

    return df


def clean_html_text(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    if text.lower() in ["n/a", "na", "none", "null"]:
        return ""

    return text

def convert_labels(df):
    df["fraudulent"] = df["fraudulent"].map({
        "f": 0,
        "t": 1
    })

    return df


def remove_conflicting_labels(df):
    label_counts = df.groupby("description")["fraudulent"].nunique()

    conflicting_descriptions = label_counts[
        label_counts > 1
    ].index

    before = len(df)

    df = df[
        ~df["description"].isin(conflicting_descriptions)
    ]

    print("Conflicting records removed:", before - len(df))

    return df

def prepare_clean_dataset():
    df = load_raw_dataset()

    df = remove_duplicates(df)

    df = remove_empty_descriptions(df)

    df["description"] = df["description"].apply(clean_html_text)


    df = df.dropna(subset=["description"])
    df = df[df["description"].str.strip() != ""]

    df = convert_labels(df)

    df = remove_conflicting_labels(df)

    df.to_csv(CLEANED_DATASET_PATH, index=False)

    print("\nCleaned dataset saved successfully!")
    print("Final records:", len(df))
    print("Fraud distribution:")
    print(df["fraudulent"].value_counts())


if __name__ == "__main__":
    prepare_clean_dataset()
    