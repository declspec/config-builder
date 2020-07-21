from config_builder import ConfigurationBuilder, ConfigurationOptions
from json_source import add_json_file
from cli_source import add_cli_source

import sys

builder = ConfigurationBuilder(delimiter=':')
add_json_file(builder, './config.json')
add_cli_source(builder, sys.argv, { '-lld': 'logging:loglevel:default'})

config = builder.build()
print(config.get('logging:logLevel:default'))
print(config.get('logging:logLevel:microsoft'))
