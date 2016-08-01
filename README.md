# walmart_api
# Requires python 2.7, requests, pytest, and flask(web interface only)
# Uses config.ini to retrieve an api key
# run pytest to check for no items returned and no recommended products
# and various successful queries. (23 second runtime on my machine)
# sample execution: "python walmart_api_cli xbox"
# sample execution: 
#		"import walmart_api_cli"
#		walmart_api_cli.hello_world('xbox')
# sample execution: "py.test main_cli_test.py"
# To use a web browser, run "python walmart_api" and navigate to 
# "127.0.0.1:5000/?query={Your Query}&api_key={APIKEY}"