# TRAMOOC-MT
MT MODULE IN TRAMOOC PROJECT

## Information
maintainer: Roman Grundkiewicz <rgrundki@staffmail.ed.ac.uk>

version: 3

## Installation
on Ubuntu 16.04, the server can be installed natively.

  - install required Ubuntu packages (see Dockerfile for list)
    - if you don't use docker, you might install CUDA and CUDNN manually;
      choose version compatible with [the Docker file](https://gitlab.com/nvidia/cuda/blob/ubuntu16.04/8.0/devel/cudnn5/Dockerfile),
      i.e. CUDA 8.0 and CUDNN-dev 5.1.10, which is downloadable from [here](http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libcudnn5-dev_5.1.10-1+cuda8.0_amd64.deb)

  - install required python packages with pip:

    pip install -r requirements.txt --user

  - install MarianNMT:

    make marian

on other Linux systems, the server can be deployed via a Docker container.

 - install Docker: https://docs.docker.com/engine/installation/
 - install nvidia-docker: https://github.com/NVIDIA/nvidia-docker/wiki
 - execute `make build`

## Models
If you want to download model, do:
```
make models
```

## Usage instructions

you can run the local server as follows (for English-German):

    ./docker-entrypoint.py en-de

you can run the server in a docker container as follows:

    nvidia-docker run --rm -p 8080:8080 -v model:/model tramooc/mt_server en-de

a single server can also support multiple languages:

    nvidia-docker run --rm -p 8080:8080 -v model:/model tramooc/mt_server en-de en-ru

you can also specify GPU devices which should be used by the server for each language pair;
for example, to use GPU with ID 0 and 1 for en-de, and only GPU 1 for en-ru, you should type:

    nvidia-docker run --rm -p 8080:8080 -v model:/model tramooc/mt_server en-de:0,1 en-ru:1

If you want to run more than one instance of the server, specify ports for subprocessors:

    nvidia-docker run --rm -p 8080:8080 -v model:/model tramooc/mt_server en-de --subproc-port 60000

See `./docker-entrypoint.py --help` for other options, which can be also passed
to `nvidia-docker` (at the end of the command line options).

A simple sample client is provided by `sample-client.py`. `sample-client-2.py`
allows the translation of text passed via standard input.

## License

The code in this repository is released under the FreeBSD License.

By default, the tool downloads and uses pre-trained models for 11 language pairs (see below).
These models are released for research purposes only.


## Supported language pairs

    - en-bg (English-Bulgarian)
    - en-cs (English-Czech)
    - en-de (English-German)
    - en-el (English-Greek)
    - en-hr (English-Croatian)
    - en-it (English-Italian)
    - en-nl (English-Dutch)
    - en-pl (English-Polish)
    - en-pt (English-Portuguese)
    - en-ru (English-Russian)
    - en-zh (English-Chinese)

## Acknowledgments

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement 644333 (TraMOOC).
