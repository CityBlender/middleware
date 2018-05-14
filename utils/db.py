import os, errno
import pymongo
from pymongo import MongoClient
from pprint import pprint

import settings

import utils.dataHelper as dataHelper
import data.songkick as sk
import data.artist as artistData


# print console header
def printHeader():
  return dataHelper.printHeader('DB:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)

# print underline
def printUnderline(string):
  return dataHelper.printUnderline(string)

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

# set event index
def createEventIndex(db_collection):
  db_collection.create_index([('date', pymongo.DESCENDING)], background=True)
  db_collection.create_index([('id', pymongo.ASCENDING)], background=True)


# insert events into database
def dbInsertEvent(event_data, db_collection):
  event = event_data
  event_id = event['id']
  event_name = event['name']
  if eventExists(event_id, db_collection):
    print_skip = printHeader() + ' Skipping ' + printUnderline('event') + ' ' + printGreen(event_name) + ' (already exits)'
    print(print_skip)
    pass
  else:
    db_collection.insert(event)
    print_insert = printHeader() + ' Inserted  ' + printUnderline('event') + ' ' + printGreen(event_name)
    print(print_insert)


# create artist index
def createArtistIndex(db_collection):
  db_collection.create_index([('id', pymongo.ASCENDING)], background=True)

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
    print_skip = printHeader() + ' Skipping ' + printUnderline('artist') + ' ' + printGreen(artist_name) + ' (already exits)'
    print(print_skip)
    pass
  else:
    db_collection.insert(artist_data)
    print_console = printHeader() + ' Inserted ' + printUnderline('artist') + ' ' + printGreen(artist_name)
    print(print_console)


