import os
import json
from pathlib import Path
import inspect
import importlib.util
import sys
import types
import abc

ADDON_TYPES = {
    "monitor": "monitoring",
    "calendar": "calendar",
    "music": "music_player",
    "notes": "notes"
}

BASE_CLASS_IMPORT = "from axela_devtools import {class_name}\n\n"

MAIN_TEMPLATE = '''{base_import}
class {class_name}Impl({class_name}):
    def __init__(self):
        pass  # Initialize your addon

    def run(self):
        pass  # Main logic of the addon
'''

README_TEMPLATE = """# {project_name}

Addon of type `{addon_type}`.

## Description

Describe your addon here.
"""

REQUIREMENTS = ["axela_devtools"]


def load_module_from_path(path: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location("abstracts", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["abstracts"] = module
    spec.loader.exec_module(module)
    return module


def generate_implementations(module, output_file):
    with open(output_file, "w") as f:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if not issubclass(obj, abc.ABC) or obj.__module__ != module.__name__:
                continue
            f.write(f"class {name}Impl({name}):\n")
            for method_name, method in inspect.getmembers(obj, predicate=inspect.isfunction):
                if getattr(method, "__isabstractmethod__", False):
                    sig = str(inspect.signature(method))
                    f.write(f"    def {method_name}{sig}:\n")
                    f.write("        pass\n")
            f.write("\n")


def prompt_user():
    print("Welcome to the Addon Project Generator!")
    name = input("Project name: ").strip()
    author = input("Author: ").strip()

    print("Select addon type:")
    for i, addon in enumerate(ADDON_TYPES, 1):
        print(f"{i}. {addon.capitalize()}")

    while True:
        try:
            choice = int(input("Enter the number of addon type: "))
            addon_type = list(ADDON_TYPES.keys())[choice - 1]
            break
        except (IndexError, ValueError):
            print("Invalid choice. Please try again.")

    return {
        "name": name,
        "author": author,
        "addon_type": addon_type,
        "class_name": ADDON_TYPES[addon_type]
    }


def create_structure(data):
    project_dir = Path(data["name"])
    os.makedirs(project_dir, exist_ok=True)

    # Create secondary scripts folder
    (project_dir / "scripts").mkdir(exist_ok=True)

    try:
        abstract_module = importlib.import_module(f"axela_devtools.{data["class_name"]}")
    except ModuleNotFoundError:
        # Fallback: use relative path if running from source
        source_path = Path(__file__).parent.parent / "axela_devtools" / f"{data["class_name"]}.py"
        spec = importlib.util.spec_from_file_location(f"axela_devtools.{data["class_name"]}", str(source_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        abstract_module = module
    generate_implementations(abstract_module, project_dir / "main.py")


    # metadata.json
    metadata = {
        "name": data["name"],
        "author": data["author"],
        "main": "main.py",
        "version": "0.1.0",
        "type": data["addon_type"],
        "config": [
            {
                "name": "example_config",
                "type": "str",
                "value": ""
            },
            {
                "name": "max_limit",
                "type": "int",
                "value": 10
            }
        ]
    }
    with (project_dir / "metadata.json").open("w") as f:
        json.dump(metadata, f, indent=4)

    # README.md
    with (project_dir / "README.md").open("w") as f:
        f.write(README_TEMPLATE.format(
            project_name=data["name"],
            addon_type=data["addon_type"]
        ))

    # requirements.txt
    with (project_dir / "requirements.txt").open("w") as f:
        f.write("\n".join(REQUIREMENTS))

    # setup.py
    with (project_dir / "setup.py").open("w") as f:
        f.write(f"""from setuptools import setup, find_packages
                    
setup(
    name="{data['name']}",
    version="0.1.0",
    packages=find_packages(),
    install_requires={REQUIREMENTS},
    author="{data['author']}",
    description="Addon of type {data['addon_type']}",
)
""")

    print(f"✅ Project '{data['name']}' has been created successfully!")


if __name__ == "__main__":
    user_data = prompt_user()
    create_structure(user_data)
