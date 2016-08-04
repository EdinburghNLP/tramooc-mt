#!/bin/bash

.secondary:

run_docker:
	docker run --rm -p 8080:8080 tramooc/mt_server

run_local:
	./docker-entrypoint.py en-de en-ru

.phony: run_docker

build:
	docker build -t tramooc/mt_server .

models: ./model/en-de/config.yml ./model/en-ru/config.yml

.phony: models

amunmt:
	git clone https://github.com/emjotde/amunmt.git -b cpu_stable $<

./model/%/config.yml: amunmt
	mkdir -p $(@D)
	python $</scripts/download_models.py -w $(@D) -m $*

