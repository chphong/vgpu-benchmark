import urllib
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread, Event


class NvmlThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.result = []
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            self.result.append(time.time())
            time.sleep(0.01)

    def get_result_count(self):
        return len(self.result)

    def get_avg_result(self):
        utilization_sum = 0
        num = self.get_result_count()
        if num == 0:
            return 0
        for u in self.result:
            utilization_sum = utilization_sum + u
        return 0.01*utilization_sum/num


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        post_data = self.rfile.read(
            int(self.headers['content-length'])).decode()
        print(post_data)
        data = {'cost': 0, 'utilization': 0.}
        path, args = urllib.parse.splitquery(self.path)
        if path == "/predict":
            thread = NvmlThread()
            thread.start()
            time.sleep(1)
            thread.stop()
            thread.join()
            print("utilization samples num:", thread.get_result_count())
            data['utilization'] = thread.get_avg_result()
        self.send_response(200)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


httpd = HTTPServer(('0.0.0.0', 8051), HttpHandler)
print("starting server...")
httpd.serve_forever()
