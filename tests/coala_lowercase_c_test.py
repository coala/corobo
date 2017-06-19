pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

def test_coala_lowercase(testbot):
    testbot.assertCommand('what is Coala?',
                          'coala is always written with a lower case c')

def test_cep(testbot):
    testbot.assertCommand('what is a CEP?',
                          'cEP is always written with a lower case c')
