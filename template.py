
import os
from pathlib import Path

# Project Directory
project_name ="us_visa"

# Project template
list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py"
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artificial_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipline/__init__.py",
    f"{project_name}/pipline/training_pipeline.py",
    f"{project_name}/pipline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/notebook/mongodb_demo.ipynb",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "demo.py",
    "setup.py",
    "config/model/yaml",
    "config/schema.yaml",
]

# Iterate over each file path in the list
for filepath in list_of_files:
    # Convert the file path to a Path object for easier manipulation
    filepath = Path(filepath)
    # Get the parent directory of the file
    filedir = filepath.parent

    # If there is a parent directory (i.e., the file is not in the root directory)
    if filedir:
        # Create the directory and any necessary parent directories if they don't exist
        filedir.mkdir(parents=True, exist_ok=True)

    # Check if the file does not exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        # Create an empty file
        filepath.touch()
    else:
        # Print a message if the file already exists and is not empty
        print(f"File is already present as {filepath}")