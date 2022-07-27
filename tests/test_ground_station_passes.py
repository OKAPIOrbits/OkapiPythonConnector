import os
import pytest
from okapi_pkg import okapi_init, okapi_get_objects, okapi_add_object, okapi_delete_object, okapi_change_object


@pytest.fixture(scope="module")
def test_token():
    test_url = os.environ['OKAPI_TEST_URL']
    test_username = os.environ['OKAPI_TEST_USERNAME']
    test_password = os.environ['OKAPI_TEST_PASSWORD']
    okapi_login, error = okapi_init(test_url,
                                    test_username,
                                    test_password)

    return {"okapi_login": okapi_login, "error": error}


def test_auth0_login(test_token):
    okapi_login = test_token['okapi_login']
    error = test_token['error']
    assert error['web_status'] == 200
    assert error['status'] == 'OK'
    assert 'token' in okapi_login
    assert 'access_token' in okapi_login['token']


@pytest.fixture(scope="module")
def add_ground_station_passes(test_token):
    okapi_login = test_token['okapi_login']
    object_to_add = {
        "elements": [
            {
                "spacecraft": "SALSAT",
                "passes": [
                    {
                        "start": "2020-10-13T10:00:23Z",
                        "end": "2020-10-13T10:09:54Z"
                    },
                    {
                        "start": "2020-10-13T12:57:08Z",
                        "end": "2020-10-13T13:08:50Z"
                    },
                    {
                        "start": "2020-10-13T20:41:06Z",
                        "end": "2020-10-13T20:49:45Z"
                    }
                ]
            },
            {
                "spacecraft": "TUBIN",
                "passes": [
                    {
                        "start": "2020-10-13T22:15:37Z",
                        "end": "2020-10-13T22:24:34Z"
                    },
                    {
                        "start": "2020-10-14T09:49:20Z",
                        "end": "2020-10-14T09:58:45Z"
                    },
                    {
                        "start": "2020-10-14T12:45:58Z",
                        "end": "2020-10-14T12:57:41Z"
                    }
                ]
            }
        ]
    }

    added_passes, error = okapi_add_object(okapi_login, object_to_add, 'multi-ground-station-passes')
    return added_passes


def test_get_objects(test_token, add_ground_station_passes):
    okapi_login = test_token['okapi_login']
    all_passes, error = okapi_get_objects(okapi_login, 'multi-ground-station-passes-info')
    assert add_ground_station_passes
    assert 'elements' in all_passes
    assert len(all_passes['elements']) > 0
    assert 'ground_station_passes_id' in all_passes['elements'][0]
    assert error['web_status'] == 200
