import re
import string
import textwrap

from errbot import BotPlugin, botcmd


class Pitchfork(BotPlugin):
    """
    To pitchfork users down to ...
    """

    @botcmd
    def pitchfork(self, msg, arg):
        """
        To pitchfork user down to ...
        """
        match = re.match(r'@?([\w-]+)(?:\s+(?:down\s+)?to\s+(.+))?$',
                         arg)
        if match:
            user = match.group(1)
            place = match.group(2) if match.group(2) else 'offtopic'
            return textwrap.dedent((
                string.Template(r"""
                    @$user, you are being pitchforked down to $place
                    ```
                                                          .+====----->
                                                           \\('
                    =====================================<%{%{%{>>+===---> $user
                                                           //(,
                                                          .+====----->
                    ```
                """).substitute(user=user,
                                place=('[offtopic]('
                                       'https://gitter.im/coala/coala/offtopic)'
                                       if place == 'offtopic' else place))
                ))
        else:
            return "Usage: `pitchfork user [[down] to place]`"
