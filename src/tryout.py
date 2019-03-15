#!/usr/bin/python

from okapi_init import okapi_init
from okapi_send_passprediction_request import okapi_send_passprediction_request
from okapi_get_result import okapi_get_result

import time

pass_pred_data = {
    "tle": "                        \n1 25544U 98067A   18218.76369510  .00001449  00000-0  29472-4 0  9993\n2 25544  51.6423 126.6422 0005481  33.3092  62.9075 15.53806849126382",
    "groundLocation": {
        "longitude": 10.645,
        "latitude": 52.3283,
        "altitude": 0.048
    },
    "timeWindow": {
        "start": "2018-08-07T18:00:00.000Z",
        "end": "2018-08-08T00:00:00.000Z"
    }
}

# For auth info: See www.okapiorbits.space or contact us
auth_response = okapi_init("http://okapi.ddns.net:34569/", "YOUR LOGIN NAME", "YOUR LOGIN PASSWORD")
print(auth_response)
request_response = okapi_send_passprediction_request(auth_response[0], pass_pred_data, "overview")
print(request_response)
time.sleep(1)
results_response = okapi_get_result(auth_response[0], request_response[0])
print(results_response)
