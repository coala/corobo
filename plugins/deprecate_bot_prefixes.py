from errbot import BotPlugin


class DeprecateBotPrefixes(BotPlugin):
    """
    A callback for every message that starts with depecrated prefix, hence,
    leaving a deprecation notice
    """

    def callback_message(self, msg):
        """
        Notify the user issuing the command that use deprecated prefix.
        """

        for deprecated_prefix in self.bot_config.BOT_DEPRECATED_PREFIXES:
            if msg.body.startswith(deprecated_prefix):
                self.send(
                    msg.frm,
                    "@{} usage of {} has been deprecated, please use {} "
                    "from now on.".format(msg.frm.nick, deprecated_prefix,
                                          self.bot_config.BOT_PREFIX)
                )
