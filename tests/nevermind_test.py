from tests.isolated_testcase import IsolatedTestCase


class NevermindTest(IsolatedTestCase):

    def test_nevermind(self):
        self.assertCommand('!nevermind', 'I\'m sorry :(')
        self.assertCommand('!nm', 'I\'m sorry :(')
        self.assertCommand('!nEverMINd', 'I\'m sorry :(')
        self.assertCommand('!nM', 'I\'m sorry :(')
        self.assertCommand('!nmxyz', 'Command "nmxyz" not found.')
        self.assertCommand('!hey nM', 'Command "hey" / "hey nM" not found.')
        self.assertCommand('!nevermindxyz', 'Command "nevermindxyz" not found.')
        self.assertCommand('!hey nEverMINd',
                           'Command "hey" / "hey nEverMINd" not found.')
