from config_builder import ConfigurationSource

class CliConfigurationSource(ConfigurationSource):
    def __init__(self, args, switch_mappings=None):
        super().__init__()
        self.args = args
        self.switch_mappings = switch_mappings

    def load(self, options):
        