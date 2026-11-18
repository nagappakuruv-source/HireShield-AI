import fitz

# Create a new PDF
doc = fitz.open()

# Add one page
page = doc.new_page()

# Add sample job advertisement text
job_text = """
PYTHON DEVELOPER JOB

Company: Example Company

Job Description:
We are looking for a Python Developer.

Candidates should know Python, SQL,
and basic programming.

Pay 2000 rupees as a registration fee
to get a guaranteed job.
"""

page.insert_text(
    (72, 72),
    job_text,
    fontsize=12
)

# Save the PDF in the project root
doc.save("sample.pdf")
doc.close()

print("Sample PDF created successfully!")