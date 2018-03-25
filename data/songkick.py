import json
import os
import random
import requests

# SongKick API keys
songkick_keys = ([
  os.getenv('SK_API_KEY_1'),
  os.getenv('SK_API_KEY_2')
])

# SongKick metropolitan area codes
metro_london = '24426'

# get random SongKick API key function
def getSongkickKey():
  key = random.choice (songkick_keys)
  print('using Songkick key: ' + key)
  return key

# get gigs in given metropolitan area
def getGigs(metro_area_code):
  area = metro_area_code
  key = getSongkickKey()
  url = 'http://api.songkick.com/api/3.0/metro_areas/'+area+'/calendar.json?apikey='+key

  response = requests.get(url)
  data = json.loads(response.text)
  results = data['resultsPage']['results']
  print(json.dumps(results, indent=4))


