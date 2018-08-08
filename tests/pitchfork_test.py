from tests.isolated_testcase import IsolatedTestCase


class PitchForkTest(IsolatedTestCase):

    def test(self):
        self.assertCommand('!pitchfork @meet', 'being pitchforked')
        self.assertCommand('!pitchfork @meet down to hell', 'being pitchforked')
        self.assertCommand('!pitchfork meet to hell', 'being pitchforked')
        self.assertCommand('!pitchfork', 'Usage')
