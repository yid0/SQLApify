SQLAPIFY_VERSION ?=1.0.0
ALPINE_VERSION ?=3.20
OPTIONS ?=
BUILD_TARGET ?=postgres
TAG ?=${SQLAPIFY_VERSION}-alpine${ALPINE_VERSION}

.PHONY:	build
build:
	docker buildx build -t yidoughi/sqlapify:${TAG} . --progress=plain ${OPTIONS}
	docker tag yidoughi/sqlapify:${TAG} yidoughi/sqlapify:latest

.PHONY:	build-test
build-test:
	docker buildx build -f Dockerfile.test -t yidoughi/sqlapify-test:${TAG} . --progress=plain ${OPTIONS}

push:
	docker push yidoughi/sqlapify:${TAG}
	docker push yidoughi/sqlapify:latest

.PHONY:	run
run:
	docker rm -f sqlapify 
	docker run --rm --name sqlapify -d --network host yidoughi/sqlapify:${TAG}

.PHONY:	exec
exec:
	docker exec -it sqlapify sh

.PHONY:	run-all
run-all:
	make build
	make run
	make exec

run-deps:
	docker compose up -d --force-recreate 

.PHONY:	install
install:
	source venv/bin activate && pip -r requirement.txt
	
.PHONY:	local
local:
	BUILD_TARGET=${BUILD_TARGET} POSTGRES_HOST=localhost uvicorn src.main:app --host 0.0.0.0 --reload --env-file env/.env.postgres.dev 

.PHONY:	dev
dev:
	docker ps -qa | docker rm -f "@"
	docker compose up -d --force-recreate --remove-orphans 
	BUILD_TARGET=${BUILD_TARGET} docker compose -f compose.api.yml up --build


.PHONY:	test
test:
	BUILD_TARGET=${BUILD_TARGET} docker compose -f compose.test.yml up --build

.PHONY: deploy-sqlapify
deploy-sqlapify:
	microk8s kubectl apply -k deploy/sqlapify