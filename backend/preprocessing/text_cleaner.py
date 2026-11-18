import re

def clean_text(text):
    if not text:
        return ""
    

    cleaned_text = text.lower()
    cleaned_text = " ".join(cleaned_text.split())
    cleaned_text = re.sub(r"!{2,}", "!", cleaned_text)

    return cleaned_text
def tokenize_text(text):
    cleaned_text = clean_text(text)
    tokens = cleaned_text.split()
    return tokens