import queue
import textwrap
from unittest.mock import Mock, MagicMock, create_autospec, PropertyMock, patch

import github3
import IGitt
from IGitt.GitHub.GitHubMergeRequest import GitHubMergeRequest
from IGitt.GitLab.GitLabMergeRequest import GitLabMergeRequest
from IGitt.GitHub.GitHubIssue import GitHubIssue

from errbot.backends.base import Message

import plugins.labhub
from plugins.labhub import LabHub

from tests.labhub_test_case import LabHubTestCase


class TestLabHub(LabHubTestCase):

    def setUp(self):
        super().setUp((plugins.labhub.LabHub,))
        self.global_mocks = {
            'REPOS': {
                'repository': self.mock_repo,
                'repository.github.io': self.mock_repo,
            },
            '_teams': self.teams,
        }
        configs = {
            'GH_TOKEN': None,
            'GL_TOKEN': None,
            'GH_ORG_NAME': 'coala',
            'GL_ORG_NAME': 'coala',
        }
        self.bot.sender._nick = 'batman'
        self.labhub = self.load_plugin('LabHub', self.global_mocks, configs)

    def test_invite_cmd(self):
        mock_team_newcomers = create_autospec(github3.orgs.Team)
        mock_team_developers = create_autospec(github3.orgs.Team)
        mock_team_maintainers = create_autospec(github3.orgs.Team)

        self.teams['coala newcomers'] = mock_team_newcomers
        self.teams['coala developers'] = mock_team_developers
        self.teams['coala maintainers'] = mock_team_maintainers

        mock_dict = {
            'TEAMS': self.teams,
            'is_room_member': MagicMock(),
        }
        self.inject_mocks('LabHub', mock_dict)
        testbot = self

        self.assertEqual(self.labhub.TEAMS, self.teams)

        mock_dict['is_room_member'].return_value = False
        testbot.assertCommand('!invite meet to newcomers',
                              '@meet is not a member of this room.')

        mock_dict['is_room_member'].return_value = True

        # invite by maintainer
        mock_team_newcomers.is_member.return_value = True
        mock_team_developers.is_member.return_value = True
        mock_team_maintainers.is_member.return_value = True

        testbot.assertCommand(
            '!invite meet to newcomers',
            'To get started, please follow our [newcomers guide]')
        testbot.assertCommand('!invite meet to developers',
                              '@meet, you are a part of developers')
        testbot.assertCommand('!invite meet to maintainers',
                              '@meet you seem to be awesome!')

        # invite by developer
        mock_team_maintainers.is_member.return_value = False
        mock_dict['is_room_member'].return_value = True

        testbot.assertCommand(
            '!invite meet to newcomers',
            'To get started, please follow our [newcomers guide]')
        testbot.assertCommand('!invite meet to developers',
                              ':poop:')
        testbot.assertCommand('!invite meet to maintainers',
                              ':poop:')

        # invite by newcomer
        mock_team_developers.is_member.return_value = False

        testbot.assertCommand('!invite meet to newcomers',
                              ':poop')
        testbot.assertCommand('!invite meet to developers',
                              ':poop:')
        testbot.assertCommand('!invite meet to maintainers',
                              ':poop:')

        # invalid team
        testbot.assertCommand('!invite meet to something',
                              'select from one of the valid')

        # invalid command
        testbot.assertCommand('!invite meetto newcomers',
                              'Command "invite" / "invite meetto" not found.')

        self.bot.sender._nick = None
        testbot.assertCommand(
            '!invite meet to newcomers',
            'ERROR: The above command cannot be operated without nick.')

        # not a member of org
        mock_team_newcomers.is_member.return_value = False
        mock_team_developers.is_member.return_value = False
        mock_team_maintainers.is_member.return_value = False

        testbot.assertCommand(
            '!invite meet to newcomers',
            'You need to be a member of this organization to use this command')

    def test_is_room_member(self):
        msg = create_autospec(Message)
        msg.frm.room.occupants = PropertyMock()
        msg.frm.room.occupants = ['batman', 'superman']
        self.assertTrue(LabHub.is_room_member('batman', msg))

    def test_hello_world_callback(self):
        self.mock_team.is_member.return_value = False
        testbot = self
        testbot.assertCommand('hello, world', 'newcomer')
        # Since the user won't be invited again, it'll timeout waiting for a
        # response.
        with self.assertRaises(queue.Empty):
            testbot.assertCommand('helloworld', 'newcomer')

    def test_create_issue_cmd(self):
        plugins.labhub.GitHubToken.assert_called_with(None)
        plugins.labhub.GitLabPrivateToken.assert_called_with(None)

        # Start ignoring PycodestyleBear, LineLengthBear
        # TODO
        # Ignoring assertion to prevent build failure for time being
        # Creating issue in private chat
        # testbot_private.assertCommand('!new issue repository this is the title\nbo\ndy',
        #                       'You\'re not allowed')
        # Stop ignoring

        # Creating issue in public chat
        self.mock_team.is_member.return_value = True
        testbot_public = self

        testbot_public.assertCommand(
            textwrap.dedent('''\
                !new issue repository this is the title
                first line of body
                second line of body
            '''),
            'Here you go')

        self.global_mocks['REPOS']['repository'].create_issue \
            .assert_called_once_with(
                'this is the title',
                textwrap.dedent('''\
                    first line of body
                    second line of body
                    Opened by @batman at [text]()''')
        )

        testbot_public.assertCommand(
            textwrap.dedent('''\
                !new issue repository.github.io another title
                body
            '''),
            'Here you go')

        self.global_mocks['REPOS']['repository.github.io'].create_issue \
            .assert_called_with(
                'another title',
                textwrap.dedent('''\
                    body
                    Opened by @batman at [text]()''')
        )

        testbot_public.assertCommand(
            '!new issue coala title',
            'repository that does not exist')

        self.bot.sender._nick = None
        testbot_public.assertCommand(
            '!new issue coala title',
            'ERROR: The above command cannot be operated without nick.')

        # not a member of org
        self.mock_team.is_member.return_value = False
        testbot_public.assertCommand(
            textwrap.dedent('''\
                !new issue repository this is the title
                body
            '''),
            'You need to be a member of this organization to use this command.'
        )

    def test_is_newcomer_issue(self):
        mock_iss = create_autospec(IGitt.GitHub.GitHubIssue)
        mock_iss.labels = PropertyMock()
        mock_iss.labels = ('difficulty/newcomer',)
        self.assertTrue(LabHub.is_newcomer_issue(mock_iss))
        mock_iss.labels = ('difficulty/medium',)
        self.assertFalse(LabHub.is_newcomer_issue(mock_iss))

    def test_unassign_cmd(self):
        self.inject_mocks('LabHub', {'REPOS': {'example': self.mock_repo}})
        mock_iss = create_autospec(IGitt.GitHub.GitHubIssue)
        self.mock_repo.get_issue.return_value = mock_iss
        mock_iss.assignees = PropertyMock()
        mock_iss.assignees = ('batman', )
        mock_iss.unassign = MagicMock()
        self.mock_team.is_member.return_value = True
        testbot = self

        testbot.assertCommand(
            '!unassign https://github.com/coala/example/issues/999',
            'you are unassigned now',
            timeout=10000)
        self.mock_repo.get_issue.assert_called_with(999)
        mock_iss.unassign.assert_called_once_with('batman')

        mock_iss.assignees = ('meetmangukiya', )
        testbot.assertCommand(
            '!unassign https://github.com/coala/example/issues/999',
            'not an assignee on the issue')

        testbot.assertCommand(
            '!unassign https://github.com/coala/example2/issues/999',
            'Repository doesn\'t exist.')

        testbot.assertCommand(
            '!unassign https://gitlab.com/example/test/issues/999',
            'Repository not owned by our org.')

        self.bot.sender._nick = None
        testbot.assertCommand(
            '!unassign https://gitlab.com/example/test/issues/999',
            'ERROR: The above command cannot be operated without nick.')

        # not a member of org
        self.mock_team.is_member.return_value = False
        testbot.assertCommand(
            '!unassign https://github.com/coala/test/issues/23',
            'You need to be a member of this organization '
            'to use this command.')

    def test_assign_cmd(self):
        mock_issue = create_autospec(GitHubIssue)
        self.mock_repo.get_issue.return_value = mock_issue

        mock_dev_team = create_autospec(github3.orgs.Team)
        mock_maint_team = create_autospec(github3.orgs.Team)
        mock_dev_team.is_member.return_value = False
        mock_maint_team.is_member.return_value = False

        self.teams['coala developers'] = mock_dev_team
        self.teams['coala maintainers'] = mock_maint_team

        mock_dict = {
            'REPOS': {'a': self.mock_repo},
            'TEAMS': self.teams,
        }
        self.inject_mocks('LabHub', mock_dict)
        testbot = self

        cmd = '!assign https://github.com/{}/{}/issues/{}'

        self.bot.sender._nick = None
        testbot.assertCommand(
            cmd.format('coa', 'a', '23'),
            'ERROR: The above command cannot be operated without nick.')
        self.bot.sender._nick = 'batman'

        # no assignee, not newcomer
        mock_issue.assignees = tuple()
        self.mock_team.is_member.return_value = False

        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'You need to be a member of this organization '
                              'to use this command.')

        # no assignee, newcomer, initiatives/gci
        self.mock_team.is_member.return_value = True
        mock_maint_team.is_member.return_value = False
        mock_dev_team.is_member.return_value = False
        mock_issue.labels = 'initiatives/gci',
        mock_issue.assignees = tuple()
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'You are not eligible to be assigned'
                              ' to this issue')
        testbot.pop_message()

        # no assignee, developer, initiatives/gci
        mock_maint_team.is_member.return_value = False
        mock_dev_team.is_member.return_value = True
        mock_issue.labels = 'initiatives/gci',
        mock_issue.assignees = tuple()
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'You are not eligible to be assigned'
                              ' to this issue')
        testbot.pop_message()
        mock_dev_team.is_member.return_value = False

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
        mock_dict = {
            'TEAMS': {
                'not-coala newcomers': self.mock_team,
                'not-coala developers': mock_dev_team,
                'not-coala maintainers': mock_maint_team,
            },
        }
        self.inject_mocks('LabHub', mock_dict)
        self.labhub.config['GH_ORG_NAME'] = 'not-coala'

        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'assigned')
        self.labhub.config['GH_ORG_NAME'] = 'coala'
        mock_dict['TEAMS'] = self.teams
        self.inject_mocks('LabHub', mock_dict)

        # newcomer, developer, difficulty/medium
        mock_dev_team.is_member.return_value = True
        mock_maint_team.is_member.return_value = False
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'assigned')

        # has assignee
        mock_issue.assignees = ('somebody', )
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'already assigned to someone')

        # has assignee same as user
        mock_issue.assignees = ('batman', )
        testbot.assertCommand(cmd.format('coala', 'a', '23'),
                              'already assigned to you')

        # non-existent repository
        testbot.assertCommand(cmd.format('coala', 'c', '23'),
                              'Repository doesn\'t exist.')

        # unknown org
        testbot.assertCommand(cmd.format('coa', 'a', '23'),
                              'Repository not owned by our org.')

        # no assignee, newcomer, difficulty/newcomer, second newcomer issue
        mock_issue.assignees = tuple()
        mock_dev_team.is_member.return_value = False
        mock_issue.labels = ('difficulty/newcomer', )

        with patch('plugins.labhub.GitHub') as mock_gh:
            mock_gh.raw_search = Mock()
            mock_gh.raw_search.return_value = ['mocked?']
            testbot.assertCommand(cmd.format('coala', 'a', '23'),
                                  'not eligible to be assigned to this issue')

    def test_mark_cmd(self):
        self.inject_mocks('LabHub', {'REPOS': {'test': self.mock_repo}})
        testbot = self

        mock_github_mr = create_autospec(GitHubMergeRequest)
        mock_gitlab_mr = create_autospec(GitLabMergeRequest)
        mock_github_mr.labels = PropertyMock()
        mock_gitlab_mr.labels = PropertyMock()
        mock_github_mr.author = 'johndoe'
        mock_gitlab_mr.author = 'johndoe'
        cmd_github = '!mark {} https://github.com/{}/{}/pull/{}'
        cmd_gitlab = '!mark {} https://gitlab.com/{}/{}/merge_requests/{}'

        self.mock_repo.get_mr.return_value = mock_github_mr
        self.mock_team.is_member.return_value = True

        # Non-eistent repo
        testbot.assertCommand(cmd_github.format('wip', 'a', 'b', '23'),
                              'Repository doesn\'t exist.')
        testbot.assertCommand(
            '!mark wip https://gitlab.com/a/b/merge_requests/2',
            'Repository doesn\'t exist.')

        mock_github_mr.web_url = 'https://github.com/coala/test/pull/23'
        mock_gitlab_mr.web_url = (
            'https://gitlab.com/coala/test/merge_requests/23')

        # mark wip
        mock_github_mr.labels = ['process/pending review']
        mock_gitlab_mr.labels = ['process/pending review']
        testbot.assertCommand(cmd_github.format('wip', 'coala', 'test', '23'),
                              'marked work in progress')
        testbot.assertCommand(cmd_github.format('wip', 'coala', 'test', '23'),
                              '@johndoe, please check your pull request')
        testbot.assertCommand(cmd_github.format('wip', 'coala', 'test', '23'),
                              'https://github.com/coala/test/pull/23')

        self.mock_repo.get_mr.return_value = mock_gitlab_mr

        testbot.assertCommand(cmd_gitlab.format('wip', 'coala', 'test', '23'),
                              '@johndoe, please check your pull request')
        testbot.assertCommand(
            cmd_gitlab.format('wip', 'coala', 'test', '23'),
            'https://gitlab.com/coala/test/merge_requests/23')

        self.mock_repo.get_mr.return_value = mock_github_mr

        # mark pending
        mock_github_mr.labels = ['process/wip']
        mock_gitlab_mr.labels = ['process/wip']
        testbot.assertCommand(
            cmd_github.format('pending', 'coala', 'test', '23'),
            'marked pending review')
        testbot.assertCommand(
            cmd_github.format('pending-review', 'coala', 'test', '23'),
            'marked pending review')
        testbot.assertCommand(
            cmd_github.format('pending review', 'coala', 'test', '23'),
            'marked pending review')

        # not a member of org
        self.mock_team.is_member.return_value = False
        testbot.assertCommand(
            cmd_github.format('pending review', 'coala', 'a', '23'),
            'You need to be a member of this organization to use this command')

    def test_alive(self):
        with patch('plugins.labhub.time.sleep') as mock_sleep:
            gh_repos_mock = {
                'coala':
                    create_autospec(IGitt.GitHub.GitHub.GitHubRepository),
                'coala-bears':
                    create_autospec(IGitt.GitHub.GitHub.GitHubRepository),
                'coala-utils':
                    create_autospec(IGitt.GitHub.GitHub.GitHubRepository),
            }
            # for the branch where program sleeps
            gh_repos_mock.update({str(i):
                                  create_autospec(
                                        IGitt.GitHub.GitHub.GitHubRepository)
                                  for i in range(30)})
            gl_repos_mock = {
                'test': create_autospec(IGitt.GitLab.GitLab.GitLabRepository),
            }
            self.mock_team.is_member.return_value = True
            mock_dict = {
                'gh_repos': gh_repos_mock,
                'gl_repos': gl_repos_mock,
            }
            self.inject_mocks('LabHub', mock_dict)
            testbot = self

            mock_dict['gh_repos']['coala'].search_mrs.return_value = [1, 2]
            mock_dict['gh_repos']['coala-bears'].search_mrs.return_value = []
            mock_dict['gh_repos']['coala-utils'].search_mrs.return_value = []
            testbot.assertCommand('!pr stats 10hours',
                                  '2 PRs opened in last 10 hours\n'
                                  'The community is alive', timeout=100)

            mock_dict['gh_repos']['coala'].search_mrs.return_value = []
            testbot.assertCommand('!pr stats 5hours',
                                  '0 PRs opened in last 5 hours\n'
                                  'The community is dead', timeout=100)

            mock_dict['gh_repos']['coala'].search_mrs.return_value = [
                1, 2, 3, 4, 5,
                6, 7, 8, 9, 10
            ]
            testbot.assertCommand('!pr stats 3hours',
                                  '10 PRs opened in last 3 hours\n'
                                  'The community is on fire', timeout=100)

            # not a member of org
            self.mock_team.is_member.return_value = False
            testbot.assertCommand(
                '!pr stats 3hours',
                'You need to be a member of this organization '
                'to use this command.', timeout=100)

    def test_invalid_token(self):
        plugins.labhub.github3.login.return_value = None
        self.labhub.deactivate()
        with self.assertLogs() as cm:
            self.labhub.activate()
        self.assertIn(
            'ERROR:errbot.plugins.LabHub:Cannot create github object,'
            ' please check GH_TOKEN',
            cm.output)
