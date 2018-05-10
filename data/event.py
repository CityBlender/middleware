import os, errno
from pprint import pprint

import settings as settings
import utils.db as db
import data.songkick as sk
import data.lastfm as lastfm
import data.artist as artistData

def fetchAll(area, events_collection, artist_collection, min_date = settings.today, max_date = settings.today):
  # get all the events
  events = sk.fetchGigs(metro_area_code=area, min_date=min_date, max_date=max_date)

  # loop throught each event
  for event in events:

    # get all the artists
    artists = event['artists']

    # loop throught artists
    for artist in artists:
      artist_ref = artistData.getArtistRef(artist)
      artist_lastfm = lastfm.getArtistInfo(artist_ref)
      # artist_data = artistData.getArtistObject(artist_ref)

      # store entire artist data object into database first
      # db.dbInsertArtist(artist_data, artist_collection)

      # get selected data and attatch it to an artist in the event

    # store event into db
    # db.dbInsertEvents(events, events_collection)



