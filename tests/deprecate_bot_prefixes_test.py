from tests.isolated_testcase import IsolatedTestCase


class DeprecateBotPrefixesTest(IsolatedTestCase):

    def test_deprecated_prefixes_other(self):
        self.bot_config.BOT_DEPRECATED_PREFIXES = ('oldbot', 'deprecatedbot')
        self.assertCommand('oldbot just a test', 'has been deprecated')
        self.assertCommand('deprecatedbot just a test', 'has been deprecated')
