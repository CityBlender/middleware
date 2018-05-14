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
  os.getenv('LAST_API_KEY_1'),
  os.getenv('LAST_API_KEY_2')
])

# set URL base
api_url_base = 'http://ws.audioscrobbler.com/2.0/'

# get random Last.fm API key function
def getLastKey():
  key = random.choice (last_keys)
  return key

# print console header
def printHeader():
  return dataHelper.printHeader('Last.Fm:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)

# load JSON
def getJson(url):
  return dataHelper.getJson(url)


#######################
### getArtistInfo() ###
#######################
def getArtistInfo(artist_ref):

  artist_name = artist_ref['name']
  artist_mbid = artist_ref['mbid']

  # get API key
  key = getLastKey()

  ### mbid lookup
  if artist_mbid:
    url = api_url_base + '?method=artist.getinfo&mbid=' + str(artist_mbid) + '&api_key=' + str(key) + '&format=json'

    # get JSON response
    data = getJson(url)

    # if mbid returns an error try search instead
    if 'error' in data:
      # escape spaces for URL lookup
      search = artist_name.replace(' ', '%20')
      url = api_url_base + '?method=artist.getinfo&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'

      #get JSON response
      data = getJson(url)

      # set empty object if no artist is found
      if 'error' in data:
        # print(printHeader() + ' Cannot find' + printGreen(artist_name) + ' using search. Returning empty object.')
        data_return = {}

      # return a first search result
      else:
        # print(printHeader() + ' Got data for ' + printGreen(artist_name) + ' using search.')
        data_return = data

    # return data if found using mbid
    else:
      # print(printHeader() + ' Got data for ' + printGreen(artist_name) + ' using mbid.')
      data_return = data

  ### search lookup
  else:
    # escape spaces so the name can be parsed via url
    search = artist_name.replace(' ', '%20')
    url = api_url_base + '?method=artist.getinfo&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'
    data = getJson(url)

    # set empty object if no artist is found
    if 'error' in data:
      # print(printHeader() + ' Cannot find ' + printGreen(artist_name) + ' using search. Returning empty object.')
      data_return = {}
    # otherwise return search results
    else:
      # print(printHeader() + ' Got data for ' + printGreen(artist_name) + ' using search.')
      data_return = data

  # finally return the object
  return data_return


##########################
### getArtistTopTags() ###
##########################
def getArtistTopTags(data):

  # get API key
  key = getLastKey()

  # get artist data
  data = data

  # return empty array if the artist object is empty
  if not data:
    top_tags_return = []
  else:
    # get artist object
    artist = data['artist']

    # set API call URL via mbid if available
    if 'mbid' in artist:
      url = api_url_base + '?method=artist.gettoptags&mbid=' + artist['mbid'] + '&api_key=' + str(key) + '&format=json'
      tags_data = getJson(url)

    # use name otherwise
    else:
      search = artist['name'].replace(' ', '%20')
      url = api_url_base + '?method=artist.gettoptags&artist=' + search + '&api_key=' + str(key) + '&format=json'
      tags_data = getJson(url)

    # read in actual tags data
    tags = tags_data['toptags']['tag']

    # only get top 10 tags
    tags_reduced = tags[:10]

    top_tags_return = tags_reduced
    # print(printHeader() + ' Got top 10 tags for ' + printGreen(artist['name']))

  # return top 10 tags
  return top_tags_return




############################
### getArtistTopTracks() ###
############################
def getArtistTopTracks(data):

  # get API key
  key = getLastKey()

  # get artist data
  data = data

  # return empty array if the artist object is empty
  if not data:
    top_tracks_return = []
  else:
    # get artist object
    artist = data['artist']

    # set API call URL via mbid if available
    if 'mbid' in artist:
      url = api_url_base + '?method=artist.gettoptracks&mbid=' + artist['mbid'] + '&api_key=' + str(key) + '&limit=10&format=json'
      tracks_data = getJson(url)

    # use name otherwise
    else:
      search = artist['name'].replace(' ', '%20')
      url = api_url_base + '?method=artist.gettoptracks&artist=' + search + '&api_key=' + str(key) + '&limit=10&autocorrect=1&format=json'
      tracks_data = getJson(url)

    # read in actual tracks data
    tracks = tracks_data['toptracks']['track']

    # create empty array to populate with tracks
    top_tracks_return = []

    # create an object for each track
    for track in tracks:
      track_object = {
        'name': track['name'],
        'playcount': int(track['playcount']),
        'listeners': int(track['listeners']),
        'url': track['url'],
        'rank': track['@attr']['rank']
      }

      # get mbid is track has one
      if 'mbid' not in track:
        track_object['mbid'] = ''
      else:
        track_object['mbid'] = track['mbid']

      # append individual track to top tracks array
      top_tracks_return.append(track_object)

  # return top 10 tracks
  # print(printHeader() + ' Got top 10 tracks for ' + printGreen(artist['name']))
  return top_tracks_return



############################
### getArtistObject() ###
############################
def getArtistObject(artist_ref):

  # get artist data
  artist_data = getArtistInfo(artist_ref)

  # return empty object if the artist is empty
  if not artist_data:
    artist_object = {}
  else:
    artist_tags = getArtistTopTags(artist_data)
    artist_tracks = getArtistTopTracks(artist_data)

    # get artist data
    artist = artist_data['artist']

    # set up mbid
    if 'mbid' in artist:
      artist_mbid = artist['mbid']
    else:
      artist_mbid = ''

    # get artist images array
    artist_images = []
    for image in artist['image']:
      image = {
        'url': image['#text'],
        'size': image['size']
      }
      artist_images.append(image)

    # put together a final artist object
    artist_object = {
      'name': artist['name'],
      'mbid': artist_mbid,
      'url': artist['url'],
      'listeners': int(artist['stats']['listeners']),
      'playcount': int(artist['stats']['playcount']),
      'image': artist_images,
      'bio': {
        'summary': artist['bio']['summary'],
        'content': artist['bio']['content'],
        'url': artist['bio']['links']['link']['href'],
        'published': artist['bio']['published']
      },
      'tags': artist_tags,
      'tracks': artist_tracks
    }

  # return complete artist object
  print_result = printHeader() + ' Returning an object for ' + printGreen(artist_ref['name'])
  print(print_result)
  return artist_object