import dateutil
import json
import os, errno
import random
import requests
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials

import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper

# Last.fm API keys
musix_keys = ([
  os.getenv('MUSIX_API_KEY_1')
])

# get random Last.fm API key function
def getMusixKey():
  key = random.choice (musix_keys)
  return key


# get MusixMatch track id for better lyrics lookup
def getMusixId(mbid):
  # configure API call
  key = getMusixKey()
  url = 'http://api.musixmatch.com/ws/1.1/track.get?track_mbid=' + str(mbid) + '&apikey=' + str(key)

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

  # get the track data
  track_id = data['message']['body']['track']['track_id']

  # return JSON
  return track_id

# get track lyrics
def getTrackLyrics(mbid):
  # get MusixMatch track id first
  track_id = getMusixId(mbid)

  # configure API call
  key = getMusixKey()
  url = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id=' + str(track_id) + '&apikey=' + str(key)

  # get API response
  response = requests.get(url)

  # parse respons as JSON
  data = json.loads(response.text)

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

  return lyrics_object
