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
	git clone https://github.com/amunmt/amunmt.git
	cd amunmt && git checkout 5ef48d5 -b 5ef48d5
	mkdir -p amunmt/build && cd amunmt/build && cmake -DCMAKE_BUILD_TYPE=release .. && make -j 2 && make -j 2 python

./model/%/config.yml: amunmt
	mkdir -p $(@D)
	python server/download_models.py -w $(@D) -m $*

