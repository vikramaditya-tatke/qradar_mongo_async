import dotenv
import os
import urllib
import logging
from pymongo import MongoClient

dotenv.load_dotenv(".env")

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PWD = urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_HOST = os.environ.get("MONGO_HOST")

#TODO: Use a dataclass
class MyMongoClient:
    def __init__(self) -> None:
        try:
            self.client: MongoClient = MongoClient(
                f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}"
            )
            logging.info(f"Client created")
        except Exception as e:
            logging.warning(f"Exception in MyMongoClient __init__(): {e}")
        self.coll = "Dump"

    def get_client(self) -> MongoClient:
        return self.client
