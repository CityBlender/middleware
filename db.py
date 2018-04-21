import os, errno
from pymongo import MongoClient
from pprint import pprint

import settings

# test connection to MongoDB
db_test_uri = os.getenv('DB_TEST')
db_test_client = MongoClient(str(db_test_uri))
db_test = db_test_client.test

def dbStatus():
  server_status = db_test.command("serverStatus")
  pprint(server_status)

# events
db_uri = os.getenv('DB')
db_client = MongoClient(str(db_uri))
db = db_client.master
db_events_collection = db['events']
db_artist_collection = db['artists']

def dbInsertEvents(events):
  db_events_collection.insert(events)
