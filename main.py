import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.call_functions import call_function


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

    # System prompt for Gemini.
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Keep it concise. Use simple words.

Solve this problem in the most practical way, not the most efficient or clever. Prioritize simplicity, clarity, and ease of maintenance. Write code as if another developer will need to read and update it in six months. Avoid over-engineering or unnecessary optimization—just make it work well and be easy to understand. Add brief comments if needed to explain your approach.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    # Enable chat conversation history between user and Gemini.
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_content)])
    ]

    # Declare functions for the LLM to use.
    # get_files_info
    schema_get_files_info = genai.types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "directory": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    # get_file_content
    schema_get_file_content = genai.types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieve the contents of the specified file.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The path to the file, relative to the working directory.",
                ),
            },
        ),
    )

    # run_python_file
    schema_run_python_file = genai.types.FunctionDeclaration(
        name="run_python_file",
        description="Execute the specified python file.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The path to the file, relative to the working directory.",
                ),
            },
        ),
    )

    # write_file
    schema_write_file = genai.types.FunctionDeclaration(
        name="write_file",
        description="Write contents to the specified python file.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The path to the file, relative to the working directory.",
                ),
                "content": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The contents to be written to the specified file.",
                ),
            },
        ),
    )

    available_functions = genai.types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    config = genai.types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    # Generate a response from Goolge genai.
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config,
    )

    # Process response. Make a loop to simulate a conversation.
    for i in range(0, 19):
        # Generate a response from Goolge genai.
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config,
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        calls = response.function_calls
        if calls:
            for call in calls:
                call_response = call_function(call)
                content_response = call_response.parts[0].function_response.response

                messages.append(call_response)

                if verbose == True:
                    print(f"-> {content_response}")
        else:
            print(f"\n{response.text}")
            break

    if verbose:
        print(f"\n-> {response.text}")
        print(f"-> User prompt: {user_content}")
        print(f"-> Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"-> Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
