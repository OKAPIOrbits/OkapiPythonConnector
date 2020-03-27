#!/usr/bin/python

import time
import json

import okapi

import sys

okapi = okapi.Okapi()
# later: space_monitor = space_monitor.SpaceMonitor()
response = okapi.init(YOUR_LOGIN_AS_STRING, YOUR_PASSWORD_AS_STRING)

print("Initialization result status: " + str(response["status"]))
if response["status"]["type"] == "FATAL":
  sys.exit(1)

response = okapi.tdms.get()

print("TDM-Get result status: " + str(response["status"]))
#if response["status"]["type"] == "FATAL":
#  sys.exit(1)
print("TDM-Get result data: " + str(response["actual_response"]))

response = okapi.tdms.add(TDM_KVN_TXT_FILE_PATH_AS_STRING, "txt")

print("TDM-Add result status: " + str(response["status"]))
#if response["status"]["type"] == "FATAL":
#  sys.exit(1)
print("TDM-Add result data: " + str(response["actual_response"]))

response = okapi.tdms.get()

print("TDM-Get result status: " + str(response["status"]))
#if response["status"]["type"] == "FATAL":
#  sys.exit(1)
print("TDM-Get result data: " + str(response["actual_response"]))


