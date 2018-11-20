from pymongo import MongoClient
from pprint import pprint
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://127.0.0.1:27017")

print(client.guardian.news.find_one({}, {'content': 0, '_id': 0}))


#client.guardian.news.remove({})
#client.startjobs.jobs_entries.remove({})
