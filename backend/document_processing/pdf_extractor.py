
import pymupdf

from backend.document_processing.ocr_extractor import (
    extract_text_using_ocr
)


def extract_text_from_pdf(pdf_path):

    try:
        with open(pdf_path, "rb") as file:
            pdf_bytes = file.read()

        return extract_text_from_pdf_bytes(pdf_bytes)

    except Exception as error:
        print("PDF Extraction Error:", error)
        return None


def extract_text_from_pdf_bytes(pdf_bytes):

    try:
        # First, try normal PDF text extraction
        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        ) as document:

            extracted_text = ""

            for page in document:
                extracted_text += page.get_text() + "\n"

        # If text exists, return it
        if extracted_text.strip():
            print("Text extracted using PyMuPDF.")
            return extracted_text.strip()

        # Otherwise, use OCR
        print("No selectable text found. Starting OCR...")

        return extract_text_using_ocr(pdf_bytes)

    except Exception as error:

        print("PDF text extraction failed:", error)
        print("Trying OCR extraction...")

        return extract_text_using_ocr(pdf_bytes)


if __name__ == "__main__":

    text = extract_text_from_pdf("sample.pdf")

    if text:
        print("\nEXTRACTED PDF TEXT")
        print("------------------")
        print(text)
    else:
        print("No text could be extracted.")
