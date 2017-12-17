import logging
import unittest

from errbot.backends.test import TestBot


class TestSpam(unittest.TestCase):

    def setUp(self):
        self.testbot = TestBot(extra_plugin_dir='plugins',
                               loglevel=logging.ERROR)
        self.testbot.start()

    def test_spam_callback(self):
        self.testbot.assertCommand('c'*1001, 'you\'re spamming')
        self.testbot.assertCommand('\n\n'*11, 'you\'re spamming')

    def test_spam_configuration(self):
        self.testbot.assertCommand('!plugin config SpammingAlert '
                                   '{\'MAX_LINES\': 10}',
                                   'configuration done')
        self.testbot.assertCommand('!plugin config SpammingAlert '
                                   '{\'MAX_MSG_LEN\':1, \'MAX_LINES\': 1}',
                                   'configuration done')
