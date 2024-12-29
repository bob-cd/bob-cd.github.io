# Pipelines

A Pipeline is the only unit of execution in Bob.

A pipeline consists of the following:

## Image

Bob implements a pipeline as a series of steps carried out on a starting container image.
This image is used to set the context of the build and is used to get the prerequisites like
compilers, build tooling, deployment tooling etc.

**Always use a fully qualified name to denote the registry to be downloaded from.**

Examples:

- For docker hub: `docker.io/library/ubuntu:latest`
- For quay: `quay.io/podman/stable`

## Vars

Vars is a map of key-value pairs which denotes the environment variables that is to be available
to all the steps of the pipeline.

Example:

```json
{
  "user": "wendy",
  "env": "prod"
}
```

## A List of Steps

A Step is essentially a key-value pair consisting of the following keys:

- `cmd`: String, Required: This is the command that is to be executed.
  This is generally a shell command and it's validity is determined by image used
  and/or the preceding steps.

Example: `cargo build` in case the `rust` Docker image being used.

- `vars`: Same as the pipeline Vars mentioned before, but scoped to the this step.
  This is merged with the vars from the pipeline level.

- `needs_resource`: String, Optional: This denotes that a [Resource](resources.md) should
  be mounted before the `cmd` is executed. The resource generally denotes something that the
  command will be needing to successfully run. The resource is referred by the name its defined
  in the resources section of the pipeline.

Example:

```json
{ "needs_resource": "app-source-code" }
```

- `produces_artifact`: Key-Value Pair, Optional: This denotes the step will produce an
  [Artifact](artifacts.md) if successfully executed. This consists of the following keys: - `path`: String, Required: This is the path relative to the command being executed
  where the expected artifact will be produced. Bob will stream the artifact to the
  registered artifact store. The path must exist. - `name`: String, Required: This is the unique name with which the artifact will be uploaded
  to the artifact store. - `store`: String, Required: This is the name of the registered artifact store where the artifact will be uploaded.

Example:

```json
{
  "produces_artifact": {
    "path": "target/app.jar",
    "name": "app-jar",
    "store": "s3"
  }
}
```

## List of Resources

Resources is a list of key-value pairs which defines the list of [Resources](resources.md) which may be
consumed by one or more of the steps of the pipeline.

## Full working pipeline example

```json
{
  "image": "docker.io/library/busybox:musl",
  "vars": {
    "env": "test",
    "url": "test.com"
  },
  "steps": [
    {
      "cmd": "echo hello"
    },
    {
      "cmd": "sleep 10"
    },
    {
      "vars": {
        "foo": "bar"
      },
      "cmd": "sh -c 'touch test.txt && echo $env >> test.txt'"
    },
    {
      "cmd": "cat test.txt",
      "produces_artifact": {
        "name": "afile",
        "path": "test.txt",
        "store": "local"
      }
    },
    {
      "needs_resource": "my-source",
      "cmd": "ls",
      "produces_artifact": {
        "name": "license-file",
        "path": "LICENSE",
        "store": "local"
      }
    }
  ],
  "resources": [
    {
      "name": "my-source",
      "type": "external",
      "provider": "git",
      "params": {
        "repo": "https://github.com/bob-cd/bob",
        "branch": "main"
      }
    },
    {
      "name": "another-source",
      "type": "external",
      "provider": "git",
      "params": {
        "repo": "https://github.com/into-docker/clj-docker-client",
        "branch": "main"
      }
    }
  ]
}
```
