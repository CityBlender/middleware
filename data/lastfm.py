import dateutil
import json
import os, errno
import random
import requests
from pprint import pprint

import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper

# SongKick API keys
last_keys = ([
  os.getenv('LAST_API_KEY_1')
])

# get random Last.fm API key function
def getLastKey():
  key = random.choice (last_keys)
  return key

#  get artist info
def getArtistInfo(mbid=None, search=None):
  # configure API call
  key = getLastKey()

  if (mbid is not None):
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid=' + str(mbid) + '&api_key=' + str(key) + '&format=json'
  else:
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=' + search + '&api_key=' + str(key) + '&format=json'

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

  # print info to console
  name = data['artist']['name']
  print('Got JSON data for ' + '\033[92m' + name + '\033[0m')

  # return JSON
  return data

# dump artist by id
def dumpArtistInfo(mbid=None, search=None):
  if (mbid is not None):
    data = getArtistInfo(mbid=mbid)
  else:
    data = getArtistInfo(search=search)

  dump_dir = './temp/artist-json-dumps/last-fm/'
  dropbox_dir = '/data/artist-json-dumps/last-fm/'

  name = data['artist']['name']

  # define filename
  filename = name + '.json'

  # dump JSON
  dataHelper.dumpJson(filename, data, dump_dir)

  # save to Dropbox
  dropboxHelper.uploadToDrobpox(filename, dump_dir, dropbox_dir)

  print('Dumped JSON for ' + '\033[92m' + name + '\033[0m' + ' in ' + dropbox_dir)




