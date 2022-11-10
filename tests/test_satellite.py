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
def add_satellite(test_token):
    okapi_login = test_token['okapi_login']
    object_to_add = {
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

    added_satellite, error = okapi_add_object(okapi_login, object_to_add, 'satellites')
    return added_satellite


def test_get_objects(test_token, add_satellite):
    okapi_login = test_token['okapi_login']
    all_satellites, error = okapi_get_objects(okapi_login, 'satellites')
    assert add_satellite
    assert 'satellite_id' in add_satellite
    assert 'elements' in all_satellites
    assert len(all_satellites['elements']) > 0
    assert 'satellite_id' in all_satellites['elements'][0]
    assert error['web_status'] == 200


def test_change_objects(test_token, add_satellite):
    okapi_login = test_token['okapi_login']
    object_to_modify = {
        "satellite_id": object_to_add["satellite_id"],
        "area": 0.01
    }
    object_to_modify, error = okapi_change_object(okapi_login, object_to_modify, 'satellites')
    assert 'satellite_id' in object_to_modify
    assert object_to_modify["area"] == 0.01
    assert object_to_modify["thrust_uncertainty"] == 2
    assert error['web_status'] == 200


def test_remove_objects(test_token, add_satellite):
    okapi_login = test_token['okapi_login']
    added_satellite = add_satellite
    deleted_satellite, error = okapi_delete_object(okapi_login, added_satellite, 'satellites')
    assert 'satellite_id' in deleted_satellite
    assert error['web_status'] == 200
