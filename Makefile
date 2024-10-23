ALPINE_VERSION ?=3.20
OPTIONS ?=
BUILD_TARGET ?=postgres
.PHONY:	build
build:
	docker buildx build -t yidoughi/sql-api:alpine${ALPINE_VERSION} . --progress=plain ${OPTIONS}
	docker tag yidoughi/sql-api:alpine${ALPINE_VERSION} yidoughi/sql-api:latest

.PHONY:	run
run:
	docker rm -f sqlapi 
	docker run  --rm --name sqlapi -d --network host yidoughi/sql-api:alpine${ALPINE_VERSION}

.PHONY:	exec
exec:
	docker exec -it sqlapi sh

.PHONY:	run-all
run-all:
	make build
	make run
	make exec

.PHONY:	dev
dev:
	docker ps -qa | docker rm -f "@"
	docker compose up -d --force-recreate --remove-orphans 
	BUILD_TARGET=${BUILD_TARGET} docker compose -f compose.api.yml up 