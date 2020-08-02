import os

# subreddit
SUBREDDIT = 'SUBREDDIT'

# application
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
USER_AGENT = 'USER_AGENT'

# bot credentials
BOT_USERNAME = 'BOT_USERNAME'
BOT_PASSWORD = 'BOT_PASSWORD'

# developer info
DEV_USERNAME = 'DEV_USERNAME'
DEV_PASSWORD = 'DEV_PASSWORD'
DEV_EMAIL = 'DEV_EMAIL'

# bot errors account
ERROR_USERNAME = 'ERRORS_USERNAME'
ERROR_PASSWORD = 'ERRORS_PASSWORD'

# database connection info
DATABASE = 'DATABASE'

def env(var):
  return os.environ[var]
