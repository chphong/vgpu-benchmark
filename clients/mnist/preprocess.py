import numpy
import json

test_set = numpy.loadtxt(open("./clients/mnist/mnist_test.csv","rb"),delimiter=",",skiprows=0)
test_set = numpy.delete(test_set, -1, axis=1)

for s in range(1000):
    image = test_set[s:s+1].reshape(-1, 28, 28, 1)
    data = json.dumps({"signature_name": "serving_default", "instances": image.tolist()})
    f = open("./clients/mnist/input/"+str(s)+".json", "w+")
    f.write(data)
    f.flush()
    f.close()
