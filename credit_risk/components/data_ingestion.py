

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.constants import COLLECTION_NAME
from credit_risk.data_extraction.mongodb import CustomerData
from credit_risk.entity.config_entity import dataingestionconfig
from credit_risk.entity.artifact_entity import dataingestionartifact
from credit_risk.utils.main_utils import create_directories
from sklearn.model_selection import train_test_split
import pandas as pd


class DataIngestion:
    def __init__(self,data_ingestion_config:dataingestionconfig):
        self.data_ingestion_config = data_ingestion_config
    
    def extract_data_and_save(self,collection_name)->str:
        try:
            logger.info("Entered  into extract data and save function in dataingestion class")
            customerdata_object = CustomerData()
            customer_data = customerdata_object.get_data_from_mongodb(collection_name=collection_name)
            create_directories(directory=self.data_ingestion_config.data_ingestion_raw_data_filepath)
            customer_data.to_csv(self.data_ingestion_config.data_ingestion_raw_data_filepath,index=False)

            "now split data into train and test "
            train,test= train_test_split(customer_data,test_size=self.data_ingestion_config.train_test_split_ratio,shuffle=False)
            create_directories(directory=self.data_ingestion_config.data_ingestion_ingested_folder)
            train.to_csv(self.data_ingestion_config.data_ingestion_train_filepath,index=False)
            test.to_csv(self.data_ingestion_config.data_ingestion_validation_filepath,index=False)
            return self.data_ingestion_config.data_ingestion_train_filepath,self.data_ingestion_config.data_ingestion_validation_filepath
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self)->dataingestionartifact:
        try:
            train_path,validation_path = self.extract_data_and_save(collection_name=COLLECTION_NAME)
            data_ingestion_artifact = dataingestionartifact(
                train_filepath=train_path,
                validation_filepath=validation_path
            )
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e,sys)