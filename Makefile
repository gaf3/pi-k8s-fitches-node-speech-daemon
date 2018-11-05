IMAGE=pi-k8s-fitches-speech-daemon
VERSION=0.1
ACCOUNT=gaf3
NAMESPACE=fitches

pull:
	docker pull $(ACCOUNT)/$(IMAGE)login 

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell: build
	docker run --device=/dev/vchiq -it $(ACCOUNT)/$(IMAGE):$(VERSION) sh

run: build
	docker run --device=/dev/vchiq -it --rm -h $(IMAGE) $(ACCOUNT)/$(IMAGE):$(VERSION)

push: build
	docker push $(ACCOUNT)/$(IMAGE):$(VERSION)

create: push
	kubectl -n $(NAMESPACE) create -f k8s/pi-k8s.yaml

update: push
	kubectl -n $(NAMESPACE) replace -f k8s/pi-k8s.yaml

delete:
	kubectl -n $(NAMESPACE) delete -f k8s/pi-k8s.yaml
