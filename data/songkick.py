import dateutil
import dateutil.parser
import json
import os, errno
import random
import requests
from pprint import pprint


import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper

# SongKick API keys
songkick_keys = ([
  os.getenv('SK_API_KEY_1'),
  os.getenv('SK_API_KEY_2'),
  os.getenv('SK_API_KEY_3'),
  os.getenv('SK_API_KEY_4')
])

# get random SongKick API key function
def getSongkickKey():
  key = random.choice (songkick_keys)
  return key

# print console header
def printHeader():
  return dataHelper.printHeader('SongKick:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)


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

def dumpGigs(area, metro_area_code, folder, min_date = settings.tomorrow, max_date = settings.tomorrow):
  results = 50 # get the max number by default
  page = 1 # get first page
  dump_dir = './temp/songkick-json-dumps/'
  dropbox_dir = '/data/songkick-json-dumps/' + folder

  # get first page
  data = getGigs(metro_area_code, min_date, max_date, results, page)

  # define filename
  filename_root = area + '_(' + min_date + ')_page-'
  filename_init = filename_root  + str(page) + '.json'

  # dump first page
  dataHelper.dumpJson(filename_init, data, dump_dir)

  # save to Dropbox
  dropboxHelper.uploadToDrobpox(filename_init, dump_dir, dropbox_dir)

  # get total number of entries from the call
  total_entries = data['resultsPage']['totalEntries']
  print('\033[92m' + str(total_entries) + '\033[0m' + ' entries for ' + area + ' on ' + min_date)

  while total_entries > results :
    page = page + 1 # increase page count
    total_entries = total_entries - results # reduce total by
    filename = filename_root + str(page) + '.json' # update filename to reflect new page count
    data = getGigs(metro_area_code, min_date, max_date, results, page) # fetch additional page

    # dump additional page
    dataHelper.dumpJson(filename, data, dump_dir)

    # save additional page to Dropbox
    dropboxHelper.uploadToDrobpox(filename, dump_dir, dropbox_dir)

  # finally get rid of the temp folder
  dataHelper.removeDirectory(dump_dir)



#
# getEventsObject()
#
def getEventsObject(data):
  events = data['resultsPage']['results']['event']
  all_events = []

  for event in events:
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

    # convert dates into correct format for MongoDB
    event_datetime_string = event['start']['datetime']
    if event_datetime_string is not None:
      event_datetime = dateutil.parser.parse(event_datetime_string)
      # event_datetime = str(event_datetime)
    else:
      event_datetime = ''

    # put everything together into an object
    event_object = {
      # event meta
      'id': event['id'],
      'name': event['displayName'],
      'type': event['type'],
      'url': event['uri'],
      'popularity': event['popularity'],

      # time
      'date': event['start']['date'],
      'time': event['start']['time'],
      'datetime': event_datetime,
      'datetime_source': event['start']['datetime'],

      # location
      'location': {
        'lng': event['location']['lng'],
        'lat': event['location']['lat']
      },

      # venue info
      'venue': {
        'id': event['venue']['id'],
        'name': event['venue']['displayName'],
        'location': {
          'lng': event['venue']['lng'],
          'lat': event['venue']['lat']
        }
      },

      # artist
      'artists': artist_list
    }

    all_events.append(event_object)

  # return all events
  return all_events



#
# fetchGigs() - fetches Gigs
#

def fetchGigs(metro_area_code, min_date = settings.today, max_date = settings.today):
  results = 50 # get the max number by default
  page = 1 # get first page
  events_list = [] # create empty list

  # get first batch of events
  data = getGigs(metro_area_code, min_date, max_date, results, page)

  # add first list of events dicitionaries
  events_list = getEventsObject(data)

  # find out the total number of entries for given call
  total_entries = data['resultsPage']['totalEntries']

  while total_entries > results :
    page = page + 1 # increase page count
    total_entries = total_entries - results # reduce total

    data = getGigs(metro_area_code, min_date, max_date, results, page) # fetch additional page

    # add additional page of events dictionaries
    # - we are concatenating the lists instead of appending them so we only get a single list of dictionaries
    events_list = events_list + getEventsObject(data)

  # return object with all events for given dates
  print(printHeader() + ' Fetched ' + printGreen(str(total_entries)) + ' entries for ' + metro_area_code + ' on ' + min_date)

  return events_list




# functions put together
def dumpUk():
  for city in settings.metro_uk:
    area = city[0]
    code = city[1]
    dumpGigs(area, code, 'uk/')

def dumpEur():
  for city in settings.metro_eur:
    area = city[0]
    code = city[1]
    dumpGigs(area, code, 'eur/')

def dumpAmericas():
  for city in settings.metro_americas:
    area = city[0]
    code = city[1]
    dumpGigs(area, code, 'americas/')

def dumpAsia():
  for city in settings.metro_asia:
    area = city[0]
    code = city[1]
    dumpGigs(area, code, 'asia/')

def dumpOceania():
  for city in settings.metro_oceania:
    area = city[0]
    code = city[1]
    dumpGigs(area, code, 'oceania/')

def dumpTest():
  for city in settings.metro_test:
    area = city[0]
    code = city[1]
    dumpGigs(area, code, 'test/')
