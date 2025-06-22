import os


def get_file_content(working_directory, file_path):
    root_path = os.path.abspath(working_directory)
    requested_path = os.path.abspath(os.path.join(root_path, file_path))

    # If requested path is outside the working directory, return error.
    if not requested_path.startswith(root_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if file_path is a file or not.
    if not os.path.isfile(requested_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Open file for reading. We need to limit reading to 10 000 chars.
    MAX_CHAR_READ = 10000

    with open(requested_path, "r") as file:
        file_contents = file.read(MAX_CHAR_READ)

        if len(file_contents) >= MAX_CHAR_READ:
            file_contents = (
                f'{file_contents}...File "{file_path}" truncated at 10000 characters'
            )

    return file_contents
