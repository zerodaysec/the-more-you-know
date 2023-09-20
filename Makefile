SHELL=/bin/bash

# read env variables
-include .env
export

build:
	@echo "Building $(APP_NAME):$(APP_VERSION) ..." && \
	docker build -t $(APP_NAME):build . && \
	echo "Build $(APP_NAME):$(APP_VERSION) complete" 

run:
	docker run -p8080:8080 $(APP_NAME):build

update-feeds:
	pushd app && \
	cat feeds/* > rss_feeds.csv && \
	popd

get-news: update-feeds
	pushd app && \
	cat feeds/* pipenv run python get_rss.py && \
	popd

freeze:
	pipenv run pip freeze > requirements.txt
