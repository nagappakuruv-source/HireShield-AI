
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

from backend.preprocessing.load_dataset import split_data
from backend.ml_engine.load_model import load_model


def compare_models():

    X_train, X_test, y_train, y_test = split_data()

    # Existing Logistic Regression model
    logistic_model = load_model()

    # New Random Forest model
    random_forest = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=100000,
            min_df=2,
            sublinear_tf=True
        )),
        ("classifier", RandomForestClassifier(
            n_estimators=150,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ))
    ])

    print("\nTraining Random Forest...")
    random_forest.fit(X_train, y_train)

    # Predictions
    logistic_predictions = logistic_model.predict(X_test)
    print("\n====missed fraudulent jobs====")
    count=0
    for i in range(len(y_test)):
        if y_test[i] == 1 and logistic_predictions[i] == 0:
            count += 1
            print(f"\nMissed fraudulent job {count}:")
            print(X_test[i][:500])
            if count ==10:
                break



    
    # Random Forest probabilities
    rf_probabilities = random_forest.predict_proba(X_test)[:, 1]
    # Test different thresholds
    for threshold in [0.50, 0.40, 0.30, 0.20]:

        rf_predictions = (rf_probabilities >= threshold).astype(int)

        print(f"\n===== RANDOM FOREST (Threshold: {threshold}) =====")

        print(classification_report(
            y_test,
            rf_predictions,
            target_names=["Genuine", "Fraudulent"]
        ))

       # Logistic Regression probabilities
    lr_probabilities = logistic_model.predict_proba(X_test)[:, 1]

    # Test different Logistic Regression thresholds
    for threshold in [0.50, 0.40, 0.35, 0.30, 0.25]:

        lr_predictions = (lr_probabilities >= threshold).astype(int)

        print(f"\n===== LOGISTIC REGRESSION (Threshold: {threshold}) =====")

        print(classification_report(
            y_test,
            lr_predictions,
            target_names=["Genuine", "Fraudulent"]
        ))

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, lr_predictions))

    # Confusion Matrix Comparison
    rf_predictions = (rf_probabilities >= 0.30).astype(int)

    print("\n===== LOGISTIC REGRESSION CONFUSION MATRIX =====")
  

    print("\n===== RANDOM FOREST (0.30) CONFUSION MATRIX =====")
    print(confusion_matrix(y_test, rf_predictions))


if __name__ == "__main__":
    compare_models()
