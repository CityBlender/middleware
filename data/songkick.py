import json
import os
import pandas as pd
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

  response = requests.get(url)
  data = json.loads(response.text)
  results = data['resultsPage']['results']['event']

  for event in results:

    # event meta
    event_id = event['id']
    event_type = event['type']
    event_url = event['uri']
    event_popularity = event['popularity']
    event_name = event['displayName']

    # time
    start_datetime = event['start']['datetime']
    start_date = event['start']['date']
    start_time = event['start']['time']

    # generic location
    location_lng = event['location']['lng']
    location_lat = event['location']['lat']

    # venue info
    venue_id = event['venue']['id']
    venue_name = event['venue']['displayName']
    venue_lng = event['venue']['lng']
    venue_lat = event['venue']['lat']

    artist_list = []

    # artist(s)
    for artist in event['performance']:
      artist_name = artist['displayName']
      artist_billing_index = artist['billingIndex']
      artist_billing = artist['billing']
      artist_id = artist['artist']['id']
      artist_url = artist['artist']['uri']
      artist_mbid = []

      for identifier in artist['artist']['identifier']:
        mbid = identifier['mbid']
        artist_mbid.append(mbid)

      artist_object = {
        'mbid': artist_mbid,
        'id': artist_id,
        'name': artist_name,
        'songkick_url': artist_url,
        'billing_index': artist_billing_index,
        'artist_billing': artist_billing
      }

      artist_list.append(artist_object)

    # ger everything ready for database query



