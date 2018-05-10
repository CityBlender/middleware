import os, errno
from pymongo import MongoClient
from pprint import pprint

import settings

import data.songkick as sk
import data.artist as artistData

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
  server_status = db_client.london.command("serverStatus")
  pprint(server_status)


# check if event exists
def eventExists(new_event_id, db_collection):
  if db_collection.find({'id': new_event_id}).count() > 0:
    return True
  else:
    return False

# insert events into database
def dbInsertEvents(event_data, db_collection):
  events = event_data
  events_inserted = 0
  events_skipped = 0
  for event in events:
    event_id = event['id']
    if eventExists(event_id, db_collection):
      events_skipped = events_skipped + 1
      pass
    else:
      events_inserted = events_inserted + 1
      db_collection.insert(event)

  print('DB: Inserted ' + '\033[92m' + str(events_inserted) + '\033[0m' + ' events')
  print('DB: Skipped ' + '\033[92m' + str(events_skipped) + '\033[0m' + ' duplicate events')


# check if artist exists
def artistExists(new_artist_id, db_collection):
  if db_collection.find({'id': new_artist_id}).count() > 0:
    return True
  else:
    return False

# insert events into database
def dbInsertArtist(artist_data, db_collection):
  artist_id = artist_data['id']
  artist_name = artist_data['name']
  if artistExists(artist_id, db_collection):
    pass
  else:
    db_collection.insert(artist_data)
    print('DB: Inserted ' + '\033[92m' + str(artist_name) + '\033[0m')


