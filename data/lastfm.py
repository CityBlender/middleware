import dateutil
import json
import os, errno
import random
import requests
from pprint import pprint

import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper

# Last.fm API keys
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
    search = search.replace(' ', '%20')
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

  # print info to console
  name = data['artist']['name']
  print('Got JSON data for ' + '\033[92m' + name + '\033[0m')

  # return JSON
  return data


# dump artist info
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


# get artist tags
def getArtistTopTags(mbid=None, search=None):
  key = getLastKey()

  if (mbid is not None):
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&mbid=' + str(mbid) + '&api_key=' + str(key) + '&format=json'
  else:
    search = search.replace(' ', '%20')
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

  # get tags array
  tags_array = data['toptags']['tag']

  # print info to console
  name = data['toptags']['@attr']['artist']
  print('Got Top Tags data for ' + '\033[92m' + name + '\033[0m')

  return tags_array


# return last-fm artist object
def returnArtistObject(mbid=None, search=None):
  if (mbid is not None):
    data = getArtistInfo(mbid=mbid)
    tags = getArtistTopTags(mbid=mbid)
  else:
    data = getArtistInfo(search=search)
    tags = getArtistTopTags(search=search)

  artist = data['artist']

  artist_images = []

  # combine images into an array of objects
  for image in artist['image']:
    image = {
      'size': image['size'],
      'url': image['#text']
    }
    artist_images.append(image)

  # cobmine tags into an array of objects
  # for tag in artist['tags']['tag']:


  # put together a final object
  artist_object = {
    'name': artist['name'],
    'mbid': artist['mbid'],
    'url': artist['url'],
    'listeners': artist['stats']['listeners'],
    'playcount': artist['stats']['playcount'],
    'image': artist_images,
    'bio': {
      'summary': artist['bio']['summary'],
      'content': artist['bio']['content'],
      'url': artist['bio']['links']['link']['href'],
      'published': artist['bio']['published']
    },
    'tags': tags
  }

  # finally return an artist object
  pprint(artist_object)
  return artist_object

