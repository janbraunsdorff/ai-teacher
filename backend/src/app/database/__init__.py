import pymongo
from pymongo import MongoClient
from app.config import configMongo as cf

connection = f"{cf.protocol}://{cf.user}:{cf.password}@{cf.servers}/{cf.database}"
print(f"connect to: {connection}")
client = MongoClient(connection)
print(f"Avible Databases {client.list_database_names()}")

db = client["teacher"]
user_collection = db["user"]