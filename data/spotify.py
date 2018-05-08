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

spotify_credentials = [
  [os.getenv('SPOTIFY_CLIENT_ID_1'), os.getenv('SPOTIFY_CLIENT_SECRET_1')]
]

def connectSpotify():
  client = random.choice (spotify_credentials)
  client_id = client[0]
  client_secret = client[1]

  client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

  spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

  return spotify


# search for artist by query
def searchArtist(search):

  # configure connection to API
  spotify = connectSpotify()

  # get results
  results = spotify.search(q='artist:' + search, type='artist')

  # print progress
  print('Got search results for ' + '\033[92m' + search + '\033[0m')

  # return JSON
  return results


# get artist info based on a search
def getArtistInfo(search):
  # get results
  search_results = searchArtist(search)

  # get first result (let's just assume that is the most relevant one, right..)
  artist = search_results['artists']['items'][0]

  # create an artist object
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

  print('Got artist information for ' + '\033[92m' + artist['name'] + '\033[0m')

  return artist_object


# get top tracks for an artist
def getArtistTopTracks(search):
  # get artist information first
  artist = getArtistInfo(search)
  artist_id = artist['id']

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

  # print results to console
  print('Got Top Tracks data for ' + '\033[92m' + artist['name'] + '\033[0m')

  # return
  return top_tracks_array



