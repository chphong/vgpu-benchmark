# vgpu-benchmark
tos krux和nvidia k8s-device-plugin两种GPU方案性能测试工具。

# 使用方法
所有的操作均可以基于Makefile进行操作，常用的测试指令说明如下：
- `make all`：编译镜像并推送到docker hub
- `make deploy-mnist-krux`：部署tos krux方案mnist推理服务性能测试服务端，采用副本数为2的Deployment进行部署，每个实例占用50 vgpu-core和7G vgpu-memory，共享同一块GPU
- `make deploy-cifar10-krux`：部署tos krux方案cifar-10推理服务性能测试服务端，采用副本数为2的Deployment进行部署，每个实例占用50 vgpu-core和7G vgpu-memory，共享同一块GPU
- `make deploy-mnist-nvidia`：部署nvidia k8s-device-plugin方案mnist推理服务性能测试服务端，采用副本数为1的Deployment进行部署，独占一块GPU
- `make deploy-cifar10-nvidia`：部署nvidia k8s-device-plugin方案cifar-10推理服务性能测试服务端，采用副本数为1的Deployment进行部署，独占一块GPU
- `make generate-mnist-input`：生成mnist推理服务测试输入文件
- `make generate-cifar10-input`：生成cifar-10推理服务测试输入文件
- `make test-mnist`：测试mnist推理服务的时延和GPU使用率
- `make test-cifar10`：测试mnist推理服务的时延和GPU使用率
- 还有其他更多指令，可以直接查阅Makefile文件