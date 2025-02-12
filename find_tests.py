import os
import ast

EXCLUDED_FOLDERS = {".venv", "venv", "site-packages"}

def find_test_files(directory):
    """Find all Python files with 'test' in their name, excluding virtual env folders."""
    test_files = []
    for root, _, files in os.walk(directory):
        if any(excluded in root.split(os.sep) for excluded in EXCLUDED_FOLDERS):
            continue  # Skip virtual environment folders
        for file in files:
            if file.endswith(".py") and "test" in file.lower():
                test_files.append(os.path.join(root, file))
    return test_files

def extract_test_functions(file_path):
    """Extract all functions containing 'test' in their name from a given Python file."""
    test_functions = []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and "test" in node.name.lower():
                    test_functions.append(node.name)
        except SyntaxError:
            print(f"Skipping {file_path} due to syntax errors.")
    return test_functions

def main(directory, output_file="test_list.txt"):
    """Find all test files, extract test functions, and write to a file."""
    test_files = find_test_files(directory)
    test_count = 0

    with open(output_file, "w", encoding="utf-8") as f:
        for test_file in test_files:
            test_functions = extract_test_functions(test_file)
            for test_function in test_functions:
                f.write(f"{test_file}::{test_function}\n")
                test_count += 1

    print(f"Results saved to {output_file}")
    print(f"Total test functions found: {test_count}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python find_tests.py <directory>")
    else:
        main(sys.argv[1])