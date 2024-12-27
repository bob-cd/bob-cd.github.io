# Getting Started

This document is meant to help you to run Bob locally on some popular platforms

## Running Bob on other platforms

Checkout the [bob-deploy](https://github.com/bob-cd/bob-deploy) repo for reference deployments on various platforms

## Running a local Bob cluster on Podman or Docker

To get a minimal setup running locally (with a simple Github public repo and file system based storage), we will run [bob](https://github.com/bob-cd/bob), [resource-git](https://github.com/bob-cd/resource-git) and [artifact-store](https://github.com/bob-cd/artifact-local).

1. Download [Podman](https://podman.io/getting-started/installation) or [Rootless Docker](https://docs.docker.com/engine/security/rootless/)
1. Fetch this [docker-compose.yml](https://github.com/bob-cd/bob-deploy/blob/main/docker-compose.yml) file with `curl -LfO 'https://raw.githubusercontent.com/bob-cd/bob-deploy/main/docker-compose.yml'`
1. In the same directory, start the cluster using [podman-compose](https://github.com/containers/podman-compose#installation) or [docker-compose](https://docs.docker.com/compose/):
   ```bash
   podman-compose up
   ```
   or
   ```bash
   docker-compose up
   ```
1. When it all comes up, bob should be available on port `7777`

### Using the API

Bob exposes itself fully via a REST API as described [here](https://bob-cd.github.io/pages/api-reference.html)
A HTTP client like [curl](https://curl.haxx.se/) or [HTTPie](https://httpie.org/) or [Insomnia](https://insomnia.rest/) is recommended to use.

The reference CLI for Bob: [Wendy](https://github.com/bob-cd/wendy) is under construction and should be ready soon! Any PRs and help on Wendy is much much appreciated!

### Building a simple project on Bob

This assumes the above steps have been followed and a Bob cluster is available on `http://localhost:7777`. A 2xx response here signifies success.

- Test if Bob is ready:
   ```bash
   curl "http://localhost:7777/can-we-build-it?"
   ```
   should respond:
   ```json
   {
     "message": "Yes we can! 🔨 🔨"
   }
   ```
- Create a pipeline creation request body in a file `pipeline.json`, set the `GOOS` and `GOARCH` [values](https://golang.org/doc/install/source#environment) according to your OS:
   ```json
   {
     "group": "dev",
     "name": "pipeline1",
     "image": "docker.io/library/golang:latest",
     "steps": [
       {
         "needs_resource": "source",
         "cmd": "go test"
       },
       {
         "needs_resource": "source",
         "vars": {
           "GOOS": "darwin",
           "GOARCH": "amd64"
         },
         "cmd": "go build -o app",
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
- Create the pipeline:
   ```bash
   curl -X POST -d@pipeline.json -H "Content-Type: application/json" http://localhost:7777/pipelines
   ```
- Register the resource provider:
   ```bash
   curl -X POST -d'{"name": "resource-git", "url": "http://resource:8000"}' -H "Content-Type: application/json" http://localhost:7777/resource-providers
   ```
- Register the artifact store:
   ```bash
   curl -X POST -d'{"name": "local", "url": "http://artifact:8001"}' -H "Content-Type: application/json" http://localhost:7777/artifact-stores
   ```
- Start the pipeline:
   ```bash
   curl -X POST http://localhost:7777/pipelines/start/groups/dev/names/pipeline1
   ```
   should respond with a run id like this:
   ```json
   {
     "message": "r-0ef66ba9-e397-461b-a6d9-f52f91889264"
   }
   ```
   This `run-id` is like a tracing id, all subsequent interactions can be done with this.
- Follow the events of the run via [SSE](https://en.wikipedia.org/wiki/Server-sent_events):
   ```bash
   curl -H "Accept: text/event-stream" http://localhost:7777/events
   ```
   should respond with JSON encoded events, hit ctrl-c to close it:
   ```
   data: {"run-id":"r-0ef66ba9-e397-461b-a6d9-f52f91889264","type":"pipeline","event":"pull","group":"dev","name":"pipeline1","timestamp":1699339368930}
   ```
   This is ideal for UIs/CLIs reacting to changes in the cluster.
- Check the pipeline status with the run id:
   ```bash
   curl http://localhost:7777/pipelines/status/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264
   ```
   should respond:
   ```json
   {
     "message": "running"
   }
   ```
- See the logs of the run at any time:
   ```bash
   curl http://localhost:7777/pipelines/logs/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264/offset/0/lines/50
   ```
- If all goes well, eventually it should respond with a `passed` status with the same status call as above.
- Download the produced artifact:
   ```bash
   curl -o artifact.tar http://localhost:7777/pipelines/groups/dev/names/pipeline1/runs/r-0ef66ba9-e397-461b-a6d9-f52f91889264/artifact-stores/local/artifact/app
   ```
- Extract the TAR file:
   ```bash
   tar xvf artifact.tar
   ```
- Test the executable file. Running following command should give "Hello Casey"
   ```bash
   ./app
   ```
