#
# Base classes for building configuration
#
class ConfigurationOptions:
    """ Class to encapsulate well-named configuration options """
    def __init__(self, delimiter=':'):
        self.delimiter = delimiter

class ConfigurationRoot:
    """ Root configuration compiled by combining multiple sources """
    def __init__(self, sources, options):
        self.options = options
        self.sources = sources

        self._configs = [ None ] * len(sources)
        self._keymaps = [ None ] * len(sources)

        for idx, source in enumerate(sources):
            config = source.load(options)
            self._configs[idx] = config
            self._keymaps[idx] = { key.lower(): key for key in config }

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        lower_key = key.lower()

        for idx, keymap in enumerate(reversed(self._keymaps)):
            mapped_key = keymap.get(lower_key, None)

            if mapped_key is not None:
                return self._configs[idx][mapped_key]

        raise KeyError('key not found in any config providers: "%s"' % key)

    def get_all(self):
        merged = dict()

        for config in self._configs:
            merged.update(config)

        return merged

class ConfigurationSource:
    """ Configuration primitive, handles loading a {string: string} dictionary from a single source """
    def __init__(self):
        pass

    def load(self, options):
        raise NotImplementedError('load(options) should be implemented by child class')

class ConfigurationBuilder:
    def __init__(self, **kwargs):
        self.sources = []
        self.options = ConfigurationOptions(**kwargs)

    def add(self, source):
        if not isinstance(source, ConfigurationSource):
            raise TypeError('source must be an instance of ConfigurationSource')

        self.sources.append(source)
        return self

    def build(self):
        return ConfigurationRoot(self.sources, self.options)
