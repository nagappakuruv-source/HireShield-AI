
import pymupdf

# Create a PDF containing sample job text
original = pymupdf.open()
page = original.new_page(width=595, height=842)

job_text = """
PYTHON DEVELOPER JOB

Company: Example Company

Job Description:

We are looking for a Python Developer.

Candidates should know Python and SQL.

Pay 2000 rupees as a registration fee
to get a guaranteed job.
"""

page.insert_text(
    (60, 100),
    job_text,
    fontsize=18
)

# Convert the page into an image
pix = page.get_pixmap(
    dpi=120,
    colorspace=pymupdf.csGRAY
)
image_bytes = pix.tobytes("jpeg", jpg_quality=65)

# Create a new PDF containing only the image
scanned_pdf = pymupdf.open()
new_page = scanned_pdf.new_page(width=595, height=842)

new_page.insert_image(
    new_page.rect,
    stream=image_bytes
)

scanned_pdf.save("scanned_sample.pdf")

original.close()
scanned_pdf.close()

print("Scanned-style PDF created successfully!")
