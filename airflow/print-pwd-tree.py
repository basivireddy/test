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
