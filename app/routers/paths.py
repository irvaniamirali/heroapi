import os

directory_path, pattern = "app/routers", ".py"
root_path_of_routers = "app/routers/sources/"

addition_paths = [
    "app.settings.docs.router"
]
forbidden_files = ["paths.py", "routers.py", "__init__.py"]


def list_files_walk(start_path="."):
    paths = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path.endswith(pattern) and file not in forbidden_files:
                paths.append(file)
    return paths


def replace_suffix(paths):
    routes = []
    for path in paths:
        path = root_path_of_routers + path
        without_suffix_path = path.replace(pattern, ".router")
        routes.append(without_suffix_path.replace("/", "."))
    return routes


full_paths = list_files_walk(directory_path)

# Path of APIRouters
paths = sorted(replace_suffix(full_paths))
paths += addition_paths
