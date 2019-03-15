from okapi_send_general_request import okapi_send_general_request


def okapi_send_passprediction_request(okapi_login, pass_prediction_request,
                                      type_of_request):
    # OkapiSendpass_prediction_request() Send pass prediction request to okapi
    #
    #   Inputs
    #       okapi_login - Dict, containing at least URL, options and Token for
    #       okapi. Can be obtained using okapit:init().
    #       pass_prediction_request - Dict containing the request.
    #       type_of_request - 'track' for tracking file, 'overview' for a summary
    #                       of main characteristics of a pass
    #
    #   Outputs
    #       request - dict containing an 'id' to access the results on the
    #                 server, and the 'service', which is a possible endpoint
    #                 under which the result can be retrieved.
    #       error - Dict containing error information. Always check
    #               error['status'] If it is 'FATAL' something went very wrong,
    #               'WARNING's are less critical and 'NONE' or 'INFO' are no
    #               concern. error['message'] gives some explanation on the
    #               status, error['web_states'] gives the http response.
    #
    #   NOTE: This way of sending pass prediction reqeusts will be replaced in
    #         future releases by a more flexible approach.

    # check the type that is requested
    if type_of_request == 'track':
        url_endpoint = 'pass/prediction/requests/long'
        request_endpoint = 'pass/predictions/long'
    elif type_of_request == 'overview':
        url_endpoint = 'pass/prediction/requests'
        request_endpoint = 'pass/predictions'
    else:
        error = dict()
        request = dict()
        error['message'] = 'Wrong type of request. Use track or overview'
        error['status'] = 'FATAL'
        error['web_status'] = 0
        return request, error

    request, error = okapi_send_general_request(okapi_login,
                                                pass_prediction_request,
                                                url_endpoint, request_endpoint)

    return request, error
