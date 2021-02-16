ORG := security
PROJECT := snyk_watcher
TAG := $(REPOSITORY)/$(ORG)/$(PROJECT):latest
TEST_IMAGE_NAME := $(ORG)/$(PROJECT)-test:latest
TEST_ARGS:= --volume "$(CURDIR)/build":"/build" --name snyk_watcher-test $(TEST_IMAGE_NAME)

DOCKER_RUN:= docker run

build:
	docker build . --tag $(PROJECT)
	docker tag $(PROJECT) $(PROJECT):latest

build-test:
	echo $(TEST_IMAGE_NAME)
	docker build --file Dockerfile.test . --tag $(TEST_IMAGE_NAME)

test: build-test clean-test
	$(DOCKER_RUN) $(TEST_ARGS)

serve:
	docker-compose up --build 

clean:
	rm -rf build

clean-test:
	-@docker rm $(TEST_IMAGE_NAME)
