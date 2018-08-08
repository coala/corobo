import errbot.rendering

from plugins.lmgtfy import Lmgtfy
from tests.isolated_testcase import IsolatedTestCase

text = errbot.rendering.text()


class LmgtfyTest(IsolatedTestCase):

    def test_lmgtfy(self):
        self.assertCommand('!lmgtfy py c', 'https://www.lmgtfy.com/?q=py c')
