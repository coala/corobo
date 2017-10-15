import logging
import os
import queue
import time
import unittest
from unittest.mock import Mock, MagicMock, create_autospec, PropertyMock, patch

import github3
import IGitt
from IGitt.GitHub.GitHubMergeRequest import GitHubMergeRequest
from IGitt.GitHub.GitHubIssue import GitHubIssue

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
        # Since the user won't be invited again, it'll timeout waiting for a
        # response.
        with self.assertRaises(queue.Empty):
            testbot.assertCommand('helloworld', 'newcomer')
        self.mock_team.invite.assert_called_with(None)

    def test_create_issue_cmd(self):
        plugins.labhub.GitHub = create_autospec(IGitt.GitHub.GitHub.GitHub)
        plugins.labhub.GitLab = create_autospec(IGitt.GitLab.GitLab.GitLab)
        plugins.labhub.GitHubToken = create_autospec(IGitt.GitHub.GitHubToken)
        plugins.labhub.GitLabPrivateToken = create_autospec(IGitt.GitLab.GitLabPrivateToken)

        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        labhub.activate()
        plugins.labhub.GitHubToken.assert_called_with(None)
        plugins.labhub.GitLabPrivateToken.assert_called_with(None)


        labhub.REPOS = {'repository': self.mock_repo}

        testbot.assertCommand('!new issue repository this is the title\nbo\ndy',
                              'Here you go')

        labhub.REPOS['repository'].create_issue.assert_called_once_with(
            'this is the title', 'bo\ndy\nOpened by @None '
        )

        testbot.assertCommand('!new issue coala title', 'repository that does not exist')

    def test_unassign_cmd(self):
        plugins.labhub.GitHub = create_autospec(IGitt.GitHub.GitHub.GitHub)
        plugins.labhub.GitLab = create_autospec(IGitt.GitLab.GitLab.GitLab)
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

    def test_assign_cmd(self):
        plugins.labhub.GitHub = create_autospec(IGitt.GitHub.GitHub.GitHub)
        plugins.labhub.GitLab = create_autospec(IGitt.GitLab.GitLab.GitLab)
        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        labhub.activate()

        mock_issue = create_autospec(GitHubIssue)
        self.mock_repo.get_issue.return_value = mock_issue

        labhub.REPOS = {'a': self.mock_repo}

        mock_dev_team = create_autospec(github3.orgs.Team)
        mock_maint_team = create_autospec(github3.orgs.Team)
        mock_dev_team.is_member.return_value = False
        mock_maint_team.is_member.return_value = False

        labhub.TEAMS = {'coala newcomers': self.mock_team,
                        'coala developers': mock_dev_team,
                        'coala maintainers': mock_maint_team}

        cmd = '!assign https://github.com/{}/{}/issues/{}'
        # no assignee, not newcomer
        mock_issue.assignees = tuple()
        self.mock_team.is_member.return_value = False

        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'You\'ve been assigned to the issue')

        # no assignee, newcomer, difficulty/low
        mock_issue.labels = PropertyMock()
        mock_issue.labels = ('difficulty/low', )
        mock_issue.assignees = tuple()
        self.mock_team.is_member.return_value = True

        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'You\'ve been assigned to the issue')

        # no assignee, newcomer, no labels
        self.mock_team.is_member.return_value = True
        mock_issue.labels = tuple()
        mock_issue.assignees = tuple()
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'not eligible to be assigned to this issue')
        testbot.pop_message()

        # no assignee, newcomer, difficulty medium
        mock_issue.labels = ('difficulty/medium', )
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'not eligible to be assigned to this issue')
        testbot.pop_message()

        # no assignee, newcomer, difficulty medium
        labhub.GH_ORG_NAME = 'not-coala'
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'assigned')
        labhub.GH_ORG_NAME = 'coala'

        # newcomer, developer, difficulty/medium
        mock_dev_team.is_member.return_value = True
        mock_maint_team.is_member.return_value = False
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'assigned')

        # has assignee
        mock_issue.assignees = ('somebody', )
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'already assigned to someone')

        # non-existent repository
        testbot.assertCommand(cmd.format('coala', 'c', '23'),
                              'Repository doesn\'t exist.')

        # unknown org
        testbot.assertCommand(cmd.format('coa', 'a', '23'),
                              'Repository not owned by our org.')

    def test_mark_cmd(self):
        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        labhub.activate()

        labhub.REPOS = {'a': self.mock_repo}
        mock_mr = create_autospec(GitHubMergeRequest)
        self.mock_repo.get_mr.return_value = mock_mr
        mock_mr.labels = PropertyMock()
        cmd = '!mark {} https://github.com/{}/{}/pull/{}'

        # Non-eistent repo
        testbot.assertCommand(cmd.format('wip', 'a', 'b', '23'),
                              'Repository doesn\'t exist.')
        testbot.assertCommand('!mark wip https://gitlab.com/a/b/merge_requests/2',
                              'Repository doesn\'t exist.')

        # mark wip
        mock_mr.labels = ['process/pending review']
        testbot.assertCommand(cmd.format('wip', 'coala', 'a', '23'),
                              'marked work in progress')
        # mark pending
        mock_mr.labels = ['process/wip']
        testbot.assertCommand(cmd.format('pending', 'coala', 'a', '23'),
                              'marked pending review')

    def test_alive(self):
        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        with patch('plugins.labhub.time.sleep') as mock_sleep:
            labhub.gh_repos = {
                'coala': create_autospec(IGitt.GitHub.GitHub.GitHubRepository),
                'coala-bears': create_autospec(IGitt.GitHub.GitHub.GitHubRepository),
                'coala-utils': create_autospec(IGitt.GitHub.GitHub.GitHubRepository)
            }
            # for the branch where program sleeps
            labhub.gh_repos.update({str(i):
                                    create_autospec(IGitt.GitHub.GitHub.GitHubRepository)
                                    for i in range(30)})
            labhub.gl_repos = {
                'test': create_autospec(IGitt.GitLab.GitLab.GitLabRepository)
            }
            labhub.activate()

            labhub.gh_repos['coala'].search_mrs.return_value = [1, 2]
            labhub.gh_repos['coala-bears'].search_mrs.return_value = []
            labhub.gh_repos['coala-utils'].search_mrs.return_value = []
            testbot.assertCommand('!pr stats 10hours',
                                  '2 PRs opened in last 10 hours\n'
                                  'The community is alive', timeout=100)

            labhub.gh_repos['coala'].search_mrs.return_value = []
            testbot.assertCommand('!pr stats 5hours',
                                  '0 PRs opened in last 5 hours\n'
                                  'The community is dead')

            labhub.gh_repos['coala'].search_mrs.return_value = [
                1, 2, 3, 4, 5,
                6, 7, 8, 9, 10
            ]
            testbot.assertCommand('!pr stats 3hours',
                                  '10 PRs opened in last 3 hours\n'
                                  'The community is on fire')

    def test_invite_me(self):
        teams = {
            'coala maintainers': self.mock_team,
            'coala newcomers': self.mock_team,
            'coala developers': self.mock_team
        }

        labhub, testbot = plugin_testbot(plugins.labhub.LabHub, logging.ERROR)
        labhub.activate()
        labhub._teams = teams

        plugins.labhub.os.environ['GH_TOKEN'] = 'patched?'
        testbot.assertCommand('!invite me',
                              'We\'ve just sent you an invite')
        with self.assertRaises(queue.Empty):
            testbot.pop_message()
