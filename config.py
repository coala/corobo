import logging
import os

COBOT_ROOT = os.environ.get('COBOT_ROOT', os.getcwd())

BACKEND = os.environ.get('BACKEND', 'Gitter')

BOT_EXTRA_BACKEND_DIR = os.path.join(COBOT_ROOT, 'err-backend-gitter')

HIDE_RESTRICTED_COMMANDS = True

BOT_DATA_DIR = os.path.join(COBOT_ROOT, 'data')
BOT_EXTRA_PLUGIN_DIR = COBOT_ROOT

BOT_LOG_FILE = os.path.join(COBOT_ROOT, 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

BOT_PREFIX = os.environ.get('COBOT_PREFIX', 'corobo ')

BOT_ADMINS = os.environ.get(tuple('BOT_ADMINS'.split()), ('meetmangukiya', ))

BOT_IDENTITY = {
    'token': os.environ['COBOT_TOKEN']
}

DIVERT_TO_PRIVATE = ('help', )

CHATROOM_PRESENCE = os.environ.get(
    tuple(os.environ.get('ROOMS').split()),
    ('coala/coala',
     'coala/coala/offtopic',
     'coala/cobot-test',
     'coala/corobo',
     'coala/devops',
     'coala/community',
     'coala/coala/gsoc',
     'coala/coala/maintainers',
     'coala/coala-bears',
     'coala/bearship',
     'coala/gci',
     'coala/cobot')
)

AUTOINSTALL_DEPS = True
