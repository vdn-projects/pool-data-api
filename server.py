from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import logging.config
import os
import json
import math
import traceback

class PoolDataServer(BaseHTTPRequestHandler):
    pool_data = {}

    def get_percentile(self, values, percentile):
        """
        Caculate percentile value 
        """
        k = (len(values)-1) * (percentile/100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return values[int(k)]
        
        return values[int(f)] * (c-k) + values[int(c)] * (k-f)
    
    def validate_data(self, data, var_type):
        """
        Validate input data including: pool_id, pool_values and percentile
        """
        if var_type == "pool_values":
            for d in data:
                if not type(d) in (int, float):
                    return False
        elif var_type == "pool_id":
            if not type(data) == int:
                return False
        elif var_type == "percentile":
            if not type(data) in (int, float):
                return False
            if data < 0 or data > 100:
                return False
        else:
            raise ValueError(f"No suport data validation for '{var_type}'")
        return True

    def query(self, pool_id, post_data):
        """
        Handle '/query' endpoint call.
        """

        percentile = post_data.get("percentile", None)
        
        if self.validate_data(percentile, var_type="percentile"):
            self.set_response(resp_type="success")
            values = self.pool_data.get(pool_id, None)
            val_length = None if values is None else len(values)
            result = None if values is None else self.get_percentile(values, percentile)

            resp_data = {
                "length": val_length,
                "result": result
            }
            self.wfile.write(json.dumps(resp_data).encode(encoding="utf8"))

        else:
            self.set_response(resp_type="client_error")
    
    def append(self, pool_id, post_data):
        """
        Handle '/append' endpoint call.
        """
        pool_values = post_data.get("poolValues", [])
        if self.validate_data(pool_values, var_type="pool_values"):

            self.set_response("success")
            if pool_id in self.pool_data:
                self.pool_data[pool_id] += pool_values
                resp_status = {"status": "appended"}
                logger.debug(f"Values appended: {self.pool_data}")

            else:
                self.pool_data[pool_id] = pool_values
                resp_status = {"status": "inserted"}
                logger.debug(f"Values inserted: {self.pool_data}")
            
            # Write status response and sorting pool_values to improve query speed
            self.wfile.write(json.dumps(resp_status).encode(encoding="utf8"))
            self.pool_data[pool_id] = sorted(self.pool_data[pool_id])

        else:
            self.set_response("client_error")

    def set_response(self, resp_type):
        """
        Set return response code and header.
        """

        if resp_type == "success":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

        elif resp_type == "client_error":
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Bad input data."}).encode(encoding="utf8"))

        elif resp_type == "server_error":
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Internal server error."}).encode(encoding="utf8"))

        else:
            raise ValueError(f"Not support this reponse type '{type}'")

    def do_POST(self):
        """
        Post method for 2 endpoints: /append and /query
        """

        try:
            content_length = int(self.headers["Content-Length"])
            post_data = json.loads(self.rfile.read(content_length).decode("utf-8"))
            pool_id = post_data.get("poolId", None)

            if self.validate_data(pool_id, "pool_id"):
                if self.path == "/append":
                    self.append(pool_id, post_data)

                elif self.path == "/query":
                    self.query(pool_id, post_data)
            else:
                self.set_response("client_error")

        except Exception:
            logger.error(traceback.format_exc())
            self.set_response("server_error")

if __name__ == "__main__":

    # Setup logging
    base_path = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(os.path.join(base_path, "logging.ini"))
    logger = logging.getLogger("pool_value_app")

    # HTTP Server operation
    port = 8081
    server_address = ("", port)
    httpd = HTTPServer(server_address, PoolDataServer)

    logger.info("HTTP Server starting...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logger.info("HTTP Server stoping...")