IMAGE=pi-k8s-fitches-speech-daemon
VERSION=0.2
ACCOUNT=gaf3
NAMESPACE=fitches
VOLUMES=-v ${PWD}/lib/:/opt/pi-k8s/lib/ -v ${PWD}/test/:/opt/pi-k8s/test/ -v ${PWD}/bin/:/opt/pi-k8s/bin/

.PHONY: pull build shell test run push create update delete

pull:
	docker pull $(ACCOUNT)/$(IMAGE)login 

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run --device=/dev/vchiq -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

test:
	docker run --device=/dev/vchiq -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include lib/*.py"

run:
	docker run --device=/dev/vchiq -it $(VOLUMES) --rm -h $(IMAGE) $(ACCOUNT)/$(IMAGE):$(VERSION)

push: build
	docker push $(ACCOUNT)/$(IMAGE):$(VERSION)

create: push
	kubectl -n $(NAMESPACE) create -f k8s/pi-k8s.yaml

update: push
	kubectl -n $(NAMESPACE) replace -f k8s/pi-k8s.yaml

delete:
	kubectl -n $(NAMESPACE) delete -f k8s/pi-k8s.yaml
