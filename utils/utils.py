import os
import subprocess

import git

from errbot import BotPlugin, botcmd


class Utils(BotPlugin):
    """
    Some random utilities
    """

    @botcmd
    def sync(self, msg, arg):
        """Sync the repository from github."""  # Ignore QuotesBear
        repo = git.Repo(os.environ.get('COBOT_ROOT'))
        try:
            repo.pull('--rebase')
            yield 'Sync\'d successfully! :tada:'
        except git.exc.GitCommandError:
            yield 'Can\'t update automatically :('

    @botcmd
    def get_head(self, msg, arg):
        """Yields the head commit."""  # Ignore QuotesBear
        repo = git.Repo(os.environ.get('COBOT_ROOT'))
        head = repo.commit('HEAD')
        yield '`{}`: {}'.format(head.hexsha, head.message)
