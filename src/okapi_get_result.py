import requests


def okapi_get_result(picard_login, request):
    # OkapiGetResult() Get results from Picard
    #
    #   Inputs
    #       picard_login - Dict, containing at least URL, options and Token for
    #       Picard. Can be obtained using OkapiInit().
    #       request - dict containing the request_id and request_type, needed
    #       to get the results from Picard.
    #
    #   Outputs
    #       results - list, containing the results from the request
    #       error - Dict containing error information. Always check
    #               error['status'] If it is 'FATAL' something went very wrong,
    #               'WARNING's are less critical and 'NONE' or 'INFO' are no
    #               concern. error['message'] gives some explanation on the
    #               status, error['web_states'] gives the http response.

    # init
    result = dict()
    error = dict()
    error['message'] = 'NONE'
    error['status'] = 'NONE'
    error['web_status'] = 0

    # check the input
    if not('id' in request) or not('service' in request):
        error['message'] = 'Request was empty or incomplete.'
        error['status'] = 'FATAL'
        error['web_status'] = 204
        return result, error

    url = picard_login["url"]+request["service"]+'/' + str(request["id"])
    # print(type(url))
    try:
        result["service"] = request["service"]
        response = requests.get(url, headers=picard_login["header"], timeout=5)

        # raise for status!
        response.raise_for_status()

        # extract result and stuff: Loop over all objects in the list that was
        # nicely provided to us
        result = response.json()
        i = 0
        while i < len(result):
            # Get the state msgs and stuff
            current_result_dict = result[i]
            if ('stateMsg' in current_result_dict):
                state_msg = current_result_dict['stateMsg']
                error['status'] = state_msg['text']
                error['message'] = state_msg['type']
            elif('stateMsgs' in current_result_dict):
                state_msgs = current_result_dict['stateMsgs']
                # go through all the messages, check if there is fatal
                j = 0
                while j < len(state_msgs):
                    state_msgs_temp = state_msgs[j]
                    error['status'] = state_msgs_temp['text']
                    error['message'] = state_msgs_temp['type']
                    j += 1

            i += 1

        error['web_status'] = response.status_code

    except requests.exceptions.HTTPError:

        # need to get the response from the result to send the error
        result = response.json()
        result_dict = result[0]
        if ('stateMsg' in result_dict):
            state_msg = result_dict['stateMsg']
            error['status'] = state_msg['text']
            error['message'] = state_msg['type']
        elif('stateMsgs' in result_dict):
            result_dict = result[1]
            state_msgs = result_dict['stateMsgs']

            print("Printing all that")
            print(result_dict)
            print(state_msgs)
            print()

            state_msgs_temp = state_msgs[0]
            error['status'] = state_msgs_temp['text']
            error['message'] = state_msgs_temp['type']

        error['web_status'] = response.status_code
        return result, error
    except requests.exceptions.Timeout:
        error['message'] = 'Got timeout when sending request. '
        error['status'] = 'FATAL'
        error['web_status'] = 408
        return result, error
    except requests.exceptions.RequestException:
        error['message'] = 'Got unknown exception. '
        error['status'] = 'FATAL'
        error['web_status'] = 520  # non-standard
        return result, error

    return result, error
