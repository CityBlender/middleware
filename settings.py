# settings.py
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# load .env variables
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(base_dir, '.env')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file, verbose=True)



def checkEnvironment():
  environment = os.getenv('ENV')
  if environment == 'production':
    return 'production'
  elif environment == 'dev':
    return 'dev'
  else:
    pass

# get today's and tomorrows date in YYYY-MM-DD
date_format = '%Y-%m-%d'
today = datetime.datetime.now().strftime(date_format)
tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime(date_format)
today_plus_2 = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime(date_format)
today_plus_3 = (datetime.datetime.today() + datetime.timedelta(days=3)).strftime(date_format)
today_plus_4 = (datetime.datetime.today() + datetime.timedelta(days=4)).strftime(date_format)
today_plus_5 = (datetime.datetime.today() + datetime.timedelta(days=5)).strftime(date_format)
today_plus_6 = (datetime.datetime.today() + datetime.timedelta(days=6)).strftime(date_format)
today_plus_7 = (datetime.datetime.today() + datetime.timedelta(days=7)).strftime(date_format)
today_plus_8 = (datetime.datetime.today() + datetime.timedelta(days=8)).strftime(date_format)
today_plus_9 = (datetime.datetime.today() + datetime.timedelta(days=9)).strftime(date_format)



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

metro_asia = [
  ['Tokyo', '30717']
]

metro_oceania = [
  ['Brisbane', '26778'],
  ['Melbourne', '26790'],
  ['Sydney', '26794']
]

metro_test = [
  ['London', '24426']
]
