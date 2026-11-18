
import pymupdf
import pytesseract
from PIL import Image
import io


# Set the Tesseract installation location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_using_ocr(pdf_bytes):

    extracted_text = ""

    try:
        # Open uploaded PDF from memory
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        # Process every page
        for page_number, page in enumerate(document):

            # Convert PDF page into an image
            pix = page.get_pixmap(
    dpi=120,
    colorspace=pymupdf.csGRAY
)

            image_bytes = pix.tobytes("jpeg", jpg_quality=65)

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            # Extract text using Tesseract
            page_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            extracted_text += page_text + "\n"

        document.close()

        return extracted_text.strip()

    except Exception as error:

        print("OCR Extraction Error:", error)

        return None


if __name__ == "__main__":

    print("OCR module loaded successfully.")
    print("Tesseract OCR is configured.")
