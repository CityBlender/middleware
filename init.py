import settings
import data.songkick as sk

# SongKick metropolitan area codes
metro_london = '24426'

sk.getGigs(metro_london, results=1)