

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.config_entity import ModelTrainingConfig
from credit_risk.entity.artifact_entity import ModelTrainingArtifcat,DataTransformationArtifact
from credit_risk.utils.main_utils import read_yaml,save_object,load_numpy_data,load_object
from credit_risk.entity.estimator import CreditriskModel
from credit_risk.constants import MODEL_FILE
import numpy as np
from credit_risk.model_factory.model_storage import models_dictionary
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score


class ModelTraining:
    def __init__(self,model_training_config:ModelTrainingConfig,
                      data_transformation_artifcat:DataTransformationArtifact,
                      model_file = MODEL_FILE):
        self.model_training_config = model_training_config
        self.data_transformation_artifcat = data_transformation_artifcat
        self.model = read_yaml(model_file)

    def evaluation_metrics(self,actual,predicted)->dict:
        try:
            logger.info("Entered into evaluation metrics")
            metrics = {
                "accuracy_score":accuracy_score(actual,predicted),
                "precision":precision_score(actual,predicted),
                "recall":recall_score(actual,predicted),
                "f1_score":f1_score(actual,predicted)
            }
            logger.info(f"Model accuracy score {metrics['accuracy_score']} and recall {metrics['recall']}")
            return metrics
        except Exception as e:
          raise CustomException(e,sys)
    @staticmethod
    def extract_features(data:np.ndarray):
        try:
            train_x = data[:,:-1]
            train_y = data[:,-1]
            return train_x,train_y
        except Exception as e:
            raise CustomException(e,sys)
    
    def model_training(self)->dict:
        try:
            train_data = load_numpy_data(filepath=self.data_transformation_artifcat.processed_train_filepath)
            validation_data = load_numpy_data(filepath=self.data_transformation_artifcat.processed_validation_filepath)
            logger.info("entered into model training function ")
            "train independent features and target feature"
            train_x,train_y = self.extract_features(train_data)
            validation_x,validation_y = self.extract_features(validation_data)
            model_class = models_dictionary[self.model.model.model_name]
            model_params = self.model.model_params
            params_loaded_model = model_class(**model_params)#actual mdoel
            "training model"
            trained_model = params_loaded_model.fit(train_x,train_y)
            predcition = trained_model.predict(validation_x)
            metrics = self.evaluation_metrics(validation_y,predcition)
            "load preprocess object"
            preprocess_obj = load_object(self.data_transformation_artifcat.processed_obj_filepath)
            creditriskmdoel = CreditriskModel(preprocess_object=preprocess_obj,trained_model=trained_model)
            "save the mdoel"
            save_object(filepath=self.model_training_config.model_training_trained_model_object_filepath,data=creditriskmdoel)
            return metrics
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_training(self)->ModelTrainingArtifcat:
        try:
            metrics = self.model_training()
            model_training_artifact = ModelTrainingArtifcat(
                accuracy=metrics["accuracy_score"],
                precision=metrics["precision"],
                recall=metrics["recall"],
                f1_score=metrics["f1_score"],
                trained_model=self.model_training_config.model_training_trained_model_object_filepath
            )
            return model_training_artifact
        except Exception as e:
            raise CustomException(e,sys)



    