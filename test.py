import requests
import json

host_url = "http://127.0.0.1:8081"
headers = {
    "Content-type": "application/json"
}

def test_insert():
    endpoint = f"{host_url}/append"
    pool_id = 1000
    pool_values = [8, 4, 9, 1, 4]

    post_data =  {
            "poolId": pool_id,
            "poolValues": pool_values
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    assert resp.json().get("status", None) == "inserted"

def test_append():
    endpoint = f"{host_url}/append"
    pool_id = 1000
    pool_values = [10, 2, 1]

    post_data =  {
            "poolId": pool_id,
            "poolValues": pool_values
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    assert resp.json().get("status", None) == "appended"

def test_calculate_percentile():
    endpoint = f"{host_url}/query"
    pool_id = 1000
    percentile = 50

    post_data =  {
            "poolId": pool_id,
            "percentile": percentile
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    # Percentile 50% of [8, 4, 9, 1, 4] + [10, 2, 1] = 4
    # Length should be 8
    assert resp.json().get("result", None) == 4 and resp.json().get("length", None) == 8


def test_pool_id_as_nonnumeric():
    endpoint = f"{host_url}/append"
    pool_id = "Ab100"
    pool_values = [8, 4, 9, 1, 4]

    post_data =  {
            "poolId": pool_id,
            "poolValues": pool_values
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    assert resp.status_code == 400

def test_pool_values_as_nonnumeric():
    endpoint = f"{host_url}/append"
    pool_id = 1001
    pool_values = ["a", 1, 3]

    post_data =  {
            "poolId": pool_id,
            "poolValues": pool_values
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    assert resp.status_code == 400

def test_percentile_as_nonnumeric():
    endpoint = f"{host_url}/query"
    pool_id = 1000
    percentile = "50!"

    post_data =  {
            "poolId": pool_id,
            "percentile": percentile
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    assert resp.status_code == 400

def test_percentile_out_range():
    endpoint = f"{host_url}/query"
    pool_id = 1000
    percentile = 110

    post_data =  {
            "poolId": pool_id,
            "percentile": percentile
        }

    resp = requests.post(endpoint, data=json.dumps(post_data), headers=headers)

    assert resp.status_code == 400
