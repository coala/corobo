from itertools import chain

from errbot import BotPlugin
from errbot.templating import tenv

from plugins import constants


class SpammingAlert(BotPlugin):
    """
    A plugin which alerts the user that they might be spamming.
    """

    CONFIG_TEMPLATE = {
        'MAX_MSG_LEN': constants.MAX_MSG_LEN,
        'MAX_LINES': constants.MAX_LINES
    }

    def get_configuration_template(self):
        return self.CONFIG_TEMPLATE

    def configure(self, configuration):
        """
        Enable partial configuration.
        """

        if configuration:
            config = dict(chain(self.CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = self.CONFIG_TEMPLATE
        super(SpammingAlert, self).configure(config)

    def check_configuration(self, configuration):
        pass

    def callback_message(self, msg):
        """
        Alert the user that his/her message is too long or has too
        many lines.
        """

        if (len(msg.body) > self.config['MAX_MSG_LEN'] or
                msg.body.count('\n') >= self.config['MAX_LINES']):
            user = msg.frm.nick
            response = tenv().get_template(
                'spam_alert.jinja2.md'
            ).render(
                target=user
            )
            self.send(msg.frm, response)
