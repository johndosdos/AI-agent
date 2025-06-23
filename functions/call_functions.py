from functions import get_file_content, get_files_info, run_python, write_file
from google import genai


def call_function(function_call_part, verbose=False):
    func = function_call_part.name
    args = function_call_part.args

    if verbose == True:
        print(f"-> Calling function: {func}({args})")

    print(f"-> Calling function: {func}")

    function_dict = {
        "get_files_info": get_files_info.get_files_info,
        "get_file_content": get_file_content.get_file_content,
        "run_python_file": run_python.run_python_file,
        "write_file": write_file.write_file,
    }

    func_to_call = function_dict.get(func)

    if not func_to_call:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=func,
                    response={"error": f"Unknown function: {func}"},
                )
            ],
        )

    args["working_directory"] = "./calculator"

    result = func_to_call(**args)

    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=func,
                response={"result": result},
            )
        ],
    )
