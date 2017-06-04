pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

def test_search_cmd(testbot):
    testbot.assertCommand('!search api this is search string',
                          'http://api.coala.io/en/latest/search.html?q=this+is+search+string')
    testbot.assertCommand('!search user this is search string',
                          'http://docs.coala.io/en/latest/search.html?q=this+is+search+string')
    testbot.assertCommand('!search not matching',
                          'Invalid syntax')
