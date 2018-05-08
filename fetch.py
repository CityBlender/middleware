import settings as settings
import utils.db as db
import utils.dataHelper as data
import data.songkick as sk
import data.lastfm as last
import data.spotify as spotify
import data.musixmatch as musix
import data.artist as artist
from pprint import pprint

#  London metropolitan area code
london_area = '24426'

# check connection to the database
# db.dbStatus()

# configure database connection
db_london = db.db_client.london
db_london_events = db_london['events']
db_london_artist = db_london['artists']

# insert into database
# db.dbInsertEvents(london_area, db_london_events)

# last.getLastById('b6b8a637-e4f1-4d30-b400-2116e9182630')

# last.getArtistTopTracks(mbid='cbc9199f-944b-42e9-a945-627c9fc0ba6e')

# pprint(last.getArtistTopTags(mbid='cbc9199f-944b-42e9-a945-627c9fc0ba6e'))

# final_last = last.returnArtistObject(mbid='cbc9199f-944b-42e9-a945-627c9fc0ba6e')
# data.dumpJson('final-last-fm-test.json', final_last, './temp/')
# last.getArtistTopTracks(search='Streetlight Manifesto')
# data.dumpJson('spotify-test-blockhead-final.json', spotify.returnArtistObject('Blockhead'), './temp/')
# spotify.getArtistInfo('Blockhead')

# data.dumpJson('last-fm-doors.json', last.returnArtistObject(search='The Doors'), './temp/')

# data.dumpJson('musix-restricted.json', musix.getTrackLyrics('96734374-9968-40e2-ae97-a7632793dd82'), './temp/' )
# data.dumpJson('musix-instrumental.json', musix.getTrackLyrics('d5a1ad42-898d-4d5b-922c-5891b6c73f5a'), './temp/' )
# data.dumpJson('musix-lyrics.json', musix.getTrackLyrics('00bde944-7562-446f-ad0f-3d4bdc86b69f'), './temp/' )
# data.dumpJson('drake.json', last.returnArtistObject(search='Drake'), './temp/' )
data.dumpJson('test-artist-object.json', artist.getArtistObject(mbid='cbc9199f-944b-42e9-a945-627c9fc0ba6e'), './temp/')
# data.dumpJson('test-artist-object-with-search.json', artist.getArtistObject(search='Streetlight Manifesto'), './temp/')