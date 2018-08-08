import queue

from tests.isolated_testcase import IsolatedTestCase


class TestSpam(IsolatedTestCase):

    def setUp(self):
        super().setUp()
        self.testbot = self

    def test_spam_callback(self):
        self.testbot.assertCommand('c'*1001, 'you\'re spamming')
        self.testbot.assertCommand('\n\n'*11, 'you\'re spamming')

    def test_spam_configuration(self):
        self.testbot.assertCommand('!plugin config SpammingAlert '
                                   '{\'MAX_LINES\': 10}',
                                   'configuration done')
        self.testbot.assertCommand('!plugin config SpammingAlert',
                                   '{\'MAX_LINES\': 10}')
        self.testbot.assertCommand('!plugin config SpammingAlert '
                                   '{\'MAX_LINES\': 20, \'MAX_MSG_LEN\': 200}',
                                   'configuration done')
        self.testbot.assertCommand('!plugin config SpammingAlert',
                                   '{\'MAX_LINES\': 20, \'MAX_MSG_LEN\': 200}')


class TestSpamExtraConfig(IsolatedTestCase):

    def setUp(self):
        extra_config = {
            'DEFAULT_CONFIG': {
                'SpammingAlert': {
                    'MAX_MSG_LEN': 500,
                    'MAX_LINES': 5,
                }
            }
        }
        super().setUp(extra_config=extra_config)
        self.testbot = self

    def test_spam_extra_config_callback(self):
        self.testbot.assertCommand('c'*501, 'you\'re spamming')
        self.testbot.assertCommand('\n'*6, 'you\'re spamming')
        # Since the message is not a spam, testbot will timeout
        # waiting for a response
        with self.assertRaises(queue.Empty):
            self.testbot.assertCommand('Not a spam', 'you\'re spamming')

    def test_spam_extra_config_configuration(self):
        self.testbot.assertCommand('!plugin config SpammingAlert '
                                   '{\'MAX_LINES\': 10}',
                                   'configuration done')
        self.testbot.assertCommand('!plugin config SpammingAlert',
                                   '{\'MAX_LINES\': 10}')
        self.testbot.assertCommand('!plugin config SpammingAlert '
                                   '{\'MAX_LINES\': 20, \'MAX_MSG_LEN\': 200}',
                                   'configuration done')
        self.testbot.assertCommand('!plugin config SpammingAlert',
                                   '{\'MAX_LINES\': 20, \'MAX_MSG_LEN\': 200}')
