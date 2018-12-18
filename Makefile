MACHINE=$(shell uname -m)
IMAGE=pi-k8s-fitches-node-speech-daemon
VERSION=0.3
ACCOUNT=gaf3
NAMESPACE=fitches
VOLUMES=-v ${PWD}/lib/:/opt/pi-k8s/lib/ -v ${PWD}/test/:/opt/pi-k8s/test/ -v ${PWD}/bin/:/opt/pi-k8s/bin/

ifeq ($(MACHINE),armv7l)
BASE=resin/rpi-raspbian
DEVICE=--device=/dev/vchiq
else
BASE=debian:jessie
endif

.PHONY: build shell test run push create update delete

build:
	docker build . -f $(MACHINE).Dockerfile --build-arg BASE=$(BASE) -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run $(DEVICE)-it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

test:
	docker run $(DEVICE) -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include lib/service.py"

run:
	docker run $(DEVICE) -it $(VOLUMES) --rm -h $(IMAGE) $(ACCOUNT)/$(IMAGE):$(VERSION)

push: build
	docker push $(ACCOUNT)/$(IMAGE):$(VERSION)

create:
	kubectl create -f k8s/pi-k8s.yaml

update:
	kubectl replace -f k8s/pi-k8s.yaml

delete:
	kubectl delete -f k8s/pi-k8s.yaml
