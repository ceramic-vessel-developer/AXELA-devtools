import os
import json
from idlelib.iomenu import errors
from pathlib import Path
import ast
import importlib.util
import inspect
import sys
import types
import abc

REQUIRED_FILES = ["main.py", "metadata.json", "README.md", "requirements.txt", "setup.py"]
REQUIRED_DIRS = ["scripts"]


def _check_main_file(path):
    try:
        with open(path / "main.py", "r") as f:
            tree = ast.parse(f.read())
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        if not any(cls.endswith("Impl") for cls in classes):
            return False, "No class ending with 'Impl' found in main.py"
        return True, ""
    except Exception as e:
        return False, f"Error parsing main.py: {e}"


def _check_metadata_file(path):
    try:
        with open(path / "metadata.json", "r") as f:
            data = json.load(f)
        required_keys = ["name", "author", "main", "version", "type", "config"]
        for key in required_keys:
            if key not in data:
                return False, f"Missing key '{key}' in metadata.json"
        if not isinstance(data["config"], list):
            return False, "Config must be a list of config objects"
        for item in data["config"]:
            if not all(k in item for k in ["name", "type", "value"]):
                return False, f"Incomplete config item: {item}"
        return True, ""
    except json.JSONDecodeError:
        return False, "metadata.json is not valid JSON"
    except Exception as e:
        return False, f"Error reading metadata.json: {e}"


def _check_structure(project_path):
    errors = []

    for file in REQUIRED_FILES:
        if not (project_path / file).exists():
            errors.append(f"Missing required file: {file}")

    for directory in REQUIRED_DIRS:
        if not (project_path / directory).exists():
            errors.append(f"Missing required directory: {directory}")

    is_main_valid, msg = _check_main_file(project_path)
    if not is_main_valid:
        errors.append(msg)

    is_meta_valid, msg = _check_metadata_file(project_path)
    if not is_meta_valid:
        errors.append(msg)

    return errors


def check(project_path):
    project_path = Path(project_path)
    errors = _check_structure(project_path)
    return errors



def _cli():
    project_name = input("Enter the path to the addon project: ").strip()
    project_path = Path(project_name)

    if not project_path.exists() or not project_path.is_dir():
        print("❌ Provided path does not exist or is not a directory.")
        return

    errors = check(project_path)

    if errors:
        print("❌ Project check failed with the following issues:")
        for error in errors:
            print(f" - {error}")
    else:
        print("✅ Project structure and contents are valid!")


if __name__ == "__main__":
    _cli()
