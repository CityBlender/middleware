import settings as settings
import data.songkick as sk



# run dump functions

for city in settings.metro_uk:
  area = city[0]
  code = city[1]
  sk.dumpGigs(area, code, 'uk/')

for city in settings.metro_eur:
  area = city[0]
  code = city[1]
  sk.dumpGigs(area, code, 'eur/')

for city in settings.metro_americas:
  area = city[0]
  code = city[1]
  sk.dumpGigs(area, code, 'americas/')

for city in settings.metro_oceania:
  area = city[0]
  code = city[1]
  sk.dumpGigs(area, code, 'oceania/')



