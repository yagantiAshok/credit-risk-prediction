
import sys 
from credit_risk.cloud_storage.aws_storage import S3Functionalities
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.estimator import CreditriskModel
import pandas as pd

class S3estimator:
    def __init__(self,bucket_name,model_path=None):
        self.s3_functionalities: S3Functionalities = S3Functionalities()
        self.bucket_name = bucket_name
        self.model_name = model_path
        self.loaded_model:CreditriskModel = None
    
    def is_model_present(self):
        try:
            return self.s3_functionalities.is_key_path_avialble(bucket_name = self.bucket_name, s3_key = self.model_name)
        except Exception as e:
            raise CustomException(e,sys)
    def load_model(self):
        try:
            return self.s3_functionalities.load_model(bucket_name=self.bucket_name,model_name=self.model_name)
        except Exception as e:
            raise CustomException(e,sys)
    def save_model(self,from_file,to_file):
        try:
            return self.s3_functionalities.upload_file(from_filename=from_file,bucket_name=self.bucket_name,to_filename=to_file)
        except Exception as e:
            raise CustomException(e,sys)
    def predict(self,data:pd.DataFrame):
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(data_frame=data)
        except Exception as e:
            raise CustomException(e,sys)
    
    