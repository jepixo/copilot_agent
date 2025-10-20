import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(abs_working_dir, directory))
    if not abs_directory.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    contents = os.listdir(abs_directory)
    finalResponse = ''
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        finalResponse += f'{content}: {size} bytes. isDir = {is_dir}\n'
        # if is_dir:
    return finalResponse
        # else:
        #     yield {
        #         "type": "file",
        #         "name": content,
        #         "path": os.path.relpath(content_path, abs_working_dir),
        #         "size": os.path.getsize(content_path),
        # }

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)