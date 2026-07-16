

MOGODB_SERVER = "credit_risk_mongodb"
DATABASE_NAME  = "credit-risk-customers"
COLLECTION_NAME = "customers"

TRAIN_FILE_NAME = "cutomers_train.csv"
VALIDATION_FILE_NAME = "customers_validation.csv"
TEST_FILE_NAME = "customers_test.csv"

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


