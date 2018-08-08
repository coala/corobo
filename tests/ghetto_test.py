import requests_mock
import vcr

from tests.isolated_testcase import IsolatedTestCase


class GhettoTest(IsolatedTestCase):

    @vcr.use_cassette('tests/cassettes/ghetto.yaml')
    def test_ghetto(self):
        self.assertCommand('!ghetto hi, whats up?', 'hi, wassup?')
        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'http://www.gizoogle.net/textilizer.php',
                           text='test text which will not match with the regex')
            self.assertCommand('!ghetto ...', 'Shiznit happens!')
