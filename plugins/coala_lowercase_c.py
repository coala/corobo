import random
import re

from errbot import BotPlugin


class Coala_lowercase_c(BotPlugin):
    """coala is always written with a lower case c."""  # Ignore QuotesBear

    def callback_message(self, msg):
        emots = [':(', ':angry:', ':confounded:',
                 ':disappointed:', ':triumph:']

        match_coala = re.search(r'(?:^|[^\w])C+[Oo]+[Aa]+[Ll]+[Aa]+(?:$|[^\w])',
                                msg.body)
        if match_coala:
            self.send(
                msg.frm,
                '@{}, coala is always written with a lower case c. {}'.format(
                    msg.frm.nick, emots[random.randint(0, len(emots) - 1)]
                )
            )

        match_cep = re.search(r'(?:^|[^\w])CEP(?:$|[^\w])', msg.body)
        if match_cep:
            self.send(
                msg.frm,
                '@{}, cEP is always written with a lower case c.'.format(
                    msg.frm.nick
                )
            )
