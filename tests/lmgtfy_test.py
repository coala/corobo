import errbot.rendering

from plugins.lmgtfy import Lmgtfy

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

text = errbot.rendering.text()


def test_lmgtfy(testbot):
    testbot.assertCommand("!lmgtfy py c", "https://www.lmgtfy.com/?q=py c")
