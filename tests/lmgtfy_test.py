from tests.isolated_testcase import IsolatedTestCase


class LmgtfyTest(IsolatedTestCase):

    def test_lmgtfy(self):
        self.assertCommand('!lmgtfy py c', 'https://www.lmgtfy.com/?q=py c')
