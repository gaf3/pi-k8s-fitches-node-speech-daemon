MACHINE=$(shell uname -m)
IMAGE=pi-k8s-fitches-node-speech-daemon
VERSION=0.3
TAG="$(VERSION)-$(MACHINE)"
ACCOUNT=gaf3
NAMESPACE=fitches
VOLUMES=-v ${PWD}/lib/:/opt/pi-k8s/lib/ -v ${PWD}/test/:/opt/pi-k8s/test/ -v ${PWD}/bin/:/opt/pi-k8s/bin/

ifeq ($(MACHINE),armv7l)
DEVICE=--device=/dev/vchiq
endif

.PHONY: build shell test run push create update delete

build:
	docker build . -f $(MACHINE).Dockerfile -t $(ACCOUNT)/$(IMAGE):$(TAG)

shell:
	docker run $(DEVICE)-it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(TAG) sh

test:
	docker run $(DEVICE) -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(TAG) sh -c "coverage run -m unittest discover -v test && coverage report -m --include lib/service.py"

run:
	docker run $(DEVICE) -it $(VOLUMES) --rm -h $(IMAGE) $(ACCOUNT)/$(IMAGE):$(TAG)

push: build
	docker push $(ACCOUNT)/$(IMAGE):$(TAG)

create:
	kubectl create -f k8s/pi-k8s.yaml

update:
	kubectl replace -f k8s/pi-k8s.yaml

delete:
	kubectl delete -f k8s/pi-k8s.yaml
