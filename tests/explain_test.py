import errbot.rendering

from plugins.explain import Explain

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

text = errbot.rendering.text()

def test_explain(testbot):
    testbot.assertCommand("!explain REView", 'For a good review,')
    testbot.assertCommand("!explain gOOgle", 'use google')
    testbot.assertCommand("!explain not_found",
                          text.convert(Explain.ERROR_MSG))
    testbot.assertCommand("!explain review to @meet",
                          '@meet')
    testbot.assertCommand("!please explain review",
                          "Command \"please\" / \"please explain\" not found.")
