
import sys
from credit_risk.logger import logger
from credit_risk.exception import CustomException
import pandas as pd
from credit_risk.externel_connections.mongodb_connection import MongodbClient
from typing import Optional

class CustomerData:
    def __init__(self):
        self.mongo_client:MongodbClient = MongodbClient()
    def get_data_from_mongodb(self,collection_name:str,database:Optional[str]=None)->pd.DataFrame:

        try:
            logger.info("Entered into get data from mongodb function")
            if database is not None:
                database_name = self.mongo_client.client[database]
            else:
                database_name = self.mongo_client.database
            collections = database_name[collection_name]
            data = list(collections.find())
            if not data:
                logger.info(f"collection {collection_name} is empty ")
                return pd.DataFrame
            data_frame = pd.DataFrame(data)
            if "_id" in data_frame.columns:
                data_frame.drop("_id",axis=1,inplace=True)
            if "Unnamed: 0" in data_frame.columns:
                data_frame.drop("Unnamed: 0",axis = 1,inplace=True)
            logger.info(f"Converted Mongodb data into pandas dataframe {data_frame.shape}")
            return data_frame
        except Exception as e:
            raise CustomException(e,sys)