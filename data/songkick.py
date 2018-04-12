import json
import os, errno
import pandas as pd
import random
import requests

import settings
import data.dataHelper as dataHelper
import data.dropboxHelper as dropboxHelper

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


#
# getGigs() - generic function for returning raw SongKick JSON based on input parameters
#

def getGigs(metro_area_code, min_date = settings.today, max_date = settings.today, results = 50, page = 1):
  # configure API call
  area = metro_area_code
  key = getSongkickKey()
  url = 'http://api.songkick.com/api/3.0/metro_areas/'+area+'/calendar.json?min_date='+min_date+'&max_date='+max_date+'&per_page='+str(results)+'&page='+str(page)+'&apikey='+key

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

  # return JSON
  return data


#
# dumpGigs() - function for dumping raw SongKick JSON into Dropbox directory
#

def dumpGigs(metro_area_code, min_date=settings.today, max_date=settings.today):
  results = 50 # get the max number by default
  page = 1 # get first page
  dump_dir = './temp/songkick-json-dumps/'
  dropbox_dir = '/data/songkick-json-dumps/'

  # get first page
  data = getGigs(metro_area_code, min_date, max_date, results, page)

  # define filename
  filename = metro_area_code + '__' + min_date + '__' + max_date + '__' + str(page) + '.json'

  # dump first page
  dataHelper.dumpJson(filename, data, dump_dir)

  # save to Dropbox
  dropboxHelper.uploadToDrobpox(filename, dump_dir, dropbox_dir)

  # get total number of entries from the call
  total_entries = data['resultsPage']['totalEntries']
  print('There are total of ' + str(total_entries) + ' entries matching your call')

  while total_entries > results :
    page = page + 1 # increase page count
    total_entries = total_entries - results # reduce total by
    filename = metro_area_code + '__' + min_date + '__' + max_date + '__' + str(page) + '.json' # update filename to reflect new page count
    data = getGigs(metro_area_code, min_date, max_date, results, page) # fetch additional page

    # dump additional page
    dataHelper.dumpJson(filename, data, dump_dir)

    # save additional page to Dropbox
    dropboxHelper.uploadToDrobpox(filename, dump_dir, dropbox_dir)

  # finally get rid of the temp folder
  # dataHelper.removeDirectory(dump_dir)



#
# fetchGigs() - fetches Gigs
#

def fetchGigs(data):
  results = data['resultsPage']['results']['event']

  all_events = []

  for event in results:
    artist_list = []

    # create artist list
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

    # put everything together into an object
    event_object = {
      # event meta
      'event_id': event['id'],
      'event_type': event['type'],
      'event_url': event['uri'],
      'event_popularity': event['popularity'],
      'event_name': event['displayName'],

      # time
      'start_datetime': event['start']['datetime'],
      'start_date': event['start']['date'],
      'start_time': event['start']['time'],

      # generic location
      'location_lng': event['location']['lng'],
      'location_lat': event['location']['lat'],

      # venue info
      'venue_id': event['venue']['id'],
      'venue_name': event['venue']['displayName'],
      'venue_lng': event['venue']['lng'],
      'venue_lat': event['venue']['lat'],

      # artist
      'artists': artist_list
    }

    all_events.append(event_object)

  # return all events
  return all_events
