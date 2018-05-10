import dateutil
import json
import os, errno
import random
import requests
from pprint import pprint

import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper

import data.lastfm as lastfm
import data.spotify as spotify
import data.musixmatch as musix


#######################
### getArtistRef() ###
#######################
def getArtistRef(artist):
  artist_id = artist['id']
  artist_name = artist['name']
  artist_mbid_object = artist['mbid']

  artist_ref = {
    'id': artist_id,
    'name': artist_name,
  }

  # create an empty list of mbid-s and loop through them
  mbid_array = []
  for mbid in artist_mbid_object:
    mbid_array.append(mbid)

  # if there is mbid add it to reference object
  if mbid_array:
    artist_ref['mbid'] = mbid_array[0]
  # otherwise leave it empty
  else:
    artist_ref['mbid'] = ''

  # return reference
  return artist_ref

# create a single artist object
def getArtistObject(artist_ref):
  artist_name = artist_ref['name']
  artist_id = artist_ref['id']
  artist_mbid = artist_ref['mbid']

  # mbid based artist lookup
  if (artist_mbid):
    last_data = lastfm.returnArtistObject(artist_ref)

  # search based artist lookup
  else:
    last_data = lastfm.returnArtistObject(search=search)

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

  # return aggregate object
  return artist_object