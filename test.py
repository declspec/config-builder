from config_builder import ConfigurationBuilder, ConfigurationOptions
from json_source import add_json_file

builder = ConfigurationBuilder(delimiter=':')
add_json_file(builder, './config.json')

config = builder.build()
print(config.get('logging:logLevel:default'))
print(config['logging'])