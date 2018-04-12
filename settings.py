# settings.py
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# load .env variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# get today's date
today = datetime.datetime.now().strftime('%Y-%m-%d') # YYYY-MM-DD

