import logging
import os
import unittest
from unittest.mock import Mock, MagicMock, create_autospec, PropertyMock

import github3
import IGitt

from errbot.backends.test import TestBot

import plugins.labhub
from plugins.labhub import LabHub

from tests.helper import plugin_testbot

class TestLabHub(unittest.TestCase):

    def setUp(self):
        plugins.labhub.github3 = create_autospec(github3)

        self.mock_org = create_autospec(github3.orgs.Organization)
        self.mock_gh = create_autospec(github3.GitHub)
        self.mock_team = create_autospec(github3.orgs.Team)
        self.mock_team.name = PropertyMock()
        self.mock_team.name = 'mocked team'
        self.mock_repo = create_autospec(IGitt.GitHub.GitHub.GitHubRepository)

        plugins.labhub.github3.login.return_value = self.mock_gh
        self.mock_gh.organization.return_value = self.mock_org
        self.mock_org.iter_teams.return_value = [self.mock_team]
        plugins.labhub.github3.organization.return_value = self.mock_org

        plugins.labhub.GitHub = create_autospec(IGitt.GitHub.GitHub.GitHub)
        plugins.labhub.GitLab = create_autospec(IGitt.GitLab.GitLab.GitLab)

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
        self.assertEqual(labhub.TEAMS, teams)
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

    def test_create_issue_cmd(self):
        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        labhub.activate()
        plugins.labhub.GitHub.assert_called_once_with(None)
        plugins.labhub.GitLab.assert_called_once_with(None)

        labhub.REPOS = {'repository': self.mock_repo}

        testbot.assertCommand('!new issue repository this is the title\nbo\ndy',
                              'Here you go')

        labhub.REPOS['repository'].create_issue.assert_called_once_with(
            'this is the title', 'bo\ndy'
        )

        testbot.assertCommand('!new issue coala title', 'repository that does not exist')

    def test_unassign_cmd(self):
        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)

        labhub.activate()
        labhub.REPOS = {'name': self.mock_repo}

        mock_iss = create_autospec(IGitt.GitHub.GitHubIssue)
        self.mock_repo.get_issue.return_value = mock_iss
        mock_iss.assignees = PropertyMock()
        mock_iss.assignees = (None, )
        mock_iss.unassign = MagicMock()

        testbot.assertCommand('!unassign https://github.com/coala/name/issues/23',
                              'you are unassigned now', timeout=10000)
        self.mock_repo.get_issue.assert_called_with(23)
        mock_iss.unassign.assert_called_once_with(None)

        mock_iss.assignees = ('meetmangukiya', )
        testbot.assertCommand('!unassign https://github.com/coala/name/issues/23',
                           'not an assignee on the issue')

        testbot.assertCommand('!unassign https://github.com/coala/s/issues/52',
                              'Repository doesn\'t exist.')


        testbot.assertCommand('!unassign https://gitlab.com/ala/am/issues/532',
                               'Repository not owned by our org.')
