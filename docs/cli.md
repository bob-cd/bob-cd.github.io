# CLI

Bob and its ecosystem strongly follows a philosophy of being [spec-first](https://www.atlassian.com/blog/technology/spec-first-api-development) from the server side to all the clients.

## Wendy

[Wendy](https://github.com/bob-cd/wendy) is an opinionated, reference CLI/TUI for Bob and she strives to have the following purposes:

- Use a spec-first approach to implement a CLI for all of Bob's REST API
- Implement a declarative interface to Bob's resources and be a platform for it
- Implement a "command centre" for Bob: think [k9s](https://k9scli.io/) or [Kibana](https://www.elastic.co/kibana)
- Possibly more

### Using Wendy

Wendy is built using the [Go](https://go.dev/) programming language and uses [climate](https://github.com/lispyclouds/climate) at its core for its functionality.

#### Installation

- As of now its to be built from source:
  - Clone the repo:
    ```bash
    git clone https://github.com/bob-cd/wendy
    ```
  - Make sure Go 1.23+ is [installed](https://go.dev/doc/install)
  - Build:
    ```bash
    go build
    ```
  - Place the resulting binary `wendy` into your PATH

#### Usage

The following are the configuration options and the defaults:

- `endpoint`: The endpoint to connect to bob. Defaults to `"http://localhost:7777"`
- `api_path`: The path where the OpenAPI spec is located. Used for bootstrapping. Defaults to `"/api.yaml"`

Run `wendy configure` to set them to different values.

Wendy is able to bootstrap the commands from the spec, run the following for the first time or to refresh the commands

```bash
wendy bootstrap
```

After this the full set of commands will be available and the cluster can be interacted with.

All commands and their nested, contexual help can be seen with the `--help` flag.

- `wendy --help`
- `wendy pipelines create --help`
- etc

#### Types of commands

The commands that are bootstrapped from Bob are mostly imperative, eg:

- `wendy pipelines delete --group foo --name bar`
- `wendy resource-providers create --spec '{"name": "resource-git", "url": "http://resource-git:8000"}'`

Wendy offers the `apply` command to declaratively and idempotently deal with resources via manifest files.

A manifest file is of the following shape

```yaml title="pipeline.yaml" linenums="1"
apiVersion: wendy.bob.cd/v1alpha1 # version of the spec
kind: Pipeline # can also be ResourceProvider, ArtifactStore
identifiedBy: # These fields are used as id for this resource from the spec
  - group
  - name
spec: # The spec should be a JSON encodable map
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

The `spec` should correspond to the `--spec` in the implement commands.

Apply as:

```bash
wendy apply -m pipeline.yaml
```

More examples of manifests can be found [here](https://github.com/bob-cd/wendy/tree/main/manifests)

Wendy is a work in progress but mostly usable. Thing may change and feedback is most welcome!
