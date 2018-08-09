import os
import logging

from errbot.backends.test import FullStackTest
import vcr
import requests_mock

import plugins.answer


class TestAnswer(FullStackTest):

    def setUp(self,
              extra_plugin_dir=None,
              extra_test_file=None,
              loglevel=logging.DEBUG,
              extra_config=None):
        super().setUp(extra_plugin_dir='plugins',
                      loglevel=logging.ERROR)
        # Ignore InvalidLinkBear
        self.answer_end_point = 'http://0.0.0.0:8000'
        os.environ['ANSWER_END'] = self.answer_end_point

    def tearDown(self):
        del os.environ['ANSWER_END']

    @vcr.use_cassette('tests/cassettes/answer.yaml')
    def test_answer(self):
        self.assertCommand('!answer something', 'Dunno')
        self.push_message('!answer getting started with coala')
        self.assertIn('Please checkout the following links', self.pop_message())
        self.push_message('!answer shell autocompletion')
        self.assertIn('Please checkout the following links', self.pop_message())

    def test_invalid_json(self):
        with requests_mock.Mocker() as m:
            m.get('{}/answer?question=foo'.format(self.answer_end_point),
                  text='invalid')
            self.assertCommand(
                '!answer foo',
                'Something went wrong, please check logs')

    def test_invalid_repo(self):
        with requests_mock.Mocker() as m:
            m.get('{}/answer?question=foo'.format(self.answer_end_point),
                  text='[["Wrong answer\\n/wrong/link\\n"]]')
            self.assertCommand(
                '!answer foo',
                'Computer says nooo. See logs for details:\n'
                'Unrecognised answer: /wrong/link')
