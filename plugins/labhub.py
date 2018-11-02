import datetime
import re
import time

import github3
from IGitt.GitHub.GitHub import GitHub, GitHubToken
from IGitt.GitLab.GitLab import GitLab, GitLabPrivateToken
from errbot import BotPlugin, cmdfilter, re_botcmd
from errbot.templating import tenv

from plugins import constants
from utils.backends import message_link
from utils.mixin import DefaultConfigMixin


class LabHub(DefaultConfigMixin, BotPlugin):
    """GitHub and GitLab utilities"""  # Ignore QuotesBear

    CONFIG_TEMPLATE = {
        'GH_ORG_NAME': None,
        'GH_TOKEN': None,
        'GL_ORG_NAME': None,
        'GL_TOKEN': None,
    }

    def activate(self):
        super().activate()

        teams = dict()
        try:
            gh = github3.login(token=self.config['GH_TOKEN'])
            assert gh is not None
        except AssertionError:
            self.log.error('Cannot create github object, please check GH_TOKEN')
        else:
            self.GH3_ORG = gh.organization(self.GH_ORG_NAME)
            for team in self.GH3_ORG.teams():
                teams[team.name] = team

        self._teams = teams

        self.IGH = GitHub(GitHubToken(self.config['GH_TOKEN']))
        self.IGL = GitLab(GitLabPrivateToken(self.config['GL_TOKEN']))

        self.REPOS = dict()

        try:
            self.gh_repos = {repo.full_name.split('/')[-1]: repo for repo in
                             filter(lambda x: (x.full_name.split('/')[0] ==
                                               self.GH_ORG_NAME),
                                    self.IGH.write_repositories)}
        except RuntimeError:  # pragma: no cover, for logging
            self.log.exception('Something went wrong in fetching github repos.')
        else:
            self.REPOS.update(self.gh_repos)

        try:
            self.gl_repos = {repo.full_name.split('/')[-1]: repo for repo in
                             filter(lambda x: (x.full_name.split('/')[0] ==
                                               self.GL_ORG_NAME),
                                    self.IGL.write_repositories)}
        except RuntimeError:  # pragma: no cover, for logging
            self.log.exception('Something went wrong in fetching gitlab repos.')
        else:
            self.REPOS.update(self.gl_repos)

        self.hello_world_users = set()

    @property
    def GH_ORG_NAME(self):
        return self.config['GH_ORG_NAME']

    @property
    def GL_ORG_NAME(self):
        return self.config['GL_ORG_NAME']

    @property
    def TEAMS(self):
        return self._teams

    @TEAMS.setter
    def TEAMS(self, new):
        self._teams = new

    def team_mapping(self):
        return {
            'newcomers': self.TEAMS[self.GH_ORG_NAME + ' newcomers'],
            'developers': self.TEAMS[self.GH_ORG_NAME + ' developers'],
            'maintainers': self.TEAMS[self.GH_ORG_NAME + ' maintainers'],
        }

    @cmdfilter
    def members_only(self, msg, cmd, args, dry_run):
        user = msg.frm.nick
        commands = constants.PRIVATE_CMDS

        if cmd in commands:
            for team in self.team_mapping().values():
                if team.is_member(user):
                    return msg, cmd, args
            self.send(msg.frm, 'You need to be a member of this organization '
                      'to use this command.')
            return None, None, None
        else:
            return msg, cmd, args

    def is_team_member(self, user, team):
        teams = self.team_mapping()
        return teams[team].is_member(user)

    @staticmethod
    def is_room_member(invitee, msg):
        return invitee in msg.frm.room.occupants

    # Ignore LineLengthBear, PycodestyleBear
    @re_botcmd(pattern=r'^(?:(?:welcome)|(?:inv)|(?:invite))\s+@?([\w-]+)(?:\s+(?:to)\s+(\w+))?$',
               re_cmd_name_help='invite ([@]<username> [to <team>]|me)')
    def invite_cmd(self, msg, match):
        """
        Invite given user to given team. By default it invites to
        "newcomers" team.
        """
        invitee = match.group(1)
        inviter = msg.frm.nick
        if not inviter:
            yield 'ERROR: The above command cannot be operated without nick.'
            return

        team = 'newcomers' if match.group(2) is None else match.group(2)
        team = team.lower()

        is_developer = self.is_team_member(inviter, 'developers')
        is_maintainer = self.is_team_member(inviter, 'maintainers')

        self.log.info('{} invited {} to {}'.format(inviter, invitee, team))

        valid_teams = self.team_mapping()
        if team not in valid_teams:
            yield 'Please select from one of the valid teams: ' + ', '.join(
                   valid_teams)
            return

        def invite(invitee, team):
            self.team_mapping()[team].invite(invitee)

        if not self.is_room_member(invitee, msg):
            yield '@{} is not a member of this room.'.format(invitee)
            return

        if is_maintainer:
            invite(invitee, team)
            yield tenv().get_template(
                'labhub/promotions/{}.jinja2.md'.format(team)
            ).render(
                target=invitee,
            )
        elif is_developer:
            if team == 'newcomers':
                invite(invitee, team)
                yield tenv().get_template(
                    'labhub/promotions/{}.jinja2.md'.format(team)
                ).render(
                    target=invitee,
                )
            else:
                yield tenv().get_template(
                    'labhub/errors/not-eligible-invite.jinja2.md'
                ).render(
                    action='invite someone to developers or maintainers',
                    designation='maintainer',
                    target=inviter,
                )
        else:
            yield tenv().get_template(
                'labhub/errors/not-eligible-invite.jinja2.md'
            ).render(
                action='invite other people',
                designation='developer/maintainer',
                target=inviter,
            )

    def callback_message(self, msg):
        """Invite the user whose message includes the holy 'hello world'"""
        if re.search(r'hello\s*,?\s*world', msg.body, flags=re.IGNORECASE):
            user = msg.frm.nick
            if (not self.is_team_member(user, 'newcomers')
                    and user not in self.hello_world_users):
                response = tenv().get_template(
                    'labhub/hello-world.jinja2.md'
                ).render(
                    target=user,
                )
                self.send(msg.frm, response)
                self.hello_world_users.add(user)

    @re_botcmd(pattern=r'(?:new|file) issue ([\w\-\.]+?)(?: |\n)(.+?)(?:$|\n((?:.|\n)*))',  # Ignore LineLengthBear, PyCodeStyleBear
               re_cmd_name_help='new issue repo-name title\n[description]',
               flags=re.IGNORECASE)
    def create_issue_cmd(self, msg, match):
        """Create issues on GitHub and GitLab repositories."""  # Ignore QuotesBear, LineLengthBear, PyCodeStyleBear
        user = msg.frm.nick
        if not user:
            yield 'ERROR: The above command cannot be operated without nick.'
            return
        repo_name = match.group(1)
        iss_title = match.group(2)
        iss_description = match.group(3) if match.group(3) is not None else ''
        extra_msg = '\nOpened by @{username} at [{backend}]({msg_link})'.format(
            username=user,
            backend=self.bot_config.BACKEND,
            msg_link=message_link(self, msg)
        )

        if repo_name in self.REPOS:
            repo = self.REPOS[repo_name]
            iss = repo.create_issue(iss_title, iss_description + extra_msg)
            yield 'Here you go: {}'.format(iss.web_url)
        else:
            yield tenv().get_template(
                'labhub/errors/no-repository.jinja2.md'
            ).render(
                target=user,
            )

    @staticmethod
    def is_newcomer_issue(iss):
        diff_labels = filter(lambda x: 'difficulty' in x, iss.labels)
        if list(filter(lambda x: 'newcomer' in x, diff_labels)):
            return True
        else:
            return False

    @re_botcmd(pattern=r'^unassign\s+https://(github|gitlab)\.com/([^/]+)/([^/]+)/issues/(\d+)',  # Ignore LineLengthBear, PyCodeStyleBear
               re_cmd_name_help='unassign <complete-issue-URL>',
               flags=re.IGNORECASE)
    def unassign_cmd(self, msg, match):
        """Unassign from an issue."""  # Ignore QuotesBear
        org = match.group(2)
        repo_name = match.group(3)
        issue_number = match.group(4)

        user = msg.frm.nick
        if not user:
            yield 'ERROR: The above command cannot be operated without nick.'
            return

        try:
            assert org == self.GH_ORG_NAME or org == self.GL_ORG_NAME
        except AssertionError:
            yield 'Repository not owned by our org.'
            return

        try:
            iss = self.REPOS[repo_name].get_issue(int(issue_number))
        except KeyError:
            yield 'Repository doesn\'t exist.'
        else:
            if user in iss.assignees:
                iss.unassign(user)
                yield '@{}, you are unassigned now :+1:'.format(user)
            else:
                yield 'You are not an assignee on the issue.'

    @re_botcmd(pattern=r'mark\s+(wip|pending(?:(?:-|\s+)review)?\b)\s+https://(github|gitlab)\.com/([^/]+)/([^/]+)/(pull|merge_requests)/(\d+)',  # Ignore LineLengthBear, PyCodeStyleBear
               re_cmd_name_help='mark (wip|pending) <complete-PR-URL>',
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
            yield 'Repository doesn\'t exist.'
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

                ping = ''
                if mr.author is not None:
                    ping = ('\n@{user_login}, please check your pull '
                            'request.'.format(user_login=mr.author))

                yield ('The pull request {mr_link} is marked *work in progress'
                       '*. Use `{bot_prefix} mark pending` or push to your '
                       'branch if feedback from the community is needed '
                       'again.{ping}'.format(
                           mr_link=mr.web_url,
                           bot_prefix=self.bot_config.BOT_PREFIX,
                           ping=ping)
                       )
            else:
                wip_labels = ['process/wip']
                for label in filter(lambda x: x in current_labels,
                                    wip_labels):
                    current_labels.remove(label)
                current_labels.append('process/pending review')
                mr.labels = current_labels
                yield ('The pull request {mr_link} is marked *pending review*,'
                       'so you will get feedback from the community. Use '
                       '`{bot_prefix} mark wip` if there are known issues that'
                       ' should be corrected by the author.'.format(
                           mr_link=mr.web_url,
                           bot_prefix=self.bot_config.BOT_PREFIX)
                       )

    @re_botcmd(pattern=r'^assign\s+https://(github|gitlab)\.com/([^/]+)/([^/]+/)+issues/(\d+)',  # Ignore LineLengthBear, PyCodeStyleBear
               re_cmd_name_help='assign <complete-issue-URL>',
               flags=re.IGNORECASE)
    def assign_cmd(self, msg, match):
        """Assign to GitLab and GitHub issues."""  # Ignore QuotesBear
        org = match.group(2)
        repo_name = match.group(3)[:-1]
        iss_number = match.group(4)

        user = msg.frm.nick
        if not user:
            yield 'ERROR: The above command cannot be operated without nick.'
            return

        try:
            assert org == self.GH_ORG_NAME or org == self.GL_ORG_NAME
        except AssertionError:
            yield 'Repository not owned by our org.'
            return

        checks = []

        def register_check(function):
            checks.append(function)
            return function

        if self.GH_ORG_NAME == 'coala' and self.GL_ORG_NAME == 'coala':
            @register_check
            def difficulty_level(user, iss):
                """
                True if:
                1. A newcomer is asking for assignment to low or newcomer issue.
                2. The user belongs to developers or maintainers team as well as
                   newcomers team.
                False if:
                1. A newcomer asks for assignment to an issue that has no
                   difficulty label.
                2. A newcomer asks for assignment to an issue with difficulty
                   higher than low.
                """
                if (self.is_team_member(user, 'newcomers') and not
                    (self.is_team_member(user, 'developers') or
                        self.is_team_member(user, 'maintainers'))):
                    diff_labels = filter(
                        lambda x: 'difficulty' in x, iss.labels)
                    if list(filter(lambda x: ('low' in x) or ('newcomer' in x),
                                   diff_labels)):
                        return True
                    else:
                        return False
                elif self.GH3_ORG.is_member(user):
                    return True

            @register_check
            def newcomer_issue_check(user, iss):
                """
                True if:  Issue is not labeled `difficulty/newcomer` and
                          user is not a newcomer.
                False if: A `difficulty/newcomer` issue is already assigned
                          to the user.
                """
                if (self.is_newcomer_issue(iss)
                        and self.is_team_member(user, 'newcomers')):
                    search_query = 'user:coala assignee:{} ' \
                                   'label:difficulty/newcomer'.format(user)
                    result = GitHub.raw_search(GitHubToken(
                        self.config['GH_TOKEN']), search_query)
                    return not (sum(1 for _ in result) >= 1)
                else:
                    return True

            @register_check
            def block_gci_issue_assignment(user, iss):
                """
                True if the issue is not labelled with 'initiatives/gci'.
                False if the issue has been labelled with 'initiatives/gci'.
                """
                return 'initiatives/gci' not in iss.labels

        def eligible(user, iss):
            for chk in checks:
                if not chk(user, iss):
                    return False
            return True

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
                    yield tenv().get_template(
                        'labhub/errors/not-eligible.jinja2.md'
                    ).render(
                        organization=self.GH_ORG_NAME,
                    )
            elif user in iss.assignees:
                yield ('The issue is already assigned to you.')
            else:
                yield tenv().get_template(
                    'labhub/errors/already-assigned.jinja2.md'
                ).render(
                    username=user,
                )

    @staticmethod
    def community_state(pr_count: dict):
        if (sum(pr_count.values())):
            if any([pr_count.get('coala-bears', 0) >= 2,
                    pr_count.get('coala', 0) >= 5,
                    pr_count.get('coala-utils', 0) >= 1]):
                return 'on fire'
            else:
                return 'alive'
        else:
            return 'dead'

    @re_botcmd(pattern=r'pr\s+stats\s+(\d+)(?:hours|hrs)',
               re_cmd_name_help='pr stats <number-of-hours>(hours|hrs)')
    def pr_stats(self, msg, match):
        hours = match.group(1)
        pr_count = dict()
        start = time.time()
        for count, (name, repo) in enumerate(self.gh_repos.items(), 1):
            pr_count[name] = len(list(repo.search_mrs(
                                         created_after=(datetime.datetime.now()
                                                        - datetime.timedelta(
                                                              hours=int(hours)))
                             )))
            # handle github rate limiting
            if (count % 30 == 0):
                seconds_to_sleep = 60 - (time.time() - start)
                self.log.info(
                    'Sleeping for {} seconds'.format(seconds_to_sleep))
                time.sleep(seconds_to_sleep)
                self.log.info('Waking up from sleep')
                start = time.time()

        for name, repo in self.gl_repos.items():
            pr_count[name] = len(list(repo.search_mrs(
                                         created_after=(datetime.datetime.now()
                                                        - datetime.timedelta(
                                                              hours=int(hours)))
                             )))
        reply = ''
        reply += '{} PRs opened in last {} hours'.format(sum(pr_count.values()),
                                                         hours)

        reply += '\nThe community is {state}'.format(
                    state=type(self).community_state(pr_count)
                 )
        yield reply
