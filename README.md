# TRAMOOC-MT
MT MODULE IN TRAMOOC PROJECT

## Information
maintainer: Tomasz Dwojak <t.dwojak@amu.edu.pl>
version: 0.1

## Installation
on Ubuntu 16.04, the server runs natively. To install required python packages, execute:

    pip install -r requirements.txt --user

on other Linux systems, the server can be deployed via a Docker container.

 - Install Docker: https://docs.docker.com/engine/installation/
 - execute `make build`

## Models
If you want to download model, do:
```
make models
```

## Usage instructions

you can run the local server as follows (for English-German):

    ./docker-entrypoint.py en-de

you can run the server in a docker container as follows (for English-German):

    docker run --rm -p 8080:8080 tramooc/mt_server

A simple sample client is provided by `test.py`