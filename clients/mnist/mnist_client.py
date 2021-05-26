import grequests
import time

concurrency = int(input("please input concurrent num: "))

req_list = []   # 请求列表

for i in range(concurrency):
    f = open("clients/mnist/input/"+str(i)+".json")
    data = f.read()
    f.close()
    headers = {"content-type": "application/json"}
    req_list.append(grequests.post(
        'http://tos59:31500/v1/models/input_1:predict', data=data, headers=headers))

start = time.time()
res_list = grequests.map(req_list)    # 并行发送，等最后一个运行完后返回
end = time.time()
cost = end - start
for i in range(concurrency):
    print("request"+str(i)+":\n", res_list[i].text)  # 打印第一个请求的响应文本
print("total cost: ", cost, ", avg latency: ", cost/concurrency)
