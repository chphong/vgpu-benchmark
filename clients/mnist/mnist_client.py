import grequests
import requests
import json
import random

concurrency = int(input("please input concurrent num: "))
headers = {"content-type": "application/json"}

req_list = []   # 请求列表

for i in range(concurrency):
    lucky_dog = random.randint(0, 9999)
    f = open("./clients/mnist/input/" +
             str(lucky_dog)+".json")
    data = json.loads(f.read())
    f.close()
    req_list.append(grequests.post(
        'http://tos59:31500/predict', data=json.dumps({'data': data}), headers=headers))

requests.get('http://tos59:31300/reset', headers=headers)
res_list = grequests.map(req_list)    # 并行发送，等最后一个运行完后返回
util_resp = requests.get('http://tos59:31300/util', headers=headers)
cost_sum = 0.
cost_count = 0
for i in range(concurrency):
    if res_list[i] != None:
        print("request", i, ":", res_list[i].text, end="")  # 打印第一个请求的响应文本
        resp = json.loads(res_list[i].text)
        cost_sum = cost_sum + resp["cost"]
        if resp["cost"] != 0.:
            cost_count = cost_count+1
utilization = json.loads(util_resp.text)
print("avg cost: ", cost_sum/cost_count, ", avg utilization: ", utilization)
