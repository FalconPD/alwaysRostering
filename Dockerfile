FROM ubuntu:18.04

# reuiqred for pipenv to work
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# print log messages immediately
ENV PYTHONUNBUFFERED=1

# put the alwaysRostering module in our path
ENV PYTHONPATH=/alwaysRostering

# using mirrors is MUCH faster
COPY docker/sources.list /etc/apt/sources.list

# we use a ppa to get python 3.7 which seems to work better with aiohttp
RUN apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install python3.7 python3.7-dev && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && \
    apt-get -y install python3-pip git build-essential libffi-dev && \
    pip3 install pipenv && \
    git clone https://github.com/FalconPD/alwaysRostering.git && \
    cd alwaysRostering && \
    pipenv install

# credentials.py is confidential and not found in the git repo
COPY AR/credentials.py /alwaysRostering/AR/

# for testing
COPY docker/run.sh /alwaysRostering/docker/
     
WORKDIR /alwaysRostering
CMD docker/run.sh
