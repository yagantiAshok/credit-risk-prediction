

import os 
from pathlib import Path

project_name = "credit_risk"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_training.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/externel_connections/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/schema.yaml",
    f"{project_name}/config/model.yaml",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/exception/__init__.py",
    "DockerFile",
    ".dockerignore",
    "testing.py",
    "app.py"
]
for filepath in list_of_files:
    file_obj = Path(filepath)
    folder,file = os.path.split(file_obj)
    if folder!="":
        os.makedirs(folder,exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,"w") as file:
            pass
    else:
        print(f"{filepath} already exists")
