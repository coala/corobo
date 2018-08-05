from itertools import chain

class DefaultConfigMixin():

    @property
    def _default_config(self):
        if (hasattr(self.bot_config, 'DEFAULT_CONFIG') and
                self.name in self.bot_config.DEFAULT_CONFIG):
            return self.bot_config.DEFAULT_CONFIG[self.name]

    def __init__(self, bot, name=None):
        super().__init__(bot, name=name)
        if not hasattr(self, 'CONFIG_TEMPLATE'):  # pragma: no cover
            self.log.error('CONFIG_TEMPLATE for plugin {} is missing.'
                           .format(self.name))

    def get_configuration_template(self):
        default_config = self._default_config
        config_template = self.CONFIG_TEMPLATE

        if default_config:
            config = dict(chain(config_template.items(),
                                default_config.items()))
        else:
            config = config_template

        return config

    def configure(self, configuration):
        config_template = self.get_configuration_template()

        if configuration is not None and configuration != {}:
            config = dict(chain(config_template.items(),
                                configuration.items()))
        else:
            config = config_template

        self.config = config
