import re

from errbot import BotPlugin, re_botcmd


class The_rules(BotPlugin):
    """
    List the bot rules
    """

    @re_botcmd(pattern=r'the\s+rules',
               re_cmd_name_help='the rules',
               flags=re.IGNORECASE,
               template='the_rules.jinja2')
    def the_rules(self, msg, args):
        """
        Show the bot rules.
        """
        return {'rules': True}
