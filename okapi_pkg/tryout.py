#!/usr/bin/python

import time

# Import OKAPI routines. If you use the script with OKAPI installed by PIP,
# adapt it (see below)
from okapi_init import okapi_init
from okapi_send_request import okapi_send_request
from okapi_get_result import okapi_get_result
# when using OKAPI installed with PIP:
# from okapi_pkg.okapi_init import okapi_init
# from okapi_pkg.okapi_send_request import okapi_send_request
# from okapi_pkg.okapi_get_result import okapi_get_result

#
# Init --> Get a token to run the analyses
#
# For auth info: See www.okapiorbits.space or contact us
okapi_login, error = okapi_init(  < adress to okapi server as string > ,
                                 < user account as string > ,
                                 < user password as string > )
print("OkapiLogin: {}".format(okapi_login))
# check for the error status
if (error['status'] == 'FATAL'):
    print(error)
    exit('Error during authentification.')
elif(error['status'] == 'WARNING'):
    print(error)
# print(okapi_login)


#
# Pass predictions
#

#
# # Prepare your request
pass_pred_request_body = {
    "orbit": {
        "type": "tle.txt",
        "content": "1 25544U 98067A   18218.76369510  .00001449  00000-0  29472-4 0  9993\n2 25544  51.6423 126.6422 0005481  33.3092  62.9075 15.53806849126382"
    },
    "ground_location": {
        "type": "ground_loc.json",
        "content": {
            "longitude": 10.645,
            "latitude": 52.3283,
            "altitude": 0.048
        }
    },
    "time_window": {
        "type": "tw.json",
        "content": {
            "start": "2018-08-07T18:00:00.000Z",
            "end": "2018-08-08T00:00:00.000Z"
        }
    },
    "settings": {
        "type": "shared_prop_settings.json",
        "content": {
            "output_step_size": 60
        }
    }

}

#
# # send different pass prediction pass prediction requests
#
# # send a request to use SGP4 for pass prediction
request_sgp4, error = okapi_send_request(okapi_login, pass_pred_request_body,
                                         'predict-passes/sgp4/requests')
# DEBUG                                        
# print("RequestSGP4: {}".format(request_sgp4))
# print("RequestError: {}".format(error))
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(request_sgp4)

# wait a short while to let the server process all requests
time.sleep(15)

# get the results and print them to the console

# get the result from SGP4 pass prediction (Note: There will be more formats
# available soon)

# get the result from SGP4
print("Getting pass predictions SGP4 result")
result_sgp4, error = okapi_get_result(okapi_login, request_sgp4,
                                      'predict-passes/sgp4/results/{}/simple')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(result_sgp4)

#
# Propagation: NEPTUNE
#

# set up the data
# you can request neptune propagations with "simple states". The neptune_config
# is optional. The values stated are identical to the standard.
propagate_neptune_simple_request_body = {
    "orbit":
    {
        "type": "state.json",
        "content":
        {
            "area": 1,
            "mass": 1,
            "x": 615.119526,
            "y": -7095.644839,
            "z": -678.668352,
            "x_dot": 0.390367,
            "y_dot": 0.741902,
            "z_dot": -7.39698,
            "epoch": "2016-07-21T00:31:50.000Z"
        }
    },
    "settings": {
        "type": "prop_settings.json",
        "content":
        {
            "propagation_end_epoch": "2016-07-23T00:31:50.000Z",
        }
    }
}


# send the simple request to the server
request_neptune_simple, error = okapi_send_request(
    okapi_login,
    propagate_neptune_simple_request_body,
    'propagate-orbit/neptune/requests')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(request_neptune_simple)

# again, give the server some time to process therequest. Note that numerical
# propagation can take a while
time.sleep(25)

# get the results from the simple request as oem results
print("Getting OEM result")
result_oem, error = okapi_get_result(okapi_login, request_neptune_simple,
                                     'propagate-orbit/neptune/results/{}/oem')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(result_oem)

# or as opm
print("Getting OPM result")
result_opm, error = okapi_get_result(okapi_login, request_neptune_simple,
                                     'propagate-orbit/neptune/results/{}/opm')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(result_opm)


# you can also send the result as OPM, which provide some more details for
# input. Note that all fields are required. Again, neptune_config and all
# parameters from there are optional
propagate_neptune_opm_request_body = {
    "orbit": {
        "type": "opm.json",
        "content": {
            "OPM_HEADER": {
                "CCSDS_OPM_VERS": 2
            },
            "OPM_META_DATA": {
                "OBJECT_NAME": "ISS (ZARYA)",
                "OBJECT_ID": "1998-067-A",
                "CENTER_NAME": "EARTH",
                "REF_FRAME": "GCRF",
                "REF_FRAME_EPOCH": "2000-01-01T00:00:00Z",
                "TIME_SYSTEM": "UTC"
            },
            "OPM_DATA": {
                "EPOCH": "2016-07-21T00:31:50.000Z",
                "X": 615.119526,
                "Y": -7095.644839,
                "Z": -678.668352,
                "X_DOT": 0.390367,
                "Y_DOT": 0.741902,
                "Z_DOT": -7.39698,
                "MASS": 1,
                "SOLAR_RAD_COEFF": 1.3,
                "DRAG_AREA": 1,
                "DRAG_COEFF": 2.2
            }
        }
    },
    "settings": {
        "type": "prop_settings.json",
        "content": {
            "propagation_end_epoch": "2016-07-23T00:31:50.000Z",
            "more": {
                "output_step_size": 30,
            }
        }
    }
}


# # send the opm request to the server
request_neptune_opm, error = okapi_send_request(
    okapi_login,
    propagate_neptune_opm_request_body,
    'propagate-orbit/neptune/requests')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(request_neptune_opm)

# again, the server needs some time to process the request. Instead of sleeping
# we introduce a "while" loop and just ask the surver until we get the
# result we want. We introduce a maximum numbers of calls to avoid getting
# fully stuck for some reason
counter = 0
error['web_status'] = 202
while (counter < 50) and (error['web_status'] == 202):

    # get the results from the OPM request as simple state
    print("Getting OPM result in loop")
    result_simple, error = okapi_get_result(
        okapi_login, request_neptune_opm,
        'propagate-orbit/neptune/results/{}/simple')
    if (error['status'] == 'FATAL'):
        print(error)
        exit()
    elif(error['status'] == 'WARNING'):
        print(error)
    #print(result_simple)

    # we wait a second, to not trigger some DOD on the server ;-)
    time.sleep(1)

    counter += 1

print("resultopm: {}".format(result_simple))
#
# Propagation: SGP4
#
propagate_sgp4_request_body = {
    "orbit": {
        "type": "tle.txt",
        "content": "1 25544U 98067A   18218.76369510  .00001449  00000-0  29472-4 0  9993\n2 25544  51.6423 126.6422 0005481  33.3092  62.9075 15.53806849126382"
    },
    "settings": {
        "type": "prop_settings.json",
        "content": {
            "propagation_end_epoch": "2018-08-08T00:00:00.000Z",
            "more": {
                "output_step_size": 100
            }
        } 
    }
}

# send it to the server
print("Getting OPM result")
request_neptune_opm, error = okapi_send_request(
    okapi_login,
    propagate_sgp4_request_body,
    'propagate-orbit/sgp4/requests')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
# print(request_neptune_opm)

# sgp4 is rather fast, so we do not have to wait that long.
time.sleep(2)

# as simple result
print("Getting simple result")
result_simple, error = okapi_get_result(
    okapi_login, request_neptune_opm, 'propagate-orbit/sgp4/results/{}/simple')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(result_simple)

# as omm result
print("Getting OMM result")
result_simple, error = okapi_get_result(
    okapi_login, request_neptune_opm, 'propagate-orbit/sgp4/results/{}/omm')
if (error['status'] == 'FATAL'):
    print(error)
    exit()
elif(error['status'] == 'WARNING'):
    print(error)
# print(result_simple)
