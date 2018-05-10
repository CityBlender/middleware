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

#########################
### getArtistObject() ###
#########################
def getArtistObject(artist_ref):

  # get data from APIs
  lastfm_data = lastfm.getArtistObject(artist_ref)
  spotify_data = spotify.getArtistObject(artist_ref)

  # return a complete artist object
  artist_object = {
    'lastfm': lastfm_data,
    'spotify': spotify_data
  }

  # return aggregate object
  return artist_object