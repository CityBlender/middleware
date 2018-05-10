# mongo-example.py
import os
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient

# load .env variable
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(base_dir, '.env')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file, verbose=True)

# get the MongoDB URI
db_uri = os.getenv('DB_URI')

# create a new MongoDB Client
db_client = MongoClient(str(db_uri))

# choose a database to connect to (.london)
db_london = db_client.london

# choose a collection
db_london_events = db_london['events']
db_london_artist = db_london['artists']


# lookup all the documents in a collection
db_london_events.find()

# lookup documents based on a query
db_london_events.find({'event_id': your_event_id})
