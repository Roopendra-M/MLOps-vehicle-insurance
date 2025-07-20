import os
import sys
import certifi
from pymongo import MongoClient

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME,MONGODB_URL_KEY

# Load the certificate authority file to avoid  timeout errors when connecting mongoDB

ca=certifi.where()


class mongoDBClient:
    """It is the responsible for establishing a connecting to the mangoDB
        Attributs:
        -----------------------------
        client:mangodb client 
                A shared mangoDBClient instance for the class.....
        Database:Database
                The specific database instance that mangoDBClient connects to...
        Methods:
        ------------------------------
        __init__(Database_name:str)->None:
        initializes the mangoDB connection using the given data base name...
    """
    client=None
    def __init__(self,database_name:str = DATABASE_NAME):
        """initialize the connection to the mangoDB database...If no existing connecton is found ,it establishes a new one...
        Raise:
        ---------------------------------
        MyException
                    if there is an issue connecting to mangoDB or if the environment variable  for the mangoDB URL is not set
        """
        try:
            # check if a mangoDB client connection has already been established ;if not,create one...
            if mongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY) # retrives mongo db url from the environment  variables....
                if mongo_db_url is None:
                    raise Exception(f"Environment variable {MONGODB_URL_KEY} is not set.... ")
                #Establishes a new mongodb connection
                mongoDBClient.client= MongoClient(mongo_db_url,tlsCAFile=ca)
            # use the shared mongoClient for this instance....
            self.client=mongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("MongoDB connection successful.....")
        except Exception as e:
            raise MyException(e,sys)
