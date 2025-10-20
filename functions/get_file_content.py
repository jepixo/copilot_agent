import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot get contents of "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a valid file'
    file_content = ''
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += f'\n\n... (truncated to {MAX_CHARS} characters)'
        return file_content
    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'

schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Gets the content of the given file path as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)