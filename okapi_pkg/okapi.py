import requests
import time


def get_status_severity(status_type):
    if status_type == "NONE":
        return 0
    elif status_type == "NORMAL":
        return 100
    elif status_type == "REMARK":
        return 200
    elif status_type == "WARNING":
        return 300
    elif status_type == "FATAL":
        return 400
    else:
        print("WARNING: Unknown status type \"" + status_type + "\"")
        return 1000


def handle_rest_call(func, is_login_call=False, max_retries=3):
    connector_status = dict()
    connector_status["text"] = "OK"
    connector_status["type"] = "NORMAL"
    connector_status["web_status"] = 0

    retries = 1
    while retries <= max_retries:
        try:
            response = func()
            response.raise_for_status()
            break

        except requests.exceptions.HTTPError as err:
            # 403 is probably wrong password:
            if is_login_call and response.status_code == 403:
                try:
                    connector_response = response.json()
                    connector_status['text'] = "Got error from Auth0: " \
                                               + response['error'] + ': ' + response['error_description']
                    connector_status['type'] = 'FATAL'
                    connector_status['web_status'] = response.status_code
                    break
                except:
                    # print("Could not convert response data to json")
                    connector_status['text'] = "Got unknown error from Auth0: " + str(err)
                    connector_status['type'] = 'FATAL'
                    connector_status['web_status'] = response.status_code
                    break
            else:
                connector_status['text'] = 'Got HTTPError when sending request: ' + str(err)
                connector_status['type'] = 'FATAL'
                connector_status['web_status'] = response.status_code
                break
        except requests.exceptions.Timeout as err:
            if retries == max_retries:
                connector_status['text'] = 'Got timeout when sending request: ' + str(err)
                connector_status['type'] = 'FATAL'
                connector_status['web_status'] = 408
            retries += 1
            continue
        except requests.exceptions.RequestException as err:
            connector_status['text'] = 'Got unknown exception (Wrong url?).'
            connector_status['type'] = 'FATAL'
            connector_status['web_status'] = 520  # non-standard
            connector_status['error'] = err
            break
        break

    connector_response = dict()
    try:
        connector_response["actual_response"] = response.json()
    except:
        # print("Could not convert response data to json")
        connector_response["actual_response"] = response.content
    connector_response["status"] = connector_status
    return connector_response


class Okapi:

    def __init__(self):
        self.initialized = False
        self.okapi_login = dict()
        self.url = "http://platform.okapiorbits.com"
        self.tdms = None

    def init(self, username, password, url="http://platform.okapiorbits.com"):
        # init
        self.url = url

        request_token_payload = \
            {
                "grant_type": "password",
                "username": username,
                "password": password,
                "audience": "https://api.okapiorbits.space/picard",
                "scope": ("neptune_propagation neptune_propagation_request "
                          "pass_predictions pass_prediction_requests "
                          "pass_predictions_long pass_prediction_requests_long"),
                "client_id": "jrk0ZTrTuApxUstXcXdu9r71IX5IeKD3",
            }

        url_auth = "https://okapi-development.eu.auth0.com/oauth/token"
        connector_response = handle_rest_call(True)

        okapi_login_token = connector_response["actual_response"]

        self.okapi_login = \
            {
                "token": okapi_login_token,
                "url": url,
                "accessTime": str(time.time()),
                "header":
                    {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "access_token": okapi_login_token["access_token"],
                        "expires_in": str(okapi_login_token["expires_in"]),
                        "token_type": okapi_login_token["token_type"],
                        "scope": okapi_login_token["scope"]
                    }
            }

        self.tdms = Tdms(self.okapi_login, self.url)

        return connector_response


class Tdms:

    def __init__(self, okapi_login, url):
        self.okapi_login = okapi_login
        self.url = url + "/tdms"

    def get(self):
        return handle_rest_call()

    def add(self, file_path, file_format):
        with open(file_path, "r") as tdm_file:
            data = \
                {
                    "tdm":
                        {
                            "type": "tdm." + file_format,
                            "content": tdm_file.read()
                        }
                }
            return handle_rest_call()
