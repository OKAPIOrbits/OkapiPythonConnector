#!/usr/bin/python
import os

import okapi
import sys

okapi = okapi.Okapi()
# later: space_monitor = space_monitor.SpaceMonitor()
username = os.getenv("OKAPI_USERNAME")
password = os.getenv("OKAPI_PASSWORD")
# You can either load the username and password from the environment or simply hardcode them here for testing purposes
response = okapi.init(username, password)

print("Initialization result status: " + str(response["status"]))
if response["status"]["type"] == "FATAL":
    sys.exit(1)

response = okapi.tdms.get()

print("TDM-Get result status: " + str(response["status"]))
print("TDM-Get result data: " + str(response["actual_response"]))

TDM_KVN_TXT_FILE_PATH_AS_STRING = None
if TDM_KVN_TXT_FILE_PATH_AS_STRING is None:
    print("Make sure to load a TDM (KVN) into TDM_KVN_TXT_FILE_PATH_AS_STRING.")
    sys.exit(1)
response = okapi.tdms.add(TDM_KVN_TXT_FILE_PATH_AS_STRING, "txt")

print("TDM-Add result status: " + str(response["status"]))
print("TDM-Add result data: " + str(response["actual_response"]))

response = okapi.tdms.get()

print("TDM-Get result status: " + str(response["status"]))
print("TDM-Get result data: " + str(response["actual_response"]))
