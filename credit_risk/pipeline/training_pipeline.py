

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.components.data_ingestion import DataIngestion
from credit_risk.components.data_validation import DataValidation
from credit_risk.entity.config_entity import (dataingestionconfig,
                                              DataValidationConfig)
from credit_risk.entity.artifact_entity import (dataingestionartifact,
                                                DatavalidationArtifcat)


class TrainingPipeline:
    def __init__(self,data_ingestion_config:dataingestionconfig,
                      data_validation_config:DataValidationConfig):
        self.data_ingestion_config = data_ingestion_config
        self.data_validation_config = data_validation_config
    
    def start_data_ingestion(self)->dataingestionartifact:
        try:
            data_ingestion_object = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion_object.initiate_data_ingestion()
            logger.info("Data Ingestion Stage Completed")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:dataingestionartifact)->DatavalidationArtifcat:
        try:
            data_validation_object=DataValidation(data_validation_config=DataValidationConfig,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifcat=data_validation_object.initiate_data_validation()
            logger.info("DataValidation Stage Completed")
            return data_validation_artifcat
        except Exception as e:
            raise CustomException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise CustomException(e,sys)

