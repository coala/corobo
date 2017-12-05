import re
import glob
import os.path

from errbot import BotPlugin, re_botcmd
from errbot.templating import tenv


class Explain(BotPlugin):
    """
    Explain various terms
    """

    files = glob.glob('plugins/templates/explain/*.jinja2.md')
    KNOWN_KEYS = []
    for fname in files:
        KNOWN_KEYS.append(fname.replace(
            'plugins/templates/explain/', ''
        ).replace('.jinja2.md', ''))

    ERROR_MSG = (
        'Sorry, I only know about these things:\n- ' +
        '\n- '.join(KNOWN_KEYS)
    )

    @re_botcmd(pattern=r'^explain\s+(\w+)(?:\s+to\s+@?([\w-]+))?$',
               re_cmd_name_help='explain <term>',
               flags=re.IGNORECASE)
    def explain(self, msg, match):
        """Explain various terms."""  # Ignore QuotesBear
        user = msg.frm.nick
        response = ''
        filename = 'explain/{}.jinja2.md'.format(match.group(1).lower())
        if match.group(1).lower() in self.KNOWN_KEYS:
            if match.group(2):
                response += '@{}: \n'.format(match.group(2))
            response += tenv().get_template(filename).render(
                username=user,
                target=match.group(2),
                bot_prefix=self.bot_config.BOT_PREFIX,
            )
        else:
            response = self.ERROR_MSG

        return response
