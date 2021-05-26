from tensorflow.keras import datasets
import json

(_, _), (test_images, _) = datasets.cifar10.load_data()

# 将像素的值标准化至0到1的区间内。
test_images = test_images / 255.0
batch_size = 1

for s in range(100000):
    image = test_images[s*batch_size:(s+1)*batch_size]
    data = json.dumps(image.tolist())
    f = open("./clients/cifar10/input/"+str(s)+".json", "w+")
    f.write(data)
    f.flush()
    f.close()
