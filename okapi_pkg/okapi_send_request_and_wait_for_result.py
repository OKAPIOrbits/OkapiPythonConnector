import requests
import json
from okapi_init import okapi_init
from okapi_send_request import okapi_send_request
from okapi_get_result import okapi_get_result
import time

# This is a wrapper class that is supposed to make it easy to try the python connector
def okapi_send_request_and_wait_for_result(okapi_login, request_body, url_endpoint_requests, url_endpoint_results, maxPollTime, generic_or_not ='not'):
    # send the request to the server
    request, error = okapi_send_request(okapi_login, request_body, url_endpoint_requests)

    if (error['status'] == 'FATAL'):
        print(error)
        exit()
    elif(error['status'] == 'WARNING'):
        print(error)

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
