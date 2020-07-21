from config_builder import ConfigurationSource

##
# Rules
# --long options can be either the full key name, or aliased in 'switch_mappings' (must retain prefix)
# -short options must be aliased in 'switch_mappings' (must retain prefix)
# /long options with a forward slash are forwarded onto their --long equivalent
#
# All options can be specified either as `--key=value` or `--key value`
# but in order to support boolean options, "value" can never start with a hyphen when using the `--key value` syntax.

class CliConfigurationSource(ConfigurationSource):
    def __init__(self, args, switch_mappings=None):
        super().__init__()
        self.args = args
        self.switch_mappings = switch_mappings

    def load(self, options):
        idx = 0
        limit = len(self.args)
        config = dict()

        while idx < limit:
            arg = self.args[idx]
            idx += 1
            key_start = 0
            key_end = 0

            if arg.startswith('--'):
                key_start = 2
            elif arg.startswith('-'):
                key_start = 1
            elif arg.startswith('/'):
                # dodgy handling to make this simpler
                key_start = 2
                arg = '--%s' % arg[1:]

            try:
                delim_idx = arg.index('=')
                key_end = delim_idx
                value = arg[delim_idx+1:]
            except ValueError: # no '=' in arg
                if key_start == 0:
                    # keys with no prefix (--, - or /) can only be used in key=value form
                    continue

                key_end = len(arg)

                if idx >= limit or self.args[idx].startswith('-'):
                    # treat as flag
                    # BUG (or at least 'documented behaviour'): in order to support flags, certain sacrifices have to be made;
                    #   flags cannot be followed by `key=value` format configuration items as they will be interpreted as `real_key: "key=value"` instead
                    value = None
                else:
                    value = self.args[idx]
                    idx += 1

            key = arg[:key_end]

            # check for a switch mapping
            if self.switch_mappings is not None and key in self.switch_mappings:
                key = self.switch_mappings[key]
            elif key_start != 1:
                key = key[key_start:]
            else:
                # short options must be defined in switch_mapping
                continue

            print('{"%s": "%s"}' % (key, value))

            if key not in config:
                config[key] = value
            else:
                current = config[key]
                if isinstance(current, list):
                    current.append(value)
                else:
                    config[key] = [current, value]

        # flatten the config
        flattened = dict()

        for key, value in config.items():
            if not isinstance(value, list):
                flattened[key] = value
            else:
                for idx, item in enumerate(value):
                    subkey = '%s%s%d' % (key, options.delimiter, idx)
                    flattened[subkey] = item
        
        return flattened
            
def add_cli_source(builder, args, switch_mappings=None):
    builder.add(CliConfigurationSource(args, switch_mappings))
    return builder