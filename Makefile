SCRIPT_FOLDER = `pwd`

.PHONY: build
build:
	docker-compose build

.PHONY: docker_build
docker_build:
	docker build . -f Dockerfile -t exeltesttask

.PHONY: start
start:
	docker-compose up
