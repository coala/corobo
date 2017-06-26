import unittest
import logging

import vcr
from errbot.backends.test import TestBot

from plugins.wolfram_alpha import WolframAlpha

my_vcr = vcr.VCR(match_on=['method', 'scheme', 'host', 'port', 'path'],
                 filter_query_parameters=['appid'])


class WolframAlphaTest(unittest.TestCase):

    def setUp(self):
        self.testbot = TestBot(extra_plugin_dir='plugins',
                               loglevel=logging.ERROR)
        self.testbot.start()

    @my_vcr.use_cassette('tests/cassettes/wa.yaml')
    def test_wa(self):
        self.testbot.assertCommand("!wa 2^6", "64")
        with self.assertLogs() as cm:
            self.testbot.assertCommand('!wa this is a sentence',
                                       'Dunno')
        self.assertIn('INFO:errbot.plugins.wolfram alpha:KeyError triggered on '
                      'retrieving pods.', cm.output)
