
from backend.ml_engine.load_model import load_model


def predict_job(job_description):

    # Step 1: Load the saved model
    model = load_model()

    # Step 2: Predict the job category
    prediction = model.predict([job_description])[0]

    # Step 3: Get prediction probabilities
    probabilities = model.predict_proba([job_description])[0]

    genuine_probability = probabilities[0] * 100
    fraud_probability = probabilities[1] * 100

    # Step 4: Display the result
    if prediction == 1:
        result = "Fraudulent Job"
    else:
        result = "Genuine Job"

    print("Job Description:", job_description)
    print("Prediction:", result)
    print(f"Genuine Probability: {genuine_probability:.2f}%")
    print(f"Fraud Probability: {fraud_probability:.2f}%")

    return prediction


if __name__ == "__main__":

  sample_job = " ".join([
    "Software Engineer",
    "Urgent hiring! We offer guaranteed placement for all candidates.",
    "",
    "No interview required. Candidates must pay Rs. 2000 registration fee to confirm their job.",
    "",
    "",
    "",
    "",
    ""
])
predict_job(sample_job)
