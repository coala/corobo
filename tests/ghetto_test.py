import requests_mock

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

def test_ghetto(testbot):
    testbot.assertCommand("!ghetto hi, whats up?", "hi, wassup?")
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'http://www.gizoogle.net/textilizer.php',
                       text='test text which will not match with the regex')
        testbot.assertCommand("!ghetto ...", "Shiznit happens!")
