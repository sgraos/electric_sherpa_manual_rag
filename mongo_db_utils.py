from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("DB_URI")
mongo_app = os.getenv("MONGO_APPNAME")
mongodb_client = MongoClient(mongo_uri, appname=mongo_app)

def get_collection_list():
    db = mongodb_client["ev_manuals"]
    return db.list_collection_names()
