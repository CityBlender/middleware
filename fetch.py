import settings as settings
import db as db
import data.songkick as sk

# get events in London
london_events = sk.fetchGigs(metro_area_code='24426')


# check connection to the database
# db.dbStatus()


db_london = db.db_client.london
db_london_events = db_london['events']
db_london_artist = db_london['artists']

# insert into database
db.dbInsertEvents(london_events, db_london_events)
