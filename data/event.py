import os, errno
from statistics import median
from statistics import median_low
from statistics import median_high
from statistics import mean
from statistics import pvariance
from scipy import stats
from pprint import pprint

import settings as settings
import utils.db as db
import utils.dataHelper as dataHelper
import data.songkick as sk
import data.lastfm as lastfm
import data.spotify as spotify
import data.foursquare as fq
import data.artist as artistData

def fetchAll(area, events_collection, artist_collection, min_date = settings.today, max_date = settings.today):

  # get all the events
  events = sk.fetchGigs(metro_area_code=area, min_date=min_date, max_date=max_date)

  # loop throught each event
  for event in events:
    event_id = event['id']

    if db.eventExists(event_id, events_collection):
      pass

    else:


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

        # get a subset of Spotify data to attach to event
        spotify_data = artistData.appendSpotifyData(artist_data)
        artist_object['spotify'] = spotify_data

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
        artist_object['lastfm'] = lastfm_data

        # finally insert each artist into database
        db.dbInsertArtist(artist_object, artist_collection)


        if lastfm_data:
          for item in [lastfm_data]:
            lastfm_listeners.append(item['listeners'])
            lastfm_playcount.append(item['playcount'])
            lastfm_tags.extend(item['tags'])
        else:
          pass

        if spotify_data:
          if spotify_data['features']['acousticness']:
            # attach aggregate spotify data to event
            event['spotify'] = {
              'genres' : spotify_genres,
              'popularity' : spotify_popularity,
              'popularity_median': median(spotify_popularity),
              'popularity_min': min(spotify_popularity),
              'popularity_max': max(spotify_popularity),
              'popularity_pvariance': pvariance(spotify_popularity),
              'followers' : spotify_followers,
              'followers_sum': sum(spotify_followers),
              'danceability' : danceability,
              'danceability_median': median(danceability),
              'danceability_min': min(danceability),
              'danceability_max': max(danceability),
              'danceability_pvariance': pvariance(danceability),
              'energy' : energy,
              'energy_median': median(energy),
              'energy_min': min(energy),
              'energy_max': max(energy),
              'enery_pvariance': pvariance(energy),
              'key' : key,
              'key_mode': stats.mode(key)[0].tolist(),
              'key_min': min(key),
              'key_max': max(key),
              'loudness' : loudness,
              'loudness_median': median(loudness),
              'loudness_min': min(loudness),
              'loudness_max': max(loudness),
              'loudness_pvariance': pvariance(loudness),
              'mode' : mode,
              'mode_mode': stats.mode(mode)[0].tolist(),
              'speechiness' : speechiness,
              'speechiness_median': median(speechiness),
              'speechines_min': min(speechiness),
              'speechines_max': max(speechiness),
              'speechines_pvariance': pvariance(speechiness),
              'acousticness' : acousticness,
              'acousticness_median': median(acousticness),
              'acousticness_min': min(acousticness),
              'acousticness_max': max(acousticness),
              'acousticness_pvariance': pvariance(acousticness),
              'instrumentalness' : instrumentalness,
              'instrumentalness_median': median(instrumentalness),
              'instrumentalness_min': min(instrumentalness),
              'instrumentalness_max': max(instrumentalness),
              'instrumentalness_pvariance': pvariance(instrumentalness),
              'liveness' : liveness,
              'liveness_median': median(liveness),
              'liveness_min': min(liveness),
              'liveness_max': max(liveness),
              'liveness_pvariance': pvariance(liveness),
              'valence' : valence,
              'valence_median': median(valence),
              'valence_min': min(valence),
              'valence_max': max(valence),
              'valence_pvariance': pvariance(valence),
              'tempo' : tempo,
              'tempo_median': median(tempo),
              'tempo_min': min(tempo),
              'tempo_max': max(tempo),
              'tempo_pvariance': pvariance(tempo),
              'duration_ms' : duration,
              'duration_ms_mean': mean(duration),
              'duration_ms_min': min(duration),
              'duration_ms_max': max(duration),
              'duration_ms_pvariance': pvariance(duration),
              'time_signature' : time_signature,
              'time_signature_mode': stats.mode(time_signature)[0].tolist()
            }

        if lastfm_data:
          # attach aggregate lastfm date to event
          event['lastfm'] = {
            'listeners' : lastfm_listeners,
            'listeners_sum': sum(lastfm_listeners),
            'playcount' : lastfm_playcount,
            'playcount_sum': sum(lastfm_playcount),
            'tags': lastfm_tags
          }

      # get venue object
      venue = event['venue']

      # get venue info
      venue_data = fq.getVenueObject(venue)

      # attach FourSquare venue info
      event['foursquare'] = venue_data


      # store event into db
      db.dbInsertEvent(event, events_collection)



