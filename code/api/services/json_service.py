import json
import socketserver
import http.server


class ApiRequestHandlerService(http.server.BaseHTTPRequestHandler):

    def send_json(self, status_code, data=None):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode("utf-8"))

# leest de mee gegeven json body
    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode())
