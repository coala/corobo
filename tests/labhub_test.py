import logging
import os
import unittest
from unittest.mock import Mock, MagicMock, create_autospec, PropertyMock

import github3
import IGitt

from errbot.backends.test import TestBot

import plugins.labhub
from plugins.labhub import LabHub

class TestLabHub(unittest.TestCase):

    def setUp(self):
        plugins.labhub.github3 = create_autospec(github3)

        self.mock_org = create_autospec(github3.orgs.Organization)
        self.mock_gh = create_autospec(github3.GitHub)
        self.mock_team = create_autospec(github3.orgs.Team)
        self.mock_team.name = PropertyMock()
        self.mock_team.name = 'mocked team'

        plugins.labhub.github3.login.return_value = self.mock_gh
        self.mock_gh.organization.return_value = self.mock_org
        self.mock_org.iter_teams.return_value = [self.mock_team]
        plugins.labhub.github3.organization.return_value = self.mock_org

    def test_invite_cmd(self):
        teams = {
            'coala maintainers': self.mock_team,
            'coala newcomers': self.mock_team,
            'coala developers': self.mock_team
        }

        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        labhub.activate()
        labhub._teams = teams

        self.mock_team.is_member.return_value = True
        plugins.labhub.os.environ['GH_TOKEN'] = 'patched?'
        testbot.assertCommand('!invite meet to developers',
                                   '@meet, you are a part of developers')
        self.assertEqual(self.labhub.TEAMS, teams)
        testbot.assertCommand('!invite meet to something',
                                   'select from one of the')

        self.mock_team.is_member.return_value = False

        testbot.assertCommand('!invite meet to developers',
                                   ':poop:')

    def test_hello_world_callback(self):
        teams = {
            'coala newcomers': self.mock_team,
        }

        testbot = TestBot(extra_plugin_dir='plugins', loglevel=logging.ERROR)
        testbot.start()
        labhub = testbot.bot.plugin_manager.get_plugin_obj_by_name('LabHub')
        labhub.TEAMS = teams
        self.mock_team.is_member.return_value = False
        testbot.assertCommand('hello, world', 'newcomer')
        testbot.assertCommand('helloworld', 'newcomer')
        self.mock_team.invite.assert_called_with(None)
