import time
import threading

from errbot import BotPlugin, botcmd


class Re_botcmd_fullmatch(BotPlugin):
    """
    Checks whether all re_botcmd regexes are fullmatches or not and warns the
    admins.
    """

    def activate(self):
        super().activate()
        # start asynchronously
        threading.Thread(target=self.check_regexes).start()

    def check_regexes(self):
        # Allow all plugins to activate
        time.sleep(60)

        if hasattr(self.bot_config, 'RE_BOTCMD_FULLMATCH_IGNORES'):
            ignores = self.bot_config.RE_BOTCMD_FULLMATCH_IGNORES
        else:
            ignores = tuple()

        msg = 'Following re_botcmds have pattern that are not fullmatches: '

        for name, func in dict(self._bot.re_commands).items():
            pattern = func._err_command_re_pattern.pattern
            if not (pattern.startswith('^') and pattern.endswith('$') and
                    name not in ignores):
                msg += '\n- `{}` - `{}`'.format(name, pattern)

        self.warn_admins(msg)
