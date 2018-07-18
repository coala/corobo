import os
import logging

from errbot.backends.test import FullStackTest
import vcr

import plugins.answer


class TestAnswer(FullStackTest):

    def setUp(self,
              extra_plugin_dir=None,
              extra_test_file=None,
              loglevel=logging.DEBUG,
              extra_config=None):
        super().setUp(extra_plugin_dir='plugins',
                      loglevel=logging.ERROR)

    @vcr.use_cassette('tests/cassettes/answer.yaml')
    def test_answer(self):
        # Ignore InvalidLinkBear
        os.environ['ANSWER_END'] = 'http://0.0.0.0:8000'
        self.assertCommand('!answer something', 'Dunno')
        self.push_message('!answer getting started with coala')
        self.assertIn('Please checkout the following links', self.pop_message())
        self.push_message('!answer shell autocompletion')
        self.assertIn('Please checkout the following links', self.pop_message())
