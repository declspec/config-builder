from config_builder import ConfigurationSource
from errno import ENOENT

import json

class JsonConfigurationSource(ConfigurationSource):
    def __init__(self, path, optional):
        super().__init__()
        self.path = path
        self.optional = optional

    def load(self, options):
        try:
            with open(self.path, 'r') as file:
                obj = json.load(file)
        except (OSError, IOError) as err:
            if not self.optional or getattr(err, 'errno', 0) != ENOENT:
                raise

            # optional config file that wasn't found
            return dict()

        if not isinstance(obj, dict):
            raise TypeError('root of configuration file must be an object')

        # start traversing recursively
        config = dict()
        self._traverse(obj, config, [], options)

        return config

    def _traverse(self, root, config, context, options):
        if _is_simple_value(root):
            key = options.delimiter.join(context)
            config[key] = _to_string(root)
        elif isinstance(root, list):
            for idx in range(len(value)):
                context.append(str(idx))
                self._traverse(root[idx], config, context, options)
                context.pop()
        elif isinstance(root, dict):
            for key, value in root.items():
                context.append(key)
                self._traverse(value, config, context, options)
                context.pop()

# fluent helper
def add_json_file(builder, path, optional=False):
    builder.add(JsonConfigurationSource(path, optional))
    return builder

def _is_simple_value(value):
    return value is None or isinstance(value, (str, int, float, bool))

def _to_string(value):
    return None if value is None else str(value)