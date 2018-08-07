import re

from errbot import BotPlugin, re_botcmd


class Nevermind(BotPlugin):
    """
    Doesn't mind
    """

    @re_botcmd(pattern=r'^(nm)$|^(nevermind)$', flags=re.IGNORECASE)
    def nevermind(self, message, match):
        """Doesn't mind"""
        return "I'm sorry :("
