pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = ['plugins']


def test_nevermind(testbot):
    testbot.assertCommand("!nevermind", "I'm sorry :(")
    testbot.assertCommand("!nm", "I'm sorry :(")
    testbot.assertCommand("!nEverMINd", "I'm sorry :(")
    testbot.assertCommand("!nM", "I'm sorry :(")
    testbot.assertCommand("!nmxyz", 'Command "nmxyz" not found.')
    testbot.assertCommand("!hey nM", 'Command "hey" / "hey nM" not found.')
    testbot.assertCommand("!nevermindxyz", 'Command "nevermindxyz" not found.')
    testbot.assertCommand(
        "!hey nEverMINd", 'Command "hey" / "hey nEverMINd" not found.')
