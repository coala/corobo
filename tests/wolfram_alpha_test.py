import logging

import vcr
from errbot.backends.test import FullStackTest

from plugins.wolfram_alpha import WolframAlpha

my_vcr = vcr.VCR(match_on=['method', 'scheme', 'host', 'port', 'path'],
                 filter_query_parameters=['appid'])


class WolframAlphaTest(FullStackTest):

    def setUp(self,
              extra_plugin_dir=None,
              extra_test_file=None,
              loglevel=logging.DEBUG,
              extra_config=None):
        super().setUp(extra_plugin_dir='plugins',
                      loglevel=logging.ERROR)

    @my_vcr.use_cassette('tests/cassettes/wa.yaml')
    def test_wa(self):
        self.push_message('!wa 2^6')
        self.assertIn('64', self.pop_message())
        with self.assertLogs() as cm:
            self.assertCommand('!wa this is a sentence',
                               'Dunno')
        self.assertIn('INFO:errbot.plugins.wolfram alpha:KeyError triggered on '
                      'retrieving pods.', cm.output)
