DB_NAME ?= fsa-demo-db
DB_HOST ?= localhost
DB_PORT ?= 5438
DB_USER ?= postgres
DB_PASS ?= postgres

LOCAL_TEST_DB_NAME ?= fsa-demo-test-db
LOCAL_TEST_DB_HOST ?= localhost
LOCAL_TEST_DB_PORT ?= 5439
LOCAL_TEST_DB_USER ?= postgres
LOCAL_TEST_DB_PASS ?= postgres

ARCHITECTURE := $(shell eval uname -m)
POSTGRES_IMAGE := postgres
POSTGRES_TAG := 14.5
PLATFORM_ARCH := linux/amd64

# If you have an ARM, use different postgis image
ifeq ($(ARCHITECTURE),arm64)
	POSTGRES_IMAGE=kartoza/postgis
	POSTGRES_TAG=14-3.3
	PLATFORM_ARCH=linux/arm64
endif

LOCAL_PKG_DIR := $(shell eval pwd)
DB_DATA_FOLDER ?= ${LOCAL_PKG_DIR}/db_data
TEST ?=""


.PHONY: db-folder
db-folder:
	mkdir -p ${DB_DATA_FOLDER}

.PHONY: rundb
rundb: ## Starts a local dev database in docker
	docker run --platform ${PLATFORM_ARCH} --name ${DB_NAME} \
	-e POSTGRES_DB=${DB_NAME} \
	-e POSTGRES_USER=${DB_USER} \
	-e POSTGRES_PASSWORD=${DB_PASS} \
	-p ${DB_PORT}:5432 \
	--volume ${DB_DATA_FOLDER}:/var/lib/postgresql/data \
	-d ${POSTGRES_IMAGE}:${POSTGRES_TAG}

.PHONY: db-up
db-up: db-folder rundb ## Starts a local dev database in docker

.PHONY: db-down
db-down: ## Stops and destroys the local dev database in docker
	docker stop ${DB_NAME}
	docker rm ${DB_NAME}


.PHONY: test-db-up
test-db-up: ## Starts a local test database in docker
	docker run --name ${LOCAL_TEST_DB_NAME} \
	-e POSTGRES_DB=${LOCAL_TEST_DB_NAME} \
	-e POSTGRES_USER=${LOCAL_TEST_DB_USER} \
	-e POSTGRES_PASSWORD=${LOCAL_TEST_DB_PASS} \
	-p ${LOCAL_TEST_DB_PORT}:5432 \
	-d ${POSTGRES_IMAGE}:${POSTGRES_TAG}

.PHONY: test-db-down
test-db-down: ## Stops and destroys the local test database in docker
	docker stop ${LOCAL_TEST_DB_NAME}
	docker rm ${LOCAL_TEST_DB_NAME}

.PHONY: run
run: ## Runs the web-server
	DB_HOST=${DB_HOST} \
	DB_PORT=${DB_PORT} \
	DB_NAME=${DB_NAME} \
	DB_USER=${DB_USER} \
	DB_PASS=${DB_PASS} \
	poetry run uvicorn main:app --reload

.PHONY: test
test: ## Runs tests
	TEST_DB_HOST=${LOCAL_TEST_DB_HOST} \
	TEST_DB_PORT=${LOCAL_TEST_DB_PORT} \
	TEST_DB_NAME=${LOCAL_TEST_DB_NAME} \
	TEST_DB_USER=${LOCAL_TEST_DB_USER} \
	TEST_DB_PASS=${LOCAL_TEST_DB_PASS} \
	poetry run python -m pytest -v -k ${TEST} --ignore=db_data

.PHONY: black
black: ## Formats code using black
	poetry run black .

.PHONY: ruff
ruff: ## Runs ruff to check and fix code
	poetry run ruff --fix .

.PHONY: checks
checks: black ruff ## Runs code formatting and checks
