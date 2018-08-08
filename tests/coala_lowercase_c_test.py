from tests.isolated_testcase import IsolatedTestCase


class CoalaLowercaseTest(IsolatedTestCase):

    def test_coala_lowercase(self):
        self.assertCommand('what is Coala?',
                           'coala is always written with a lower case c')

    def test_cep(self):
        self.assertCommand('what is a CEP?',
                           'cEP is always written with a lower case c')
