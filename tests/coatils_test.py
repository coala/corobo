import logging
import unittest

from errbot.backends.test import TestBot
import vcr

from plugins.coatils import Coatils


class TestCoatils(unittest.TestCase):

    def setUp(self):
        self.testbot = TestBot(extra_plugin_dir='plugins',
                               loglevel=logging.ERROR)
        self.testbot.start()

    @vcr.use_cassette('tests/cassettes/coatils_total_bears.yaml')
    def test_total_bears(self):
        self.assertEqual(Coatils.total_bears(),
                         102)

    @vcr.use_cassette('tests/cassettes/coatils_all_langs.yaml')
    def test_all_langs(self):
        self.assertEqual(len(Coatils.all_langs()),
                         63)

    @vcr.use_cassette('tests/cassettes/coatils_contrib.yaml')
    def test_contrib_stats(self):
        self.testbot.assertCommand('!contrib stats sils',
                                    'Commited 2654 commits')
        self.testbot.assertCommand('!contrib stats some-non-existent',
                                   'stats for some-non-existent not found')

    @vcr.use_cassette('tests/cassettes/coatils_lang_stats.yaml')
    def test_lang_stats(self):
        self.testbot.assertCommand('!lang  stats',
                                   'coala supports 63 languages')

    @vcr.use_cassette('tests/cassettes/coatils_bear_stats.yaml')
    def test_bear_stats(self):
        self.testbot.assertCommand('!bear stats',
                                   'There are total 102 bears')

    @vcr.use_cassette('tests/cassettes/coatils_bear_stats_lang.yaml')
    def test_bear_stats_lang(self):
        self.testbot.assertCommand('!bear stats python',
                                   'There are 17 bears for python language')
        self.testbot.assertCommand('!bear stats abc',
                                   'No bear exists for abc')

    @vcr.use_cassette('tests/cassettes/coatils_stats.yaml')
    def test_stats(self):
        self.testbot.assertCommand('!stats',
                                   'coala has 102 bears across 63 languages')
