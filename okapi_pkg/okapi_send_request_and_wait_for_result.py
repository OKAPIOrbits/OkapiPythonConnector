import time
from . import okapi_send_request, okapi_get_result


def okapi_send_request_and_wait_for_result(okapi_login, request_body, url_endpoint_requests, url_endpoint_results,
                                           max_poll_time):
    """
    Send a request to the OKAPI Platform and wait for the results. This is a wrapper function that makes using the
    OKAPI backend simpler
    :param okapi_login: dict containing at least URL, options and token for OKAPI. Can be obtained using okapi_init().
    :param request_body: dict containing details of the request e.g. orbit, propagation settings etc.
    :param url_endpoint_requests: the url where to send the request
    :param url_endpoint_results: the url where to get the result from
    :param max_poll_time: the maximum time (in seconds) to wait for the result. Measurement is NOT exact
    :return result: dict containing the results from the request
    :return error: dict containing error information. Always check error['status'] If it is 'FATAL' something went very
    wrong, WARNING's are less critical and 'NONE' or 'INFO' are no concern. error['message'] gives some explanation on
    the status, error['web_status'] gives the http response.
    """

    # send the request to the server
    request, error = okapi_send_request(okapi_login, request_body, url_endpoint_requests)

    if error['status'] == 'FATAL':
        print(error)
        exit()
    elif error['status'] == 'WARNING':
        print(error)

    # Wait the specified time for the result. Max time makes sure that we cannot get stuck
    counter = 0
    result = dict()
    error['web_status'] = 202
    while (counter < int(max_poll_time)) and (error['web_status'] == 202):

        # get the results from the request
        result, error = okapi_get_result(
            okapi_login, request,
            url_endpoint_results)
        if error['status'] == 'FATAL':
            print(error)
            exit()
        elif error['status'] == 'WARNING':
            print(error)

        time.sleep(1)

        counter += 1

    return result, error
