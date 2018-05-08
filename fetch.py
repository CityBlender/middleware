import settings as settings
import utils.db as db
import utils.dataHelper as data
import data.songkick as sk
import data.lastfm as last
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

final_last = last.returnArtistObject(mbid='cbc9199f-944b-42e9-a945-627c9fc0ba6e')
data.dumpJson('final-last-fm-test.json', final_last, './temp/')
# last.getArtistTopTracks(search='Streetlight Manifesto')