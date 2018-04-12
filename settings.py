# settings.py
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# load .env variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# get today's date
today = datetime.datetime.now().strftime('%Y-%m-%d') # YYYY-MM-DD

# SongKick metropolitan area codes
metro_uk = [
  ['Birmingham', '24542'],
  ['Belfast', '24523'],
  ['Brighton', '24554'],
  ['Bristol', '24521'],
  ['Edinburgh', '24551'],
  ['Glasgow', '24473'],
  ['Liverpool', '24526'],
  ['London', '24426'],
  ['Manchester', '24475'],
  ['Newcastle', '24577']
]

metro_eur = [
  ['Amsterdam', '31366'],
  ['Barcelona', '28714'],
  ['Berlin', '28443'],
  ['Dublin', '29314'],
  ['Moscow', '32051'],
  ['Paris', '28909'],
  ['Prague', '28425']
]

metro_americas = [
  ['Buenos-Aires', '32911'],
  ['Mexico-City', '34385'],
  ['New-York', '7644'],
  ['San-Francisco', '26330'],
  ['Sao-Paulo', '27274'],
  ['Toronto', '27396']
]

metro_oceania = [
  ['Brisbane', '26778'],
  ['Melbourne', '26790'],
  ['Sydney', '26794']
]

