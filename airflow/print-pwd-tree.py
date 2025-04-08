import os

def print_tree(start_path='.', indent=''):
    for item in os.listdir(start_path):
        path = os.path.join(start_path, item)
        print(indent + '├── ' + item)
        if os.path.isdir(path):
            print_tree(path, indent + '│   ')

# Get and print current working directory
cwd = os.getcwd()
print(f"Current Directory: {cwd}\n")
print_tree(cwd)


import os

def find_file(filename, search_path='.'):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

# Example usage
file_to_find = 'target.txt'
found_path = find_file(file_to_find)

if found_path:
    print(f"Found: {found_path}")
else:
    print("File not found.")
