import settings as settings
import utils.db as db
import data.songkick as sk
import data.lastfm as last

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

last.getArtistTopTags(mbid='cbc9199f-944b-42e9-a945-627c9fc0ba6e')
# last.getArtistTopTags(search='Streetlight Manifesto')