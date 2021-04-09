import requests


def okapi_get_objects(okapi_login, url_endpoint, sub_id='', max_retries=3):
    # okapi_get_objects() Get objects from an endpoint
    #
    #   Inputs
    #       okapi_login - Dict, containing at least URL, options and Token for
    #       OKAPI. Can be obtained using OkapiInit().
    #       url_endpoint - adress, from which the results shall be retrieved
    #
    #   Outputs
    #       results - dict, containing the results from the request
    #       error - Dict containing error information. Always check
    #               error['status'] If it is 'FATAL' something went very wrong,
    #               'WARNING's are less critical and 'NONE' or 'INFO' are no
    #               concern. error['message'] gives some explanation on the
    #               status, error['web_states'] gives the http response.
    #   Examples
    #      Get all conjunctions for one user
    #       conjunctions, error = okapi_get_objects(okapi_login,'conjunctions')
    #      Get all CDMs for the first conjunction of conjunctions
    #       cdms, error = okapi_get_objects(okapi_login,'conjunctions/{}/cdms',conjunctions["elements"][0]["conjunction_id"])
    #

    # init
    response = dict()
    result = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    # check what kind of object is requested
    if sub_id == '':
        url = okapi_login["url"] + url_endpoint
    else:
        url = okapi_login["url"] + url_endpoint.format(sub_id)

    retries = 1
    while retries <= max_retries:
        try:
            result["service"] = url_endpoint
            response = requests.get(url, headers=okapi_login["header"], timeout=5)

            # raise for status!
            response.raise_for_status()

            # extract result and stuff: Loop over all objects in the list that was
            # nicely provided to us
            result = response.json()

            # Get the state msgs and stuff
            current_result_dict = result
            if 'status' in current_result_dict:
                state_msg = current_result_dict['status']
                error['status'] = state_msg['type']
                error['message'] = state_msg['text']

            error['web_status'] = response.status_code

            # Finally: Check, if status is 202 which means "results might not be
            # complete"
            if (response.status_code == 202) and (error['status'] != 'FATAL'):
                error['status'] = 'WARNING'
                error['message'] = 'Result has been accepted but not been fully processed yet.'

            break

        except requests.exceptions.HTTPError as e:
            print("Exception: " + str(e))
            print("Response Body: {}".format(response.json()))
            # need to get the response from the result to send the error
            try:
                result = response.json()
                result_dict = result[0]
            except:
                result = dict()
                result_dict = dict()

            if 'state_msg' in result_dict:
                state_msg = result_dict['state_msg']
                error['status'] = state_msg['type']
                error['message'] = state_msg['text']
            elif 'state_msgs' in result_dict:
                result_dict = result[1]
                state_msgs = result_dict['state_msgs']

                state_msgs_temp = state_msgs[0]
                error['status'] = state_msgs_temp['type']
                error['message'] = state_msgs_temp['text']

            error['web_status'] = response.status_code
            return result, error
        except requests.exceptions.Timeout:
            if retries == max_retries:
                error['message'] = 'Got timeout when sending request. '
                error['status'] = 'FATAL'
                error['web_status'] = 408
                return result, error
            retries += 1
            continue
        except requests.exceptions.RequestException:
            error['message'] = 'Got unknown exception. '
            error['status'] = 'FATAL'
            error['web_status'] = 520  # non-standard
            return result, error

    return result, error
