from urllib.parse import urljoin

import requests
import json


def okapi_delete_object(okapi_login, object_to_delete, url_endpoint, max_retries=3):
    """
    Delete one object from the platform
    :param okapi_login: dict containing at least URL, options and token for OKAPI. Can be obtained using okapi_init().
    :param object_to_delete: the object (e.g. satellite) to be deleted. Note the dict must contain one of the keys:
    'satellite_id' or 'conjunction_id'.
    :param url_endpoint: the sub url, where to send the request, e.g. satellites
    :param max_retries: number of times to repeat the get request, when the backend does not respond in time
    :return results: dict containing the results from the request
    :return error: dict containing error information. Always check error['status'] If it is 'FATAL' something went very
    wrong, WARNING's are less critical and 'NONE' or 'INFO' are no concern. error['message'] gives some explanation on
    the status, error['web_status'] gives the http response.
    """

    # init
    response = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    if "satellite_id" in object_to_delete:
        url = "/".join(
            map(lambda x: str(x).rstrip('/'), [okapi_login["url"], url_endpoint, object_to_delete["satellite_id"]]))
    elif "conjunction_id" in object_to_delete:
        url = "/".join(
            map(lambda x: str(x).rstrip('/'), [okapi_login["url"], url_endpoint, object_to_delete["conjunction_id"]]))
    else:
        error['message'] = 'Object to delete appears incomplete. Missing id.'
        error['status'] = 'FATAL'
        error['web_status'] = 204
        return response, error

    retries = 1
    response_json = dict()
    while retries <= max_retries:
        try:
            response = requests.delete(url, data=json.dumps(object_to_delete),
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
            return response_json, error
        except requests.exceptions.Timeout as e:
            if retries == max_retries:
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
