from plugins.the_rules import The_rules

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

def test_the_rules(testbot):
    testbot.assertCommand('!the rules', 'A robot may not harm humanity')
    testbot.assertCommand('!the  rules', 'A robot may not injure a human')
    testbot.assertCommand('!THE RUles', 'A robot must obey any orders')
