import requests
import json


def okapi_add_object(okapi_login, object_to_add, url_endpoint, max_retries=3):
    """
    Add (post) one object to the platform
    :param okapi_login: dict containing at least URL, options and token for OKAPI. Can be obtained using okapi_init().
    :param object_to_add: the object (e.g. satellite as JSON dict) to be added
    :param url_endpoint: the sub url, where to send the request, e.g. satellites
    :param max_retries:
    :return results: dict containing the results from the request
    :return error: dict containing error information. Always check error['status'] If it is 'FATAL' something went very
    wrong, WARNING's are less critical and 'NONE' or 'INFO' are no concern. error['message'] gives some explanation on
    the status, error['web_status'] gives the http response.

    Example:
    satellite_to_add = {
        "satellite_id": "550e8400-e29b-11d4-a716-446655440000",
        "name": "My testing satellite",
        "norad_ids": [1234567],
        "area": 1,
        "mass": 1,
        "thrust_uncertainty": 2,
        "thrust_pointing_uncertainty": 2,
        "thrust_output": 1.1e-8,
        "propulsion_type": "continuous",
        "accepted_collision_probability": 0.0001,
        "accepted_minimum_distance": 100,
        "use_ai_risk_prediction": False,
        "space_track_status": "satellite_registered",
        "space_track_status_other": "string",
        "space_track_company_name": "OKAPI:Orbits GmbH",
        "space_track_poc_name": "Max Musterman",
        "space_track_poc_address": "Examplestreet 32, 34562 Examplecity, Germany",
        "space_track_login": "example@someprovider.com",
        "active": True,
        "maneuver_strategy": "short_term_and_long_term"
    }

    added_satellite, error = okapi_add_object(okapi_login, satellite_to_add, 'satellites')
    """

    # init
    response = dict()
    error = dict()
    response_json = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    url = "/".join(map(lambda x: str(x).rstrip('/'), [okapi_login["url"], url_endpoint]))

    retries = 1
    while retries <= max_retries:

        try:
            response = requests.post(url, data=json.dumps(object_to_add),
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
