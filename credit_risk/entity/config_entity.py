
import os 
from datetime import datetime
from credit_risk.constants import *
from dataclasses import dataclass

TIMESTAMP = f"{datetime.now().strftime('%B %d, %Y %H-%M-%S')}"
MAIN_FOLDER = "Artifact"

@dataclass
class TrainingPipelineConfiguration:
    artifcat :str = os.path.join(MAIN_FOLDER,TIMESTAMP)

trainingpipelineconfig :TrainingPipelineConfiguration = TrainingPipelineConfiguration()

@dataclass
class dataingestionconfig:
    data_ingestion_main_folder :str = os.path.join(trainingpipelineconfig.artifcat,DATA_INGESTION_MAIN_FOLDER)
    data_ingestion_ingested_folder: str = os.path.join(data_ingestion_main_folder,DATA_INGESTION_INGESTED_FOLDER)
    data_ingestion_raw_data_filepath :str = os.path.join(data_ingestion_main_folder,DATA_INGESTION_RAW_DATA_FOLDER,DATA_INGESTION_RAW_FILE_NAME)
    data_ingestion_train_filepath :str = os.path.join(data_ingestion_main_folder,DATA_INGESTION_INGESTED_FOLDER,DATA_INGESTION_INGESTED_TRAIN_FILE_NAME)
    data_ingestion_validation_filepath :str = os.path.join(data_ingestion_main_folder,DATA_INGESTION_INGESTED_FOLDER,DATA_INGESTION_INGESTED_VALIDATION_FILE_NAME)
    train_test_split_ratio :float = train_test_split_ratio

@dataclass
class DataValidationConfig:
    data_validation_main_folder:str = os.path.join(trainingpipelineconfig.artifcat,DATA_VALIDATION_MAIN_FOLDER)
    data_validation_filepath:str = os.path.join(data_validation_main_folder,DATA_VALIDATION_VALIDATION_FOLDER,DATA_VALIDAION_VALIDATION_FILEPATH)
    data_validation_drift_filepath : str = os.path.join(data_validation_main_folder,DATA_VALIDATION_DRIFT_FOLDER,DATA_VALIDATION_DRIFT_FILE_PATH)
    data_validation_data_mismatch_filepath: str = os.path.join(data_validation_main_folder,DATA_VALIDATION_DATA_MISMATCH_FOLDER,DATA_VALIDATION_DATA_MISMATCH_FILEPATH)
    