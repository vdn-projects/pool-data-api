## Introduction
This project developed to run REST API with two POST endpoints:
* `/append`: 
    * post data:
        ```
        {
            "poolId": 123546,
            "poolValues": [1,7,2,6]
        }
        ```
    * response: show the status values are inserted (poolId not exist) or appended.
        ```
        {"status": "inserted"}
        or
        {"status": "appended"}
        ```
* `/query`:
    * post data: 
        ```
        {
            "poolId": 123546,
            "percentile": 50
        }
        ```
    * response: show total pool values count (`length`) and its calculated quantile (`result`). 
        ```
        {
           "length": 4,
           "result": 4.0
        }
        ```

## Required setup
Please use python version 3.6 or higher, and ensure below 2 modules are installed.
* `requests==2.25.1`
* `pytest==6.2.2`


## How to run
* Run the server: `python server.py`, default host: `http://127.0.0.1:8081`.
* Run pytest for the unit test: `pytest test.py`

## 