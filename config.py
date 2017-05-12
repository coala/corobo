import logging
import os

# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

COBOT_ROOT = os.environ.get("COBOT_ROOT", os.getcwd())

BACKEND = 'Gitter'

BOT_EXTRA_BACKEND_DIR = os.path.join(COBOT_ROOT, 'err-backend-gitter')

BOT_DATA_DIR = os.path.join(COBOT_ROOT, 'data')
BOT_EXTRA_PLUGIN_DIR = os.path.join(COBOT_ROOT, 'plugins')

BOT_LOG_FILE = os.path.join(COBOT_ROOT, 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('meetmangukiya', )

BOT_IDENTITY = {
    'token': os.environ["COBOT_TOKEN"]
}
