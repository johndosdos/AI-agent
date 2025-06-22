import subprocess
import os


def run_python_file(working_directory, file_path):
    root_path = os.path.abspath(working_directory)
    requested_path = os.path.abspath(os.path.join(root_path, file_path))

    if not requested_path.startswith(root_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(requested_path):
        return f'Error: File "{file_path}" not found.'

    if not requested_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", requested_path],
            timeout=30,
            capture_output=True,
            cwd=root_path,
            text=True,
            check=True,
        )

        output = result.stdout
        err = result.stderr
        code = result.check_returncode

        if result.returncode != 0:
            final_output = f"Process exited with code {code}\n"
        if not output:
            final_output = "No output produced."

        final_output = f"STDOUT: {output}\nSTDERR: {err}"

        output_format = f"start...\n{final_output}\n...end"

        return output_format
    except Exception as e:
        return f"Error: executing Python file: {e}"
