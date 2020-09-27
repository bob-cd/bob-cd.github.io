---
layout: default
title: API Reference
---

<div id="swagger-ui"></div>
<link href="/assets/css/swagger-ui.css" rel="stylesheet">
<link href="/assets/css/api-reference.css" rel="stylesheet">
<script src="/assets/js/swagger-ui-bundle.js"></script>
<script>
  SwaggerUIBundle({
    url: "https://raw.githubusercontent.com/bob-cd/bob/master/apiserver/src/main/resources/bob/api.yaml",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIBundle.SwaggerUIStandalonePreset
    ],
    layout: "BaseLayout"
  })
</script>
