# Why Bob?

Some of the (non exhaustive) reasons of why Bob

- Be fully Free and Open Source (FOSS) under the MIT License.
- Have a very small core with a limited feature set and be opinionated about them.
  - Steps (direct commands like shell)
  - Pipeline (Collection of steps which can consume artifacts from other pipelines)
  - Environment (Key value store associated with either steps and/or Pipelines)
  - Resources (Things like source code or artifacts produced by pipelines)
  - Artifacts (Something built by a Pipeline)
- Expose the above feature set entirely via an API, hence allow any client to configure/control it. Also not be affected by bugs in it.
- Be agnostic of an UI
- Be more extensible than great things like Concourse.ci
- Accept the above stuff via an YAML as well
- Build pretty much everything else external resources or orchestrate via API
- Scale via multiple federated bob instances(think Cassandra) and share loads and resources

## Bob vs the rest of the CI tools

Some of the perceived pain points in the currently established CI/CD systems:

- The plugin architecture. They are mainly to be extended via JARs which are loaded by the main process. This presents the following issues:
  - Bugs and vulnerabilities in the plugin. Most if not all of the plugins we use for these systems are the primary root cause for much of the CVEs. Also a badly written plugin can bring the whole thing down.
  - We absolutely have to use a JVM language to write the plugins if the CI is in Java.
  - We are limited by the API provided by the main system to do stuff like get resources and orchestrate the artifacts around.
- Monolithic, large and complex. IMO these systems have grown to a stage where they have a complex UX and requires a good amount of learning curve to use properly.
- The UI is merged with the back-end source hence pretty much providing an opinionated view of the CI infra and to control it. Building mobile interfaces or accessing on them can be tricky.
- The API is patchy. They don’t really expose the entire infra via API and extending/controlling them via just their API is hard.
- Jenkins doesn’t even have a proper notion of Pipeline and the flow of artifacts.
- Some good ones aren’t even FOSS.
- Infra is hard to version control

## Inspiration

- [Concourse CI](https://concourse-ci.org/)
- EMacs architecture
- UNIX [philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)
- [The Zen of Python](https://www.python.org/dev/peps/pep-0020/)

Talks that inspired bob:

- [Narcissistic design](https://www.youtube.com/watch?v=LEZv-kQUSi4)
- [Design, composition & performance](https://youtu.be/MCZ3YgeEUPg)
