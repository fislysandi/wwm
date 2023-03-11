import os
import ast

def get_dependencies(filepath):
    with open(filepath, 'r') as file:
        try:
            tree = ast.parse(file.read())
        except Exception as e:
            print(f"Error in {filepath}: {e}")
            return []

    dependencies = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            dependencies.append(node.module)

    return dependencies

def search_folder(folder_path):
    python_scripts = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                python_scripts.append(filepath)

    dependencies = set()
    for script in python_scripts:
        script_deps = get_dependencies(script)
        for dep in script_deps:
            dependencies.add(dep)

    return dependencies

if __name__ == '__main__':
    python_folder = 'D:/Projects/dev/github/wwm-dev/Scripts'
    output_file = 'output.txt'

    dependencies = search_folder(python_folder)

    with open(output_file, 'w') as file:
        file.write('\n'.join(dependencies))
