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


###########################
### appendSpotifyData() ###
###########################
def appendSpotifyData(artist_data):
  # get Spotify data
  spotify = artist_data['spotify']

  # append empty object if there is no data
  if not spotify:
    artist = {}

  # append Spotify data otherwise
  else:
    artist = {
      'name': spotify['name'],
      'href': spotify['href'],
      'popularity': spotify['popularity'],
      'followers': spotify['followers'],
      'genre': spotify['genre'],
      'image': spotify['image']
    }

    # loop through Spotify tracks
    spotify_tracks = spotify['tracks']
    spotify_tracks_array = []

    for track in spotify_tracks:
      track_info = {
        'name': track['name'],
        'href': track['href'],
        'duration_ms': track['duration_ms'],
        'preview_url': track['preview_url'],
        'feature': {
          'danceability': track['feature']['danceability'],
          'energy': track['feature']['energy'],
          'key': track['feature']['key'],
          'loudness': track['feature']['loudness'],
          'mode': track['feature']['mode'],
          'speechiness': track['feature']['speechiness'],
          'acousticness': track['feature']['acousticness'],
          'instrumentalness': track['feature']['instrumentalness'],
          'liveness': track['feature']['liveness'],
          'valence': track['feature']['valence'],
          'tempo': track['feature']['tempo'],
          'time_signature': track['feature']['time_signature']
        }
      }
      spotify_tracks_array.append(track_info)

    # append array of tracks to spotify artist data
    artist['tracks'] = spotify_tracks_array

  # return new object
  return artist


###########################
### appendLastmData() ###
###########################
def appendLastfmData(artist_data):
  # get lastfm data
  lastfm = artist_data['lastfm']

  # append empty object if there is no data
  if not lastfm:
    artist = {}
  else:
    artist = {
      'url': lastfm['url'],
      'listeners': lastfm['listeners'],
      'playcount': lastfm['playcount'],
      'image': lastfm['image'],
    }

    # loop through lastfm tags
    lastfm_tags = lastfm['tags']
    lastfm_tags_array = []

    for tag in lastfm_tags:
      tag_info = {
        'name': tag['name'],
        'count': tag['count']
      }
      lastfm_tags_array.append(tag_info)

    # append to artist object
    artist['tags'] = lastfm_tags_array

    # loop through lastfm tracks
    lastfm_tracks = lastfm['tracks']
    lastfm_tracks_array = []

    for track in lastfm_tracks:
      track_info = {
        'name': track['name'],
        'playcount': track['playcount'],
        'listeners': track['listeners'],
        'rank': track['rank'],
      }
      lastfm_tracks_array.append(track_info)

    # append to artist object
    artist['tracks'] = lastfm_tracks_array

  # return artist object
  return artist