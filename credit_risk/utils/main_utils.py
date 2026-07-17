
import sys
from box import ConfigBox
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from pathlib import Path
from typing import Any
import numpy as np
import joblib
import yaml

def read_yaml(filepath:str)->ConfigBox:
    path = Path(filepath)
    try:
        logger.info(f"Entered into read_yaml function and file path {filepath}")
        if not path.exists():
            raise FileNotFoundError(f"filepath {filepath} not exists")
        with open(path,"r") as file:
            contents = yaml.safe_load(file) or {}
            return ConfigBox(contents)
    except Exception as e:
        raise CustomException(e,sys)

def save_to_yaml_file(data:Any,filepath:str)->None:
    path = Path(filepath)
    try:
        logger.info(f"Entered into save_to_yaml_file function and the location {filepath}")
        path.parent.mkdir(parents=True,exist_ok=True)
        logger.info(f"Filepath is created at {path}")
        with open(path,"w") as file:
            yaml.dump(data,file,default_flow_style=False,sort_keys=False)
    except Exception as e:
        raise CustomException(e,sys)

def save_to_numpy(data:np.ndarray,filepath:str)->None:
    path = Path(filepath)
    try:
        logger.info("Entered into save_to_numpy function")
        path.parent.mkdir(parents=True,exist_ok=True)
        logger.info(f"Filepath is created at {path}")
        if path.suffix!=".npy":
            path = path.with_suffix(".npy")
        np.save(path,data)
    except Exception as e:
        raise CustomException(e,sys)

def load_numpy_data(filepath:str)->np.ndarray:
    path = Path(filepath)
    try:
        logger.info("Entered into load_numpy_data function")
        if not path.exists():
            raise FileNotFoundError(f"File not found {filepath}")
        data = np.load(path)
        return data
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(data:Any,filepath:str)->None:
    path = Path(filepath)
    try:
        logger.info("Entered into save_to_binary function")
        path.parent.mkdir(parents=True,exist_ok=True)
        logger.info(f"Filepath is crated at {path}")
        joblib.dump(value=data,filename=path)
    except Exception as e:
        raise CustomException(e,sys)

def load_object(filepath:str)->Any:
    path = Path(filepath)
    try:
        logger.info("Entered into load_to_binary function")
        if not path.exists():
            raise FileNotFoundError(f"File not found {path}")
        data = joblib.load(path)
        return data
    except Exception as e:
        raise CustomException(e,sys)

def create_path(filepath:str)->None:
    path = Path(filepath)
    try:
        logger.info(f"Entered into craete_filepath function")
        if path.suffix:
            target_dir = path.parent
        else:
            target_dir = path
        target_dir.mkdir(parents=True,exist_ok=True)
        logger.info(f"Directory created at {path}")
        if path.suffix:
            path.touch(exist_ok=True)
        logger.info(f"File created at {path}")
    except Exception as e:
        raise CustomException(e,sys)
    
def create_directories(directory:str)->None:
    try:
        path = Path(directory)
        if path.suffix:
          path.parent.mkdir(parents=True,exist_ok=True)
          logger.info(f"Fodler {path} is created ")
        else:
            path.mkdir(parents=True,exist_ok=True)
            logger.info(f"folder {path} is created")
    except Exception as e:
        raise CustomException(e,sys)
