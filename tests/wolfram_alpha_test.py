from plugins.wolfram_alpha import WolframAlpha

import vcr

pytest_plugins = ['errbot.backends.test']
extra_plugin_dir = 'plugins'

my_vcr = vcr.VCR(match_on=['method', 'scheme', 'host', 'port', 'path'])

@my_vcr.use_cassette('tests/cassettes/wa.yaml')
def test_wa(testbot):
    testbot.assertCommand("!wa 2^6", "64")
