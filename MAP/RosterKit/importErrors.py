#!/usr/bin python

import csv
import requests
import sys
from requests.auth import HTTPBasicAuth

#############################################################
#                                                    		#
# Determine Python version and attempt to use config  		#
# file 'rostering.conf' Fallback to hardcoded info on fail  #
#                                                    		#
#############################################################


def which_python():
    if sys.version_info >= (3, 0):
        import configparser
        config = configparser.ConfigParser()
    else:
        import ConfigParser
        config = ConfigParser.ConfigParser()
    return config


try:
    config = which_python()
    config.read('rostering.conf')
    url = config.get('mainconf', 'host') + config.get('import types', 'errors')
    errorPath = config.get('mainconf', 'errors_output_dir')
    username = config.get('mainconf', 'username')
    password = config.get('mainconf', 'password')
#############################################################
#                                                    		#
# If you prefer to not use a config,                 		#
# enter your information below                       		#
#                                                    		#
#############################################################
except:
    url = 'https://api.mapnwea.org/services/rostering/errors'
    # Replace 'None' with your username
    username = None
    # Replace 'None' with your password
    password = None
    # Saves error file to the directory that the scripts are in -
    # change the path as you see fit
    errorPath = '/'


def submitRequest():
    # Send request for import errors to server
    r = requests.get(url, auth=(username, password))
    # Print out the server's response
    print('\nServer response: ' + str(r.status_code) + ' | ' + r.text + '\n')
    # Write and save import errors to csv file
    if not r.text.strip() == 'OK_NO_ERRORS':
        with open(errorPath + 'errors.csv', 'wt') as outFile:
            outFile.writelines(r.text)


if __name__ == '__main__':
    submitRequest()
