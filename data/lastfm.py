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

# set URL base
api_url_base = 'http://ws.audioscrobbler.com/2.0/'

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

  ### mbid lookup
  if artist_mbid:
    url = api_url_base + '?method=artist.getinfo&mbid=' + str(artist_mbid) + '&api_key=' + str(key) + '&format=json'

    # get JSON response
    data = dataHelper.getJson(url)

    # if mbid returns an error try search instead
    if 'error' in data:
      print(printHeader() + ' Cannot find ' + printGreen(artist_name) + ' by mbid. Trying search instead.')

      # escape spaces for URL lookup
      search = artist_name.replace(' ', '%20')
      url = api_url_base + '?method=artist.getinfo&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'

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
    url = api_url_base + '?method=artist.getinfo&artist=' + search + '&api_key=' + str(key) + '&autocorrect=1&format=json'
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
  return data_return


##########################
### getArtistTopTags() ###
##########################
def getArtistTopTags(artist_ref):

  # get API key
  key = getLastKey()

  # get artist data
  data = getArtistInfo(artist_ref)

  # return empty array if the artist object is empty
  if not data:
    top_tags_return = []
  else:
    # get artist object
    artist = data['artist']

    # set API call URL via mbid if available
    if 'mbid' in artist:
      url = api_url_base + '?method=artist.gettoptags&mbid=' + artist['mbid'] + '&api_key=' + str(key) + '&format=json'
      tags_data = dataHelper.getJson(url)

    # use name otherwise
    else:
      search = artist['name'].replace(' ', '%20')
      url = api_url_base + '?method=artist.gettoptags&artist=' + search + '&api_key=' + str(key) + '&format=json'
      tags_data = dataHelper.getJson(url)

    # read in actual tags data
    tags = tags_data['toptags']['tag']

    # only get top 10 tags
    tags_reduced = tags[:10]

    print(printHeader() + ' Got top 10 tags for ' + printGreen(artist_ref['name']))

    dataHelper.dumpJson('last-fm-'+ artist_ref['name'] + '-top-tags-reduced.json', tags_reduced, './temp/last-fm-dumps/')

    # return top 10 tags
    return tags_reduced





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

