import main_cli, pytest


assert main_cli.hello_world('playstation') == 'No recommended products'
assert main_cli.hello_world('abcdefghijk') == 'No items returned'

# called as main with no argument - no query provided
# no API key in config file - No section: 'Section1'
