import json
import requests


def okapi_send_general_request(okapi_login, general_request,
                               url_endpoint, request_endpoint):
    # OkapiSendPassPredictionRequest() Send pass prediction request to okapi
    #
    #   Inputs
    #       okapi_login - Dict, containing at least URL, options and Token for
    #       okapi. Can be obtained using OkapiInit().
    #       PassPredictionRequest - Dict containing the request. A dict of
    #       the correct format can be gained by OkapiGetPassPredictionRequest.
    #       typeOfRequest - 'track' for tracking file, 'overview' for an
    #
    #   Outputs
    #       request - dict containing the request_id and request_type, needed
    #                 to get the results from okapi.
    #       error - Dict containing error information. Always check
    #               error['status'] If it is 'FATAL' something went very wrong,
    #               'WARNING's are less critical and 'NONE' or 'INFO' are no
    #               concern. error['message'] gives some explanation on the
    #               status, error['web_states'] gives the http response.

    # check the type that is requested

    # init
    request = dict()
    response = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    url = okapi_login["url"] + url_endpoint

    try:
        response = requests.post(url, data=json.dumps(general_request),
                                 headers=okapi_login['header'], timeout=5)
        # raise for status
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        # if we got a 500, we received an internal error.This we would like to
        # look at
        if (response.status_code == 500):
            response_json = response.json()
            state_msg = response_json['stateMsg']
            error['message'] = state_msg['text']
            error['status'] = state_msg['type']
        else:
            error['message'] = 'Got HTTPError when sending request. '
            error['status'] = 'FATAL'
        error['web_status'] = response.status_code
        return request, error
    except requests.exceptions.Timeout:
        error['message'] = 'Got timeout when sending request. '
        error['status'] = 'FATAL'
        error['web_status'] = 408
        return request, error
    except requests.exceptions.RequestException:
        error['message'] = 'Got unknown exception. '
        error['status'] = 'FATAL'
        error['web_status'] = 520  # non-standard
        return request, error

    # apparently, all when smoothly. Get the responses
    response_json = response.json()

    # fill error
    state_msg = response_json['stateMsg']
    error['message'] = state_msg['text']
    error['status'] = state_msg['type']
    error['web_status'] = response.status_code

    # fill request -- depending on what has been called!
    request['id'] = response_json['requestId']
    request['service'] = request_endpoint

    return request, error
