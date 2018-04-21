import json

import settings as settings
import data.songkick as sk



dummy = sk.fetchGigs(metro_area_code='24426')

# with open('data.json', 'w') as outfile:
#     json.dump(dummy, outfile)