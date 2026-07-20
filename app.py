

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.pipeline.training_pipeline import TrainingPipeline
from credit_risk.entity.config_entity import (dataingestionconfig,
                                              DataValidationConfig,
                                              DataTransformationConfig,
                                              ModelTrainingConfig,
                                              ModelEvaluationConfig,
                                              ModelPusherConfig)

try:
    logger.info("Training Pipeline Started")
    obj = TrainingPipeline(data_ingestion_config=dataingestionconfig,
                           data_validation_config=DataValidationConfig,
                           data_transformation_config=DataTransformationConfig,
                           model_training_config=ModelTrainingConfig,
                           model_evaluation_config = ModelEvaluationConfig,
                           model_pusher_config=ModelPusherConfig)
    obj.run_pipeline()
    logger.info("Training pipeline ended")
except Exception as e:
    raise CustomException(e,sys)