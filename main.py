import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    # Load environment variables.
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Extract user argument from input. Must have at least 1 argument present.
    if len(sys.argv) < 2:
        print("Error: Must have at least 1 argument present.")
        sys.exit(1)

    _, user_content = sys.argv

    # Create Google genai client.
    client = genai.Client(api_key=api_key)

    # Generate a response from Goolge genai.
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=user_content,
    )

    print(response.text)

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
