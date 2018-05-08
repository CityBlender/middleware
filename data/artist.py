import dateutil
import json
import os, errno
import random
import requests
from pprint import pprint

import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper

import data.lastfm as last
import data.spotify as spotify
import data.musixmatch as musix

# create a single artist object
def getArtistObject(mbid=None, search=None):
  # mbid based artist lookup
  if (mbid is not None):
    last_data = last.returnArtistObject(mbid=mbid)
    artist_name = last_data['name']
    spotify_data = spotify.returnArtistObject(artist_name)

  # search based artist lookup
  else:
    last_data = last.returnArtistObject(search=search)
    artist_name = last_data['name']
    spotify_data = spotify.returnArtistObject(artist_name)

  artist_object = {
    'name': artist_name,
    'last_fm': last_data,
    'spotify': spotify_data
  }

  # get last.fm tracks
  tracks = artist_object['last_fm']['tracks']

  # look for tracks with mbid
  for track in tracks:
    track_mbid = track['mbid']
    if (len(track_mbid) > 0):
      # track.get('mbid')==track_mbid:
      lyrics = musix.getTrackLyrics(track_mbid)
      track['lyrics'] = lyrics
    else:
      pass

  return artist_object