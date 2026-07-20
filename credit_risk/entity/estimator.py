

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from sklearn.pipeline import Pipeline
import pandas as pd

class CreditriskModel:
    def __init__(self,preprocess_object:Pipeline,trained_model:object):
        self.preprocess_object = preprocess_object
        self.trained_model = trained_model
    
    def predict(self,data_frame:pd.DataFrame):
        try:
            logger.info("Entered into predcit function inside creditriskmodel")
            # print(data_frame)
            # for col in data_frame.columns:
            #     print(col)
            #     print(data_frame.at[0, col])
            #     print(type(data_frame.at[0, col]))
            #     logger.info(f"{col} and value {data_frame.at[0, col]} and {type(data_frame.at[0, col])}")
            transformed_features = self.preprocess_object.transform(data_frame)
            logger.info("preprocess object transforemed features")
            value = self.trained_model.predict(transformed_features)
            logger.info(f"Model is Predicted and value  is {value}")
            return value
        except Exception as e:
            raise CustomException(e,sys)