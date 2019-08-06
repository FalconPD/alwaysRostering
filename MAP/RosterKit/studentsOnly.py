#!/usr/bin python

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
    url = (
        config.get('mainconf', 'host')
        + config.get('import types', 'studentsOnly')
    )
    username = config.get('mainconf', 'username')
    password = config.get('mainconf', 'password')
    rosterPath = config.get('mainconf', 'roster_file')

#############################################################
#                                     				 		#
# If you prefer to not use a config,  				 		#
# enter your information below        				 		#
#                                     				 		#
#############################################################
except:
    url = 'https://api.mapnwea.org/services/rostering/submit/students'
    # Replace 'None' with your username
    username = None
    # Replace 'None' with your password
    password = None
    # Replace 'None' with the path to your roster file
    rosterPath = None


def submitRequest():
    # Open roster file for processing
    with open(rosterPath, 'rb') as f:
        # Prepare the roster file as an HTTP post object
        files = {'file': f}
        # Send roster to server using supplied credentials
        r = requests.post(url, auth=(username, password), files=files)
    # Print out the server's response
    print('\nServer response: ' + str(r.status_code) + ' | ' + r.text + '\n')


if __name__ == '__main__':
    submitRequest()
