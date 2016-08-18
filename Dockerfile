FROM ubuntu:16.04
MAINTAINER Tomasz Dwojak <t.dwojak@amu.edu.pl>

RUN apt-get update && apt-get install -y \
	cmake \
	git \
	libboost-dev \
	libeigen3-dev \
        libopenblas-base \
        libopenblas-dev \
	python \
	python-dev \
	python-pip \
	python-libxml2 \
	gfortran \
	zlib1g-dev \
	g++ \
	automake \
	autoconf \
	libtool \
	libboost-all-dev \
	libgoogle-perftools-dev \
	libxml2-dev \
        libxslt1-dev \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Install amunmt
RUN git clone https://github.com/emjotde/amunmt -b cpu_stable
WORKDIR /amunmt
RUN git pull
RUN mkdir -p build
WORKDIR /amunmt/build
RUN cmake -DCMAKE_BUILD_TYPE=release .. && make -j 2

# install server scripts
run mkdir -p /server
copy server /server

# install docker entrypoint
copy docker-entrypoint.py /docker-entrypoint.py
run chmod +x /docker-entrypoint.py

WORKDIR /

entrypoint ["/docker-entrypoint.py"]
cmd ["en-ru en-de"]
