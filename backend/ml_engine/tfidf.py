from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

def convert_text_to_vectors(text_data):
    tfidf_matrix = vectorizer.fit_transform(text_data)
    return tfidf_matrix
def transform_new_text(text_data):
    tfidf_matrix = vectorizer.transform(text_data)
    return tfidf_matrix