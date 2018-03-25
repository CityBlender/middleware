# settings.py
import os
import random
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)


# database
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
DB_COLL=os.getenv('DB_COLL')

# SongKick API
songkick_keys = ([
  os.getenv('SK_API_KEY_1'),
  os.getenv('SK_API_KEY_2')
])

# get random SongKick API key function
def getSongkickKey():
  key = random.choice (songkick_keys)
  print('using Songkick key: ' + key)
  return key

