pytest_plugins = ['errbot.backends.test']
extra_plugin_dir = 'plugins'

def test(testbot):
    testbot.assertCommand('!pitchfork @meet', 'being pitchforked')
    testbot.assertCommand('!pitchfork @meet down to hell', 'being pitchforked')
    testbot.assertCommand('!pitchfork meet to hell', 'being pitchforked')
    testbot.assertCommand('!pitchfork', 'Usage')
