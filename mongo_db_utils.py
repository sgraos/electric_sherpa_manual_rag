from pymongo import MongoClient

mongo_uri = "mongodb+srv://rag_access:rdMnHQ1usHRncXYp@cluster0.pfd6gvx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongodb_client = MongoClient(mongo_uri, appname="ntuakshayrao.evmanual_rag")

def get_collection_list():
    db = mongodb_client["ev_manuals"]
    return db.list_collection_names()