import dateutil
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
  [os.getenv('FQ_CLIENT_ID_1'), os.getenv('FQ_CLIENT_SECRET_1')]
]

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
def findVenue(venue):
  # get API call parameters
  lng = venue['location']['x']
  lat = venue['location']['y']
  ll = str(lat) + ',' + str(lng)

  name = venue['name']

  client = getFqClient()
  client_id = client[0]
  client_secret = client[1]

  url = 'https://api.foursquare.com/v2/venues/search'

  # define parameters for API call
  params = dict(
    client_id=client_id,
    client_secret=client_secret,
    ll = ll,
    intent = 'match',
    name = name
  )

  # get JSON
  data = dataHelper.getResponse(url, params)

  pprint(data)

  return data