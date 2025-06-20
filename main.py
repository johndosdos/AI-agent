import os
from dotenv import load_dotenv
from google import genai

# Load environment variables.
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


# Create Google genai client.
client = genai.Client(api_key=api_key)

# Generate a response from Goolge genai.
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
)

print(response.text)
