import errbot.rendering

from tests.isolated_testcase import IsolatedTestCase


class ShipItTest(IsolatedTestCase):

    def test_ship_it(self):
        text = errbot.rendering.text()
        self.assertCommand('!shipit', text.convert('![ship it!]()'))
