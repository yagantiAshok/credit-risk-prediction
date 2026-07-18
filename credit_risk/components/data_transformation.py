


import sys 
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.config_entity import DataTransformationConfig
from credit_risk.entity.artifact_entity import DataTransformationArtifact,dataingestionartifact
from credit_risk.utils.main_utils import save_object,save_to_numpy,read_yaml
from credit_risk.constants import SCHEMA_FILE
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                      data_ingestion_artifcat:dataingestionartifact,
                      schema_file = SCHEMA_FILE):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifcat = data_ingestion_artifcat
        self.schema = read_yaml(schema_file)

    def preprocess_object(self):
        try:
            "this data only have numeric features"
            numeric_features = self.schema.numeric_columns
            numeric_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])
            preprocess = ColumnTransformer(transformers=[
                ("numeric_features",numeric_pipeline,numeric_features)

            ])
            logger.info("Created preprocess object")
            return preprocess
        except Exception as e:
            raise CustomException(e,sys)
    
    def split_data_target_independent(self,data:pd.DataFrame,target:str= None):
        if target is None:
            target = self.schema.target_column.target
        try:
            if target in data.columns:
                independent_features = data.drop(target,axis=1)
                dependent_feature = data[target]
                return independent_features,dependent_feature
            else:
                return None
        except Exception as e:
            raise CustomException(e,sys)
        
    def transformation(self):
        try:
            train_data = pd.read_csv(self.data_ingestion_artifcat.train_filepath)
            validation_data = pd.read_csv(self.data_ingestion_artifcat.validation_filepath)
            # "split train data into independent and dependent features"
            # train_features = train_data.drop(self.schema.target_column.target,axis=1)
            # train_target = train_data[self.schema.target_column]

            # "split validation data into independent and dependent features"
            # validation_features = validation_data.drop(self.schema.target_column,axis=1)
            # validation_target = validation_data[self.schema.target_column]
            train_features,train_target = self.split_data_target_independent(train_data)
            validation_features,validation_target = self.split_data_target_independent(validation_data)
            preprocess = self.preprocess_object()
            train_preprocess_features = preprocess.fit_transform(train_features)#train_data
            validation_preprocess_features = preprocess.transform(validation_features)#validation data 
            numpy_train_data = np.c_[train_preprocess_features,np.array(train_target)]
            numpy_validation_data = np.c_[validation_preprocess_features,np.array(validation_target)]
            "svaing the data into specific folders"
            save_to_numpy(filepath=self.data_transformation_config.data_transformation_tranformed_trainfilepath,data=numpy_train_data)
            save_to_numpy(filepath=self.data_transformation_config.data_transformation_transformed_validation_filepath,data=numpy_validation_data)
            save_object(filepath=self.data_transformation_config.data_tranformation_preprocesses_obj_filepath,data=preprocess)

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            self.transformation()
            data_transformation_artifact = DataTransformationArtifact(
                processed_obj_filepath=self.data_transformation_config.data_tranformation_preprocesses_obj_filepath,
                processed_train_filepath=self.data_transformation_config.data_transformation_tranformed_trainfilepath,
                processed_validation_filepath=self.data_transformation_config.data_transformation_transformed_validation_filepath
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)