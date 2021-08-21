---
layout: default
title: Getting Started
---

# Getting Started

This document is meant to help you to run Bob locally on Docker.

## Running a local Bob cluster on Docker

To get a minimal setup running locally (with a simple Github public repo and file system based storage), we will run [bob](https://github.com/bob-cd/bob), [resource-git](https://github.com/bob-cd/resource-git) and [artifact-store](https://github.com/bob-cd/artifact-local).

1. Download [Docker](https://www.docker.com/)
1. Fetch this [docker-compose.yml](https://github.com/bob-cd/bob/blob/main/docker-compose.yml) file with `curl -LfO 'https://raw.githubusercontent.com/bob-cd/bob/main/docker-compose.yml'`
1. In the same directory, start the cluster using [docker-compose](https://docs.docker.com/compose/):
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
1. Create a pipeline creation request body in a file `pipeline.json`, set the `GOOS` and `GOARCH` [values](https://golang.org/doc/install/source#environment) according to your OS:
   ```json
   {
     "group": "dev",
     "name": "pipeline1",
     "image": "docker.io/library/golang:alpine",
     "steps": [
       {
         "needs_resource": "source",
         "cmd": "go test"
       },
       {
         "needs_resource": "source",
         "cmd": "sh -c 'GOOS=darwin GOARCH=amd64 go build -o app'",
         "produces_artifact": {
           "name": "app",
           "path": "app",
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
   should respond with a run id like this:
   ```json
   {
     "message": "r-0ef66ba9-e397-461b-a6d9-f52f91889264"
   }
   ```
   This `run-id` is like a tracing id, all subsequent interactions can be done with this.
1. Check the pipeline status with the run id:
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
   http http://localhost:7777/pipelines/groups/dev/names/pipeline1/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264/artifact-stores/local/artifact/app > artifact.tar
   ```
1. Extract the TAR file:
   ```bash
   tar xvf artifact.tar
   ```
1. Test the executable file. Running following command should give "Hello Casey"
   ```bash
   ./app
   ```
