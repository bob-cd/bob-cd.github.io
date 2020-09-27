---
layout: default
title: Getting Started
---

# Getting Started

This document is meant to help you to run Bob locally on Docker.

## Running a local Bob cluster on Docker

To get a minimal setup running locally (with a simple Github public repo and file system based storage), we will run [bob](https://github.com/bob-cd/bob), [resource-git](https://github.com/bob-cd/resource-git) and [artifact-store](https://github.com/bob-cd/artifact-local).

1. Download [Docker](https://www.docker.com/), if already not present and provide `privileged` permission at time of installation as Bob uses [Docker in Docker](https://www.docker.com/blog/docker-can-now-run-within-docker/) to function.
1. Create a common network for the containers
   ```bash
   docker network create bob-net
   ```
1. Start a RabbitMQ instance
   ```bash
   docker run -it --name bob-queue -p 5672:5672 --network bob-net rabbitmq:3-alpine
   ```
1. Start a PostgreSQL instance
   ```bash
   docker run -it --name bob-storage -p 5432:5432 -e POSTGRES_DB=bob -e POSTGRES_USER=bob -e POSTGRES_PASSWORD=bob --network bob-net postgres:alpine
   ```
1. Start a Bob runner:
   ```bash
   docker run -it --name bob-runner -e BOB_STORAGE_HOST=bob-storage -e BOB_QUEUE_HOST=bob-queue --network bob-net bobcd/runner
   ```
1. Start a Bob entities service:
   ```bash
   docker run -it --name bob-entities -e BOB_STORAGE_HOST=bob-storage -e BOB_QUEUE_HOST=bob-queue --network bob-net bobcd/entities
   ```
1. Start a Bob apiserver:
   ```bash
   docker run -it --name bob-apiserver -e BOB_STORAGE_HOST=bob-storage -e BOB_QUEUE_HOST=bob-queue --network bob-net bobcd/apiserver
   ```

A reference CLI like [Wendy](https://github.com/bob-cd/wendy) can be used to talk to Bob.

## A simple build example, using Wendy

### Building Wendy
1. Clone [Wendy](https://github.com/bob-cd/wendy) and navigate to the source directory
1. Ensure you have the latest [GraalVM](https://www.graalvm.org/docs/getting-started/) installed
1. Ensure you have the latest Clojure [CLI](https://clojure.org/guides/getting_started) installed
1. Ensure the Native Image module is [installed](https://www.graalvm.org/docs/reference-manual/native-image/)
1. Build the wendy binary:
   ```bash
   clojure -A:native-image
   ```
1. After a successful build it should be available in the `target` directory.

### Using Wendy
1. Check if Bob's ready:
   ```bash
   ./wendy can-we-build-it
   ```
1. Register the git resource provider:
   ```bash
   ./wendy external-resource register -n git -u "http://resource-git:8000"
   ```
1. Register the local artifact store:
   ```bash
   ./wendy artifact-store register -n local -u "http://artifact-local:8001"
   ```
1. Wendy needs a "build.toml" file to communicate to Bob. Copy the following content and create "build.toml" file at current (target) folder:
   ```toml
   [dev.build]
   image = "gradle:jdk11"

   [[dev.build.resources]]
   name = "source-code"
   type = "external"
   provider = "git"

      [dev.build.resources.params]
      branch = "master"
      repo = "https://github.com/lispyclouds/bob-example"

   [[dev.build.steps]]
   cmd = "echo starting build"

   [[dev.build.steps]]
   needs_resource = "source-code"
   cmd = "gradle test"

   [[dev.build.steps]]
   needs_resource = "source-code"
   cmd = "gradle shadowJar"
   produces_artifact = { name = "uberjar", path = "build/libs/bob-example-1.0-SNAPSHOT-all.jar", store = "local" }

   [[dev.build.steps]]
   cmd = "echo done"
   ```
1. Create the pipeline:
   ```bash
   ./wendy pipeline create -c build.toml
   ```
1. Start the pipeline:
   ```bash
   ./wendy pipeline start -g dev -n build
   ```
1. Logs can be periodically checked with:
   ```bash
   ./wendy pipeline logs -g dev -n build -num 1 -o 0 -l 100
   ```
1. Status of the pipeline can be checked with:
   ```bash
   ./wendy pipeline status -g dev -n test -num 1
   ```
1. When passed, the jar can be extracted out with following [curl](https://curl.haxx.se/) command, Bob responds with a TAR archive of the artifact path.
   ```bash
   curl http://localhost:7777/api/pipelines/groups/dev/names/build/id/<id>/artifacts/store/local/name/uberjar -o uberjar.tar
   ```
1. Extract the tar to obtain the final jar file
   ```bash
   tar xvf uberjar.tar
   ```
1. Test the jar file. Running following command should give "Hello Casey!"
   ```bash
   java -jar bob-example-1.0-SNAPSHOT-all.jar
   ```

Due to Bob's distributed architecture, supporting of installation of Bob via a package manager is not a priority at the moment, but any help here would be much appreciated!
