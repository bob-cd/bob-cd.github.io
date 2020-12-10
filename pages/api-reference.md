---
layout: default
title: API Reference
---

<div id="api-container" style="background-color:white"></div>

<script src="/assets/js/redoc.standalone.js"></script>
<script>
Redoc.init(
  "https://raw.githubusercontent.com/bob-cd/bob/main/apiserver/src/main/resources/bob/api.yaml",
  {
    scrollYOffset: 50,
  },
  document.getElementById("api-container")
);
</script>
