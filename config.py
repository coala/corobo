import logging
import os

BOT_ROOT_KEY = 'BOT_ROOT'

if 'COBOT_ROOT' in os.environ and BOT_ROOT_KEY not in os.environ:
    logging.warning(
        "Environment variable COBOT_ROOT is deprecated, use {} instead."
        .format(BOT_ROOT_KEY))
    BOT_ROOT_KEY = 'COBOT_ROOT'
BOT_ROOT = os.environ.get(BOT_ROOT_KEY, os.getcwd())


_BOT_IDENTITY_KEYS = (
    'endpoint',
    'nickname',
    'password',
    'port',
    'server',
    'ssl',
    'token',
    'username',
)

BOT_IDENTITY = {}

for _key in _BOT_IDENTITY_KEYS:
    BOT_IDENTITY[_key] = os.environ.get('BOT_' + _key.upper())

if not BOT_IDENTITY['token']:
    BOT_IDENTITY['token'] = os.environ.get('COBOT_TOKEN')

if BOT_IDENTITY['server'] and ':' in BOT_IDENTITY['server']:
    server, port = os.environ['BOT_SERVER'].split(':')
    BOT_IDENTITY['server'] = (server, int(port))

BACKEND = os.environ.get('BACKEND')
if not BACKEND:
    if BOT_IDENTITY['token']:
        BACKEND = 'Gitter'
    else:
        BACKEND = 'Text'

if BACKEND == 'Gitter':
    BOT_EXTRA_BACKEND_DIR = os.path.join(BOT_ROOT, 'err-backend-gitter')
else:
    BOT_EXTRA_BACKEND_DIR = None

if BOT_EXTRA_BACKEND_DIR:
    plug_file = BACKEND.lower() + '.plug'
    if not os.path.exists(os.path.join(BOT_EXTRA_BACKEND_DIR, plug_file)):
        raise SystemExit('Directory %s not initialised' %
                         BOT_EXTRA_BACKEND_DIR)

HIDE_RESTRICTED_COMMANDS = True

BOT_DATA_DIR = os.path.join(BOT_ROOT, 'data')
if not os.path.isdir(BOT_DATA_DIR):
    # create an empty data directory
    os.mkdir(BOT_DATA_DIR)

BOT_EXTRA_PLUGIN_DIR = BOT_ROOT

BOT_LOG_FILE = os.path.join(BOT_ROOT, 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

if not os.environ.get('BOT_PREFIX'):
    raise SystemExit("Environment variable BOT_PREFIX not specified")

BOT_PREFIX = os.environ.get('BOT_PREFIX')

if 'COBOT_PREFIX' in os.environ:
    BOT_PREFIX = os.environ['COBOT_PREFIX']
    logging.warning(
        'Deprecation warning: environment variable COBOT_PREFIX is replaced '
        'by BOT_PREFIX.')

# Also listen to cobot, if the bot being ran is corobo
if not os.environ.get('BOT_PREFIX'):
    BOT_ALT_PREFIXES = ('cobot ', )

BOT_DEPRECATED_PREFIXES = os.environ.get(
    'BOT_DEPRECATED_PREFIXES', '').split() or ('cobot ', )

BOT_ADMINS = os.environ.get('BOT_ADMINS', '').split() or ('*@localhost', )
# Text is a special case
if BACKEND == 'Text':
    BOT_ADMINS = ('@localhost', )

IGNORE_USERNAMES = os.environ.get("IGNORE_USERNAMES",
                                  'co-robo coala-bot '
                                  'from-somewhere-else').split()

DIVERT_TO_PRIVATE = ('help', )

ROOMS_TO_JOIN = [
    'coala',
    'coala-bears',
    'corobo',
    'depman',
    'ast',
    'gci',
]

if BACKEND == 'Gitter':
    ROOMS_TO_JOIN += [
        'aspects',
        'bearship',
        'coala',
        'coala/artwork-corner',
        'coala/gsoc',
        'coala/maintainers',
        'coala/offtopic',
        'coala/workshops',
        'cobot',
        'cobot-test',
        'community',
        'community',
        'conferences',
        'devops',
        'documentation',
        'editor-plugins',
        'freelancers',
        'performance',
    ]
elif BACKEND == 'Zulip':
    ROOMS_TO_JOIN += [
        'maintainers',
        'gci-mentors-2018',
        'gitmate',
        'gsoc',
        'moban',
        'test',
        'zulip',
    ]

if BACKEND == 'Gitter':
    ROOMS_TO_JOIN = ['coala/' + item for item in ROOMS_TO_JOIN]

CHATROOM_PRESENCE = os.environ.get('ROOMS', '').split() or ROOMS_TO_JOIN

ACCESS_CONTROLS = {'render test': {
    'allowrooms': ('coala/cobot-test', 'coala/corobo',)},
    'LabHub:*': {'allowprivate': False}}

AUTOINSTALL_DEPS = True

DEFAULT_CONFIG = {
    'answer': {
        'ANSWER_END': os.environ.get('ANSWER_END'),
    },
    'LabHub': {
        'GH_TOKEN': os.environ.get('GH_TOKEN'),
        'GL_TOKEN': os.environ.get('GL_TOKEN'),
        'GH_ORG_NAME': os.environ.get('GH_ORG_NAME', 'coala'),
        'GL_ORG_NAME': os.environ.get('GL_ORG_NAME', 'coala'),
    },
    'WolframAlpha': {
        'WA_TOKEN': os.environ.get('WA_TOKEN'),
    },
}
