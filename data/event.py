import os, errno
from pprint import pprint

import settings as settings
import utils.db as db
import utils.dataHelper as dataHelper
import data.songkick as sk
import data.lastfm as lastfm
import data.spotify as spotify
import data.artist as artistData

def fetchAll(area, events_collection, artist_collection, min_date = settings.today, max_date = settings.today):

  # get all the events
  events = sk.fetchGigs(metro_area_code=area, min_date=min_date, max_date=max_date)

  # loop throught each event
  for event in events:

    # get additional venue info via Foursquare

    # get all the artists
    artists = event['artists']

    # create empty features array to populate with artist data

    # loop throught artists
    for artist in artists:
      artist_ref = artistData.getArtistRef(artist)

      # get artist data from different APIs
      artist_data = artistData.getArtistObject(artist_ref)
      artist_object = artist_data

      # attach SongKick meta to artist object for easier cross-reference
      artist_object['id'] = artist_ref['id']
      artist_object['mbid'] = artist_ref['mbid']
      artist_object['name'] = artist_ref['name']

      # store stand-alone artist object into database
      # db.dbInsertArtist(artist_object, artist_collection)
      # features = artistData.appendSpotifyData(artist_data)
      # dataHelper.dumpJson(str(artist_ref['id'])+'.json', artist_data, './temp/artist-db-dump/')

      # get a subset of Spotify data to attach to event
      artist['spotify'] = artistData.appendSpotifyData(artist_data)
      artist['lastfm'] = artistData.appendLastfmData(artist_data)
      # spotify = artistData.appendSpotifyData(artist_data)

      # loop through Spotify artist data
      # spotify_features = spotify['tracks']





    # store individual event into database
    dataHelper.dumpJson(event['name'] + '.json', event, './temp/final-event-db-dump/')



    # get selected data and attatch it to an artist in the event

    # store event into db
    # db.dbInsertEvents(events, events_collection)



