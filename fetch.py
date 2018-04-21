import settings as settings
import db as db
import data.songkick as sk

# get events in London
london_events = sk.fetchGigs(metro_area_code='24426')

# insert into database
db.dbInsertTestEvents(london_events)
