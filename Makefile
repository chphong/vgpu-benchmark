.PHONY: all
all: cifar10 mnist utilization

.PHONY: cifar10
cifar10:
	cd ./CIFAR-10 && docker build -t chph/cifar-10:latest -f Dockerfile . && docker push chph/cifar-10:latest

.PHONY: mnist
mnist:
	cd ./MNIST && docker build -t chph/mnist:latest -f Dockerfile . && docker push chph/mnist:latest

.PHONY: utilization
utilization:
	cd ./utilization && docker build -t chph/utilization-server:latest -f Dockerfile . && docker push chph/utilization-server:latest

.PHONY: deploy-utilization undeploy-utilization
deploy-utilization:
	kubectl apply -f ./utilization/deployment.yaml
undeploy-utilization:
	kubectl delete -f ./utilization/deployment.yaml

.PHONY: deploy-cifar10-krux undeploy-cifar10-krux deploy-cifar10-nvidia undeploy-cifar10-nvidia
deploy-cifar10-krux: deploy-utilization
	kubectl apply -f ./CIFAR-10/deployment-krux.yaml
undeploy-cifar10-krux: undeploy-utilization
	kubectl delete -f ./CIFAR-10/deployment-krux.yaml
deploy-cifar10-nvidia: deploy-utilization
	kubectl apply -f ./CIFAR-10/deployment-nvidia.yaml
undeploy-cifar10-nvidia: undeploy-utilization
	kubectl delete -f ./CIFAR-10/deployment-nvidia.yaml

.PHONY: deploy-mnist-krux undeploy-mnist-krux deploy-mnist-nvidia undeploy-mnist-nvidia
deploy-mnist-krux: deploy-utilization
	kubectl apply -f ./MNIST/deployment-krux.yaml
undeploy-mnist-krux: undeploy-utilization
	kubectl delete -f ./MNIST/deployment-krux.yaml
deploy-mnist-nvidia: deploy-utilization
	kubectl apply -f ./MNIST/deployment-nvidia.yaml
undeploy-mnist-nvidia: undeploy-utilization
	kubectl delete -f ./MNIST/deployment-nvidia.yaml

.PHONY: test-mnist
test-mnist:
	python3 clients/mnist/mnist_client.py

.PHONY: test-cifar10
test-cifar10:
	python3 clients/cifar10/cifar10_client.py

.PHONY: generate-mnist-input clean-mnist-input
generate-mnist-input:
	mkdir -p clients/mnist/input/
	python3 clients/mnist/preprocess.py
clean-mnist-input:
	rm -rf clients/mnist/input/

.PHONY: generate-cifar10-input clean-cifar10-input
generate-cifar10-input:
	mkdir -p clients/cifar10/input/
	python3 clients/cifar10/preprocess.py
clean-cifar10-input:
	rm -rf clients/cifar10/input/
