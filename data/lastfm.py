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
def getArtistById(mbid):
  # configure API call
  key = getLastKey()
  url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=Cher&api_key=' + str(key) + '&mbid' + str(mbid) + '&format=json'

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

  # print info to console
  name = data['artist']['name']
  print('Got JSON data for ' + '\033[92m' + name + '\033[0m')

  # return JSON
  return data


# dump artist
def dumpArtist(mbid):
  data = getArtistById(mbid)
  dump_dir = './temp/artist-json-dumps/last-fm/'
  dropbox_dir = '/data/artist-json-dumps/last-fm/'

  name = data['artist']['name']

  # define filename
  filename = name + '-' + mbid + '.json'

  # dump JSON
  dataHelper.dumpJson(filename, data, dump_dir)

  # save to Dropbox
  dropboxHelper.uploadToDrobpox(filename, dump_dir, dropbox_dir)

  print('Dumped JSON for ' + '\033[92m' + name + '\033[0m' + ' in ' + dropbox_dir)



