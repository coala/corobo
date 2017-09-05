from errbot import BotPlugin


class Deprecate_corobo(BotPlugin):
    """
    A callback for every message that starts with cobot, hence, leaving a deprecation notice
    """

    def callback_message(self, msg):
        """
        Notify the user issuing the command that cobot is deprecated.
        """
        if msg.body.startswith("cobot "):
            self.send(
                msg.frm,
                "@{} usage of `cobot` has been deprecated, please use `corobo` "
                "from now on.".format(msg.frm.nick)
            )
