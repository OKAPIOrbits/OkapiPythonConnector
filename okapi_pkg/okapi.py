

import requests
import time


class Okapi:



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
      print("WARNING: Unkown status type \"" + status_type + "\"")
      return 1000



  #def merge_statuses(source_status, target_status):
  #  result_status = target_status
  #  if get_status_severity(source_status["type"]) > get_statu


  def handle_rest_call(func, is_login_call = False, max_retries=3):

    connector_status = dict()
    connector_status["text"] = "All ok"
    connector_status["type"] = "NORMAL"
    connector_status["web_status"] = 0
    
    retries = 1
    while(retries <= max_retries):
      try:
        response = func()
        response.raise_for_status()
        break

      except requests.exceptions.HTTPError as err:
        #print(err)
        # we know that 403 is probably wrong password:
        if (is_login_call and response.status_code == 403):
          try:
            connector_response = response.json()
            connector_status['text'] = "Got error from Auth0: " \
              + response['error'] + ': ' + response['error_description']
            connector_status['type'] = 'FATAL'
            connector_status['web_status'] = response.status_code
            break
          except:
            #print("Could not convert response data to json")
            connector_status['text'] = "Got unknown error from Auth0: " + str(err)
            connector_status['type'] = 'FATAL'
            connector_status['web_status'] = response.status_code
            break
        else:
          connector_status['text'] = 'Got HTTPError when sending request: ' \
            + str(err)
          connector_status['type'] = 'FATAL'
          connector_status['web_status'] = response.status_code
          break
      except requests.exceptions.Timeout as err:
        if(retries == max_retries):
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
      #print("Could not convert response data to json")
      connector_response["actual_response"] = response.content
    connector_response["status"] = connector_status
    #print("auch hier: " + str(connector_response))
    return connector_response


  def __init__(self):

    self.initialized = False


  def init(self, username, password, url 
    = "http://platform.okapiorbits.com"):
    
    # init
    self.okapi_login = dict()
    self.url = url
    #status = dict()
    #status["text"] = "NONE"
    #status["type"] = "NONE"
    #status["web_status"] = 0

    #if self.initialized:
    #    status["type"] = "FATAL"
    #    status["message"] = "

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
    connector_response = Okapi.handle_rest_call(lambda: requests.post(url_auth,
      data = request_token_payload, timeout = 5), True)


    okapi_login_token = connector_response["actual_response"]

    #try:
    #  okapi_login_token_response = requests.post(url_auth,
    #    data=request_token_payload, timeout=5)
    #  okapi_login_token_response.raise_for_status()
    #  okapi_login_token = okapi_login_token_response.json()

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

    #except requests.exceptions.HTTPError as err:
    #  print(err)
    #  # we now that 403 is probably wrong password:
    #  if (okapi_login_token_response.status_code == 403):
    #    response = okapi_login_token_response.json()
    #    status["text"] = ("Got error from Auth0: " + response["error"] +
    #      ": " + response["error_description"])
    #    status["type"] = "FATAL"
    #    status["web_status"] = okapi_login_token_response.status_code
    #  else:
    #    status["text"] = "Got HTTPError when sending request. "
    #    status["type"] = "FATAL"
    #    status["web_status"] = okapi_login_token_response.status_code
    #  return status
    #except requests.exceptions.Timeout as err:
    #  print(err)
    #  status["text"] = "Got timeout when sending request. "
    #  status["type"] = "FATAL"
    #  status["web_status"] = 408  # correct timeout?
    #  return status
    #except requests.exceptions.RequestException as err:
    #  print(err)
    #  status["text"] = "Got unknown exception. "
    #  status["type"] = "FATAL"
    #  status["web_status"] = 520  # non-standard
    #  return status

    self.tdms = Tdms(self.okapi_login, self.url)

    return connector_response





class Tdms:


  def __init__(self, okapi_login, url):

    self.okapi_login = okapi_login
    self.url = url + "/tdms"


  def get(self):
    #print("jup")
    return Okapi.handle_rest_call(lambda: requests.get(self.url,
      headers = self.okapi_login["header"], timeout = 5))


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
      #print(data)
      return Okapi.handle_rest_call(lambda: requests.post(self.url, json = data,
        headers = self.okapi_login["header"], timeout = 5))

