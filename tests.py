from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def main():
    working_dir='calculator'
    get_files_info(working_dir)
    root_contents = get_files_info(working_dir)
    pkg_contents = get_files_info(working_dir, 'pkg')
    print("Pkg contents:\n", pkg_contents)
    print("Root contents:\n", root_contents)
    pkg_contents = get_files_info(working_dir, '/bin')
    print("bin contents:\n", pkg_contents)
    pkg_contents = get_files_info(working_dir, '../')
    print("up contents:\n", pkg_contents)
    print(get_file_content(working_dir, 'lorem.txt'))
    print(get_file_content(working_dir, 'main.py'))
    print(get_file_content(working_dir, 'pkg/calculator.py'))
    print(get_file_content(working_dir, 'pkg/tor.py'))
    print(get_file_content(working_dir, '/bin/cat.py'))
    # print(write_file(working_dir, "lorem.txt", "wait, this isn't lorem ipsum"))
    # print(write_file(working_dir, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file(working_dir, "/tmp/temp.txt", "this should not be allowed")) 
    # print(write_file(working_dir, "pkg2/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(run_python_file(working_dir, "main.py"))
    print(run_python_file(working_dir, "tests.py"))
    print(run_python_file(working_dir, "main.py", ["3 + 5"]))
    print(run_python_file(working_dir, "ma.py", ["3 + 5"]))
    print(run_python_file(working_dir, "/ty.py", ["3 + 5"]))


main()