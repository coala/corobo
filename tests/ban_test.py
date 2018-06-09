import logging
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

import plugins.ban

from tests.helper import plugin_testbot


class TestBan(unittest.TestCase):

    @patch('plugins.ban.requests')
    @patch('plugins.ban.json')
    def test_ban_cmd(self, mockjson, mockreq):
        ban, testbot = plugin_testbot(plugins.ban.Ban, logging.ERROR)
        ban.activate()

        ban.bot_config.ROOMS_TO_JOIN = ('coala/coala', 'coala/coala-bears')
        ban.bot_config.BOT_IDENTITY['token'] = 'mocked?'
        status_mock = MagicMock()
        type(status_mock).status_code = PropertyMock(return_value=200)
        mockreq.post.return_value = status_mock

        fake_room_data = [
            {'id': '130', 'uri': 'coala/coala'},
            {'id': '234', 'name': 'Nitanshu'},
            {'id': '897', 'uri': 'coala/coala-bears'}
        ]
        mockjson.loads.return_value = fake_room_data
        testbot.assertCommand('!ban @nvzard',
                              'nvzard has been banned from: coala/coala, '
                              'coala/coala-bears')

    @patch('plugins.ban.requests')
    @patch('plugins.ban.json')
    def test_unban_cmd(self, mockjson, mockreq):
        ban, testbot = plugin_testbot(plugins.ban.Ban, logging.ERROR)
        ban.activate()

        ban.bot_config.ROOMS_TO_JOIN = ('coala/coala', 'coala/coala-bears')
        ban.bot_config.BOT_IDENTITY['token'] = 'mocked?'
        status_mock = MagicMock()
        type(status_mock).status_code = PropertyMock(return_value=200)
        mockreq.delete.return_value = status_mock

        fake_room_data = [
            {'id': '130', 'uri': 'coala/coala'},
            {'id': '234', 'name': 'Nitanshu'},
            {'id': '897', 'uri': 'coala/coala-bears'}
        ]
        mockjson.loads.return_value = fake_room_data
        testbot.assertCommand('!unban @nvzard',
                              'nvzard has been unbanned from: coala/coala, '
                              'coala/coala-bears')
