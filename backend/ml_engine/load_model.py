
from pathlib import Path
import joblib


# Find project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Saved model location
MODEL_PATH = PROJECT_ROOT / "trained_models" / "hire_shield_model.joblib"


def load_model():

    # Check whether the saved model exists
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Please train and save the model first."
        )

    # Load the saved model
    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully!")

    return model


if __name__ == "__main__":
    load_model()
