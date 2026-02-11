import os

from google.genai import types

READ_LIMIT = 10000


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file in a specified directory relative to the working directory, returning the contents of the file to the caller.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a file, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

    try:
        valid_path = (
            os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        )
    except ValueError as e:
        return f"Error: {e}"

    if not valid_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file) as file:
            content = file.read(READ_LIMIT)

            if file.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated at {READ_LIMIT} characters]'
                )

            return content

    except OSError as e:
        return f"Error: {e}"
