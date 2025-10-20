import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot get contents of "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a valid file'
    if file_path.endswith('.py'):
        try:
            result = subprocess.run(['python', abs_file_path] + args, capture_output=True, text=True, timeout=30, cwd=abs_working_dir)
            if result.returncode != 0:
                print(result.returncode)
                return f'Error executing file "{file_path}": {result.stderr}'
            return result.stdout + f'Process executed with return code {result.returncode}'
        except Exception as e:
            return f'Error executing file "{file_path}": {str(e)}'
    else:
        return f'Error: "{file_path}" is not a Python file'
       
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts additional CLI args as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)