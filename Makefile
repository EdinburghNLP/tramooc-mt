#!/bin/bash

LANGS=de ru pl zh bg el hr it pt nl cs
CONFIGS=$(patsubst %,./model/en-%/config.yml,$(LANGS))

.secondary:

run_docker:
	docker run --rm -p 8080:8080 tramooc/mt_server

run_local:
	./docker-entrypoint.py en-de en-ru

.phony: run_docker

build:
	docker build -t tramooc/mt_server .

models: $(CONFIGS)

.phony: models

marian:
	git -C $@ pull || git clone https://github.com/marian-nmt/marian-dev.git -b nematus $@
	mkdir -p $@/build && cd $@/build && cmake -DCMAKE_BUILD_TYPE=release .. && make -j4

./model/%/config.yml: marian
	mkdir -p $(@D)
	python server/download_models.py -w $(@D) -m $*

.PHONY: marian
