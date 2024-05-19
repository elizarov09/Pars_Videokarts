import os

def print_directory_tree(root_dir, indent=""):
    for item in os.listdir(root_dir):
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            print(f"{indent}├── {item}/")
            print_directory_tree(path, indent + "    ")
        else:
            print(f"{indent}├── {item}")

# Замените 'your_project_directory' на путь к вашему проекту
root_directory = '/Users/olegelizarov/PycharmProjects/Pars_Videokarts'
print(f"{root_directory}/")
print_directory_tree(root_directory)
