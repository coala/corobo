import os
import unittest
import logging

from errbot.backends.test import TestBot
import vcr

import plugins.answer
from tests.helper import plugin_testbot


class TestAnswer(unittest.TestCase):
    @vcr.use_cassette('tests/cassettes/answer.yaml')
    def test_answer(self):
        os.environ['ANSWER_END'] = 'http://0.0.0.0:8000'
        testbot = TestBot(extra_plugin_dir='plugins', loglevel=logging.ERROR)
        testbot.start()

        testbot.assertCommand('!answer something', 'Dunno')

        testbot.push_message('!answer getting started with coala')
        testbot.pop_message()
        self.assertIn('You can read more here', testbot.pop_message())
        testbot.push_message('!answer shell autocompletion')
        testbot.pop_message()
        self.assertIn('You can read more here', testbot.pop_message())
