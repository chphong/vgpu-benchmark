import urllib
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path, args = urllib.parse.splitquery(self.path)
        print("GET", path, args)
        self._response(path, args)

    def _response(self, path, args):
        if args:
            args = urllib.parse.parse_qs(args).items()
            args = dict([(k, v[0]) for k, v in args])
        else:
            args = {}
        data = {'cost': 0, 'prediction': '', }
        if path == "/predict":
            input_str = args["input"]
            data['cost'] = time.time()
            data['prediction'] = input_str
        self.send_response(200)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


print("hello")
httpd = HTTPServer(('0.0.0.0', 8051), HttpHandler)
httpd.serve_forever()
