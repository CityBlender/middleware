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

    # Spotify features
    danceability = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    duration = []
    time_signature = []

    # Spotify other
    spotify_genres = []
    spotify_popularity = []
    spotify_followers = []

    # Lastfm data
    lastfm_listeners = []
    lastfm_playcount = []
    lastfm_tags = []

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

      # get a subset of Spotify data to attach to event
      spotify_data = artistData.appendSpotifyData(artist_data)
      artist['spotify'] = spotify_data

      # add artist features to an aggregate event array
      if spotify_data:
        for item in [spotify_data]:
          spotify_followers.append(item['followers'])
          spotify_popularity.append(item['popularity'])

          spotify_genres.extend(item['genre'])
          danceability.extend(item['features']['danceability'])
          energy.extend(item['features']['energy'])
          key.extend(item['features']['key'])
          loudness.extend(item['features']['loudness'])
          mode.extend(item['features']['mode'])
          speechiness.extend(item['features']['speechiness'])
          acousticness.extend(item['features']['acousticness'])
          instrumentalness.extend(item['features']['instrumentalness'])
          liveness.extend(item['features']['liveness'])
          valence.extend(item['features']['valence'])
          tempo.extend(item['features']['tempo'])
          duration.extend(item['features']['duration_ms'])
          time_signature.extend(item['features']['time_signature'])
      else:
        pass

      # get last.fm data
      lastfm_data = artistData.appendLastfmData(artist_data)
      artist['lastfm'] = lastfm_data

      if lastfm_data:
        for item in [lastfm_data]:
          lastfm_listeners.extend(item['listeners'])
          lastfm_playcount.extend(item['playcount'])
          lastfm_tags.extend(item['tags'])
      else:
        pass

    # attach aggregate spotify data to event
    event['spotify'] = {
      'genres' : spotify_genres,
      'popularity' : spotify_popularity,
      'followers' : spotify_followers,
      'danceability' : danceability,
      'energy' : energy,
      'key' : key,
      'loudness' : loudness,
      'mode' : mode,
      'speechiness' : speechiness,
      'acousticness' : acousticness,
      'instrumentalness' : instrumentalness,
      'liveness' : liveness,
      'valence' : valence,
      'tempo' : tempo,
      'duration_ms' : duration,
      'time_signature' : time_signature
    }

    # attach aggregate lastfm date to event
    event['lastfm'] = {
      'listeners' : lastfm_listeners,
      'playcount' : lastfm_playcount,
      'tags': lastfm_tags
    }







    # store individual event into database
    dataHelper.dumpJson(event['name'] + '.json', event, './temp/final-event-db-dump/')



    # get selected data and attatch it to an artist in the event

    # store event into db
    # db.dbInsertEvents(events, events_collection)



