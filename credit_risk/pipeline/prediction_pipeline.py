

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.estimator import CreditriskModel
from credit_risk.entity.s3_estimator import S3estimator
import pandas as pd
from credit_risk.constants import AWS_S3_BUSCKET_NAME,MODEL_NAME

class CustomerData:
    def __init__(self,
                RevolvingUtilizationOfUnsecuredLines,
                age,
                NumberOfTime30to59DaysPastDueNotWorse,
                DebtRatio,
                MonthlyIncome,
                NumberOfOpenCreditLinesAndLoans,
                NumberOfTimes90DaysLate,
                NumberRealEstateLoansOrLines,
                NumberOfTime60to89DaysPastDueNotWorse,
                NumberOfDependents):
        self.RevolvingUtilizationOfUnsecuredLines = RevolvingUtilizationOfUnsecuredLines
        self.age = age
        self.NumberOfTime30to59DaysPastDueNotWorse = NumberOfTime30to59DaysPastDueNotWorse
        self.DebtRatio = DebtRatio
        self.MonthlyIncome = MonthlyIncome
        self.NumberOfOpenCreditLinesAndLoans = NumberOfOpenCreditLinesAndLoans
        self.NumberOfTimes90DaysLate = NumberOfTimes90DaysLate
        self.NumberRealEstateLoansOrLines = NumberRealEstateLoansOrLines
        self.NumberOfTime60to89DaysPastDueNotWorse = NumberOfTime60to89DaysPastDueNotWorse
        self.NumberOfDependents = NumberOfDependents
    
    def convert_to_dictionary(self)->dict:
        try:
            customer_data_dict = {
                'RevolvingUtilizationOfUnsecuredLines':self.RevolvingUtilizationOfUnsecuredLines,
                'age':self.age,
                'NumberOfTime30-59DaysPastDueNotWorse':self.NumberOfTime30to59DaysPastDueNotWorse,
                'DebtRatio':self.DebtRatio,
                'MonthlyIncome':self.MonthlyIncome,
                'NumberOfOpenCreditLinesAndLoans':self.NumberOfOpenCreditLinesAndLoans,
                'NumberOfTimes90DaysLate':self.NumberOfTimes90DaysLate,
                'NumberRealEstateLoansOrLines':self.NumberRealEstateLoansOrLines,
                'NumberOfTime60-89DaysPastDueNotWorse':self.NumberOfTime60to89DaysPastDueNotWorse,
                'NumberOfDependents':self.NumberOfDependents }
            logger.info("User Data Converted into Dictionary")
            return customer_data_dict
        except Exception as e:
            raise CustomException(e,sys)
    def convert_to_dataframe(self)->pd.DataFrame:
        try:
            user_data_dict = self.convert_to_dictionary()
            data_frame = pd.DataFrame([user_data_dict])
            logger.info("User Data Transformed Into DataFrame")
            return data_frame
        except Exception as E:
          raise CustomException(E,sys)
    
class CreditriskClassifier:
    def __init__(self,Bucket_name=AWS_S3_BUSCKET_NAME,modle_name=MODEL_NAME):
        self.bucket_name = Bucket_name
        self.modle_name = modle_name
        self.s3_estimator = S3estimator(bucket_name=Bucket_name,model_path=modle_name)
    
    def predict(self,data:pd.DataFrame):
        try:
            creditrisk_class = self.s3_estimator.predict(data=data)
            return creditrisk_class
        except Exception as e:
            raise CustomException(e,sys)
        
        



        

        