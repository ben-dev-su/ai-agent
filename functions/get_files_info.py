import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)


def get_files_info(working_directory, directory=""):

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    try:
        valid_path = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
    except ValueError as e:
        return f"Error: {e}"

    if not valid_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    entries = os.listdir(target_dir)
    str_builder = ""
    for entry in entries:
        abs_entry = os.path.join(target_dir, entry)
        try:
            entry_size = os.path.getsize(abs_entry)
        except OSError as e:
            return f"Error: {e}"

        is_dir = os.path.isdir(abs_entry)

        str_builder += f"- {entry}: file_size={entry_size} bytes, is_dir={is_dir}\n"

    return str_builder
