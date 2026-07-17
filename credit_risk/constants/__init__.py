
import os 

MOGODB_SERVER = "credit_risk_mongodb"
DATABASE_NAME  = "credit-risk-customers"
COLLECTION_NAME = "cutomers"

TRAIN_FILE_NAME = "cutomers_train.csv"
VALIDATION_FILE_NAME = "customers_validation.csv"
TEST_FILE_NAME = "customers_test.csv"
SCHEMA_FILE = os.path.join("config","schema.yaml")#config\schema.yaml

"""
DATA INGESTION CONSTANTS STARTS WITH DATA INGETSION

"""
DATA_INGESTION_MAIN_FOLDER :str = "data_ingestion"
DATA_INGESTION_RAW_DATA_FOLDER :str = "raw_data"
DATA_INGESTION_RAW_FILE_NAME :str  = "raw_customers.csv"
DATA_INGESTION_INGESTED_FOLDER :str = "ingested"
DATA_INGESTION_INGESTED_TRAIN_FILE_NAME :str = TRAIN_FILE_NAME
DATA_INGESTION_INGESTED_VALIDATION_FILE_NAME :str = VALIDATION_FILE_NAME
train_test_split_ratio :float = 0.30

"""
DATA VALIDATION CONSTANTS STARTS WITH DATA VALIDATION

"""
DATA_VALIDATION_MAIN_FOLDER :str = "data_validation"
DATA_VALIDATION_VALIDATION_FOLDER :str = "validation_status"
DATA_VALIDAION_VALIDATION_FILEPATH :str = "STATUS.txt"
DATA_VALIDATION_DRIFT_FOLDER : str = "drift"
DATA_VALIDATION_DRIFT_FILE_PATH : str = "report.yaml"
DATA_VALIDATION_DATA_MISMATCH_FOLDER :str = "data_mismatch"
DATA_VALIDATION_DATA_MISMATCH_FILEPATH : str = "DATA.txt"


