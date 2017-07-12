import logging
import unittest
import queue

from errbot.backends.test import TestBot
import vcr

from plugins.coatils import Coatils


class TestCoatils(unittest.TestCase):

    def setUp(self):
        self.testbot = TestBot(extra_plugin_dir='plugins',
                               loglevel=logging.ERROR)
        self.testbot.start()

    def tearDown(self):
        self.testbot.stop()

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

    @vcr.use_cassette('tests/cassettes/coatils_bear_stats_lang.yaml')
    def test_ls_bears(self):
        self.testbot.assertCommand('!ls bears r',
                                   'Bears for r are')
        self.assertIn('RLintBear', self.testbot.pop_message())
        self.testbot.assertCommand('!ls bears brainfuck',
                                   'No bears found for brainfuck')

    @vcr.use_cassette('tests/cassettes/coatils_stats.yaml')
    def test_stats(self):
        self.testbot.assertCommand('!stats',
                                   'coala has 102 bears across 63 languages')

    @vcr.use_cassette('tests/cassettes/coatils_run_coala.yaml')
    def test_run_coala(self):
        # no results
        self.testbot.push_message('!run python SpaceConsistencyBear use_spaces=yes\n```\nimport this\n\n```')
        self.assertEqual(self.testbot.pop_message(),
                         'coala analysis in progress...')
        self.assertEqual(self.testbot.pop_message(),
                         'Your code is flawless :tada:')
        # results and diffs
        self.testbot.push_message('!run python PyUnusedCodeBear remove_unused_imports=yes '
                                  'PycodestyleBear\n```\nimport os\nimport this\na=1\n```')
        self.assertEqual(self.testbot.pop_message(),
                         'coala analysis in progress...')
        msg = self.testbot.pop_message()
        self.assertIn('Here is what I think is wrong:', msg)
        self.assertIn('This file contains unused source code',
                      msg)

        # ensuring that only one result is yielded
        with self.assertRaises(queue.Empty):
            next_msg = self.testbot.pop_message()
        # error
        self.testbot.push_message('!run a b\n```\nc\n```')
        self.assertEqual(self.testbot.pop_message(),
                         'coala analysis in progress...')
        self.assertIn('Something went wrong, things to check for',
                      self.testbot.pop_message())

    def test_construct_settings(self):
        self.assertEqual(Coatils.construct_settings('bear1 a=1 b=2 bear2 bear3'),
                         {'bear1': {'a': '1', 'b': '2'},
                          'bear2': {},
                          'bear3': {}})

    def test_position(self):
        self.assertEqual(Coatils.position(1, 1, 1, 1),
                         'At 1:1')
        self.assertEqual(Coatils.position(1, 1, 1, 5),
                         'At line 1, between col 1 and 5')
        self.assertEqual(Coatils.position(1, 5, 3, 10),
                         'Between positions 1:5 and 3:10')
        self.assertEqual(Coatils.position(1, None, 3, None),
                         'Between lines 1 and 3')
        self.assertEqual(Coatils.position(3, None, 3, None),
                         'At line 3')
        self.assertEqual(Coatils.position(1, None, 3, 6),
                         'Between line 1 and position 3:6')
        self.assertEqual(Coatils.position(1, 4, 5, None),
                         'Between position 1:4 and line 5')
