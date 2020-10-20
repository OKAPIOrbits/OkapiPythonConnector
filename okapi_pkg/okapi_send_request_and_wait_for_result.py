import requests
import json
# from okapi_init import okapi_init
# from okapi_send_request import okapi_send_request
# from okapi_get_result import okapi_get_result
import time

# This is a wrapper class that is supposed to make it easy to try the python connector
def okapi_send_request_and_wait_for_result(okapi_login, request_body, url_endpoint_requests, url_endpoint_results, max_poll_time):
    # okapi_send_request_and_wait_for_result() Send a request to the OKAPI Platform and wait for the results
    #
    #   Inputs
    #       okapi_login - Dict, containing at least URL, options and Token for
    #       okapi. Can be obtained using OkapiInit().
    #       request_body - The body of the request (thus: the message).
    #       url_endpoint_requests - the url, where-to send the request
    #       url_endpoint_results - the url, where-from get the result
    #       max_poll_time - the maximum time (in seconds) to wait for the result. Measurement is NOT exact
    #
    #   Outputs
    #       result - dict, containing the result from the request
    #       error - Dict containing error information. Always check
    #               error['status'] If it is 'FATAL' something went very wrong,
    #               'WARNING's are less critical and 'NONE' or 'INFO' are no
    #               concern. error['message'] gives some explanation on the
    #               status, error['web_states'] gives the http response.

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
    while (counter < int(max_poll_time)) and (error['web_status'] == 202):

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
