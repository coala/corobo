from errbot.backends.test import TestBot
from errbot.plugin_info import PluginInfo
from errbot.templating import add_plugin_templates_path
from pathlib import Path


def plugin_testbot(klass, loglevel, config=None):
    config = config if config else dict()
    testbot = TestBot(loglevel=loglevel, extra_config=config)
    testbot.start()
    plugin_name = klass.__name__
    plug = klass(testbot.bot, plugin_name)
    return plug, testbot


def load_templates(plug_file_name):
    plugin_info_path = (Path(__file__)
                        .parent / '..' / 'plugins' / plug_file_name)
    with plugin_info_path.open() as plugfile:
        plugin_info = PluginInfo.load_file(plugfile, plugin_info_path)
    add_plugin_templates_path(plugin_info)
