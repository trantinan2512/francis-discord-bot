from decouple import config
import os


DEBUG = config('DEBUG', default=False, cast=bool)
BOT_TOKEN = config('BOT_TOKEN')
MY_ID = config('MY_ID', cast=str)
SERVER_ID = config('SERVER_ID', cast=str)

# Twitter stuff
TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET')

TWITTER_OWNER = config('TWITTER_OWNER')
TWITTER_OWNER_ID = config('TWITTER_OWNER_ID')

TWITTER_ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET')

FACEBOOK_ACCESS_TOKEN = config('FACEBOOK_TEST_ACCESS_TOKEN')

# francis/config.py -> francis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))