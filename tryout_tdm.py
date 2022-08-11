#!/usr/bin/python
import os
import time
from dotenv import load_dotenv
from okapi_pkg import *
#
# Init --> Get a token to run the analyses
#
# For auth info: See https://okapiorbits.space/documentation/ or contact us.
# Standard url is: https://api.okapiorbits.com/
load_dotenv()
username = os.getenv("OKAPI_USERNAME")
password = os.getenv("OKAPI_PASSWORD")
# You can either load the username and password from the environment or a .env file or
# simply hardcode them here for testing purposes.
url = os.getenv("OKAPI_URL") # "https://api.okapiorbits.com/"
okapi_login, error = okapi_init(url,
                                username,
                                password)

print("OkapiLogin: {}".format(okapi_login))
# check for the error status
if error['status'] == 'FATAL':
    print(error)
    exit('Error during authentication.')
elif error['status'] == 'WARNING':
    print(error)

tdm_body={
    "tdm": {
      "type": "tdm.txt",
      "content": "TDM KVN DATA"
    }
}

## Do this, to add a new TDM to the collection
add_tdm, error  = okapi_add_object(okapi_login, tdm_body, 'tdms')
print (f"{add_tdm}, {error}")

### Do this, to retrieve all available TDMs from the collection
get_tdm, error  = okapi_get_objects(okapi_login, 'tdms')
print (f"{get_tdm}, {error}")
