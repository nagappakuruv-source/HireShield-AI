
from backend.document_processing.pdf_extractor import (
    extract_text_from_pdf_bytes
)


def test_pdf(filename):

    print(f"\nTesting: {filename}")
    print("=" * 40)

    with open(filename, "rb") as file:
        pdf_bytes = file.read()

    extracted_text = extract_text_from_pdf_bytes(pdf_bytes)

    if extracted_text:
        print("\nEXTRACTED TEXT:")
        print(extracted_text)
    else:
        print("No text could be extracted.")


# Test 1: Normal PDF
test_pdf("sample.pdf")

# Test 2: Scanned PDF
test_pdf("scanned_sample.pdf")
