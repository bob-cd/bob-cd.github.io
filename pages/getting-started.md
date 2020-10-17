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
   docker-compose up -d
   ```
1. When it all comes up, bob should be available on port `7777`

### Using the API

Bob exposes itself fully via a REST API as described [here](https://bob-cd.github.io/pages/api-reference.html)
A HTTP client like [HTTPie](https://httpie.org/), [curl](https://curl.haxx.se/) or [Insomnia](https://insomnia.rest/) is recommended to use.

The reference CLI for Bob: [Wendy](https://github.com/bob-cd/wendy) is under construction and should be ready soon! Any PRs and help on Wendy is much much appreciated!

Due to Bob's distributed architecture, supporting of installation of Bob via a package manager is not a priority at the moment, but any help here would be much appreciated!
