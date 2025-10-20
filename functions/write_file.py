import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot get contents of "{file_path}" as it is outside the permitted working directory'
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f'Error creating directories for "{parent_dir}": {str(e)}'
        
    try:
        with open(abs_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to file "{file_path}"'
    except Exception as e:
        return f'Error writing to file "{file_path}": {str(e)}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if it doesn't exist (and creates required parent dirs safely), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to a file as a string.",
            ),
        },
    ),
)