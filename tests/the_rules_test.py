from plugins.the_rules import The_rules

pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = 'plugins'

def test_the_rules(testbot):
    testbot.assertCommand('!the rules', The_rules.RULES[0])
    testbot.assertCommand('!the  rules', The_rules.RULES[1])
    testbot.assertCommand('!THE RUles', The_rules.RULES[2])
