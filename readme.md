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
    * expected response: show the status values are inserted (poolId not exist) or appended.
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
    * expected response: show total pool values count (`length`) and its calculated quantile (`result`). 
        ```
        {
           "length": 4,
           "result": 4.0
        }
        ```

## Required setup
Please use python version 3.6 or higher, and ensure below 2 additional modules to be installed (not included in default python package).
* `requests==2.25.1`
* `pytest==6.2.2`

## How to run
* Run the server: `python server.py`, default host access: `http://127.0.0.1:8081`.
* Run pytest for the unit test: `pytest test.py`

## Potential improvement
* There is a potential of loosing data becaused of `httpd` issues need to restart, we can set a frequently dumping `pool_data` to file on disk for backup. Once it recovered, it will reloaded the file to memory back.
* There is a potential of out of memory error as all values stored on memory at `pool_data` variable. We can consider reduce this risk by settingup a separate monitoring and alert at specifict threshold, so engineer can timely fix.
* In case, the system needs to be scaled and more available, we may need to consider running `/append` & `/query` task on multiple worker nodes. This would need `load balancer` to distribute task between nodes, `message queue` handle concurent `/append` posts, and `central storage` for commond access by multiple nodes.
