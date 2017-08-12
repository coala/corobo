import re

from errbot import BotPlugin, re_botcmd


class The_rules(BotPlugin):
    """
    List the bot rules
    """

    RULES = [
        'A robot may not harm humanity, or, by inaction, allow humanity to '
        'come to harm.',
        'A robot may not injure a human being or, through inaction, allow '
        'a human being to come to harm.',
        'A robot must obey any orders given to it by human beings, except '
        'where such orders would conflict with the First Law.',
        'A robot must protect its own existence as long as such protection '
        'does not conflict with the First or Second Law.'
    ]

    @re_botcmd(pattern=r'the\s+rules',
               re_cmd_name_help='the rules',
               flags=re.IGNORECASE)
    def the_rules(self, msg, args):
        """
        Show the bot rules.
        """
        return '\n'.join(str(i) + '. ' + j for i, j in enumerate(self.RULES))
