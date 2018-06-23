pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = ['plugins']


def test_nevermind(testbot):
    testbot.assertCommand("!nevermind", "I'm sorry :(")
    testbot.assertCommand("!nm", "I'm sorry :(")
    testbot.assertCommand("!nEverMINd", "I'm sorry :(")
    testbot.assertCommand("!nM", "I'm sorry :(")
