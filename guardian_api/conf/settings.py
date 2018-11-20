import os

env = os.getenv("ENV", "PROD")

if env == "DEV":
    MONGO_URL = "mongodb://127.0.0.1:27017"
else:
    MONGO_URL = "mongo_url"