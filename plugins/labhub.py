import json
import os
import re

import github3
from IGitt.GitHub.GitHub import GitHub, GitHubToken
from IGitt.GitLab.GitLab import GitLab, GitLabPrivateToken
from errbot import BotPlugin, re_botcmd

from plugins import constants


class LabHub(BotPlugin):
    """GitHub and GitLab utilities"""  # Ignore QuotesBear

    INVITE_SUCCESS = {
        'newcomers': """
 Welcome @{}! :tada:\n\nTo get started, please follow our
 [newcomers guide](https://coala.io/newcomer). Most issues will be explained
 there and in linked pages - it will save you a lot of time, just read it.
 *Really.*\n\n*Do not take an issue if you don't understand it on your own.*
 Especially if you are new you have to be aware that getting started with an
 open source community is not trivial: you will have to work hard and most
 likely become a better coder than you are now just as we all did.\n\n
 Don't get us wrong: we are *very* glad to have you with us on this journey
 into open source! We will also be there for you at all times to help you
 with actual problems. :)
""",
        'developers': """
 Wow @{}, you are a part of developers team now! :tada: Welcome to our
 community!
""",
        'maintainers': """
 @{} you seem to be awesome! You are now a maintainer! :tada: Please go
 through https://github.com/coala/coala/wiki/Membership
"""
    }

    GH_ORG_NAME = constants.GH_ORG_NAME
    GL_ORG_NAME = constants.GL_ORG_NAME

    def __init__(self, bot, name=None):
        super().__init__(bot, name)

        teams = dict()
        try:
            gh = github3.login(token=os.environ.get('GH_TOKEN'))
            assert gh is not None
        except AssertionError:
            self.log.error('Cannot create github object, please check GH_TOKEN')
        else:
            self.GH3_ORG = gh.organization(self.GH_ORG_NAME)
            for team in self.GH3_ORG.iter_teams():
                teams[team.name] = team

        self._teams = teams

        self.IGH = GitHub(GitHubToken(os.environ.get('GH_TOKEN')))
        self.IGL = GitLab(GitLabPrivateToken(os.environ.get('GL_TOKEN')))

        self.REPOS = dict()

        try:
            self.gh_repos = {repo.full_name.split('/')[1]: repo for repo in
                             filter(lambda x: (x.full_name.split('/')[0] ==
                                               self.GH_ORG_NAME),
                                    self.IGH.write_repositories)}
        except RuntimeError:
            self.log.exception('Something went wrong in fetching github repos.')
        else:
            self.REPOS.update(self.gh_repos)

        try:
            self.gl_repos = {repo.full_name.split('/')[1]: repo for repo in
                             filter(lambda x: (x.full_name.split('/')[0] ==
                                               self.GL_ORG_NAME),
                                    self.IGL.write_repositories)}
        except RuntimeError:  # pragma: no cover, for logging
            self.log.exception('Something went wrong in fetching gitlab repos.')
        else:
            self.REPOS.update(self.gl_repos)

    @property
    def TEAMS(self):
        return self._teams

    @TEAMS.setter
    def TEAMS(self, new):
        self._teams = new

    @re_botcmd(pattern=r'(?:(?:invite)|(?:inv))\s+(\w+)\s*(?:to)\s+(\w+)')
    def invite_cmd(self, msg, match):
        """
        Invite given user to given team. By default it invites to
        "newcomers" team.
        """
        invitee = match.group(1)
        inviter = msg.frm.nick

        team = (self.GH_ORG_NAME + ' newcomers' if match.group(2) is None
                else match.group(2))

        self.log.info('{} invited {} to {}'.format(inviter, invitee, team))

        if self.TEAMS[self.GH_ORG_NAME + ' maintainers'].is_member(inviter):
            valid_teams = ['newcomers', 'developers', 'maintainers']
            if team.lower() not in valid_teams:
                return 'Please select from one of the ' + ', '.join(valid_teams)
            team_mapping = {
                'newcomers': self.GH_ORG_NAME + ' newcomers',
                'developers': self.GH_ORG_NAME + ' developers',
                'maintainers': self.GH_ORG_NAME + ' maintainers'
            }

            # send the invite
            self.TEAMS[team_mapping[team.lower()]].invite(invitee)
            return self.INVITE_SUCCESS[team.lower()].format(invitee)
        else:
            return ('@{}, you are not a maintainer, only maintainers can invite'
                    ' other people. Nice try :poop:'.format(inviter))

    def callback_message(self, msg):
        """Invite the user whose message includes the holy 'hello world'"""
        if re.search(r'hello\s*,?\s*world', msg.body, flags=re.IGNORECASE):
            user = msg.frm.nick
            if not self.TEAMS[self.GH_ORG_NAME + ' newcomers'].is_member(user):
                # send the invite
                self.send(msg.frm,
                          self.INVITE_SUCCESS['newcomers'].format(user))
                self.TEAMS[self.GH_ORG_NAME + ' newcomers'].invite(user)

    @re_botcmd(pattern=r'(?:new|file) issue ([\w-]+?)(?: |\n)(.+?)(?:$|\n((?:.|\n)*))',  # Ignore LineLengthBear, PyCodeStyleBear
               flags=re.IGNORECASE)
    def create_issut_cmd(self, msg, match):
        """Create issues on GitHub and GitLab repositories."""  # Ignore QuotesBear, LineLengthBear, PyCodeStyleBear
        repo_name = match.group(1)
        iss_title = match.group(2)
        iss_description = match.group(3) if match.group(3) is not None else ''
        if repo_name in self.REPOS:
            repo = self.REPOS[repo_name]
            iss = repo.create_issue(iss_title, iss_description)
            return 'Here you go: {}'.format(iss.url)
        else:
            return ('Can\'t create an issue for a repository that does not '
                    'exist. Please ensure that the repository is available '
                    'and owned by coala.')

    @re_botcmd(pattern=r'^unassign\s+https://(github|gitlab)\.com/([^/]+)/([^/]+)/issues/(\d+)',  # Ignore LineLengthBear, PyCodeStyleBear
               flags=re.IGNORECASE)
    def unassign_cmd(self, msg, match):
        """Unassign from an issue."""  # Ignore QuotesBear
        org = match.group(2)
        repo_name = match.group(3)
        issue_number = match.group(4)

        user = msg.frm.nick

        try:
            assert org == self.GH_ORG_NAME or org == self.GL_ORG_NAME
        except AssertionError:
            return 'Repository not owned by our org.'

        try:
            iss = self.REPOS[repo_name].get_issue(int(issue_number))
        except KeyError:
            return 'Repository doesn\'t exist.'
        else:
            if user in iss.assignees:
                iss.unassign(user)
                return '@{}, you are unassigned now :+1:'.format(user)
            else:
                return 'You are not an assignee on the issue.'

    @re_botcmd(pattern=r'mark\s+(wip|pending)\s+https://(github|gitlab)\.com/([^/]+)/([^/]+)/(pull|merge_requests)/(\d+)',  # Ignore LineLengthBear, PyCodeStyleBear
               flags=re.IGNORECASE)
    def mark_cmd(self, msg, match):
        """Mark a given PR/MR with status labels."""  # Ignore QuotesBear
        state, host, org, repo_name, xr, number = match.groups()

        if host.lower() == 'github':
            assert xr.lower() == 'pull'
        elif host.lower() == 'gitlab':
            assert xr.lower() == 'merge_requests'

        try:
            mr = self.REPOS[repo_name].get_mr(number)
        except KeyError:
            return 'Repository doesn\'t exist.'
        else:
            current_labels = list(mr.labels)
            if state == 'wip':
                pending_labels = ['process/pending_review',
                                  'process/pending review']
                for label in filter(lambda x: x in current_labels,
                                    pending_labels):
                    current_labels.remove(label)
                current_labels.append('process/wip')
                mr.labels = current_labels
                return ('The pull request {mr_link} is marked *work in progress'
                        '*. Use `cobot mark pending` or push to your branch if '
                        'feedback from the community is needed again.'.format(
                            mr_link=mr.url)
                        )
            else:
                wip_labels = ['process/wip']
                for label in filter(lambda x: x in current_labels,
                                    wip_labels):
                    current_labels.remove(label)
                current_labels.append('process/pending review')
                mr.labels = current_labels
                return ('The pull request {mr_link} is marked *pending review*,'
                        'so you will get feedback from the community. Use '
                        '`cobot mark wip` if there are known issues that should'
                        ' be corrected by the author.'.format(mr_link=mr.url))

    @re_botcmd(pattern=r'^assign\s+https://(github|gitlab)\.com/([^/]+)/([^/]+)/issues/(\d+)',  # Ignore LineLengthBear, PyCodeStyleBear
               flags=re.IGNORECASE)
    def assign_cmd(self, msg, match):
        """Assign to GitLab and GitHub issues."""  # Ignore QuotesBear
        org = match.group(2)
        repo_name = match.group(3)
        iss_number = match.group(4)

        user = msg.frm.nick

        try:
            assert org == self.GH_ORG_NAME or org == self.GL_ORG_NAME
        except AssertionError:
            yield 'Repository not owned by our org.'
            return

        checks = []

        def register_check(function):
            checks.append(function)
            return function

        @register_check
        def difficulty_level(user, iss):
            """
            True if:
            1. A newcomer is asking for assignment to low or newcomer issue.
            2. The user belongs to developers or maintainers team as well as
               newcomers team.
            False if
            1. A newcomer asks for assignment to an issue that has no difficulty
               label.
            2. A newcomer asks for assignment to an issue with difficulty higher
               than low.
            """
            if (self.TEAMS[self.GH_ORG_NAME + ' newcomers'].is_member(user) and
                not (self.TEAMS[self.GH_ORG_NAME + ' developers'].is_member(
                        user
                    ) or
                    self.TEAMS[self.GH_ORG_NAME + ' maintainers'].is_member(
                        user
                    ))):
                diff_labels = filter(lambda x: 'difficulty' in x, iss.labels)
                if list(filter(lambda x: ('low' in x) or ('newcomer' in x),
                               diff_labels)):
                    return True
                else:
                    return False
            elif self.GH3_ORG.is_member(user):
                return True

        def eligible(user, iss):
            for chk in checks:
                if not chk(user, iss):
                    return False
            return True

        eligility_conditions = [
            '- A newcomer cannot be assigned to an issue with a difficulty '
            'level higher than newcomer or low difficulty.',
        ]

        try:
            iss = self.REPOS[repo_name].get_issue(int(iss_number))
        except KeyError:
            yield 'Repository doesn\'t exist.'
        else:
            if not iss.assignees:
                if eligible(user, iss):
                    iss.assign(user)
                    yield ('Congratulations! You\'ve been assigned to the '
                           'issue. :tada:')
                else:
                    yield 'You are not eligible to be assigned to this issue.'
                    yield '\n'.join(eligility_conditions)
            else:
                yield ('The issue is already assigned to someone. Please '
                       'check if the assignee is still working on the issue, '
                       'if not, you should ask for reassignment.')
