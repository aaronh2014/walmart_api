import main_cli


#assert main_cli.hello_world('playstation') == 'No recommended products'
#assert main_cli.hello_world('api') == 'No recommended products'
assert main_cli.hello_world(26973477) == 'No recommended products'
assert main_cli.hello_world('abcdefghijk') == 'No items returned'
#assert main_cli.hello_world('xbox') == 10
assert main_cli.hello_world('snake') == 5
assert main_cli.hello_world('todo') == 4
assert main_cli.hello_world('favorites') == 6

#assert main_cli.hello_world('a') == 10
#assert main_cli.hello_world('song') == 10
#assert main_cli.hello_world('of') == 'No recommended products'
#assert main_cli.hello_world('ice') == 'No recommended products'
#assert main_cli.hello_world('and') == 'No recommended products'
#assert main_cli.hello_world('fire') == 'No recommended products'

#assert main_cli.hello_world('you') == 'No recommended products'
#assert main_cli.hello_world('know') == 10
#assert main_cli.hello_world('nothing') == 10
#assert main_cli.hello_world('jon') == 10
assert main_cli.hello_world('snow') == 7

assert main_cli.hello_world('r') == 10
#assert main_cli.hello_world('plus') == 'No recommended products'
#assert main_cli.hello_world('l') == 10
#assert main_cli.hello_world('equals') == 10
assert main_cli.hello_world('j') == 'No recommended products'

# called as main with no argument - no query provided
# no API key in config file - No section: 'Section1'
#assert main_cli.hello_world('d') == 5
#assert main_cli.hello_world('g') == 7
#assert main_cli.hello_world('h') == 5
#assert main_cli.hello_world('y') == 5
#assert main_cli.hello_world('code') == 6
assert main_cli.hello_world('pytest') == 7 #6
