pytest_plugins = ['errbot.backends.test']
extra_plugin_dir = 'plugins'

def test_deprecated_prefixes_other(testbot):
    testbot.bot_config.BOT_DEPRECATED_PREFIXES = ('oldbot', 'deprecatedbot')
    testbot.assertCommand('oldbot just a test', 'has been deprecated')
    testbot.assertCommand('deprecatedbot just a test', 'has been deprecated')
