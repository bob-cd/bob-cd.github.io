# Getting Started

This document is meant to help you to run Bob on some popular platforms

Checkout the [bob-deploy](https://github.com/bob-cd/bob-deploy) repo for reference deployments on various platforms

## Running a Bob cluster

To get a minimal setup running locally (with a simple Github public repo and file system based storage), we will run [bob](https://github.com/bob-cd/bob), [resource-git](https://github.com/bob-cd/resource-git) and [artifact-store](https://github.com/bob-cd/artifact-local).

### On Kubernetes

1. Use a remote cluster or setup a local one using [kind](https://kind.sigs.k8s.io/) or [Minikube](https://minikube.sigs.k8s.io/docs/) etc
1. Clone the [repo](https://github.com/bob-cd/bob-deploy)
1. Apply the manifests: `kubectl apply -f k8s/`
1. This depolys the cluster exposed via the `bob-apiserver` ClusterIP Serivce:
    - If using a remote cluster, you may want to [expose](https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/) it
    - If on a local cluster, port forward it: `kubectl port-forward service/bob-apiserver 7777:7777`

### On Podman or Docker

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
HTTP clients like [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Insomnia](https://insomnia.rest/) etc could be used to directly interact with the [API](api.md).

We would be using [Wendy](cli.md#wendy), the reference CLI.

### Building a simple project on Bob

This assumes the above steps have been followed and a Bob cluster is available on `http://localhost:7777` and Wendy is set up.

- Test if Bob is ready:
    ```bash
    wendy cluster ping
    ```
    should respond with a resounding `Pong` if all good.
- Create a pipeline manifest and set the `GOOS` and `GOARCH` [values](https://golang.org/doc/install/source#environment) according to your OS:
    ```yaml title="pipeline.yaml" linenums="1"
    apiVersion: wendy.bob.cd/v1alpha1
    kind: Pipeline
    identifiedBy:
        - group
        - name
    spec:
        group: dev
        name: pipeline1
        image: docker.io/library/golang:alpine
        steps:
            - needs_resource: source
              cmd: go test
            - needs_resource: source
              vars:
                  GOOS: linux
                  GOARCH: amd64
              cmd: go build -o app
              produces_artifact:
                  name: app
                  path: app
                  store: artifact-local
        resources:
            - name: source
              type: external
              provider: resource-git
              params:
                  repo: https://github.com/lispyclouds/bob-example
                  branch: main
    ```
- Create the pipeline:
    ```bash
    wendy apply -m pipeline.yaml
    ```
- Create a resource_provider manifest in a file `resource_provider.yaml`
    ```yaml title="resource_provider.yaml" linenums="1"
    apiVersion: wendy.bob.cd/v1alpha1
    kind: ResourceProvider
    identifiedBy:
        - name
    spec:
        name: resource-git
        url: http://resource-git:8000
    ```
- Register the resource provider:
    ```bash
    wendy apply -m resource_provider.yaml
    ```
- Create an artifact_store manifest in a file `artifact_store.yaml`
    ```yaml title="artifact_store.yaml" linenums="1"
    apiVersion: wendy.bob.cd/v1alpha1
    kind: ArtifactStore
    identifiedBy:
        - name
    spec:
        name: artifact-local
        url: http://artifact-local:8001
    ```
- Register the artifact store:
    ```bash
     wendy apply -m artifact_store.yaml
    ```
- Start the pipeline:
    ```bash
    wendy pipelines start --group dev --name pipeline1
    ```
    should respond with a run id like this:
    ```json
    "r-0ef66ba9-e397-461b-a6d9-f52f91889264"
    ```
    This is like a tracing id, all subsequent interactions can be done with this.
- Follow the events of the run via [SSE](https://en.wikipedia.org/wiki/Server-sent_events):
    ```bash
    wendy events stream
    ```
    should start tailing live events, hit ctrl-c to close it.
    This is ideal for UIs/CLIs reacting to changes in the cluster.
- Check the pipeline status with the run id:
    ```bash
    wendy pipelines status --id r-0ef66ba9-e397-461b-a6d9-f52f91889264
    ```
    should respond:
    ```json
    "running"
    ```
- See the logs of the run at any time:
    ```bash
    wendy pipelines logs --id r-0ef66ba9-e397-461b-a6d9-f52f91889264 --offset 0 --lines 50
    ```
- If all goes well, eventually it should respond with a `passed` status with the same status call as above.
- Download the produced artifact:
    ```bash
    wendy pipelines fetch-artifact --group dev --name pipeline1 --id r-0ef66ba9-e397-461b-a6d9-f52f91889264 --store-name artifact-local --artifact-name app
    ```
- Extract the TAR file:
    ```bash
    tar xvf app.tar
    ```
- Test the executable file. Running following command should give "Hello Casey"
    ```bash
    ./app
    ```

See what else is possible using `wendy --help`.
