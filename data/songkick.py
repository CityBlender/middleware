import json
import os
import random
import requests

# SongKick API keys
songkick_keys = ([
  os.getenv('SK_API_KEY_1'),
  os.getenv('SK_API_KEY_2')
])

# get random SongKick API key function
def getSongkickKey():
  key = random.choice (songkick_keys)
  print('using Songkick key: ' + key)
  return key

# get gigs in given metropolitan area
def getGigs(metro_area_code, min_date, max_date):
  area = metro_area_code
  key = getSongkickKey()
  url = 'http://api.songkick.com/api/3.0/metro_areas/'+area+'/calendar.json?min_date='+min_date+'&max_date='+max_date+'&apikey='+key

  print(url)

  response = requests.get(url)
  data = json.loads(response.text)
  results = data['resultsPage']['results']['event']
  for event in results:
    event_id = event['id']
    event_type = event['type']
    event_url = event['uri']
    popularity = event['popularity']
    name = event['displayName']

    print(event['displayName'])


