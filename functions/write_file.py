import os


def write_file(working_directory, file_path, content):
    root_path = os.path.abspath(working_directory)
    requested_path = os.path.abspath(os.path.join(root_path, file_path))

    if not requested_path.startswith(root_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # If the file_path does not exist, create it. But we also need to overwrite
    # the contents of the file so, we'll just create a new file everytime.
    with open(requested_path, "w") as file:
        file.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
