import json
import os, errno
import random
import requests
from pprint import pprint

import settings

# get MusixMatch API keys
musix_keys = ([
  os.getenv('MUSIX_API_KEY_1')
])

# get random MusixMatch API key
def getMusixKey():
  key = random.choice (musix_keys)
  return key

# print console header
def printHeader():
  return dataHelper.printHeader('MusixMatch:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)

# print underline
def printUnderline(string):
  return dataHelper.printUnderline(string)

# load JSON
def getJson(url):
  return dataHelper.getJson(url)


# set up API URL base
api_url_base = 'http://api.musixmatch.com/ws/1.1/'

####################
### getMusixId() ###
####################
def getMusixId(mbid):
  # configure API call
  key = getMusixKey()
  url = api_url_base + 'track.get?track_mbid=' + str(mbid) + '&apikey=' + str(key)

  # get data
  data = getJson(url)

  # get MusixMatch track id for better lyrics lookup
  track_id = data['message']['body']['track']['track_id']

  # return JSON
  return track_id

#######################
### getTrackLyrics() ###
#######################
def getTrackLyrics(mbid):
  # get MusixMatch track id first
  track_id = getMusixId(mbid)

  # configure API call
  key = getMusixKey()
  url = api_url_base + 'track.lyrics.get?track_id=' + str(track_id) + '&apikey=' + str(key)

  # get JSON response
  data = getJson(url)

  # get lyrics
  lyrics = data['message']['body']['lyrics']

  # if instrumental
  if (lyrics['instrumental'] == 1):
    lyrics_object = {
      'id': lyrics['lyrics_id'],
      'is_instrumental': '1',
      'url': lyrics['backlink_url']
    }
  # if not instrumental and is not restricted
  elif (lyrics['restricted'] == 0):
    lyrics_object = {
      'id': lyrics['lyrics_id'],
      'is_instrumental': '0',
      'is_restricted': '0',
      'url': lyrics['backlink_url'],
      'body': lyrics['lyrics_body'],
      'language': lyrics['lyrics_language'],
      'language_description': lyrics['lyrics_language_description'],
      'lyrics_copyright': lyrics['lyrics_copyright'],
      'tracking_url': {
        'script': lyrics['script_tracking_url'],
        'pixel': lyrics['pixel_tracking_url'],
        'html': lyrics['html_tracking_url']
      }
    }
  # if restricted
  else:
    lyrics_object = {
      'id': lyrics['lyrics_id'],
      'is_instrumental': '0',
      'is_restricted': '1',
      'url': lyrics['backlink_url'],
      'lyrics_copyright': lyrics['lyrics_copyright']
    }

  print(printHeader() + ' Got lyrics for ' + printGreen(artist_name))

  return lyrics_object
