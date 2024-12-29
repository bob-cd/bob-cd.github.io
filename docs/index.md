# Bob the Builder

> Everything should be made as simple as possible, but no simpler - Albert Einstein

Most CI/CD tools are too opinionated and do too much. Bob follows the UNIX philosophy of doing one thing and doing it well, and the Emacs/LISP like philosophy of small core with external extensibility, and strives for [simpler, decomposed and hence more composable and unbundled design](https://www.youtube.com/watch?v=MCZ3YgeEUPg). Built on secure, <b>rootless</b> runtimes, Bob is flexible to run in modern Cloud Native environments. For more information, see the [Rationale](rationale.md)

## Overview

[![ClojureD Talk](https://img.youtube.com/vi/KtMJ4lHI_qM/0.jpg)](https://www.youtube.com/watch?v=KtMJ4lHI_qM)

Bob's API (accessible entirely through HTTP) enables a core set of CI/CD features.

- **You are in control**: Bob is un-opinionated about how you build your pipelines, giving you complete control and freedom to experiment and innovate.
- **Bob is minimal**: Bob is made up for three main composable components, Pipelines, Resources & Artifacts. You have the freedom to build on top of these basic blocks to create complex pipelines designed for solving your problems.

## Join the conversation

Please start a [discussion](https://github.com/bob-cd/bob/discussions) on any topic and we are happy to help and learn from each other!

For a more Clojure specific discussion there we also have a Clojurians Slack [channel](https://clojurians.slack.com/messages/CPBAYJJF6).

Happy Building!

## License

Bob is [Free](https://www.gnu.org/philosophy/free-sw.en.html) and Open Source and always will be. Licensed fully under [MIT](https://opensource.org/licenses/MIT)
