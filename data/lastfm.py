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

# print console header
def printHeader():
  return dataHelper.printBold('Last.Fm:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)


#######################
### getArtistInfo() ###
#######################
def getArtistInfo(artist_ref):

  artist_name = artist_ref['name']
  artist_mbid = artist_ref['mbid']

  # get API key
  key = getLastKey()

  # get URL base
  url_base = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo'

  ### mbid lookup
  if artist_mbid:
    url = url_base + '&mbid=' + str(artist_mbid) + '&api_key=' + str(key) + '&format=json'

    # get JSON response
    data = dataHelper.getJson(url)

    # if mbid returns an error try search instead
    if 'error' in data:
      print(printHeader() + ' Cannot find ' + printGreen(artist_name) + ' by mbid. Trying search instead.')

      # escape spaces for URL lookup
      search = artist_name.replace(' ', '%20')
      url = url_base + '&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'

      #get JSON response
      data = dataHelper.getJson(url)

      # set empty object if no artist is found
      if 'error' in data:
        print(printHeader() + ' Cannot find' + printGreen(artist_name) + ' by search either. Returning empty object.')
        data_return = {}

      # return a first search result
      else:
        print(printHeader() + ' Got data for ' + printGreen(artist_name) + ' using search. Returning populated object.')
        data_return = data

    # return data if found using mbid
    else:
      print(printHeader() + ' Got data for ' + printGreen(artist_name) + ' using mbid. Returning populated object.')
      data_return = data

  ### search lookup
  else:
    # escape spaces so the name can be parsed via url
    search = artist_name.replace(' ', '%20')
    url = url_base + '&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'
    data = dataHelper.getJson(url)

    # set empty object if no artist is found
    if 'error' in data:
      print(printHeader() + ' Cannot find ' + printGreen(artist_name) + ' using search. Returning empty object.')
      data_return = {}
    # otherwise return search results
    else:
      print(printHeader() + ' Got data for ' + printGreen(artist_name) + ' using search. Returning populated object.')
      data_return = data

  # finally return the object
  # print(data_return)
  return data_return


# get artist tags
# def getArtistTopTags(mbid=None, search=None):
#   key = getLastKey()

#   if (mbid is not None):
#     mbid_check = getArtistInfoById(mbid)
#     if mbid_check:
#       url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&mbid=' + str(mbid) + '&api_key=' + str(key) + '&format=json'
#     else:

#   else:
#     search = search.replace(' ', '%20')
#     url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'

#   # get API response
#   response = requests.get(url)

#   # parse respons as JSON
#   data = json.loads(response.text)

#   # pprint(data)

#   if 'error' in data:
#     print('Last.fm: ' + data['message'])
#     tags_array_reduced = {}
#   else:
#     # get tags object
#     tags_array = data['toptags']['tag']

#     # limit number of tags
#     tags_array_reduced = tags_array[:10]

#     # print info to console
#     name = data['toptags']['@attr']['artist']
#     print('Got Top Tags for ' + '\033[92m' + name + '\033[0m')

#   # return tags object
#   return tags_array_reduced


# get top tracks
# def getArtistTopTracks(mbid=None, search=None):

#   # configure API call
#   key = getLastKey()
#   if (mbid is not None):
#     url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&mbid=' + str(mbid) + '&api_key=' + str(key) + '&limit=10&format=json'
#   else:
#     search = search.replace(' ', '%20')
#     url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=' + search + '&api_key=' + str(key) + '&limit=10&autocorrect=1&format=json'

#   # get API response
#   response = requests.get(url)

#   # parse respons as JSON
#   data = json.loads(response.text)

#   # crete emtpy top tracks array
#   top_tracks = []

#   if 'error' in data:
#     pass
#   else:
#     for track in data['toptracks']['track']:
#       track_object = {
#         'name': track['name'],
#         'playcount': track['playcount'],
#         'listeners': track['listeners'],
#         'url': track['url'],
#         'rank': track['@attr']['rank']
#       }

#       if 'mbid' not in track:
#         track_object['mbid'] = ''
#       else:
#         track_object['mbid'] = track['mbid']

#       top_tracks.append(track_object)
#     name = data['toptracks']['@attr']['artist']
#     print('Got Top 10 Tracks for ' + '\033[92m' + name + '\033[0m')

#   return top_tracks


# # return last-fm artist object
# def returnArtistObject(mbid=None, search=None):
#   if (mbid):
#     data = getArtistInfo(mbid=mbid)
#     tags = getArtistTopTags(mbid=mbid)
#     tracks = getArtistTopTracks(mbid=mbid)
#     artist_mbid = mbid
#   else:
#     data = getArtistInfo(search=search)
#     tags = getArtistTopTags(search=search)
#     tracks = getArtistTopTracks(search=search)
#     artist_mbid = ''

#   if not data:
#     artist_object = {}
#   else:
#     artist = data['artist']

#     artist_images = []

#     # combine images into an array of objects
#     for image in artist['image']:
#       image = {
#         'size': image['size'],
#         'url': image['#text']
#       }
#       artist_images.append(image)

#     # put together a final object
#     artist_object = {
#       'name': artist['name'],
#       'mbid': artist_mbid,
#       'url': artist['url'],
#       'listeners': artist['stats']['listeners'],
#       'playcount': artist['stats']['playcount'],
#       'image': artist_images,
#       'bio': {
#         'summary': artist['bio']['summary'],
#         'content': artist['bio']['content'],
#         'url': artist['bio']['links']['link']['href'],
#         'published': artist['bio']['published']
#       },
#       'tags': tags,
#       'tracks': tracks
#     }

#     print('Returning a complete artist object for ' + '\033[92m' + artist['name'] + '\033[0m')

#   # finally return an artist object
#   return artist_object

