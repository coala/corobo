from itertools import chain

class DefaultConfigMixin():

    @property
    def _default_config(self):
        if (hasattr(self.bot_config, 'DEFAULT_CONFIG') and
                self.name in self.bot_config.DEFAULT_CONFIG):
            return self.bot_config.DEFAULT_CONFIG[self.name]

    def __init__(self, bot, name=None):
        super().__init__(bot, name=name)
        default_config = self._default_config
        if default_config and not hasattr(self, 'config'):
            self.configure(default_config)

    def get_configuration_template(self):
        default_config = self._default_config
        if default_config:
            return default_config
        elif self.CONFIG_TEMPLATE:
            return self.CONFIG_TEMPLATE
        else:  # pragma: no cover
            return

    def configure(self, configuration):
        default_config = self._default_config
        if configuration and default_config:
            config = dict(chain(
                default_config.items(),
                configuration.items()))
        elif configuration:
            config = dict(chain(self.CONFIG_TEMPLATE.items(),
                          configuration.items()))
        elif default_config:
            config = default_config
        else:
            config = self.CONFIG_TEMPLATE

        self.config = config
