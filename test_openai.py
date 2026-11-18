
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()

# Create OpenAI client
client = OpenAI()

# Send a simple test request
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Explain job fraud detection in two simple sentences."
)

# Display GPT response
print("OpenAI API Connection Successful!")
print(response.output_text)
