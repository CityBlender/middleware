import json
import os, errno
import random
import requests
from pprint import pprint

import settings
import utils.dataHelper as dataHelper
import utils.dropboxHelper as dropboxHelper


# get random set of APP credentials
foursquare_credentials = [
  [os.getenv('FQ_CLIENT_ID_1'), os.getenv('FQ_CLIENT_SECRET_1')],
  [os.getenv('FQ_CLIENT_ID_2'), os.getenv('FQ_CLIENT_SECRET_2')]
]

foursquare_api_version = '20180513'

def getFqClient():
  client = random.choice (foursquare_credentials)
  return client

# print console header
def printHeader():
  return dataHelper.printHeader('Foursquare:')

# print green
def printGreen(string):
  return dataHelper.printGreen(string)


###################
### findVenue() ###
###################
def findVenue(venue_input):
  # get API call parameters
  lng = venue_input['location']['lng']
  lat = venue_input['location']['lat']
  ll = str(lat) + ',' + str(lng)

  name = venue_input['name']

  client = getFqClient()
  client_id = client[0]
  client_secret = client[1]

  url = 'https://api.foursquare.com/v2/venues/search'

  if lng:
    # define parameters for API call
    params = dict(
      client_id=client_id,
      client_secret=client_secret,
      v=foursquare_api_version,
      ll = ll,
      intent = 'match',
      query = name
    )
  else:
    # define parameters for API call if there is no exact location
    params = dict(
      client_id=client_id,
      client_secret=client_secret,
      v=foursquare_api_version,
      intent = 'browse',
      near = 'London, GB',
      radius = 100,
      query = name
    )

  # get JSON response
  data = dataHelper.getResponse(url, params)

  # return response
  return data


########################
### fetchVenueData() ###
########################
def fetchVenueData(venue_input):
  # find venue first
  venue_data = findVenue(venue_input)


  if not venue_data['response']['venues']:
    data = {}
    pass
  else:
    # get venue id
    venue_id = venue_data['response']['venues'][0]['id']

    # get API parameters
    client = getFqClient()
    client_id = client[0]
    client_secret = client[1]

    url = 'https://api.foursquare.com/v2/venues/' + venue_id

    # set parameters for API call
    params = dict(
      client_id=client_id,
      client_secret=client_secret,
      v=foursquare_api_version
    )

    # get JSON response
    data = dataHelper.getResponse(url, params)

  # return data
  return data


########################
### getVenueObject() ###
########################
def getVenueObject(venue_input):
  # get JSON response
  venue_source = fetchVenueData(venue_input)

  if not venue_source:
    venue_object = {}
    pass
  else:

    # get venue data
    venue = venue_source['response']['venue']

    # construct basic venue object
    venue_object = {
      'id': venue['id'],
      'name': venue['name'],
      'fq_url': venue['shortUrl']
    }

    if 'location' in venue:
      location_object = {}
      if 'address' in venue['location']:
        location_object['address'] = venue['location']['address']
      if 'postalCode' in venue['location']:
        location_object['zip'] = venue['location']['postalCode']
      if 'city' in venue['location']:
        location_object['city'] = venue['location']['city']
      venue_object['location'] = location_object

    # get price
    if 'price' in venue:
      venue_object['price'] = {
        'tier': venue['price']['tier'],
        'message': venue['price']['message'],
        'currency': venue['price']['currency']
      }

    # get description
    if 'description' in venue:
      venue_object['description'] = venue['description']

    # get likes
    if 'likes' in venue:
      if 'count' in venue['likes']:
        venue_object['likes'] = venue['likes']['count']

      if 'summary' in venue['likes']:
        venue_object['likes_summary'] = venue['likes']['summary']

    # get photo
    if 'bestPhoto' in venue:
      photo_object = {
        'prefix': venue['bestPhoto']['prefix'],
        'suffix': venue['bestPhoto']['suffix']
      }
      venue_object['photo'] = photo_object

    # get contact info
    if 'contact' in venue:
      contact = venue['contact']
      contact_object = {}
      if 'phone' in contact:
        contact_object['phone'] = contact['phone']
      if 'twitter' in contact:
        contact_object['twitter'] = contact['twitter']
      if 'instagram' in contact:
        contact_object['instagram'] = contact['instagram']
      if 'facebook' in contact:
        contact_object['facebook'] = contact['facebook']
      if 'facebookUsername' in contact:
        contact_object['facebook_username'] = contact['facebookUsername']
      if 'facebookName' in contact:
        contact_object['facebook_name'] = contact['facebookName']

      # append final contact object
      venue_object['contact'] = contact_object

    # get url
    if 'url' in venue:
      venue_object['contact']['url'] = venue['url']

    # get rating
    if 'rating' in venue:
      venue_object['rating'] = venue['rating']
      venue_object['rating_color'] = venue['ratingColor']

    # get tips
    if 'tips' in venue:
      tips = venue['tips']['groups'][0]['items']
      tips_array = []

      for tip in tips:
        tip_object = {
          'text': tip['text'],
          'url': tip['canonicalUrl'],
          'user': {
            'first_name': tip['user']['firstName'],
            'photo': {
              'prefix': tip['user']['photo']['prefix'],
              'suffix': tip['user']['photo']['suffix']
            }
          }
        }
        tips_array.append(tip_object)

      # attach tips array to venue
      venue_object['tips'] = tips_array

      # return complete object
      print(printHeader() + ' Retuning an object for ' + printGreen(venue_object['name']))

  return venue_object
