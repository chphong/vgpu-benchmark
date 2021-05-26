.PHONY: all
all: cifar10 mnist

.PHONY: cifar10
cifar10:
	cd ./CIFAR-10 && docker build -t chph/cifar-10:v1.0.0 -f Dockerfile . && docker push chph/cifar-10:v1.0.0

.PHONY: mnist
mnist:
	cd ./MNIST && docker build -t chph/mnist:v1.0.0 -f Dockerfile . && docker push chph/mnist:v1.0.0

.PHONY: deploy-cifar10
deploy-cifar10: 
	kubectl apply -f ./CIFAR-10/deployment.yaml

.PHONY: deploy-mnist
deploy-mnist: 
	kubectl apply -f ./MNIST/deployment.yaml
