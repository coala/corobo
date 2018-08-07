import vcr

from plugins.wolfram_alpha import WolframAlpha
from tests.isolated_testcase import IsolatedTestCase

my_vcr = vcr.VCR(match_on=['method', 'scheme', 'host', 'port', 'path'],
                 filter_query_parameters=['appid'])


class WolframAlphaTest(IsolatedTestCase):

    def setUp(self):
        super().setUp()

    @my_vcr.use_cassette('tests/cassettes/wa.yaml')
    def test_wa(self):
        self.push_message('!wa 2^6')
        self.assertIn('64', self.pop_message())
        with self.assertLogs() as cm:
            self.assertCommand('!wa this is a sentence',
                               'Dunno')
        self.assertIn('INFO:errbot.plugins.WolframAlpha:KeyError triggered on '
                      'retrieving pods.', cm.output)
        self.assertCommand('!plugin config WolframAlpha',
                           '{\'WA_TOKEN\': None}')
