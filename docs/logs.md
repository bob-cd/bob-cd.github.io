# Logs

Logs are generally lines of text produced by a pipeline run. Logs are also an artifact of a build.

In Bob, like artifacts its important that logs **should not** be stored within the system and should be there regardless of
Bob being there or not. This is something that is not there in most of the other CIs.

Bob uses the notion of `Loggers` to abstract away the storage and management of logs to an external system.
Logs are streamed line by line and can be streamed back via the REST API.

To use a logger for a pipeline run, pass it when calling the start api:

```bash
curl -XPOST "http://localhost:7777/pipelines/start/groups/<group>/names/<name>/loggers/<logger>"
```

## Logger

A Logger is a system with the following properties:

- It is a web server.
- It is reachable from the network that Bob is in.
- Exposes an endpoint at `/bob_logs/<run-id>` which:
    - When a `GET` request is made on it, starts streaming lines of logs.
      This should support an optional query parameter `?follow` which when set to true, streams live logs.
      Example: `bob_logs/<run-id>?follow=true`
    - When a `PUT` request is made on it with the body being the log line, the data is appended.
    - When a `DELETE` request is made on it, the corresponding logs are deleted.
- Exposes a `GET /ping` endpoint which serves as a periodic health check from Bob.

A reference logger which implements storage using local file system can be found [here](https://github.com/bob-cd/logger-local).

This gives the following advantages:

- Bob now doesn't have to care about _how_ to store logs.
- Details like auth, permissions etc can be offloaded outside of Bob.
- Multiple instances of Bob can share a Logger.
- Logs are preserved and managed regardless of Bob's availability.
- The Logger can be written an any language and be registered at runtime with Bob.

A logger **must** be registered with Bob prior to the execution of the pipeline.

To register a Logger with Bob:

- Make a `POST` request on the end point `/loggers/<name>` with the body:
  ```json
  {
    "url": "https://my-logger.bob.io"
  }
  ```
- A `202` response from Bob indicates success.
  Here `name` is the unique name with which Bob identifies this. The url must be reachable from Bob.

Conversely a `DELETE` request on `/loggers/<name>` un-registers it from Bob.

To list the loggers make a `GET` request on `/loggers`.

To retrieve logs from a pipeline run:

- Make a `GET` request on `/pipelines/logs/groups/<group>/names/<name>/runs/<id>`.
- Set the optional query parameter `follow` to true to stream live logs.
