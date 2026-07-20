
import boto3
import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
from credit_risk.constants import AWS_ACCESS_KEY_ID,AWS_SECERET_ACCESS_KEY_ID,region
import os 

class S3ConnectionManager:
    client = None
    resource = None
    def __init__(self,aws_access_key_id = AWS_ACCESS_KEY_ID,
                      aws_secret_access_key = AWS_SECERET_ACCESS_KEY_ID,
                      region = region):
        try:

            if S3ConnectionManager.client is None or S3ConnectionManager.resource  is None:
                __access_key_id  = os.getenv(aws_access_key_id)
                __secret_access_key = os.getenv(aws_secret_access_key)
                if __access_key_id is None:
                    raise ValueError(f"Enironment valriable {AWS_ACCESS_KEY_ID} is not found")
                if __secret_access_key is None:
                    raise ValueError(f"Environment variable {AWS_SECERET_ACCESS_KEY_ID} is not found")
                S3ConnectionManager.client = boto3.client("s3",
                                                    aws_access_key_id = __access_key_id,
                                                    aws_secret_access_key = __secret_access_key,
                                                    region_name  = region)
                S3ConnectionManager.resource = boto3.resource("s3",
                                                        aws_access_key_id = __access_key_id,
                                                        aws_secret_access_key = __secret_access_key,
                                                        region_name  = region)
            self.client = S3ConnectionManager.client
            self.resource = S3ConnectionManager.resource

            logger.info(f"AWS S3 connection succesfully Established in {region} ")

        except Exception as e:
          raise CustomException(e,sys)
