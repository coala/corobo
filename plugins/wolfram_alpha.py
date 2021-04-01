import wolframalpha

from errbot import BotPlugin, botcmd
from utils.mixin import DefaultConfigMixin


class WolframAlpha(DefaultConfigMixin, BotPlugin):
    """
    Query the Computational Knowledge Engine
    """

    CONFIG_TEMPLATE = {
        'WA_TOKEN': None,
    }

    def activate(self):
        super().activate()
        self.client = wolframalpha.Client(self.config['WA_TOKEN'])

    @botcmd
    def wa(self, msg, arg):
        """
        Query the Computational Knowledge Engine.
        """
        ans = ''
        res = self.client.query(arg)
        for pod in res.pods:
            if pod.title in ['Result', 'Results']:
                for sub in pod.subpods:
                    ans += sub.plaintext
        if ans == '':
            self.log.info("No results found!")
        return ans if ans else 'Dunno :('
