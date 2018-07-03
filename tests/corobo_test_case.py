from errbot.backends.test import FullStackTest
from errbot.plugin_info import PluginInfo
from errbot.templating import add_plugin_templates_path
from pathlib import Path

import logging


class CoroboTestCase(FullStackTest):

    def setUp(self, klasses: tuple):
        super().setUp(loglevel=logging.ERROR,
                      extra_config={'BACKEND': 'text'})
        self.klasses = {}
        self.plug_files = {}
        self.plugins = {}

        for klass in klasses:
            self.klasses[klass.__name__] = klass
            self.load_plugin_templates(klass)

    def load_plugin_templates(self, klass):
        plug_filename = klass.__module__.split('.')[-1] + '.plug'
        plug_file_path = (Path(__file__)
                          .parent / '..' / 'plugins' / plug_filename)
        with plug_file_path.open() as plugfile:
            plug_info = PluginInfo.load_file(plugfile, plug_file_path)
            self.plug_files[klass.__name__] = plug_info
            add_plugin_templates_path(plug_info)

    def load_plugin(self,
                    plugin_name: str,
                    mock_dict=False,
                    plugin_config=None):
        """Load plugin manually"""
        klass = self.klasses[plugin_name]
        plugin = klass(self.bot, plugin_name)
        plugin.configure(plugin_config)
        self.plugins[plugin_name] = plugin
        self.bot.plugin_manager.plugins[plugin_name] = plugin
        plug_file = self.plug_files[plugin_name]
        plugin.dependencies = plug_file.dependencies
        self.bot.plugin_manager.plugin_infos[plug_file.name] = plug_file
        plugin.activate()

        if mock_dict:
            self.inject_mocks(plugin_name=plugin_name, mock_dict=mock_dict)

        return plugin
