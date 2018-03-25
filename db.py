import settings
import pymysql.cursors

# fetch local .env variables
db_host = str(settings.DB_HOST)
db_port = int(settings.DB_PORT)
db_user = str(settings.DB_USER)
db_pass = str(settings.DB_PASS)
db_name = str(settings.DB_NAME)

# check if connection to database is working
def checkDatabaseConnection():
  try:
    connection = pymysql.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      db=db_name,
      cursorclass=pymysql.cursors.DictCursor
    )
    print('Successfuly connected to the database  ✅')
    connection.close()
    return True
  except:
    print('Failed to connect to the database  🛑')
    return False

checkDatabaseConnection()