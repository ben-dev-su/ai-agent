import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content into a file in a specified directory relative to the working directory, returning a success message the file path and the length of the content we wrote into the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a file, relative to the working directory (default is the working directory itself).",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content we want to write into the file which is specified by the file path.",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

    try:
        valid_path = (
            os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        )
    except ValueError as e:
        return f"Error: {e}"

    if not valid_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(file_path, exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
