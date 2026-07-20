

import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.entity.config_entity import ModelPusherConfig
from credit_risk.entity.artifact_entity import ModelEvaluationArtifact
from credit_risk.entity.s3_estimator import S3estimator

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluationArtifact):
        self.model_pusher_config = model_pusher_config
        self.model_evaluation_artifact = model_evaluation_artifact
    
    def model_pusher(self):
        try:
            s3_estimator = S3estimator(bucket_name=self.model_pusher_config.bucket_name)
            s3_estimator.save_model(from_file=self.model_evaluation_artifact.new_model,to_file=self.model_pusher_config.model_name)
            logger.info(f"New Model Psuhed To Production")
        except Exception as e:
            raise CustomException(e,sys)