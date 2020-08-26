import requests
import json
from okapi_init import okapi_init
from okapi_send_request import okapi_send_request
from okapi_get_result import okapi_get_result
import time

# this is a wrapper class that is supposed to wait for the result and return it automatically
def okapi_wait_and_get_result(okapi_login, request, error, url_endpoint_results, maxPollTime):

    # Wait the specified time for the result. Max time makes sure that we cannot get stuck
    counter = 0
    error['web_status'] = 202
    while (counter < int(maxPollTime)) and (error['web_status'] == 202):

    # get the results from the request
        result, error = okapi_get_result(
            okapi_login, request,
            url_endpoint_results)
        if (error['status'] == 'FATAL'):
            print(error)
            exit()
        elif(error['status'] == 'WARNING'):
            print(error)

        # we wait a second, to not trigger some DOD on the server ;-)
        time.sleep(1)

        counter += 1

    return result, error
