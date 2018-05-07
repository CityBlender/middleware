import settings as settings
import utils.db as db
import data.songkick as sk

#  London metropolitan area code
london_area = '24426'

# check connection to the database
# db.dbStatus()

# configure database connection
db_london = db.db_client.london
db_london_events = db_london['events']
db_london_artist = db_london['artists']

# insert into database
db.dbInsertEvents(london_area, db_london_events)
