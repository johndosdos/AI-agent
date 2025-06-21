import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    # Load environment variables.
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Extract user argument from input. Must have at least 1 argument present.
    len_user_input = len(sys.argv)

    if len_user_input < 2:
        print("Error: Must have at least 1 argument present.")
        sys.exit(1)

    # Have an optional "--verbose" flag.
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True

    user_content = sys.argv[1]

    # Create Google genai client.
    client = genai.Client(api_key=api_key)

    # Enable chat conversation history between user and Gemini.
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_content)])
    ]

    # Generate a response from Goolge genai.
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose:
        print(response.text)
        print(f"User prompt: {user_content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


main()
