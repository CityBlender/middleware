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

spotify_credentials = [
  [os.getenv('SPOTIFY_CLIENT_ID_1'), os.getenv('SPOTIFY_CLIENT_SECRET_1')]
]

# print console header
def printHeader():
  return dataHelper.printHeader('Spotify:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)


# authorise and connect with Spotify API
def connectSpotify():
  client = random.choice (spotify_credentials)
  client_id = client[0]
  client_secret = client[1]

  client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

  spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

  return spotify


######################
### searchArtist() ###
######################
def searchArtist(artist_ref):
  # get artist name
  artist_name = artist_ref['name']

  # configure connection to API
  spotify = connectSpotify()

  # get JSON response
  results = spotify.search(q='artist:' + artist_name, type='artist')

  # get only artists field
  artists = results['artists']['items']

  # check if we got any results back
  if artists:
    # get first result (let's just assume that is the most relevant one, right..)
    artist = artists[0]
  else:
    # setting up dummy id to make later data handling easier
    artist = {}


  # return artist
  return artist


#######################
### getArtistInfo() ###
#######################
def getArtistInfo(artist):

  # get artist
  artist = artist

  # return dummy object if empty
  if not artist:
    artist_object = {}

  # otherwise create artist object
  else:
    artist_object = {
      'name': artist['name'],
      'type': artist['type'],
      'href': artist['external_urls']['spotify'],
      'id': artist['id'],
      'uri': artist['uri'],
      'popularity': artist['popularity'],
      'followers': artist['followers']['total'],
      'genre': artist['genres'],
      'image': artist['images']
    }

    print(printHeader() + ' Got data for ' + printGreen(artist_object['name']))


  # return artist object
  return artist_object


############################
### getArtistTopTracks() ###
############################
def getArtistTopTracks(artist):
  # get artist information first
  artist = artist
  artist_id = artist['id']
  artist_name = artist['name']

  if not artist_id:
    top_tracks_array = []
  else:
    # connect to Spotify
    spotify = connectSpotify()

    # get results
    top_tracks = spotify.artist_top_tracks(artist_id=artist_id, country='GB')

    # create empty array to be populated by top tracks
    top_tracks_array = []

    # construct an object for each track
    for track in top_tracks['tracks']:
      track_object = {
        'name': track['name'],
        'type': track['type'],
        'href': track['external_urls']['spotify'],
        'id': track['id'],
        'uri': track['uri'],
        'duration_ms': track['duration_ms'],
        'preview_url': track['preview_url'],
        'album': {
          'name': track['album']['name'],
          'type': track['album']['type'],
          'href': track['album']['external_urls']['spotify'],
          'id': track['album']['id'],
          'uri': track['album']['uri'],
          'release_date': track['album']['release_date'],
          'images': track['album']['images']
        }
      }

      # append track to top tracks array
      top_tracks_array.append(track_object)

    # GET TOP TRACK FEATURES
    # create an empty array for ids of top tracks
    top_track_ids = []

    # populate the array with ids of top tracks
    for track in top_tracks['tracks']:
      track_id = track['id']
      top_track_ids.append(track_id)

    # get track features for top tracks
    top_tracks_features = spotify.audio_features(tracks=top_track_ids)

    # lookup features base on track id
    for track in top_tracks_array:
      track_id = track['id']

      # assign feature as an additional object key
      for feature in top_tracks_features:
        if feature.get('id')==track_id:
          track['feature'] = feature

    # print progress to console
    print(printHeader() + ' Got top tracks for ' + printGreen(artist_name))


  # return
  return top_tracks_array


#########################
### getArtistObject() ###
#########################
def getArtistObject(artist_ref):

  # get artist
  artist_search = searchArtist(artist_ref)

  # return empty object if there are is no artist data
  if not artist_search:
    artist_object = {}

  # otherwise construct an artist object
  else:
    # get artist data
    artist_data = getArtistInfo(artist_search)

    # get artist's top tracks
    artist_tracks = getArtistTopTracks(artist_search)

    # assign top tracks to artist object
    artist_data['tracks'] = artist_tracks

    # assign data to an object
    artist_object = artist_data

  # print progress to console
  print_result = printHeader() + ' Returning an object for ' + printGreen(artist_ref['name'])
  print(print_result)

  # return complete artist object
  return artist_object
