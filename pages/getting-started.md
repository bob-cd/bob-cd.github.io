---
layout: default
title: Getting Started
---

# Getting Started

This document is meant to help you to run Bob locally on Docker.

## Running a local Bob cluster on Docker

To get a minimal setup running locally (with a simple Github public repo and file system based storage), we will run [bob](https://github.com/bob-cd/bob), [resource-git](https://github.com/bob-cd/resource-git) and [artifact-store](https://github.com/bob-cd/artifact-local).

1. Download [Docker](https://www.docker.com/)
1. Have a file called `docker-compose.yml` somewhere with the contents from this [file](https://github.com/bob-cd/bob/blob/main/docker-compose.yml)
1. Start the cluster using [docker-compose](https://docs.docker.com/compose/) from the same directory as the file:
   ```bash
   docker-compose up
   ```
1. When it all comes up, bob should be available on port `7777`

### Using the API

Bob exposes itself fully via a REST API as described [here](https://bob-cd.github.io/pages/api-reference.html)
A HTTP client like [HTTPie](https://httpie.org/), [curl](https://curl.haxx.se/) or [Insomnia](https://insomnia.rest/) is recommended to use.

The reference CLI for Bob: [Wendy](https://github.com/bob-cd/wendy) is under construction and should be ready soon! Any PRs and help on Wendy is much much appreciated!

### Building a simple project on Bob

This uses [HTTPie](https://httpie.org/) and assumes the above steps have been followed and a Bob cluster is available on `http://localhost:7777`. A 200/202 response here signifies success.

1. Test if Bob is ready:
   ```bash
   http http://localhost:7777/can-we-build-it?
   ```
   should respond:
   ```json
   {
     "message": "Yes we can! 🔨 🔨"
   }
   ```
1. Create a pipeline creation request body in a file `pipeline.json`:
   ```json
   {
     "group": "dev",
     "name": "pipeline1",
     "image": "gradle:jdk11",
     "steps": [
       {
         "needs_resource": "source",
         "cmd": "gradle test"
       },
       {
         "needs_resource": "source",
         "cmd": "gradle shadowJar",
         "produces_artifact": {
           "name": "jar",
           "path": "build/libs/bob-example-1.0-SNAPSHOT-all.jar",
           "store": "local"
         }
       }
     ],
     "resources": [
       {
         "name": "source",
         "type": "external",
         "provider": "resource-git",
         "params": {
           "repo": "https://github.com/lispyclouds/bob-example",
           "branch": "main"
         }
       }
     ]
   }
   ```
1. Create the pipeline:
   ```bash
   cat pipeline.json | http POST http://localhost:7777/pipelines/groups/dev/names/pipeline1
   ```
1. Register the resource provider:
   ```bash
   http POST http://localhost:7777/resource-providers/resource-git url="http://resource:8000"
   ```
1. Register the artifact store:
   ```bash
   http POST http://localhost:7777/artifact-stores/local url="http://artifact:8001"
   ```
1. Start the pipeline:
   ```bash
   http POST http://localhost:7777/pipelines/start/groups/dev/names/pipeline1
   ```
1. See the docker logs of the `runner` container to get the run id. This will be improved with [#71](https://github.com/bob-cd/bob/issues/71). Let's say its `r-0ef66ba9-e397-461b-a6d9-f52f91889264`. Check the pipeline status:
   ```bash
   http http://localhost:7777/pipelines/status/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264
   ```
   should respond:
   ```json
   {
     "message": "running"
   }
   ```
1. See the logs of the run at any time:
   ```bash
   http http://localhost:7777/pipelines/logs/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264/offset/0/lines/50
   ```
1. If all goes well, eventually it should respond with a `passed` status with the same status call as above.
1. Download the produced artifact:
   ```bash
   http http://localhost:7777/pipelines/groups/dev/names/pipeline1/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264/artifact-stores/local/artifact/jar > artifact.tar
   ```
1. Extract the TAR file:
   ```bash
   tar xvf artifact.tar
   ```
1. Test the jar file. Running following command should give "Hello Casey!"
   ```bash
   java -jar bob-example-1.0-SNAPSHOT-all.jar
   ```

Due to Bob's distributed architecture, supporting of installation of Bob via a package manager is not a priority at the moment, but any help here would be much appreciated!
