from flask import Flask, request
from threading import Thread, Event
from pynvml.smi import nvidia_smi

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"


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
            utilization = nvsmi.DeviceQuery('utilization.gpu')
            u = utilization['gpu'][0]['utilization']['gpu_util']
            if u != 0:
                self.result.append(u)

    def reset(self):
        self.result = []

    def get_result_count(self):
        return len(self.result)

    def get_avg_result(self):
        print("utilization:", self.result)
        utilization_sum = 0
        num = self.get_result_count()
        if num == 0:
            return 0
        for u in self.result:
            utilization_sum = utilization_sum + u
        return (utilization_sum/num)*0.01


nvsmi = nvidia_smi.getInstance()
thread = NvmlThread()


@app.route('/util', methods=['GET'])
def utilization():
    if request.method == 'GET':
        data = {'utilization': thread.get_avg_result()}
        print("utilization samples num:", thread.get_result_count())
        return data
    return "method not supported"


@app.route('/reset', methods=['GET'])
def reset():
    if request.method == 'GET':
        thread.reset()
        return ""
    return "method not supported"


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


if __name__ == '__main__':
    thread.start()
    app.run(host="0.0.0.0", port=8051, threaded=True)
