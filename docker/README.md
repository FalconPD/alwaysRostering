# Docker Image for alwaysRostering

This directory contains extra files needed to build a Docker image of the
alwaysRostering framework. The goal is to provide a portable environment where
anyone can run alwaysRostering with very little setup required.

The `Dockerfile` and `.dockerignore` files can be found in the project root
directory.

## Loading

## Running

The default command is the `docker/run.sh` script, which will perform the
following actions:

* Create a database from the latest Genesis information with
  `Genesis/make_db.py`
* Create MAP Rosters for K-2, 3-12, and screening tests
* Import the MAP StandardRoster for the current test window

A container can be created and the default command executing within it by
running:

```console
docker run always_rostering
```

NOTE: This assumes that the image has been loaded and is named
`always_rostering`.

## Using alwaysRostering Interactively

The image can also be used to run the scripts within the alwaysRostering
framework interactively:

```console
docker run always_rostering bash
pipenv shell
```

## Building

The image is based on Ubuntu 18.04 with python3.7 added from the [deadsnakes
ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa). To build an image
named `always_rostering`, in the project root directory run:

```console
docker build -t always_rostering . in the project
```

NOTE: You will need an `AR/credentials.py` file for the image to work properly.

## Saving

