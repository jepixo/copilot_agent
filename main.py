import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

def main():
    load_dotenv()
    if len(sys.argv) <2:
        print("I need a prompt mate!")
        sys.exit(1)
        return 
    verbose_flag= False
    if len(sys.argv) >2 and sys.argv[2]=='--verbose':
        verbose_flag=True
    prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read the contents of a file
    - Write to a file (create or update)
    - Run a python file with optional CLI args
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    client = genai.Client(api_key=api_key)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_write_file,
            schema_run_python_file
        ]
    )
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
    mar_iters=20
    for i in range(mar_iters):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents = messages,
            config=config
            ) 
        if response is None or response.usage_metadata is None:
            print("Uh oh!")
            return
        if verbose_flag:
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Prompt tokens: {response.usage_metadata.candidates_token_count}')
        
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for fc in response.function_calls:
                result = call_function(fc, verbose=verbose_flag)
                messages.append(result),
                
        else:
            print(response.text)
            return

    
    

main()
# print(get_files_info("calculator"))