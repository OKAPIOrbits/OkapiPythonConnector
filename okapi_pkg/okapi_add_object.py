import requests
import json


def okapi_add_object(okapi_login, object_to_add, url_endpoint, max_retries=3):
    # okapi_add_object() Add (post) one object to the platform
    #
    #   Inputs
    #       okapi_login - Dict, containing at least URL, options and Token for
    #       okapi. Can be obtained using OkapiInit().
    #       object_to_add - The object (eg. satellite) to be added (thus: the message).
    #       url_endpoint - the url, where-to send the request
    #
    #   Outputs
    #       response_json - dict containing the added object, if successful. Else empty
    #       error - Dict containing error information. Always check
    #               error['status'] If it is 'FATAL' something went very wrong,
    #               'WARNING's are less critical and 'NONE' or 'INFO' are no
    #               concern. error['message'] gives some explanation on the
    #               status, error['web_status'] gives the http response.

    # check the type that is requested

    # init
    response = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    url = okapi_login["url"] + url_endpoint

    retries = 1
    while(retries <= max_retries):

        try:
            response = requests.post(url, data=json.dumps(object_to_add),
                                    headers=okapi_login['header'], timeout=5)
            # raise for status
            response.raise_for_status()
            break

        except requests.exceptions.HTTPError as e:
            print("Exception: " + str(e))
            print("Response Body: {}".format(response.json()))

            # if we got a 500, we received an internal error.This we would like to
            # look at
            if (response.status_code == 500):
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
            return response_json, error
        except requests.exceptions.Timeout as e:
            if(retries == max_retries):
                error['message'] = 'Got timeout when sending request: ' + str(e)
                error['status'] = 'FATAL'
                error['web_status'] = 408
                return response_json, error
            retries += 1
            continue
        except requests.exceptions.RequestException as e:
            error['message'] = 'Got unknown exception (Wrong url?): ' + str(e)
            error['status'] = 'FATAL'
            error['web_status'] = 520  # non-standard
            return response_json, error

    # apparently, all when smoothly. Get the responses
    # DEBUG
    # print("HTTP Response " + str(response.json()))
    response_json = response.json()

    # fill error
    error['web_status'] = response.status_code

    # fill request -- depending on what has been called!
    # request['id'] = response_json['request_id']

    return response_json, error
