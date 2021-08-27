import time
from . import okapi_get_result


def okapi_wait_and_get_result(okapi_login, request_body, url_endpoint_results, max_poll_time):
    """
    Send a request to the OKAPI platform and wait for the results. This is a wrapper class that is supposed to wait for
    the result and return it automatically
    :param okapi_login: ict containing at least URL, options and token for OKAPI. Can be obtained using okapi_init().
    :param request_body: dict containing details of the request e.g. orbit, propagation settings etc.
    :param url_endpoint_results: the url where to get the result from
    :param max_poll_time: the maximum time (in seconds) to wait for the result. Measurement is NOT exact
    :return result: dict containing the results from the request
    :return error: dict containing error information. Always check error['status'] If it is 'FATAL' something went very
    wrong, WARNING's are less critical and 'NONE' or 'INFO' are no concern. error['message'] gives some explanation on
    the status, error['web_status'] gives the http response.
    """

    counter = 0
    result = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 202
    while (counter < int(max_poll_time)) and (error['web_status'] == 202):

        # get the results from the request
        result, error = okapi_get_result(
            okapi_login, request_body,
            url_endpoint_results)
        if error['status'] == 'FATAL':
            print(error)
            exit()
        elif error['status'] == 'WARNING':
            print(error)

        time.sleep(1)

        counter += 1

    return result, error
