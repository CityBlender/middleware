import os, errno
from pymongo import MongoClient
from pprint import pprint

import settings

# configure database connection
db_uri = os.getenv('DB')
db_client = MongoClient(str(db_uri))
db = db_client.test
db_events = db['events']
db_artist = db['artists']

# dbStatus()
# - tests connection to MongoDB
def dbStatus():
  server_status = db.command("serverStatus")
  pprint(server_status)



# check if event exists
def eventExists(new_event_id):
  if db_events.find({'event_id': new_event_id}).count() > 0:
    return True
  else:
    return False


def dbInsertEvents(events):
  for event in events:
    event_id = event['event_id']
    if eventExists(event_id):
      pass
    else:
      db_events.insert(event)

