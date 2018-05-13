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

# insert into database
# db.dbInsertEvents(london_area, db_london_events)

# event.getEventObject(london_area)
event.fetchAll(london_area, db_london_events, db_london_artist)