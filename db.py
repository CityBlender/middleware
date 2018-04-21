import os, errno
from pymongo import MongoClient
from pprint import pprint

import settings

# test connection to MongoDB
db_test_uri = os.getenv('DB_TEST')
db_test_client = MongoClient(str(db_test_uri))
db_test = db_test_client.test
db_test_events = db_test['events']

def dbStatus():
  server_status = db_test.command("serverStatus")
  pprint(server_status)

# events
db_uri = os.getenv('DB')
db_client = MongoClient(str(db_uri))
db = db_client.master
db_events = db['events']
db_artist = db['artists']

def dbInsertEvents(events):
  db_events.insert(events)

def dbInsertTestEvents(events):
  db_test_events.insert(events)
