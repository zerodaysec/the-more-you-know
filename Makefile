SHELL=/bin/bash

# read env variables
-include .env
export

build:
	@echo "Building $(APP_NAME):$(APP_VERSION) ..." && \
	docker build -t $(APP_NAME):build . && \
	echo "Build $(APP_NAME):$(APP_VERSION) complete" 


freeze:
	pipenv requirements > requirements.txt
