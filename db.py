import settings
import pymysql.cursors

# fetch local .env variables
dbHost = str(settings.DB_HOST)
dbPort = int(settings.DB_PORT)
dbUser = str(settings.DB_USER)
dbPass = str(settings.DB_PASS)
dbName = str(settings.DB_NAME)

# check if connection to database is working
def checkDatabaseConnection():
  try:
    connection = pymysql.connect(
      host=dbHost,
      user=dbUser,
      password=dbPass,
      db=dbName,
      cursorclass=pymysql.cursors.DictCursor
    )
    print('Successfuly connected to the database  ✅')
    connection.close()
    return True
  except:
    print('Failed to connect to the database  🛑')
    return False

checkDatabaseConnection()