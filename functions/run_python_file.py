import os
import subprocess


def run_python_file(working_directory, file_path, args=None) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

    try:
        valid_path = (
            os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        )
    except ValueError as e:
        return f"Error: {e}"

    if not valid_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    file_ex = file_path.split(".")[-1]
    if file_ex != "py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]

    if args is not None:
        command.extend(args)

    output_string = ""
    try:
        process_complete = subprocess.run(
            args=command,
            cwd=abs_working_dir,
            capture_output=True,
            timeout=30,
            text=True,
        )

        # print(process_complete)

        returncode = process_complete.returncode
        if returncode != 0:
            output_string += f"Process exited with code {returncode}"

        stdout = process_complete.stdout
        stderr = process_complete.stderr

        if not stdout and not stderr:
            output_string += "\nNo output produced"
        else:
            output_string += f"\nSTDOUT: {stdout}\nSTDERR:{stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

    return output_string
