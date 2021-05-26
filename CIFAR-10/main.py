from flask import Flask, request
import tensorflow as tf
import time
from threading import Thread, Event
from pynvml.smi import nvidia_smi

app = Flask(__name__)
print("start loading model...")
imported = tf.saved_model.load("./model/1")
print("model loaded...")


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
        utilization_sum = 0
        num = self.get_result_count()
        if num == 0:
            return 0
        for u in self.result:
            utilization_sum = utilization_sum + u
        return 0.01*utilization_sum/num


nvsmi = nvidia_smi.getInstance()
thread = NvmlThread()


@app.route('/predict', methods=['POST'])
def cost():
    if request.method == 'POST':
        data = {'cost': 0}
        input_str = request.json.get('data')
        start = time.time()
        with tf.device('/GPU:0'):
            imported(input_str)
        data['cost'] = time.time() - start
        return data
    return "method not supported"


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


if __name__ == '__main__':
    thread.start()
    app.run(host="0.0.0.0", port=8051, threaded=True)
