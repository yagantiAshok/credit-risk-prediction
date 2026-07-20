

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.components.data_ingestion import DataIngestion
from credit_risk.components.data_validation import DataValidation
from credit_risk.components.data_transformation import DataTransformation
from credit_risk.components.model_training import ModelTraining
from credit_risk.components.model_evaluation import ModelEvaluation
from credit_risk.components.model_pusher import ModelPusher
from credit_risk.entity.config_entity import (dataingestionconfig,
                                              DataValidationConfig,
                                              DataTransformationConfig,
                                              ModelTrainingConfig,
                                              ModelEvaluationConfig,
                                              ModelPusherConfig)
from credit_risk.entity.artifact_entity import (dataingestionartifact,
                                                DatavalidationArtifcat,
                                                DataTransformationArtifact,
                                                ModelTrainingArtifcat,
                                                ModelEvaluationArtifact)


class TrainingPipeline:
    def __init__(self,data_ingestion_config:dataingestionconfig,
                      data_validation_config:DataValidationConfig,
                      data_transformation_config:DataTransformationConfig,
                      model_training_config:ModelTrainingConfig,
                      model_evaluation_config:ModelEvaluationConfig,
                      model_pusher_config :ModelPusherConfig):
        self.data_ingestion_config = data_ingestion_config
        self.data_validation_config = data_validation_config
        self.data_transformation_config = data_transformation_config
        self.model_training_config=model_training_config
        self.model_evaluation_config = model_evaluation_config
        self.model_pusher_config = model_pusher_config
    
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
    def start_data_transformation(self,data_ingestion_artifcat:dataingestionartifact)->DataTransformationArtifact:
        try:
            data_transformation_object= DataTransformation(data_transformation_config=self.data_transformation_config,
                                                           data_ingestion_artifcat=data_ingestion_artifcat)
            data_transformation_artifcat=data_transformation_object.initiate_data_transformation()
            logger.info("Data Transformation Completed")
            return data_transformation_artifcat
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_model_training(self,data_transformation_artifcat:DataTransformationArtifact)->ModelTrainingArtifcat:
        try:
            model_training_object = ModelTraining(model_training_config=self.model_training_config,
                                                  data_transformation_artifcat=data_transformation_artifcat)
            model_training_artifcat = model_training_object.initiate_model_training()
            logger.info("ModelTraining Stage Completed")
            return model_training_artifcat
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_evaluation(self,model_training_artifcat:ModelTrainingArtifcat,
                               data_ingestion_artifact:dataingestionartifact):
        try:
            model_evaluation_object = ModelEvaluation(model_evalutaion_config=self.model_evaluation_config,
                                                      model_training_artifcat=model_training_artifcat,
                                                      data_ingestion_artifcat=data_ingestion_artifact)
            model_evalutaion_artifact  = model_evaluation_object.initiate_model_evaluation()
            logger.info("Model Evalutaion Stage Completed")
            return model_evalutaion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_model_pusher(self,model_evaluation_artifcat:ModelEvaluationArtifact):
        try:
            model_pusher_object = ModelPusher(model_pusher_config=self.model_pusher_config,model_evaluation_artifact=model_evaluation_artifcat)
            model_pusher_object.model_pusher()
            logger.info("Model pusher Stage Completed")
        except Exception as e:
            raise CustomException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            # data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            # if not data_validation_artifact.validation_status:
            #     return f"Validation status is {data_validation_artifact.validation_status}"
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifcat=data_ingestion_artifact)
            model_training_artifcat = self.start_model_training(data_transformation_artifcat=data_transformation_artifact)
            model_evaluation_artifcat  = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,model_training_artifcat=model_training_artifcat)
            if not model_evaluation_artifcat.is_model_accepted:
                return f"New model is not accepted"
            self.start_model_pusher(model_evaluation_artifcat=model_evaluation_artifcat)
        except Exception as e:
            raise CustomException(e,sys)

