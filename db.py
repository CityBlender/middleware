import pymysql.cursors

# fetch local .env variables
db_host = str(os.getenv('DB_HOST'))
db_port = int(os.getenv('DB_PORT'))
db_user = str(os.getenv('DB_USER'))
db_pass = str(os.getenv('DB_PASS'))
db_name = str(os.getenv('DB_NAME'))

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