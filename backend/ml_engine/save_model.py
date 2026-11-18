
from pathlib import Path
import joblib

from backend.ml_engine.train_model import train_model


# Find project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define where the trained model will be saved
MODEL_PATH = PROJECT_ROOT / "trained_models" / "hire_shield_model.joblib"


def save_model():

    # Step 1: Train the ML model
    model, X_test, y_test = train_model()

    # Step 2: Create trained_models folder if it doesn't exist
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Step 3: Save the complete trained pipeline
    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully!")
    print("Model location:", MODEL_PATH)


if __name__ == "__main__":
    save_model()
