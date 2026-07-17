

from credit_risk.logger import logger
from credit_risk.exception import CustomException
import sys
import os 
import pymongo
from credit_risk.constants import DATABASE_NAME,MOGODB_SERVER
import certifi
ca = certifi.where()

class MongodbClient:

    client = None
    def __init__(self,data_base = DATABASE_NAME):
        try :
            if MongodbClient.client is None:
                mongo_db_server = os.getenv(MOGODB_SERVER)
                if mongo_db_server is None:
                    raise ValueError(f"environment variable not exists {MOGODB_SERVER}")
                MongodbClient.client = pymongo.MongoClient(mongo_db_server,tlsCAFile=ca)
                MongodbClient.client.admin.command("ping")
                logger.info("Mongodb connection established successfully")
            self.client = MongodbClient.client
            self.database = self.client[data_base]
        except Exception as e:
            raise CustomException(e,sys)

