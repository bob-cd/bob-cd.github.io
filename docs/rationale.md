# Why Bob?

Bob is mostly built out of [my](https://github.com/lispyclouds) experiences in working on platform teams in various places and seeing various pain points. Bob represents my idea of what something that could be there to not get in your way, be flexible and robust enough to serve most of the needs.
It is a very much usable piece of software which has seen use, but at the end of the day its intended as my expression of ideas: out there to inspire others and reduce some of the pains I faced for others.

Some of the (non exhaustive) reasons of why Bob

- Be fully Free and Open Source (FOSS) under the MIT License.
- Have a very small core with a limited feature set and be opinionated about them:
    - Steps (direct commands like shell)
    - Pipeline (Collection of steps which can consume artifacts from other pipelines).
    - Environment (Key value store associated with either steps and/or Pipelines).
    - Resources (Things like source code or artifacts produced by pipelines).
    - Artifacts (Something built by a Pipeline).
- Expose the above feature set entirely via an API, hence allow any client to configure/control it. Also not be affected by bugs in it.
- Be agnostic of an UI.
- Be more extensible than great things like Concourse.ci.
- Build pretty much everything else external resources or orchestrate via API.
- Scale via multiple federated Bob instances(think Cassandra) and share loads and resources.

## Bob vs the rest of the CI tools

Some of the perceived pain points in the currently established CI/CD systems

- The plugin architectures: They are mainly to be extended via loading of code into the main process. This presents the following issues:

    - Bugs and vulnerabilities in the plugin. Most if not all of the plugins we use for these systems are the primary root cause for much of the CVEs and bugs. Well known examples for this can be seen in [Jenkins](https://wiki.jenkins.io/display/JENKINS/Plugin+tutorial), [GoCD](https://docs.gocd.org/current/extension_points/), [TeamCity](https://plugins.jetbrains.com/docs/teamcity/).
    - We have to use the same tech that the core was made in. eg. JVM tech for Jenkins plugins.
    - We are limited by the API provided by the main system for instance, to get resources and orchestrate the artifacts around.
    - The core has now one more possible attack surface where an issue in the plugin can cause nasty things to happen in the core ranging from it being unstable to security [issues](https://www.cvedetails.com/vulnerability-list/vendor_id-15865/product_id-34004/Jenkins-Jenkins.html).
    - Deploying these plugins often means a restart of the system, downtimes, misconfiguration and more importantly this needs happen on the same machine as the core and opens up a possibility of creating [snowflake](https://martinfowler.com/bliki/SnowflakeServer.html) servers.

- Monolithic, large and complex. IMO these systems have grown to a stage where they have a complex UX and requires a good amount of learning curve to use intuitively.
- The UI is merged with the back-end source hence pretty much providing an opinionated view of the CI infra and to control it. Building mobile interfaces or accessing on them can be tricky.
- The API is patchy. They don’t really expose the entire infra via API and extending/controlling them via just their API is hard.
- CI Infra is hard to version control.

## Inspiration

- [Concourse CI](https://concourse-ci.org/) and [OVH CDS](https://ovh.github.io/cds/)
- The Emacs architecture
- UNIX [philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)
- [The Zen of Python](https://www.python.org/dev/peps/pep-0020/)

Talks that inspired bob:

- [Narcissistic design](https://www.youtube.com/watch?v=LEZv-kQUSi4)
- [Design, composition & performance](https://youtu.be/MCZ3YgeEUPg)
