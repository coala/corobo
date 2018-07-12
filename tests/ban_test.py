from unittest.mock import MagicMock, patch, PropertyMock

import plugins.ban

from tests.corobo_test_case import CoroboTestCase


class TestBan(CoroboTestCase):

    def setUp(self):
        super().setUp((plugins.ban.Ban,))
        self.ban = self.load_plugin('Ban')
        self.ban.bot_config.ROOMS_TO_JOIN = (
                'coala/coala', 'coala/coala-bears')
        self.ban.bot_config.BOT_IDENTITY['token'] = 'mocked?'

    @patch('plugins.ban.requests')
    @patch('plugins.ban.json')
    def test_ban_cmd(self, mockjson, mockreq):
        status_mock = MagicMock()
        type(status_mock).status_code = PropertyMock(return_value=200)
        mockreq.post.return_value = status_mock

        fake_room_data = [
            {'id': '130', 'uri': 'coala/coala'},
            {'id': '234', 'name': 'Nitanshu'},
            {'id': '897', 'uri': 'coala/coala-bears'}
        ]
        mockjson.loads.return_value = fake_room_data
        testbot = self
        testbot.assertCommand('!ban @nvzard',
                              'nvzard has been banned from: coala/coala, '
                              'coala/coala-bears')

    @patch('plugins.ban.requests')
    @patch('plugins.ban.json')
    def test_unban_cmd(self, mockjson, mockreq):
        status_mock = MagicMock()
        type(status_mock).status_code = PropertyMock(return_value=200)
        mockreq.delete.return_value = status_mock

        fake_room_data = [
            {'id': '130', 'uri': 'coala/coala'},
            {'id': '234', 'name': 'Nitanshu'},
            {'id': '897', 'uri': 'coala/coala-bears'}
        ]
        mockjson.loads.return_value = fake_room_data
        testbot = self
        testbot.assertCommand('!unban @nvzard',
                              'nvzard has been unbanned from: coala/coala, '
                              'coala/coala-bears')
