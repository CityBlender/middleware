import settings as settings
import utils.db as db
import utils.dataHelper as data
import data.event as event
from pprint import pprint

#  London metropolitan area code
london_area = '24426'

# check connection to the database
# db.dbStatus()

# configure database connection
db_london = db.db_client.london
db_london_events = db_london['events']
db_london_artist = db_london['artists']

# set up indexes
db.createEventIndex(db_london_events)
db.createArtistIndex(db_london_artist)

# fetch events
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today, settings.today)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.tomorrow, settings.tomorrow)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today_plus_2, settings.today_plus_2)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today_plus_3, settings.today_plus_3)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today_plus_4, settings.today_plus_4)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today_plus_5, settings.today_plus_5)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today_plus_6, settings.today_plus_6)
event.fetchAll(london_area, db_london_events, db_london_artist, settings.today_plus_7, settings.today_plus_7)

