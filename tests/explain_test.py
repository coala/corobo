import errbot.rendering

from plugins.explain import Explain

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

text = errbot.rendering.text()

def test_explain(testbot):
    testbot.assertCommand("!explain REView",
                          text.convert(Explain.MSGS['review']).format(
                            bot_prefix=testbot.bot_config.BOT_PREFIX
                          ))
    testbot.assertCommand("!explain gOOgle",
                          text.convert(Explain.MSGS['google']))
    testbot.assertCommand("!explain not_found",
                          text.convert(Explain.ERROR_MSG))
    testbot.assertCommand("!explain review to @meet",
                          '@meet')
    testbot.assertCommand("!please explain review",
                          "Command \"please\" / \"please explain\" not found.")
