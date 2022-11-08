import requests
import json


def okapi_send_request(okapi_login, request_body, url_endpoint, max_retries=3):
    """
    Send request to OKAPI API
    :param okapi_login: dict containing at least URL, options and token for OKAPI. Can be obtained using okapi_init().
    :param request_body: dict containing details of the request e.g. orbit, propagation settings etc.
    :param url_endpoint: the url where-to send the request
    :param max_retries: number of times to repeat the get request, when the backend does not respond in time
    :return request: dict containing the request_id needed to identify the result on OKAPI servers.
    :return error: dict containing error information. Always check error['status'] If it is 'FATAL' something went very
    wrong, WARNING's are less critical and 'NONE' or 'INFO' are no concern. error['message'] gives some explanation on
    the status, error['web_status'] gives the http response.
    """

    # init
    request = dict()
    response = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    url = "/".join(map(lambda x: str(x).rstrip('/'), [okapi_login["url"], url_endpoint]))
    retries = 1
    while retries <= max_retries:
        try:
            response = requests.post(url, data=json.dumps(request_body),
                                     headers=okapi_login['header'], timeout=10000)
            # raise for status
            response.raise_for_status()
            break

        except requests.exceptions.HTTPError as e:
            print("Exception: " + str(e))
            print("Response Body: {}".format(response.json()))

            # if we got a 500, we received an internal error.This we would like to
            # look at
            if response.status_code == 500:
                response_json = response.json()
                status = response_json['state_msg']
                error['message'] = status['text']
                error['status'] = status['type']
            else:
                error['message'] = 'Got HTTPError when sending request: ' + str(e)
                # DEBUG
                # print("HTTP Response " + str(response.json()))
                error['status'] = 'FATAL'
            error['web_status'] = response.status_code
            return request, error
        except requests.exceptions.Timeout as e:
            if retries == max_retries:
                error['message'] = 'Got timeout when sending request: ' + str(e)
                error['status'] = 'FATAL'
                error['web_status'] = 408
                return request, error
            retries += 1
            continue
        except requests.exceptions.RequestException as e:
            error['message'] = 'Got unknown exception (Wrong url?): ' + str(e)
            error['status'] = 'FATAL'
            error['web_status'] = 520  # non-standard
            return request, error

    # apparently, all when smoothly. Get the responses
    # DEBUG
    # print("HTTP Response " + str(response.json()))
    response_json = response.json()

    # fill error
    status = response_json['status']  # state_msg = response_json['state_msg']
    error['message'] = status['text']
    error['status'] = status['type']
    error['web_status'] = response.status_code

    # fill request -- depending on what has been called!
    request['id'] = response_json['request_id']

    return request, error
