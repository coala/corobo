from errbot.backends.test import TestBot

def plugin_testbot(klass, loglevel):
    testbot = TestBot(loglevel=loglevel)
    testbot.start()
    plug = testbot.bot.plugin_manager.instanciateElement(klass)
    return plug, testbot
