import settings
import data.songkick as sk
import datetime

# SongKick metropolitan area codes
metro_london = '24426'

# today's date
today = datetime.datetime.now().strftime('%Y-%m-%d') # YYYY-MM-DD


sk.getGigs(metro_london, today, today)