import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.exception import MyException
from src.constants import DATABASE_NAME
from src.configuration.mongo_db_connection import mongoDBClient

class Proj1Data:
    """A class to export MongoDB records as a pandas DataFrame"""
    
    def __init__(self) -> None:
        try:
            self.mongo_client = mongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports the entire MongoDB collection as a pandas DataFrame.
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            print("Fetching data from MongoDB...")
            documents = list(collection.find())
            print(f"Data fetched with length: {len(documents)}")

            if not documents:
                return pd.DataFrame()

            df = pd.DataFrame(documents)
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise MyException(e, sys)
