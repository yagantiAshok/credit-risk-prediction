

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.config_entity import DataValidationConfig
from credit_risk.entity.artifact_entity import DatavalidationArtifcat,dataingestionartifact
from credit_risk.utils.main_utils import read_yaml,create_directories,save_to_yaml_file
from credit_risk.constants import SCHEMA_FILE
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                       data_ingestion_artifact:dataingestionartifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifcat = data_ingestion_artifact
        self.schema_data = read_yaml(SCHEMA_FILE)
    
    def data_validation(self)->bool:
        try:
            logger.info("Entered into data validation function in Datavalidation class")
            test_data = pd.read_csv(self.data_ingestion_artifcat.validation_filepath)
            test_columns = list(test_data.columns)
            train_columns = list(self.schema_data.train_columns.keys())
            validation_status = True
            evaluation_data = []

            """
            1.MISSING COLUMNS (TRAIN COLUMNS NOT IN TEST COLUMNS)

            """
            missing_columns = []
            for column in train_columns:
                if column not in test_columns:
                    missing_columns.append(column)
            if len(missing_columns)>0:
                validation_status = False
            evaluation_data.append(f"Missing columns are : {missing_columns}")

            """
            2.Extra columns (columns that not in train data)

            """
            extra_columns = []
            for column in test_columns:
                if column not in train_columns:
                    extra_columns.append(column)
            if len(extra_columns)>0:
                validation_status=False
            evaluation_data.append(f"Extra columns are : {extra_columns}")
        
            """
            3.Schema checking
            
            """
            schema_data = []
            for column,data_type in self.schema_data.train_columns.items():
                if column in test_columns:
                    test_data_type= str(test_data[column].dtype)
                    if test_data_type!=data_type:
                        schema_data.append({
                            "column":column,
                            "original_type":data_type,
                            "wrong_type":test_data_type}
                        )
            if len(schema_data)>0:
                validation_status=False
            evaluation_data.append(f"schema mismatch columns are : {schema_data}")

            """
            4.CHECKING DUPLICATE ROWS

            """
            duplicate_rows = test_data.duplicated().sum()
            if duplicate_rows>0:
                evaluation_data.append(f"Duplicates rows exists : {duplicate_rows}")
                logger.info(f"Test data has duplicated rows : {duplicate_rows}")
            """
            5.CHECKING NAN PERCENTAGE

            """
            nan_columns = []
            for column in test_columns:
                nan_ratio = test_data[column].isnull().mean()*100
                if nan_ratio>0:
                    nan_data={
                        "Column":column,
                        "Nan_ration":nan_ratio
                    }
                    nan_columns.append(nan_data)
            if len(nan_columns)>0:
                evaluation_data.append(f"Nan column are exists : {nan_columns}")
                logger.info(f"nan columna are exists in test data {nan_columns}")
            
            create_directories(directory=self.data_validation_config.data_validation_filepath)
            with open(self.data_validation_config.data_validation_filepath,"w") as file:
                file.write(f"VALIDATION STATUS : {validation_status}")
            create_directories(directory=self.data_validation_config.data_validation_data_mismatch_filepath)
            with open(self.data_validation_config.data_validation_data_mismatch_filepath,"w") as file:
                for error_message in evaluation_data:
                    file.write(error_message + "\n")
            logger.info(f"Validation status : {validation_status}")
            return validation_status

        except Exception as e:
            raise CustomException(e,sys)
    
    def data_drift_with_evidently(self)->bool:
        try:
            logger.info("Entered into dat drift functin in DataValidaion class")
            train_data = pd.read_csv(self.data_ingestion_artifcat.train_filepath)
            validation_data = pd.read_csv(self.data_ingestion_artifcat.validation_filepath)
            report = Report(metrics=[DataDriftPreset()])
            report.run(
                reference_data=train_data,
                current_data=validation_data
            )
            report_dict = report.as_dict()
            logger.info(f"data drift report : {report_dict}")
            drift_status = report_dict["metrics"][0]["result"]["dataset_drift"]
            drifted_columns = report_dict["metrics"][0]["result"].get("drift_by_features","NOT THERE ")
            no_of_drifted_columns = report_dict["metrics"][0]["result"]["number_of_drifted_columns"]
            no_of_columns = report_dict["metrics"][0]["result"]["number_of_columns"]

            drift_report= {
                "DRIFT_STATUS": drift_status,
                "No_of_drifted_columns":no_of_drifted_columns,
                "No_of_columns":no_of_columns,
                "DRIFTED_COLUMNS": drifted_columns

            }
            save_to_yaml_file(filepath=self.data_validation_config.data_validation_drift_filepath,data=drift_report)
            return drift_status

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_validation(self)->DatavalidationArtifcat:
        try:
            data_validation_status = self.data_validation()
            data_drift_status = self.data_drift_with_evidently()
            data_validation_artifact = DatavalidationArtifcat(
                validation_status=data_validation_status,
                drift_filepath=self.data_validation_config.data_validation_drift_filepath,
                data_drift_status=data_drift_status
            )
            
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    