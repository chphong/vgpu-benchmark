from flask import Flask, request
import tensorflow as tf
import time

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

print("start loading model...")
imported = tf.saved_model.load("./model/1")
print("model loaded...")


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


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8051, threaded=True)
