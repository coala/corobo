import errbot.rendering

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

def test_ship_it(testbot):
    text = errbot.rendering.text()
    testbot.assertCommand("!shipit", text.convert("![ship it!]()"))
