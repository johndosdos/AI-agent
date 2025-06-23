import os


def get_files_info(working_directory, directory=None):
    root_path = os.path.abspath(working_directory)
    requested_path = directory

    if directory:
        requested_path = os.path.abspath(os.path.join(root_path, directory))
        # If requested path is outside the working directory, return error
        if not requested_path.startswith(root_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(requested_path):
            return f'Error: "{directory}" is not a directory'
    else:
        requested_path = root_path

    item_list = ""

    for item in os.listdir(requested_path):
        file_size = os.path.getsize(os.path.join(requested_path, item))
        is_dir = os.path.isdir(os.path.join(requested_path, item))

        item_list += f"{item}: file_size={file_size}, is_dir={is_dir}"

    return item_list
