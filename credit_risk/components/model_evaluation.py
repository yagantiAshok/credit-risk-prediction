

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.config_entity import ModelEvaluationConfig
from credit_risk.entity.artifact_entity import ModelEvaluationArtifact,dataingestionartifact,ModelTrainingArtifcat
from sklearn.metrics import f1_score
from credit_risk.entity.s3_estimator import S3estimator
from credit_risk.constants import AWS_S3_BUSCKET_NAME,MODEL_NAME
import numpy as np
from credit_risk.entity.estimator import CreditriskModel
import pandas as pd
from credit_risk.constants import TARGET_COLUMN
from credit_risk.utils.main_utils import create_directories
class ModelEvaluation:
    def __init__(self,model_evalutaion_config:ModelEvaluationConfig,
                      data_ingestion_artifcat:dataingestionartifact,
                      model_training_artifcat:ModelTrainingArtifcat):
        self.model_evaluation_config = model_evalutaion_config
        self.data_ingestion_artifact  = data_ingestion_artifcat
        self.model_training_artifact = model_training_artifcat
        self.s3estimator = S3estimator(bucket_name=AWS_S3_BUSCKET_NAME,model_path=MODEL_NAME)

    def is_model_available(self):
        try:
            return self.s3estimator.is_model_present()
        except Exception as e:
            raise CustomException(e,sys)
    
    def model_evaluation(self):
        try:
            test_data = pd.read_csv(self.data_ingestion_artifact.validation_filepath)
            # no data cleaning steps present
            test = test_data.drop(TARGET_COLUMN,axis=1)
            test_actual = test_data[TARGET_COLUMN]
            production_model_f1_score = 0
            if self.is_model_available():
                model :CreditriskModel = self.s3estimator.load_model()
                predict = model.predict(data_frame=test)
                production_model_f1_score = f1_score(test_actual,predict)
            logger.info(f"Prodcustion model f1 score {production_model_f1_score}")
            if production_model_f1_score<self.model_training_artifact.f1_score:
               create_directories(self.model_evaluation_config.model_evalutaion_model_acception_filepath)
               with open(self.model_evaluation_config.model_evalutaion_model_acception_filepath,"w") as file:
                   file.write(f"PRODUCTION MODEL HAS LESS F1 SCORE {production_model_f1_score} : NEW MDOEL ACCEPTED")
                   logger.info("New Trained Model Is accepted")
            return production_model_f1_score
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            score = self.model_evaluation()
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=score<self.model_training_artifact.f1_score,
                new_model=self.model_training_artifact.trained_model,
                changed_score=score - self.model_training_artifact.f1_score
            )
            return model_evaluation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    
    
    