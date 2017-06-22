import os
import subprocess

import git

from errbot import BotPlugin, botcmd


run = lambda x: subprocess.Popen(x.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

class Utils(BotPlugin):
    """
    Some random utilities
    """

    @botcmd(admin_only=True)
    def sync(self, msg, arg):
        """Sync the repository from github."""  # Ignore QuotesBear
        repo = git.Repo(os.environ.get('COBOT_ROOT'))
        try:
            repo.remote('origin').pull('--rebase')
            yield 'Sync\'d successfully! :tada:'
        except git.exc.GitCommandError:
            yield 'Can\'t update automatically :('

    @botcmd
    def get_head(self, msg, arg):
        """Yields the head commit."""  # Ignore QuotesBear
        repo = git.Repo(os.environ.get('COBOT_ROOT'))
        head = repo.commit('HEAD')
        yield '`{}`: {}'.format(head.hexsha, head.message)

    @botcmd(admin_only=True)
    def install_requirements(self, msg, arg):
        """Installs requirements"""  # Ignore QuotesBear
        os.chdir(os.environ.get('COBOT_ROOT'))
        ran = run('pip install -r requirements.txt')
        yield 'installing requirements...'
        yield ran.stdout.read().decode('utf-8')
        yield ran.stderr.read().decode('utf-8')
