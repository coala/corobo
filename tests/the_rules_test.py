from tests.isolated_testcase import IsolatedTestCase


class TheRulesTest(IsolatedTestCase):

    def test_the_rules(self):
        self.assertCommand('!the rules', 'A robot may not harm humanity')
        self.assertCommand('!the  rules', 'A robot may not injure a human')
        self.assertCommand('!THE RUles', 'A robot must obey any orders')
