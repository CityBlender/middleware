import os, errno
from pymongo import MongoClient
from pprint import pprint

import settings

# configure database connection
if settings.checkEnvironment() == 'production':
  db_uri = os.getenv('DB')
  db_client = MongoClient(str(db_uri))
else:
  db_uri = os.getenv('DB_TEST')
  db_client = MongoClient(str(db_uri))


# dbStatus()
# - tests connection to MongoDB
def dbStatus():
  server_status = db_london.command("serverStatus")
  pprint(server_status)


# check if event exists
def eventExists(new_event_id, db_collection):
  if db_collection.find({'event_id': new_event_id}).count() > 0:
    return True
  else:
    return False

# insert events into database
def dbInsertEvents(events, db_collection):
  for event in events:
    event_id = event['event_id']
    if eventExists(event_id, db_collection):
      pass
    else:
      db_collection.insert(event)

