import logging
import os

COBOT_ROOT = os.environ.get('COBOT_ROOT', os.getcwd())

BACKEND = os.environ.get('BACKEND', 'Text')

BOT_EXTRA_BACKEND_DIR = os.path.join(COBOT_ROOT, 'err-backend-gitter')

HIDE_RESTRICTED_COMMANDS = True

BOT_DATA_DIR = os.path.join(COBOT_ROOT, 'data')
BOT_EXTRA_PLUGIN_DIR = COBOT_ROOT

BOT_LOG_FILE = os.path.join(COBOT_ROOT, 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

BOT_PREFIX = os.environ.get('COBOT_PREFIX', 'corobo ')

# Also listen to cobot, if the bot being ran is corobo
if not os.environ.get('COBOT_PREFIX'):
    BOT_ALT_PREFIXES = ('cobot ', )

BOT_DEPRECATED_PREFIXES = os.environ.get(
    'BOT_DEPRECATED_PREFIXES', '').split() or ('cobot ', )

BOT_ADMINS = os.environ.get('BOT_ADMINS', '').split() or ('*@localhost', )
# Text is a special case
if BACKEND == 'Text':
    BOT_ADMINS = ('@localhost', )

BOT_IDENTITY = {
    'token': os.environ.get('COBOT_TOKEN')
}

IGNORE_USERNAMES = os.environ.get("IGNORE_USERNAMES",
                                  'co-robo coala-bot').split()

DIVERT_TO_PRIVATE = ('help', )

ROOMS_TO_JOIN = (
    'coala/coala',
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
    'coala/cobot'
)

CHATROOM_PRESENCE = os.environ.get('ROOMS', '').split() or ROOMS_TO_JOIN

ACCESS_CONTROLS = {'render test': {
    'allowrooms': ('coala/cobot-test', 'coala/corobo',)},
    'LabHub:*': {'allowprivate': False}}

AUTOINSTALL_DEPS = True
