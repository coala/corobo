from errbot.backends.test import TestBot

def plugin_testbot(klass, loglevel, config=None):
    config = config if config else dict()
    testbot = TestBot(loglevel=loglevel, extra_config=config)
    testbot.start()
    plug = testbot.bot.plugin_manager.instanciateElement(klass)
    return plug, testbot
