ALPINE_VERSION ?=3.20

.PHONY:	build
build:
	docker buildx build -t yidoughi/sql-api:alpine${ALPINE_VERSION} . --progress=plain

.PHONY:	run
run:
	docker rm -f sqlapi 
	docker run  --rm --name sqlapi -d -p 8080 yidoughi/sql-api:alpine${ALPINE_VERSION}

.PHONY:	exec
exec:
	docker exec -it sqlapi sh

.PHONY:	run-all
run-all:
	make build
	make run
	make exec

