
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from backend.preprocessing.load_dataset import split_data


def train_model():

    X_train, X_test, y_train, y_test = split_data()

    model = Pipeline([
       ("tfidf", TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=100000,
    min_df=2,
    sublinear_tf=True
)),
       ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000))
    ])

    model.fit(X_train, y_train)

    return model, X_test, y_test
