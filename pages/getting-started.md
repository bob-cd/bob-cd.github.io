---
layout: default
title: Getting Started
---

# Getting Started

This document is meant to help you to run Bob either locally on Docker or using Kubernetes.

## Running a local Bob cluster on Docker

To get a minimal setup running locally (with a simple Github public repo and file system based storage), we will run [bob](https://github.com/bob-cd/bob), [resource-git](https://github.com/bob-cd/resource-git) and [artifact-store](https://github.com/bob-cd/artifact-local). We will run Bob's cluster by using [docker-compose](https://docs.docker.com/compose/).

To run Bob locally on Docker:
1. Download [Docker](https://www.docker.com/), if already not present and provide `privileged` permission at time of installation as Bob uses [Docker in Docker](https://www.docker.com/blog/docker-can-now-run-within-docker/) to function.
1. Create a new directory dedicated for Bob and its supporting tools, lets call this directory, "Builder".
1. Download the [docker-compose.yaml](https://github.com/bob-cd/bob/blob/master/docker-compose.yaml) at Builder folder.
1. Download the [nginx.conf](https://github.com/bob-cd/bob/blob/master/nginx.conf) file for the basic configuration for a simple load balancer based on [NGINX](https://www.nginx.com/resources/wiki/).
1. To start a single node Bob cluster behind the NGINX local balancer, run:
   ```bash
   docker-compose up -d bob
   ```
1. (Optional) To scale up/down the Bob instances, run:
   ```bash
   docker-compose up --scale bob-node=<new-nodes-count> -d
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
   curl http://localhost:7777/api/pipelines/groups/dev/names/build/number/1/artifacts/store/local/name/uberjar -o uberjar.tar
   ```
1. Extract the tar to obtain the final jar file
   ```bash
   tar xvf uberjar.tar
   ```
1. Test the jar file. Running following command should give "Hello Casey!"
   ```bash
   java -jar bob-example-1.0-SNAPSHOT-all.jar
   ```

## Running Bob on [Kubernetes](https://kubernetes.io/)

To deploy Bob in Kubernetes, the necessary YAML files are provided in the [deploy](https://github.com/bob-cd/bob/tree/master/deploy) folder in the root of the project.

### Deploying locally on a [KinD](https://kind.sigs.k8s.io/) or [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/) cluster:
1. Install [KinD](https://kind.sigs.k8s.io/docs/user/quick-start) or [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/).
1. Run following create a single node cluster for Bob
   ```bash
   kind create cluster --name bob
   ```

   Or

   ```bash
   minikube start
   ```
1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
1. If using KinD, run following to set the cluster context.
   ```bash
   kubectl cluster-info --context kind-bob
   ```
1. Apply the privileged security policies needed for Bob.
   ```bash
   kubectl apply -f deploy/psp.yaml
   ```
1. Create a local PostgreSQL service
   ```bash
   kubectl apply -f deploy/db.yaml
   ```
1. [Optional] Create the [reference artifact store](https://github.com/bob-cd/artifact-local)
   ```bash
   kubectl apply -f deploy/artifact-local.yaml
   ```
1. Alternatively a custom artifact store may also be used here.
1. [Optional] Create the [reference resource provider](https://github.com/bob-cd/resource-git)
   ```bash
   kubectl apply -f deploy/resource-git.yaml
   ```
1. Alternatively a custom resource provider may also be used here.
1. Finally, Create a 2 replica Bob cluster. The number of replicas
   can be altered in the spec/replicas section of the Deployment.
   ```bash
   kubectl apply -f deploy/bob.yaml
   ```
1. Forward Bob's load balancer on the 7777 host port, so that cluster can be accessed via http://localhost:7777
   ```bash
   kubectl port-forward svc/bob-lb 7777:7777
   ```

### Deploying on an actual Kubernetes cluster

It's **STRONGLY RECOMMENDED** to run Bob on its own isolated cluster as it uses container privilege escalations for its functionality.

1. Ideally setup a multi-node Kubernetes cluster either On-Prem, cloud or via a managed provider like Amazon [EKS](https://aws.amazon.com/eks/).
1. Follow the steps from 5 to 11 from the previous section. For step 6, its recommended to use a managed PostgreSQL provider like Amazon [RDS](https://aws.amazon.com/rds/). Change the environment values in the container spec of Bob's Deployment accordingly.
1. Bob will be available via its load balancer's public IP.


Due to Bob's distributed architecture, supporting of installation of Bob via a package manager is not a priority at the moment, but any help here would be much appreciated!